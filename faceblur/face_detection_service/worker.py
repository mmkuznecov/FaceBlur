from celery import Celery
import io
from cv.utils import detection_processing, blurring_processing
from cv.yolov8 import YOLOv8Face
import os

# Initiate Celery
celery_app = Celery('face_detection', broker='pyamqp://guest@rabbitmq//', backend='redis://redis')

MODEL_PATH = "cv/weights/yolov8n-face.onnx"

# Initialize the model
model = YOLOv8Face(MODEL_PATH)

@celery_app.task(name='detect_faces_task')
def detect_faces_task(image_data):
    json_bboxes = detection_processing(image_data, model)
    return json_bboxes

@celery_app.task(name='blur_faces_task')
def blur_faces_task(image_data):
    encoded_image = blurring_processing(image_data, model)
    return encoded_image