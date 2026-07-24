import cv2
import threading
import time
from backend.core.config import settings
from backend.services.detection_service import detect_objects

latest_frame = None
latest_analytics = {
    "detected_count": 0,
    "occupancy_percentage": 0.0,
    "low_stock_alert": False,
    "max_capacity": 10,
}
frame_lock = threading.Lock()
stop_event = threading.Event()

PROCESS_EVERY_N_FRAMES = 5
JPEG_QUALITY = 70


def camera_capture_loop():
    global latest_frame, latest_analytics

    cap = cv2.VideoCapture(settings.camera_index, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        return

    print("Camera capture loop started.")

    frame_count = 0
    annotated_frame = None
    encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            time.sleep(0.1)
            continue

        frame_count += 1

        if frame_count % PROCESS_EVERY_N_FRAMES == 0:
            annotated_frame, analytics = detect_objects(frame)
            with frame_lock:
                latest_analytics = analytics
        else:
            annotated_frame = frame

        success, buffer = cv2.imencode('.jpg', annotated_frame, encode_params)
        if not success:
            continue

        with frame_lock:
            latest_frame = buffer.tobytes()

    cap.release()
    print("Camera capture loop stopped cleanly.")


def start_camera_thread():
    thread = threading.Thread(target=camera_capture_loop, daemon=True)
    thread.start()


def stop_camera_thread():
    stop_event.set()


def generate_frames():
    while not stop_event.is_set():
        with frame_lock:
            frame_bytes = latest_frame

        if frame_bytes is None:
            time.sleep(0.05)
            continue

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
        )

        time.sleep(0.02)