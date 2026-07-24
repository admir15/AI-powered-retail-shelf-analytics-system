from ultralytics import YOLO

model = YOLO("yolov8n.pt")

MAX_SHELF_CAPACITY = 10
LOW_STOCK_THRESHOLD = 0.3
CONFIDENCE_THRESHOLD = 0.5
INFERENCE_SIZE = 320


def detect_objects(frame):
    results = model(frame, verbose=False, conf=CONFIDENCE_THRESHOLD, imgsz=INFERENCE_SIZE)
    annotated_frame = results[0].plot()

    detected_count = len(results[0].boxes)

    occupancy_percentage = min(
        round((detected_count / MAX_SHELF_CAPACITY) * 100, 1),
        100.0
    )

    is_low_stock = (detected_count / MAX_SHELF_CAPACITY) < LOW_STOCK_THRESHOLD

    analytics = {
        "detected_count": detected_count,
        "occupancy_percentage": occupancy_percentage,
        "low_stock_alert": is_low_stock,
        "max_capacity": MAX_SHELF_CAPACITY,
    }

    return annotated_frame, analytics