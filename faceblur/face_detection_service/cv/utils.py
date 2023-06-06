import numpy as np
import cv2
import base64


def read_image(image_data):
    image = np.fromstring(image_data, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def blur_faces(image, bboxes):

    for bbox in bboxes:
        x1, y1, w, h = map(int, bbox)
        x2, y2 = x1 + w, y1 + h
        face = image[y1:y2, x1:x2]
        blurred_face = cv2.GaussianBlur(face, (99, 99), 30)
        image[y1:y2, x1:x2] = blurred_face
    return image


def bbox_to_json(bboxes):
    output = {}
    for i, box in enumerate(bboxes):
        x1, y1, w, h = map(int, box)
        x2, y2 = x1 + w, y1 + h
        output[f"face_{i+1}"] = {'facial_area': [x1, y1, x2, y2]}
    return output


def encode_image(image):
    _, encoded_image = cv2.imencode('.jpg', image)
    return base64.b64encode(encoded_image.tobytes()).decode('utf-8')


def process_image(image_data):

    image_data = base64.b64decode(image_data)
    image = read_image(image_data)

    return image


def detection_processing(image_data, model):
    image = process_image(image_data)
    bboxes = model.detect(image)
    json_bboxes = bbox_to_json(bboxes)
    return json_bboxes


def blurring_processing(image_data, model):
    image = process_image(image_data)
    bboxes = model.detect(image)
    image = blur_faces(image, bboxes)
    encoded_image = encode_image(image)
    return encoded_image