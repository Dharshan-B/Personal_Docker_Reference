# ✉️ Event-Driven Microservices (Python + Go + RabbitMQ + MongoDB)

An asynchronous microservices architecture that decouples API requests from heavy processing using a message broker.

## ⚙️ How It Works
* **Publisher (FastAPI):** Exposes a public POST endpoint `/jobs`. Instead of running the job, it drops the request onto RabbitMQ as an event and immediately returns a success response.
* **Broker (RabbitMQ):** Safely stores and handles the routing of asynchronous event queues.
* **Worker (Python Go-Mock):** Constantly consumes jobs from the RabbitMQ queue, processes them, and writes results to MongoDB.
* **Database (MongoDB):** A NoSQL document store where final processed states are logged.

## 🔄 Data Flow
1. Client POSTs a payload to `http://localhost:8000/jobs`.
2. The FastAPI Publisher enqueues the job into **RabbitMQ**'s `jobs` queue and instantly returns `{"status": "Accepted", "job_id": "..."}`.
3. The background **Worker** pulls the message off RabbitMQ, simulates a 2-second CPU processing task, and establishes a connection to **MongoDB**.
4. The Worker writes the final results directly into MongoDB.

## 🛠️ Step-by-Step Commands

### 1. Start the Stack
Start the message broker, API, worker, and MongoDB:
```bash
docker compose up -d
```

### 2. Verify Deployment
* Wait a few seconds for RabbitMQ to initialize.
* Trigger an asynchronous job via curl:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"data": "devops_exercise"}' http://localhost:8000/jobs
  ```
  *(You should get a `202 Accepted` response instantly).*
* Check worker logs to see it process the event:
  ```bash
  docker compose logs worker
  ```

### 3. Check Database Persistence
To verify the processed job made it to MongoDB, access the Mongo Shell inside the DB container:
```bash
docker compose exec db mongosh jobs --eval "db.processed_jobs.find().pretty()"
```

### 4. Clean Up
Stop the architecture:
```bash
docker compose down -v
```
