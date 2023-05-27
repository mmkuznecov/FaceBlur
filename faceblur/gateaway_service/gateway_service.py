from fastapi import FastAPI, UploadFile, File
import httpx
import base64
from json.decoder import JSONDecodeError

app = FastAPI()

async def send_image_to_detection_service(image_data, endpoint):
    url = f"http://localhost:8001/{endpoint}"
    files = {"file": ("image.jpg", image_data, "image/jpeg")}
    try:
        # Set a custom timeout (for example, 20 seconds)
        timeout = httpx.Timeout(20.0, read=30.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, files=files)
        return response.json()
    except JSONDecodeError:
        return {"error": "Failed to decode the response from the face detection service"}


@app.post("/gateway/detect_faces")
async def detect_faces(file: UploadFile = File(...)):
    image_data = await file.read()
    response = await send_image_to_detection_service(image_data, "detect_faces")
    return response

@app.post("/gateway/blur_faces")
async def blur_faces(file: UploadFile = File(...)):
    image_data = await file.read()
    response = await send_image_to_detection_service(image_data, "blur_faces")

    if "error" in response:
        return response

    base64_image_data = response['image']

    return {'image': base64_image_data}