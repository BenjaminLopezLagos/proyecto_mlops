import torch
import ultralytics
from ultralytics import YOLO

model = YOLO('./models/model.pt')

model.export(format='onnx')
