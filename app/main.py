import torch
import cv2
import numpy as np

from fastapi import FastAPI, Request, Form, File, UploadFile
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from PIL import Image

app = FastAPI()

model = torch.hub.load('ultralytics/yolov5', 'custom', path='assets/best.onnx')


class DetectionClass(int, Enum):
    RULER = 0
    TIMBER = 1


class Geometry(BaseModel):
    type: str = "line"
    geom: List[float]


class Geometries(BaseModel):
    master: Geometry
    length: Geometry
    height: Geometry


class Measurement(BaseModel):
    height: int = Field(
        title='Load height',
        description='load height in cm'
    )
    length: int = Field(
        title='Load length',
        description='load length in cm'
    )
    geometry: Geometries


def format_results(results, image_original_size, scale_factor):
    [w, h] = image_original_size
    aspect_ratio = w / h
    max_ruler_confidence = 0
    max_timber_confidence = 0

    geometry_master_geom = None
    geometry_length_geom = None
    geometry_height_geom = None

    for result in results.xyxy:
        for prediction in result:
            [x1, y1, x2, y2, detection_score, detection_class] = prediction.tolist()
            x1 = x1 / scale_factor / w
            x2 = x2 / scale_factor / w
            y1 = y1 / scale_factor / h
            y2 = y2 / scale_factor / h
            if detection_class == DetectionClass.RULER:
                if detection_score > max_ruler_confidence:
                    max_ruler_confidence = detection_score
                    geometry_master_geom = [x1, y1, x2, y2]
            if detection_class == DetectionClass.TIMBER:  # we have timber
                if detection_score > max_timber_confidence:
                    max_timber_confidence = detection_score
                    height_x = max(x1, x2) / 2  # bounding box width midpoint
                    length_y = max(y1, y2) / 2  # bounding box height midpoint
                    geometry_length_geom = [x1, length_y, x2, length_y]  # length part has zero height, so y1 and y2 are the same
                    geometry_height_geom = [height_x, y1, height_x, y2]  # height part has zero width, so x1 and x2 are the same

    if all([geometry_master_geom, geometry_length_geom, geometry_height_geom]):
        one_meter = abs(geometry_master_geom[1] - geometry_master_geom[3])
        return Measurement(
            height=100 * abs(geometry_height_geom[1] - geometry_height_geom[3]) / one_meter,
            length=100 * abs(geometry_length_geom[0] - geometry_length_geom[2]) / one_meter * aspect_ratio,
            geometry=Geometries(
                master=Geometry(geom=geometry_master_geom),
                length=Geometry(geom=geometry_length_geom),
                height=Geometry(geom=geometry_height_geom)
            )
        )
    return None


def process_image(img, img_size):
    image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    image_original_size = image.size
    scale_factor = (img_size / max(image.size))
    resized = image.resize((int(x * scale_factor) for x in image.size), Image.ANTIALIAS)
    results = model(resized)
    return format_results(results, image_original_size, scale_factor)


@app.post("/measure", response_model=Optional[Measurement])
def measure(file: UploadFile = File(...)):
    img = cv2.imdecode(np.fromstring(file.file.read(), np.uint8), cv2.IMREAD_COLOR)
    result = process_image(img, 1280)
    return result
