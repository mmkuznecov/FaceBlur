# FaceBlur

This project provides a set of microservices that can detect and blur faces in images using the YOLOv8 face detection model. The services are containerized and can be run locally or deployed to a server.

## Services

* **gateway_service**: Exposes an HTTP API for users to interact with the service.
* **face_detection_service**: Contains the YOLOv8 face detection model and performs the face detection and blurring tasks.

## API description

| Endpoint | Method | Description
| --- | --- | --- |
| `/detect_faces` | POST | Accepts an image file and returns a task ID. The image file should be sent as a binary file in a multipart/form-data POST request. The task ID can be used to retrieve the result of the face detection task.
| `/blur_faces` | POST | Similar to the `/detect_faces` endpoint but instead of detecting faces, it blurs the faces in the image.
| `/task_result/{task_id}` | GET | Retrieves the result of a task. The task ID should be replaced with the ID returned from a POST request to `/detect_faces` or `/blur_faces`.

1. **Submit an image for face detection:**

```bash
curl -X POST -H "Content-Type: multipart/form-data" -F "file=@/path/to/your/image.jpg" "http://localhost:8000/detect_faces"
```

This command will submit an image to the /detect_faces endpoint for face detection. The @ symbol indicates a file upload. Replace /path/to/your/image.jpg with the actual path to your image file. You should get a JSON response that includes a task ID:

```json
{
  "task_id": "some-task-id"
}
```

2. **Submit an image for face blurring:**

```bash
curl -X POST -H "Content-Type: multipart/form-data" -F "file=@/path/to/your/image.jpg" "http://localhost:8000/blur_faces"
```

This command is similar to the previous one, but submits the image to the /blur_faces endpoint to blur faces in the image. The response will also include a task ID:

```json
{
  "task_id": "some-task-id"
}
```

3. **Get the result of a task:**

```bash
curl "http://localhost:8000/task_result/some-task-id"
```

This command retrieves the result of a task. Replace some-task-id with the actual task ID you received from one of the previous requests. The response will include the status of the task and, if the task is finished, the result will be similar to presented below:

```json
{
  "status": "SUCCESS",
  "result": {"face_1": {"facial_area": [1044, 232, 1465, 795]}, "face_2": {"facial_area": [220, 156, 623, 700]}}
}
```

or

```json
{
  "status": "SUCCESS",
  "result": "base64-encoded-image-data"
}
```

depending on whether the task was a face detection or face blurring task.


*Note: Due to the asynchronous nature of the tasks, you may need to send multiple requests to /task_result/some-task-id until the task is finished. If the task is still running or pending, the response will not include the result field.*

## Running the Services

The services can be run using Docker Compose with the following command:

```bash
docker-compose up --build
```

## Testing the Services

Scripts for testing the face detection and blurring services are included in the repository (test_detection.py and test_blurring.py respectively). They can be run with the following commands:


```bash
python test_detection.py
python test_blurring.py
```

## Demo

Face blurring demo can be found on [huggingface](https://huggingface.co/spaces/mmkuznecov/faceblur).