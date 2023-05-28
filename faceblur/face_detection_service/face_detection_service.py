from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
from yolov8 import YOLOv8Face
import io
from typing import Dict, List
import httpx
import base64

app = FastAPI()

model = YOLOv8Face('weights/yolov8n-face.onnx')


def detect_faces(model, image: np.ndarray) -> Dict[str, Dict[str, List[int]]]:
    # Detect Objects
    boxes = model.detect(image)

    # Prepare output format
    output = {}
    for i, box in enumerate(boxes):
        x1, y1, w, h = [int(val) for val in box]
        x2, y2 = x1 + w, y1 + h
        output[f"face_{i+1}"] = {'facial_area': [x1, y1, x2, y2]}
        
    return output

@app.post("/detect_faces")
async def detect_faces_endpoint(file: UploadFile = File(...)):
    image_data = await file.read()
    
    nparr = np.fromstring(image_data, np.uint8)
    
    # Decode the image from the bytes
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    faces = detect_faces(model, image)

    # Convert numpy integers to native Python integers
    for face in faces.values():
        face['facial_area'] = [int(num) for num in face['facial_area']]

    return faces

def blur_faces(image: np.ndarray, faces: Dict[str, Dict[str, List[int]]]):
    for face in faces.values():
        x1, y1, x2, y2 = face['facial_area']
        face_image = image[y1:y2, x1:x2]
        blurred_face = cv2.GaussianBlur(face_image, (99, 99), 30)
        image[y1:y2, x1:x2] = blurred_face
    return image

@app.post("/blur_faces")
async def blur_faces_endpoint(file: UploadFile = File(...)):
    image_data = await file.read()
    nparr = np.fromstring(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    timeout = httpx.Timeout(20.0, read=30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post('http://localhost:8001/detect_faces', files={'file': ('image.jpg', image_data, 'image/jpeg')})

    faces = response.json()

    blurred_image = blur_faces(image, faces)
    blurred_image = cv2.cvtColor(blurred_image, cv2.COLOR_RGB2BGR)
    _, image_data = cv2.imencode('.jpg', blurred_image)
    base64_image_data = base64.b64encode(image_data.tostring()).decode('utf-8')

    return {"image": base64_image_data}