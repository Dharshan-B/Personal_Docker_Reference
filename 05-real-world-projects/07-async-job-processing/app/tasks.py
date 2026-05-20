from celery import Celery
import time
import os

broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app = Celery('tasks', broker=broker_url, backend=broker_url)

@app.task
def process_heavy_data(data: dict):
    print(f"Starting async processing of: {data}")
    # Simulate intensive video processing/report generation
    time.sleep(10)
    print("Async processing finished!")
    return {"status": "SUCCESS", "input_data": data}
