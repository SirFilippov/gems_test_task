FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /app

RUN pip install --upgrade pip
COPY req.txt /app/
RUN pip install -r req.txt

COPY . /app