from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from backend.services.camera_service import generate_frames, start_camera_thread, stop_camera_thread
import backend.services.camera_service as camera_service

app = FastAPI(title="Retail Shelf Analytics API")

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup_event():
    start_camera_thread()


@app.on_event("shutdown")
def shutdown_event():
    stop_camera_thread()


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/video_feed")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/analytics")
def get_analytics():
    return camera_service.latest_analytics