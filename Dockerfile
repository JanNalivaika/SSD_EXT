
# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN apt-get update 
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

# create weights
RUN python helper.py

ENV FLASK_APP=web/app.py

#start web app
CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0"]
