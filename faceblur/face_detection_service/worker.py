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
    """
    This function receives image data as a parameter,
    performs face detection on it using a pre-trained YOLOv8Face
    model and returns the bounding boxes of detected faces
    in JSON format.

    Parameters:
    - image_data: Image data to be processed.

    Returns:
    - JSON bounding boxes of detected faces.
    """
    json_bboxes = detection_processing(image_data, model)
    return json_bboxes


@celery_app.task(name='blur_faces_task')
def blur_faces_task(image_data):
    """
    This function receives image data as a parameter,
    blurs the faces detected in the image using a pre-trained
    YOLOv8Face model and returns the processed image.

    Parameters:
    - image_data: Image data to be processed.

    Returns:
    - The processed image with faces blurred.
    """
    encoded_image = blurring_processing(image_data, model)
    return encoded_image
