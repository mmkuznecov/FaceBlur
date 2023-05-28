import httpx
import time
import asyncio
import numpy as np

REQUESTS_NUM = 100

async def send_request(client, filename):
    start_time = time.time()
    files = {'file': open(filename, 'rb')}
    try:
        response = await client.post("http://localhost:8000/gateway/detect_faces", files=files, timeout=30.0)
    except httpx.ReadTimeout:
        return (time.time() - start_time, True)
    end_time = time.time()
    if response.status_code >= 400:
        return (end_time - start_time, True)
    else:
        return (end_time - start_time, False)


async def stress_test(filename, num_requests):
    async with httpx.AsyncClient() as client:
        tasks = []
        for _ in range(num_requests):
            tasks.append(send_request(client, filename))
        results = await asyncio.gather(*tasks)
    latencies, errors = zip(*results)
    return latencies, errors

def calculate_metrics(latencies, errors):
    # Convert to numpy arrays for easier manipulation
    latencies = np.array(latencies)
    errors = np.array(errors)
    # Calculate metrics
    avg_latency = np.mean(latencies)
    throughput = 1 / np.mean(latencies)
    error_rate = np.mean(errors)
    return avg_latency, throughput, error_rate

# Run the stress test
loop = asyncio.get_event_loop()
latencies, errors = loop.run_until_complete(stress_test('test.jpg', REQUESTS_NUM))
avg_latency, throughput, error_rate = calculate_metrics(latencies, errors)

print(f"Average Latency: {avg_latency} seconds")
print(f"Throughput: {throughput} requests per second")
print(f"Error Rate: {error_rate}")
