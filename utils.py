import os
import shutil
from pathlib import Path

def save_model(experiment_name: str):
    if os.path.isdir('runs'):
        model_weights = experiment_name + "/weights/best.pt"
        path_model_weights = os.path.join('.', "runs/detect", model_weights)

        shutil.copy(src=path_model_weights, dst=f'./models/model.pt')

def save_metrics(experiment_name: str) -> None:
    if os.path.isdir('runs'):
        path_metrics = os.path.join('.', "runs/detect", experiment_name)

        # save experiment training metrics  
        shutil.copy(src=f'{path_metrics}/results.csv', dst=f'./training_results/train_metrics.csv')