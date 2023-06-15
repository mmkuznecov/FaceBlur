import requests
import time
from testing_utils import read_config


def send_image_for_detection(image_filename, api_url):
    url = f"http://{api_url}/detect_faces"
    mime_type = 'image/jpeg'
    with open(image_filename, 'rb') as image_file:
        files = {
            'file': (image_filename, image_file, mime_type)
        }
        response = requests.post(url, files=files)

    if response.status_code == 200:
        return response.json()['task_id']
    else:
        print("Image submission failed.")
        return None


def get_task_result(task_id, api_url):
    url = f"http://{api_url}/task_result/{task_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Task result retrieval failed.")
        return None


def main():

    config = read_config('test_config.yaml')

    image_filename = config['test_img_path']
    api_url = config['api_url']

    task_id = send_image_for_detection(image_filename, api_url)

    if task_id:
        print(f"Submitted image for detection. Task ID: {task_id}")
        result = get_task_result(task_id, api_url)

        # Poll for result until task is done
        while result['status'] != 'SUCCESS':
            print("Task not ready yet. Waiting for 0.1 second...")
            time.sleep(0.1)
            result = get_task_result(task_id, api_url)

        if result['status'] == 'SUCCESS':
            print("Task finished. Result:")
            print(result['result'])
        else:
            print(f"Task failed with status {result['status']}")
    else:
        print("Failed to submit image for detection.")


if __name__ == "__main__":
    main()
