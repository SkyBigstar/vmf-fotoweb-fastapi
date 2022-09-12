FROM python:3.8

RUN apt-get update && apt-get install -y libgl1-mesa-glx

ENV WORK_DIR /code

WORKDIR $WORK_DIR

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app $WORK_DIR/app
COPY ./assets $WORK_DIR/assets

CMD exec uvicorn app.main:app --host 0.0.0.0 --port 80