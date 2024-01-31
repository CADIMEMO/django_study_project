FROM python:3.11

ENV PYTHONUNBUFFERED = 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install django-debug-toolbar
RUN pip install drf-spectacular

COPY mysite .
