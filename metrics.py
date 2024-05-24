import torch
import ultralytics
from ultralytics import YOLO

def main():
    print(torch.cuda.is_available())
    ultralytics.checks()

    model = YOLO(f'./models/model.pt')
    metrics = model.val()  # no arguments needed, dataset and settings remembered

if __name__ == '__main__':
    main()