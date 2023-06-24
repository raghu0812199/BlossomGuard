from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2

model = YOLO('//runs/detect/train2/weights/best.pt')
results = model.predict(source="https://192.168.0.3:8080/video", conf=0.3, show=True)
print(results)