import torch
import ultralytics
from ultralytics import YOLO
import utils
import cv2

def main():
    print(torch.cuda.is_available())
    ultralytics.checks()

    model = YOLO(f'./models/model.onnx')
    img = 'potatoes.jpg'
    results = model([img], save=True, save_txt=True)
    utils.save_test_results(img)

if __name__ == '__main__':
    main()