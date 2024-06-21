import torch
import os
import shutil
from ultralytics import YOLO

def compare_models(model_path1, model_path2):
    print(torch.cuda.is_available())

    # Load the first model
    model1 = YOLO(model_path1)
    metrics1 = model1.val()

    # Load the second model
    model2 = YOLO(model_path2)
    metrics2 = model2.val(data='/app/data/raw_dataset/data.yaml')

    # Compare MAP50-95 and print which model is better
    print(metrics1.box.map)
    print(metrics2.box.map)
    if metrics1.box.map > metrics2.box.map:
        print("Model 1 has a higher MAP50-95.")
        shutil.copy2('./models/model_new.pt', './models/model_old.pt')
        shutil.copy2('./models/model_new.pt', './models/model.pt')
    elif metrics1.box.map < metrics2.box.map:
        raise Exception("Model 2 has a higher MAP50-95.")
    else:
        raise Exception("Both models have the same MAP50-95.")

def main():
    compare_models('./models/model_new.pt', './models/model_old.pt')

if __name__ == '__main__':
    main()