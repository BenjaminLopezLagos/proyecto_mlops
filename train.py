import torch
import ultralytics
from ultralytics import YOLO
from roboflow import Roboflow

def main():
    print(torch.cuda.is_available())
    ultralytics.checks()

    model = YOLO(f'./yolov8n.pt')

    results = model.train(task='detect', workers=4, data='data/raw_dataset/data.yaml', epochs=10, cache=False, batch=8)  # train the model

if __name__ == '__main__':
    main()