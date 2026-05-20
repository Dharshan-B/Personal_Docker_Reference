from fastapi import FastAPI
from tasks import process_heavy_data
from celery.result import AsyncResult

app = FastAPI()

@app.post("/tasks")
def trigger_task(payload: dict):
    # Offload work to Celery Worker
    task = process_heavy_data.delay(payload)
    return {"task_id": task.id, "status": "Queued"}

@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    res = AsyncResult(task_id)
    return {"task_id": task_id, "state": res.state, "result": res.result}

@app.get("/")
def root():
    return {"message": "Celery & FastAPI API. Send a POST to /tasks to enqueue jobs."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
