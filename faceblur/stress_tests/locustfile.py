from locust import HttpUser, task, between
import time


class FaceBlurUser(HttpUser):
    host = "http://gateway_service:8000"
    wait_time = between(1, 2)

    @task
    def post_image(self):
        with open('/test_imgs/test.jpg', 'rb') as image_file:
            files = {'file': ('test.jpg', image_file, 'image/jpeg')}
            with self.client.post("/detect_faces", files=files, catch_response=True) as response:
                if response.status_code != 200:
                    response.failure("Got wrong response")
                    return

                task_id = response.json()['task_id']

            # Poll until the task is done
            while True:
                with self.client.get(f"/task_result/{task_id}", catch_response=True) as response:
                    if response.status_code != 200:
                        response.failure("Got wrong response")
                        break

                    status = response.json()['status']
                    if status == "SUCCESS":
                        response.success()
                        break
                time.sleep(0.1)
