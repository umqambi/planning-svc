FROM python:3.8.2-alpine3.10

RUN adduser -D planning-svc

WORKDIR /home/planning-svc

COPY requirements.txt requirements.txt
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY planning-svc.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP planning-svc.py
ENV SECRET_KEY "fd2lk2bep2o3be/sfv)ldsv!kjv4!34fg3k,m24"

RUN chown -R planning-svc:planning-svc ./
USER planning-svc