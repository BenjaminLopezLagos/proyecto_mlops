import torch
import ultralytics
from ultralytics import YOLO

def main():
    print(torch.cuda.is_available())
    ultralytics.checks()

    model = YOLO(f'./runs/detect/train23/weights/best.pt')
    results = model(["./images (2).jpg"], save=True, save_txt=True)

if __name__ == '__main__':
    main()