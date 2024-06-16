FROM continuumio/miniconda3

WORKDIR /app

COPY env_test.yaml .

RUN conda env create -n myenv -f env_test.yaml

SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

COPY streaming_api.py .
COPY models/model.onnx ./models
COPY vid.mp4 .

RUN echo "conda activate myenv" >> ~/.bashrc
EXPOSE 5000
CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "streaming_api.py"]
