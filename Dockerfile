#FROM python:3.10.14
FROM nvidia/cuda:12.5.0-runtime-ubuntu22.04

WORKDIR /app

COPY requirements.txt /app/tmp/requirements.txt

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r /app/tmp/requirements.txt
RUN pip install --no-cache-dir pytest

COPY . .

EXPOSE 5000
CMD ["python", "streaming_api.py"]

