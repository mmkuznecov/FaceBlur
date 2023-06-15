from fastapi import FastAPI, UploadFile, File
from celery import Celery
from celery.result import AsyncResult
import base64

app = FastAPI()

# Create a Celery instance
celery_app = Celery('gateway_service',
                    broker='pyamqp://guest@rabbitmq//',
                    backend='redis://redis')


@app.post("/detect_faces")
async def detect_faces(file: UploadFile = File(...)):
    """
    Endpoint to receive an image file,
    perform face detection and return a task ID.

    Parameters:
    - file: Image file uploaded by the user.

    Returns:
    - A dictionary containing a 'task_id' key
    with the ID of the face detection task.
    """
    image_data = await file.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')
    task = celery_app.send_task("detect_faces_task", args=[base64_image])
    return {"task_id": str(task.id)}


@app.post("/blur_faces")
async def blur_faces(file: UploadFile = File(...)):
    """
    Endpoint to receive an image file,
    blur the faces in the image, and return a task ID.

    Parameters:
    - file: Image file uploaded by the user.

    Returns:
    - A dictionary containing a 'task_id' key
    with the ID of the face blurring task.
    """
    image_data = await file.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')
    task = celery_app.send_task('blur_faces_task', args=[base64_image])
    return {"task_id": str(task.id)}


@app.get("/task_result/{task_id}")
def get_task_result(task_id: str):
    """
    Endpoint to get the result of a specific task based on the task ID.

    Parameters:
    - task_id: ID of the task whose result is to be fetched.

    Returns:
    - A dictionary containing 'status' key indicating the status of the task.
    If the task is successful,
    it also contains a 'result' key with the task's result.
    """
    task = AsyncResult(task_id, app=celery_app)
    if task.successful():
        result = task.result
        response = {
            "status": "SUCCESS",
            "result": result,
        }
    elif task.failed():
        response = {"status": "FAILURE"}
    elif task.state == 'PENDING':
        response = {"status": "PENDING"}
    else:
        response = {"status": "RUNNING"}
    return response
