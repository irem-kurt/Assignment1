# syntax=docker/dockerfile:1
FROM python:3.11.3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir -p /app/media

    