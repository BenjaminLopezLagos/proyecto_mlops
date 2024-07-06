import torch
import torch.nn as nn
import ultralytics
import yaml
import os
import dagshub
import mlflow
from ultralytics import YOLO
from roboflow import Roboflow
from sklearn.model_selection import ParameterGrid
import utils
from collections import defaultdict
from kfolds_yolo import perform_kfolds
from statistics import mean 

class WeightedLoss(nn.Module):
    def __init__(self, class_weights):
        super(WeightedLoss, self).__init__()
        self.class_weights = torch.tensor(class_weights)
        self.criterion = nn.CrossEntropyLoss(weight=self.class_weights)

    def forward(self, outputs, targets):
        return self.criterion(outputs, targets)

# if epochs is -1 just use the value from params.yaml
def train_current_hyperparams(hyperparams, data_path, name, epochs=-1):
    with open(r"params.yaml") as f:
        params = yaml.safe_load(f) 
        print(torch.cuda.is_available())
        
        ultralytics.checks()

        class_weights = compute_class_weights(f'{data_path}/train')
        model = YOLO(f'./yolov8n.pt')
        model.loss = WeightedLoss(class_weights)

        workers = params['WORKERS']
        batch = params['BATCH']
        if epochs == -1:
            epochs = params['EPOCHS']
            
        results = model.train(task='detect', workers=workers,
                            data=f'{data_path}/data.yaml',
                                epochs=epochs,
                                cache=False,
                                batch=batch,
                                name=name,
                                lr0=hyperparams['lr0'],
                                dropout=hyperparams['dropout'],
                                weight_decay=hyperparams['weight_decay'],
                                optimizer=hyperparams['optimizer'],)  # train the model
            
        results = model.val(data=f'{data_path}/data.yaml')

    return results.box.map

def perform_grid_search(param_grid, data_path, ksplits=5):
    best_params = {}
    best_map = 0
    folds = perform_kfolds(data_path, ksplits)

    for params in ParameterGrid(param_grid):
        cv_results = []
        print(len(list(ParameterGrid(param_grid))))

        for k in range(ksplits):
            dataset_yaml = folds[k]
            map = train_current_hyperparams(params, dataset_yaml, 'potato-detector-tuning', epochs=3)
            print(f"Params: {params}, map: {map}")
            cv_results.append(map)

        map = mean(cv_results)
        if map > best_map:
            best_map = map
            best_params = params

    return best_params

def compute_class_weights(dataset_path):
    class_counts = defaultdict(int)
    
    # Traverse through the dataset directory
    for root, _, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.txt'):
                annotation_path = os.path.join(root, file)
                with open(annotation_path, 'r') as f:
                    for line in f:
                        # The class index is the first element in each line
                        class_index = int(line.split()[0])
                        class_counts[class_index] += 1
    
    class_counts = dict(sorted(class_counts.items()))
    print(class_counts)
    total_samples = sum(class_counts.values())
    print(total_samples)
    class_weights = []
    for count in class_counts.values():
        n_classes = len(class_counts)
        weight = total_samples / (n_classes * count)
        class_weights.append(weight)
        
    return class_weights

def main():
    data_dir_path = './data/raw_dataset'
    print(compute_class_weights(f'{data_dir_path}/train'))
    experiment_name = 'potato-training'

    param_grid = {
        'lr0': [0.001, 0.0001],
        'dropout': [0.5, 0.0],
        'weight_decay': [0.01, 0.001],
        'optimizer': ['Adam'],
    }

    best_params = perform_grid_search(param_grid, data_dir_path)
    print(best_params)

    dagshub.init(repo_owner='benjamin.lopezl', repo_name='proyecto_mlops', mlflow=True)
    with mlflow.start_run():
        mlflow.autolog()
        results = train_current_hyperparams(best_params, data_path=data_dir_path, name=experiment_name)
            
        utils.save_model(experiment_name=experiment_name)
        utils.save_metrics(experiment_name=experiment_name)

if __name__ == '__main__':
    main()