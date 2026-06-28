from ultralytics import YOLO

model = YOLO("runs/detect/runs/train/training_session/weights/best.pt")
print(model.names)