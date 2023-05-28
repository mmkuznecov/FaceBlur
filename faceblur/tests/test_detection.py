import pytest
import requests

@pytest.mark.asyncio
async def test_face_detection():
    with open('test_images/test.jpg', 'rb') as f:
        response = requests.post('http://localhost:8000/gateway/detect_faces', files={'file': f})
    assert response.status_code == 200