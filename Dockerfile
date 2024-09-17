FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirments.txt requirments.txt
RUN pip install --no-cache-dir -r requirments.txt

COPY cars /app/cars
WORKDIR /app/cars