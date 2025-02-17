FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

RUN apt-get update && \
    apt-get install -y ffmpeg

COPY backend/requirements.txt /backend/

RUN pip install --no-cache-dir -r requirements.txt
