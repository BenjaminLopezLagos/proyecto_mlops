import torch
import ultralytics
from ultralytics import YOLO

def main():
    print(torch.cuda.is_available())
    ultralytics.checks()

    model = YOLO(f'./models/model.pt')
    metrics = model.val()  # no arguments needed, dataset and settings remembered
    metrics.box.map  # map50-95
    metrics.box.map50  # map50
    metrics.box.map75  # map75
    metrics.box.maps  # a list contains map50-95 of each category

if __name__ == '__main__':
    main()