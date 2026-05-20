from fastapi import FastAPI, BackgroundTasks
import pika
import json
import os
import time

app = FastAPI()

def send_to_queue(message: dict):
    # Wait for RabbitMQ to be ready
    for _ in range(10):
        try:
            url = os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')
            params = pika.URLParameters(url)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.queue_declare(queue='jobs')
            channel.basic_publish(
                exchange='',
                routing_key='jobs',
                body=json.dumps(message)
            )
            connection.close()
            return True
        except Exception as e:
            print(f"Waiting for RabbitMQ... {e}")
            time.sleep(3)
    return False

@app.post("/jobs")
def create_job(payload: dict, background_tasks: BackgroundTasks):
    job_id = str(int(time.time()))
    task_payload = {"job_id": job_id, "data": payload}
    background_tasks.add_task(send_to_queue, task_payload)
    return {"status": "Accepted", "job_id": job_id}

@app.get("/")
def read_root():
    return {"message": "Publisher running. Post to /jobs to trigger work!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
