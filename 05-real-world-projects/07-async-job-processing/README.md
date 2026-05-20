# 🕒 Asynchronous Job Processing (FastAPI + Redis + Celery)

A highly responsive pattern used to offload time-consuming tasks (like generating PDF reports or resizing images) to a dedicated worker pool, ensuring the main Web API remains fast and responsive.

## ⚙️ How It Works
* **Web (FastAPI):** Exposes endpoints to trigger long jobs and poll for results. It never executes the jobs itself.
* **Broker (Redis):** An in-memory queue broker holding queued tasks.
* **Worker (Celery):** An isolated worker container that listens to Redis, pulls queued jobs, executes them, and stores the status.

## 🔄 Data Flow
1. Client POSTs to `http://localhost:8000/tasks` requesting a heavy job.
2. FastAPI triggers the Celery worker task asynchronously (`tasks.process_heavy_data.delay(payload)`).
3. FastAPI immediately returns a `"task_id"` and `"status": "Queued"` to the user (Response Time: < 10ms).
4. The **Celery Worker** detects the job in **Redis**, locks it, and runs the 10-second task.
5. The client can fetch the status of the job at `GET /tasks/<task_id>` to see if it is `PENDING`, `SUCCESS`, or `FAILURE`.

## 🛠️ Step-by-Step Commands

### 1. Start the Stack
Spin up the FastAPI server, Redis broker, and Celery worker:
```bash
docker compose up -d --build
```

### 2. Trigger an Asynchronous Task
Enqueue a long-running job:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"item_id": 999}' http://localhost:8000/tasks
```
*(You will instantly receive a response containing your `task_id`).*

### 3. Poll for Task Progress
Using the `task_id` from the previous step, check if the worker is still working:
```bash
curl http://localhost:8000/tasks/<your-task-id>
```
*   **Within 10 seconds:** The status will show `"state": "PENDING"`.
*   **After 10 seconds:** The status will change to `"state": "SUCCESS"` and include the processed result.

### 4. Clean Up
```bash
docker compose down
```
