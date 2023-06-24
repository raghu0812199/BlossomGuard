from ultralytics import YOLO

model = YOLO()
model.train(data="D:/PyCharmProjects/flowerDetection2.0/datasets/data.yaml", epochs=30)