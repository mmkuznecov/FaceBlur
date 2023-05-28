import pytest
import requests
import base64

@pytest.mark.asyncio
async def test_face_blurring():
    with open('test_images/test.jpg', 'rb') as f:
        response = requests.post('http://localhost:8000/gateway/blur_faces', files={'file': f})
    assert response.status_code == 200
    image_data = response.json()['image']