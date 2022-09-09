# VMF Fotoweb API
Šīs ir REST API serveris, kas ļauj noteikt mērkoka un kravas koordinātes bildē, saņemot rezultātu JSON formātā.

## Sistēmas apraksts
Serveris ir uzrakstīts, izmantojot Python programmēšanas valodu. Tā pamatā ir [FastAPI](https://fastapi.tiangolo.com/) programmēšanas ietvars (framework), kas vienkāršo REST API izveidi.  Datorredzes risinājums ir [YOLOv5](https://github.com/ultralytics/yolov5) Pytorch modelis, kas tika apmācīts konkrētam nolūkam - mērkoka un kokmateriālu kravas atpazīšanai bildē. 

## Iedarbināšana ar uvicorn
Servera darbībai nepieciešama Python 3.8 vide un bibliotēkas, kas ir definētas `requirements.txt` failā. Lai uzinstalētu bibliotēkas, jāpalaiž komanda:
```
pip install -r requirements.txt
```

Servera palaišana:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```


## Iedarbināšana ar Docker

Uzbūvējiet Docker attēlu ar:
```
docker build -t vmf-fotoweb-api .
```

Uzstārtējiet Docker konteineri:
```
docker run -d --name vmf-fotoweb-api -p 8000:80 vmf-fotoweb-api
```

## Pieprasījumu veidi
Mērījumu rezultātu dabūšana tiek nodrošināta ar POST pieprasījumu `/measure`. Pieprasījums sagaida attēlu apstrādei kā `form-data` faila atribūtu ar nosaukumu `file`.

"measure" pieprasījuma piemērs:
```
curl --location --request POST 'http://127.0.0.1:8089/measure' \
--form 'file=@"/path/to/file"'
```

"measure" atbildes piemērs:
```
{
    "height": 196,
    "length": 287,
    "geometry": {
        "master": {
            "type": "line",
            "geom": [
                0.48360692771016045,
                0.3485277652740479,
                0.5044987681361931,
                0.5360345363616944
            ]
        },
        "length": {
            "type": "line",
            "geom": [
                0.05707239877947372,
                0.27690718173980716,
                0.8609803726201957,
                0.27690718173980716
            ]
        },
        "height": {
            "type": "line",
            "geom": [
                0.43049018631009783,
                0.18533778190612793,
                0.43049018631009783,
                0.5538143634796143
            ]
        }
    }
}
```

## Dokumentācija
Palaižot serveri ar jebkuru no aprakstītām metodēm, dokumentācija ir pieejama servera `/docs` lapā, piemērām:
```
localhost:8000/docs
```
