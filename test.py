import torch
import ultralytics
from ultralytics import YOLO
import utils

def main():
    print(torch.cuda.is_available())
    ultralytics.checks()

    img = 'potatoes.jpg'
    model = YOLO(f'./models/model.pt')
    results = model([img], save=True, save_txt=True)
    utils.save_test_results(img)

if __name__ == '__main__':
    main()