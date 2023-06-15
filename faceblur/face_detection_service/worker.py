from celery import Celery
from cv.utils import detection_processing, blurring_processing
from cv.yolov8 import YOLOv8Face
from utils import read_config


# Initiate Celery
celery_app = Celery('face_detection',
                    broker='pyamqp://guest@rabbitmq//',
                    backend='redis://redis')

CONFIG = read_config('detection_config.yaml')

MODEL_PATH = CONFIG['model_path']

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
