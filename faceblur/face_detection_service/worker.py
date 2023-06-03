from celery import Celery
import io
import base64
from cv.utils import read_image, blur_faces, bbox_to_json, encode_image
from cv.yolov8 import YOLOv8Face
import os

# Initiate Celery
celery_app = Celery('face_detection', broker='pyamqp://guest@rabbitmq//', backend='redis://redis')

MODEL_PATH = "cv/weights/yolov8n-face.onnx"

# Initialize the model
model = YOLOv8Face(MODEL_PATH)

@celery_app.task(name='detect_faces_task')
def detect_faces_task(image_data):
    image_data = base64.b64decode(image_data)
    image = read_image(image_data)
    bboxes = model.detect(image)
    return bbox_to_json(bboxes)

@celery_app.task(name='blur_faces_task')
def blur_faces_task(image_data):
    image_data = base64.b64decode(image_data)
    image = read_image(image_data)
    bboxes = model.detect(image)
    image = blur_faces(image, bboxes)
    return encode_image(image)