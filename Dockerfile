FROM python:3.8

RUN apt-get update && apt-get install -y libgl1-mesa-glx

ENV APP_HOME /code/app

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app $APP_HOME

CMD exec uvicorn app.main:app --host 0.0.0.0 --port 80