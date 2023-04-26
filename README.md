# VMF Fotoweb API
Šīs ir REST API serveris, kas ļauj noteikt mērkoka un kravas koordinātes bildē, saņemot rezultātu JSON formātā.

## Sistēmas apraksts
Serveris ir uzrakstīts, izmantojot Python programmēšanas valodu. Tā pamatā ir [FastAPI](https://fastapi.tiangolo.com/) programmēšanas ietvars (framework), kas vienkāršo REST API izveidi.  Datorredzes risinājums ir [YOLOv5](https://github.com/ultralytics/yolov5) Pytorch modelis, kas tika apmācīts konkrētam nolūkam - mērkoka un kokmateriālu kravas atpazīšanai bildē. 

## Iedarbināšana ar uvicorn
Servera darbībai nepieciešama Python 3.8 vide un bibliotēkas, kas ir definētas `yolov5` github konta un lokālajā `requirements.txt` failā. Lai uzinstalētu šīs bibliotēkas, jāpalaiž sekojošas komandas:
```
pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt
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

### Saiņa uzmērīšana: measure
Mērījumu rezultātu dabūšana tiek nodrošināta ar POST pieprasījumu `/measure`. Pieprasījums sagaida attēlu apstrādei kā `form-data` faila atribūtu ar nosaukumu `file`.

"measure" pieprasījuma piemērs:
```
curl --location --request POST 'http://127.0.0.1:8000/measure' \
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
Uzmērīšanas pieprasījums sagādās atbildi, tikai ja bildē ir redzams gan sainis, gan mērkoks. Ja kāds no tiem nav redzams, atbilde ir `null`

### Saiņu atpazīšana: detect
Gadījumos, kad nepieciešams izdabūt tikai saiņu skaitu, jāizmanto POST pieprasījums `/detect`. Pieprasījums sagaida attēlu apstrādei kā `form-data` faila atribūtu ar nosaukumu `file`.

"detect" pieprasījuma piemērs:
```
curl --location --request POST 'http://127.0.0.1:8000/detect' \
--form 'file=@"/path/to/file"'
```

"detect" atbildes piemērs:
```
[
    {
        "score": 0.4729708135128021,
        "x1": 0.2542073726654053,
        "x2": 0.4044743061065674,
        "y1": 0.1198440844542347,
        "y2": 0.6643966674688272
    },
    {
        "score": 0.32955077290534973,
        "x1": 0.6712018013000489,
        "x2": 0.8507447242736816,
        "y1": 0.26368020835798234,
        "y2": 0.727583143603988
    }
]
```
Saiņu skaita noteikšanas pieprasījums nostrādās arī gadījumos, kad bildē nav mērkoks.

## Dokumentācija
Palaižot serveri ar jebkuru no aprakstītām metodēm, dokumentācija ir pieejama servera `/docs` lapā, piemērām:
```
localhost:8000/docs
```
