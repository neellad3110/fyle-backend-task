FROM python:3
WORKDIR /app
COPY . /app

ENV FLASK_APP=core/server.py

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app


RUN export FLASK_APP=core/server.py
RUN rm core/store.sqlite3
RUN flask db upgrade -d core/migrations/

EXPOSE 7755

