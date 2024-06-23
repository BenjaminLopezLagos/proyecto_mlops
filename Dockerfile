FROM python:3.10.14

WORKDIR /app

COPY requirements.txt /app/tmp/requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN pip install --no-cache-dir -r /app/tmp/requirements.txt
RUN pip install --no-cache-dir pytest

RUN useradd -m -u 1000 temp_user
USER temp_user

COPY . .

EXPOSE 5000
CMD ["python", "streaming_api.py"]
