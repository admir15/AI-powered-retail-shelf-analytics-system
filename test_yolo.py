from ultralytics import YOLO

model = YOLO("yolov8n.pt")

print("YOLO model loaded successfully!")
print("Classes this model can detect:", model.names)