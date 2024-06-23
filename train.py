import torch
import ultralytics
import yaml
import os
import dagshub
import mlflow
from ultralytics import YOLO
from roboflow import Roboflow
import utils

def main():
    dagshub.init(repo_owner='benjamin.lopezl', repo_name='proyecto_mlops', mlflow=True)
    with open(r"params.yaml") as f:
        with mlflow.start_run():
            mlflow.autolog()
            params = yaml.safe_load(f) 
            print(torch.cuda.is_available())
        
            ultralytics.checks()

            model = YOLO(f'./yolov8n.pt')

            name = params['NAME']
            workers = params['WORKERS']
            batch = params['BATCH']
            epochs = params['EPOCHS']
            
            results = model.train(task='detect', workers=workers,
                                data='/app/data/raw_dataset/data.yaml',
                                    epochs=epochs,
                                    cache=False,
                                        batch=batch,
                                        name=name)  # train the model
            
            utils.save_model(experiment_name=name)
            utils.save_metrics(experiment_name=name)

if __name__ == '__main__':
    main()