# 🚀 10 Real-World Dockerized Architectures

This guide details **10 production-grade, multi-container architectures** commonly deployed in real-world DevOps environments. Each project includes a complete architectural analysis, components breakdown, step-by-step data flow, and a production-ready `docker-compose.yml` boilerplate.

---

## 🗺️ Index of Projects

1. [Three-Tier Web App (React + Node.js + PostgreSQL)](#1-three-tier-web-app-react--nodejs--postgresql)
2. [Event-Driven Microservices (Python + Go + RabbitMQ + MongoDB)](#2-event-driven-microservices-python--go--rabbitmq--mongodb)
3. [Reverse Proxy & Caching CDN (Nginx + Redis + Node.js)](#3-reverse-proxy--caching-cdn-nginx--redis--nodejs)
4. [Centralized Logging Stack (Filebeat + Logstash + Elasticsearch + Kibana)](#4-centralized-logging-stack-elk--filebeat)
5. [Monitoring & Alerting Stack (Prometheus + Grafana + Node-Exporter)](#5-monitoring--alerting-stack-prometheus--grafana)
6. [Automated SSL Reverse Ingress (Nginx + Certbot Let's Encrypt)](#6-automated-ssl-reverse-ingress-nginx--certbot)
7. [Asynchronous Job Processing (Python Web App + Redis + Celery Workers)](#7-asynchronous-job-processing-python-web-app--redis--celery-workers)
8. [Secure API Gateway & Auth Service (Kong Gateway + JWT Auth + Microservices)](#8-secure-api-gateway--auth-service-kong-gateway--jwt-auth--microservices)
9. [Distributed Object Storage (MinIO S3 + Redis Metadata Cache + Node.js)](#9-distributed-object-storage-minio-s3--redis-metadata-cache)
10. [Self-Hosted CI/CD Runner (GitLab/GitHub Runner + Docker-in-Docker)](#10-self-hosted-cicd-runner-gitlabgithub-runner--docker-in-docker)

---

## 1. Three-Tier Web App (React + Node.js + PostgreSQL)
A classic web architecture where a frontend client communicates with a backend REST API, which persists data in a secure relational database.

### 🏗️ Architecture & Network Layout
```
               ┌────────────────────── Bridge Network ──────────────────────┐
               │                                                            │
  Client ────► │  [Nginx (Frontend)] ───► [Node.js API] ───► [PostgreSQL]  │
 (Port 80/443) │    (React SPA)                                             │
               └────────────────────────────────────────────────────────────┘
```

### ⚙️ How it Works
* **Nginx (Frontend):** Serves the compiled React static files (HTML/JS/CSS) and acts as a reverse proxy, routing all api calls `/api/*` to the Node.js backend.
* **Node.js (API):** Receives HTTP requests, performs business logic, authenticates requests, and queries the database.
* **PostgreSQL:** Persists relational data securely on a dedicated volume. It is not exposed to the public internet; only the API container can connect to it.

### 🔄 Data Flow
1. **Request:** A user opens `http://localhost`. The browser fetches the React build from **Nginx**.
2. **API Trigger:** The user submits a form. React sends an HTTP POST request to `http://localhost/api/users`.
3. **Routing:** **Nginx** intercepts the `/api/` prefix and forwards the request internally to the **Node.js API** container on port `5000`.
4. **Processing & DB:** The **Node.js API** parses the request, validates the payload, runs a SQL query, and inserts data into **PostgreSQL** on port `5432`.
5. **Response:** **PostgreSQL** returns the insert status $\rightarrow$ **Node.js** compiles a JSON response $\rightarrow$ **Nginx** sends it back to **React** $\rightarrow$ UI updates.

<details>
<summary>📂 View docker-compose.yml</summary>

```yaml
version: '3.8'
services:
  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./dist:/usr/share/nginx/html:ro
    depends_on:
      - api
    networks:
      - app-net

  api:
    build: ./api
    environment:
      DATABASE_URL: postgres://admin:secret@db:5432/production
    depends_on:
      - db
    networks:
      - app-net

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: production
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - app-net

volumes:
  pgdata:

networks:
  app-net:
```
</details>

---

## 2. Event-Driven Microservices (Python + Go + RabbitMQ + MongoDB)
An asynchronous, decoupled microservices system where services communicate by publishing and subscribing to events rather than direct HTTP requests.

### 🏗️ Architecture & Network Layout
```
               ┌─────────────────────── Event Mesh ─────────────────────────┐
  HTTP Request │                                                            │
 ────────────► │ [Python Publisher] ──► [RabbitMQ] ──► [Go Worker] ──► [Mongo]│
               │   (API Ingestion)        (Broker)      (Processor)    (NoSQL)  │
               └────────────────────────────────────────────────────────────┘
```

### ⚙️ How it Works
* **Python Publisher:** A FastAPI container exposed to the internet. It accepts incoming payloads and instantly publishes a "Job Created" event to RabbitMQ before returning a `202 Accepted` status.
* **RabbitMQ:** A message broker that receives, stores, and routes asynchronous events/messages to registered worker queues.
* **Go Worker:** A high-throughput background worker that continuously listens to RabbitMQ, processes raw messages, and performs CPU-intensive workloads.
* **MongoDB:** A document store used by the Go worker to log and save the final processed results.

### 🔄 Data Flow
1. **Ingestion:** User posts data to the **FastAPI** web server.
2. **Publishing:** **FastAPI** converts the payload into a JSON event and pushes it to a queue in **RabbitMQ** (AMQP port `5672`). It immediately returns a transaction ID to the user.
3. **Queueing:** **RabbitMQ** safely holds the message in memory/disk.
4. **Consuming:** The **Go Worker** container pulls the message off the queue, processes it asynchronously (e.g., resizing an image, generating a report).
5. **Storage:** The **Go Worker** writes the final document containing the outcome directly into **MongoDB** on port `27017`.

<details>
<summary>📂 View docker-compose.yml</summary>

```yaml
version: '3.8'
services:
  publisher:
    build: ./publisher
    ports:
      - "8000:8000"
    environment:
      RABBITMQ_URL: amqp://guest:guest@broker:5672/
    depends_on:
      - broker
    networks:
      - event-net

  broker:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672" # Admin GUI
    networks:
      - event-net

  worker:
    build: ./worker
    environment:
      RABBITMQ_URL: amqp://guest:guest@broker:5672/
      MONGO_URL: mongodb://db:27017/jobs
    depends_on:
      - broker
      - db
    networks:
      - event-net

  db:
    image: mongo:6.0
    volumes:
      - mongodata:/data/db
    networks:
      - event-net

volumes:
  mongodata:

networks:
  event-net:
```
</details>

---

## 3. Reverse Proxy & Caching CDN (Nginx + Redis + Node.js)
A performance-optimized architecture where slow database queries or page generations are cached in high-speed RAM, shielding backend servers from heavy traffic.

### 🏗️ Architecture & Network Layout
```
               ┌────────────────────── Caching Web ───────────────────────┐
  Client Req   │                                                          │
 ────────────► │  [Nginx Proxy] ──► [Node.js Server]                      │
               │                        │  ▲                              │
               │                        ▼  │                              │
               │                    [Redis Cache (RAM)]                   │
               └──────────────────────────────────────────────────────────┘
```

### ⚙️ How it Works
* **Nginx:** Handles SSL termination, load balances requests, and forwards requests to the Node.js API.
* **Node.js Server:** Houses the primary application logic. Before calling a slow database, it checks Redis.
* **Redis:** An in-memory, ultra-fast key-value data store used to cache API responses.

### 🔄 Data Flow
1. **Client Request:** Browser requests `/products/123`.
2. **Proxying:** **Nginx** forwards the request to **Node.js** container.
3. **Cache Lookup (Hit vs Miss):**
   * **Node.js** checks **Redis** (`GET product:123`).
   * **Cache Hit:** Redis instantly returns the data $\rightarrow$ Node.js responds to Nginx $\rightarrow$ Nginx responds to user (**Response Time: ~5ms**).
   * **Cache Miss:** Node.js queries the slow DB $\rightarrow$ Node.js writes the result to Redis with an expiration time (`SETEX product:123 3600`) $\rightarrow$ responds to user (**Response Time: ~200ms**).

<details>
<summary>📂 View docker-compose.yml</summary>

```yaml
version: '3.8'
services:
  proxy:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
    networks:
      - cache-net

  web:
    build: ./web
    environment:
      REDIS_HOST: cache
    depends_on:
      - cache
    networks:
      - cache-net

  cache:
    image: redis:7-alpine
    command: redis-server --save "" # Disable disk persistence for pure caching
    networks:
      - cache-net

networks:
  cache-net:
```
</details>

---

## 4. Centralized Logging Stack (ELK / Filebeat)
A complete log aggregation pipeline where application logs are scraped, parsed, and stored in a central repository for searching and auditing.

### 🏗️ Architecture & Network Layout
```
   ┌───────── Production App Container ────────┐
   │ [Application] ──(Logs)──► [Stdout/Stderr] │
   └────────────────────────────────┬──────────┘
                                    │ (Docker Log Driver)
                                    ▼
               ┌─────────────── Logging Pipeline ────────────────┐
               │                                                 │
               │ [Filebeat] ──► [Logstash] ──► [Elasticsearch]  │
               │   (Harvester)     (Parser)       (DB Index)     │
               │                                      ▲          │
               │                                      │ (Query)  │
               │                                  [Kibana]       │
               │                                 (Dashboard)     │
               └─────────────────────────────────────────────────┘
```

### ⚙️ How it Works
* **Filebeat:** A lightweight agent mounted to Docker's internal host log directory (`/var/lib/docker/containers`). It detects new lines written to container logs and ships them instantly.
* **Logstash:** A processing engine. It takes raw, unstructured logs from Filebeat, parses them (e.g., extracting JSON, timestamps, log levels), and enriches them.
* **Elasticsearch:** A distributed search engine that indexes and stores log records for instant querying.
* **Kibana:** The frontend visualization dashboard that queries Elasticsearch to plot search trends and graphs.

### 🔄 Data Flow
1. **Generation:** Your custom App container writes `{"level":"error", "msg":"Login failed"}` to standard output.
2. **Harvesting:** Docker logs this to a host file. **Filebeat** notices the modification and reads it.
3. **Parsing:** **Filebeat** ships the raw string to **Logstash** (port `5044`). Logstash parses the string, separating `level` from `msg`.
4. **Indexing:** **Logstash** pushes the structured JSON to **Elasticsearch** (port `9200`).
5. **Visualization:** The engineer opens **Kibana** (port `5601`) and filters logs for `level == "error"`. Kibana retrieves matches in real-time.

<details>
<summary>📂 View docker-compose.yml</summary>

```yaml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.8.1
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - es-data:/usr/share/elasticsearch/data
    networks:
      - elk-net

  logstash:
    image: docker.elastic.co/logstash/logstash:8.8.1
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf:ro
    ports:
      - "5044:5044"
    depends_on:
      - elasticsearch
    networks:
      - elk-net

  kibana:
    image: docker.elastic.co/kibana/kibana:8.8.1
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
    networks:
      - elk-net

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.8.1
    user: root
    volumes:
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
    depends_on:
      - logstash
    networks:
      - elk-net

volumes:
  es-data:

networks:
  elk-net:
```
</details>

---

## 5. Monitoring & Alerting Stack (Prometheus + Grafana)
A metrics aggregation and real-time observability platform that continuously pulls system and application statistics for monitoring.

### 🏗️ Architecture & Network Layout
```
               ┌───────────────────── Pull-Based Metrics ─────────────────────┐
               │                                                              │
   Grafana ──► │  [Prometheus]  ──(Pull)──► [Node Exporter]                   │
 (Port 3000)   │  (Time Series) ──(Pull)──► [App with Prometheus metrics]     │
               └──────────────────────────────────────────────────────────────┘
```

### ⚙️ How it Works
* **Node Exporter:** A lightweight daemon that collects hardware metrics (CPU, RAM, Disk usage) from the host machine and exposes them as a text endpoint `/metrics`.
* **Prometheus:** A scraper and time-series database. Instead of waiting for containers to send metrics, it **polls (pulls)** metrics from designated scrapable endpoints at fixed intervals.
* **Grafana:** Queries Prometheus data to design stunning, real-time diagnostic dashboards.

### 🔄 Data Flow
1. **Metrics Generation:** **Node Exporter** collects system CPU utilization on the host.
2. **Scraping (Pulling):** **Prometheus** (every 15s) makes an internal HTTP request to `http://node-exporter:9100/metrics` and `http://app:3000/metrics`.
3. **Ingestion:** **Prometheus** processes the text responses and stores them in its time-series database.
4. **Querying:** **Grafana** (on port `3000`) queries Prometheus using PromQL (`Prometheus Query Language`) to fetch CPU rates.
5. **Alerting:** If CPU utilization $> 90\%$ for 5 minutes, Prometheus triggers an alert and sends a payload to a configured webhook (like Slack or Discord).

<details>
<summary>📂 View docker-compose.yml</summary>

```yaml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:v2.44.0
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prom-data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - monitor-net

  grafana:
    image: grafana/grafana:9.5.2
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    depends_on:
      - prometheus
    networks:
      - monitor-net

  node-exporter:
    image: prom/node-exporter:v1.6.0
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
    networks:
      - monitor-net

volumes:
  prom-data:
  grafana-data:

networks:
  monitor-net:
```
</details>

---

## 6. Automated SSL Reverse Ingress (Nginx + Certbot)
A highly secure edge proxy architecture that terminates SSL, achieves an "A+" security rating, and dynamically renews Let's Encrypt certificates.

### 🏗️ Architecture & Network Layout
```
               ┌─────────────────────── Secure Boundary ──────────────────────┐
  HTTPS (443)  │                                                              │
 ────────────► │ [Nginx Proxy (SSL Terminated)] ──(Plain HTTP)──► [Web App]   │
               │       ▲                                                      │
               │       │ (Mounts Certificates)                                │
               │   [Certbot (Let's Encrypt)]                                  │
               └──────────────────────────────────────────────────────────────┘
```

### ⚙️ How it Works
* **Nginx:** Exposes ports `80` (HTTP) and `443` (HTTPS) to the internet. Standard HTTP traffic is redirected to HTTPS. It proxies clean decrypted internal traffic to downstream web servers.
* **Certbot (Let's Encrypt):** A containerized script that executes Let's Encrypt validation protocols. It generates and automates the renewal of free SSL certificates, dumping them into a shared folder.

### 🔄 Data Flow
1. **Verification Request:** **Certbot** starts up and requests Let's Encrypt for a domain certificate.
2. **ACME Challenge:** Let's Encrypt issues an ACME challenge file $\rightarrow$ **Certbot** places this challenge in a shared volume $\rightarrow$ Let's Encrypt hits `http://yourdomain.com/.well-known/acme-challenge/` to verify ownership.
3. **Certificate Issuance:** Ownership verified $\rightarrow$ Let's Encrypt issues the certificates $\rightarrow$ Certbot saves them in the shared volume `cert-vol`.
4. **Traffic Encryption:** Client initiates HTTPS connection $\rightarrow$ **Nginx** reads the certificates from `cert-vol` to complete the SSL handshake.
5. **Decrypted Proxying:** **Nginx** forwards the plain HTTP request to the internal **Web App** container securely inside the isolated Docker network.

<details>
<summary>📂 View docker-compose.yml</summary>

```yaml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - cert-vol:/etc/letsencrypt
      - web-root:/var/www/html
    depends_on:
      - app
    networks:
      - sec-net

  app:
    build: ./app
    networks:
      - sec-net

  certbot:
    image: certbot/certbot
    volumes:
      - cert-vol:/etc/letsencrypt
      - web-root:/var/www/html
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
    networks:
      - sec-net

volumes:
  cert-vol:
  web-root:

networks:
  sec-net:
```
</details>

---

## 7. Asynchronous Job Processing (Python Web App + Redis + Celery Workers)
A pattern designed to offload time-consuming tasks (e.g., resizing videos, generating PDF invoices, sending bulk emails) from the main API thread to isolated background workers.

### 🏗️ Architecture & Network Layout
```
               ┌────────────────────── Workers Mesh ──────────────────────┐
  Client Ingest│                                                          │
 ────────────► │  [FastAPI App] ──(Push Job)──► [Redis]                   │
               │                                   │                      │
               │                                   ▼                      │
               │                             [Celery Worker]              │
               │                              (Executes Job)              │
               └──────────────────────────────────────────────────────────┘
```

### ⚙️ How it Works
* **FastAPI App:** Handles user HTTP requests. It needs to perform heavy computations but must respond immediately to prevent UI lag.
* **Redis:** Acts as a broker, holding a queue of tasks in memory.
* **Celery Worker:** A Python container running background processes. It listens to Redis and pulls jobs down to process them one at a time.

### 🔄 Data Flow
1. **User Action:** Client uploads a video file to **FastAPI** to be transcoded to 1080p.
2. **Queuing:** FastAPI saves the file to disk and pushes a task message `{"task": "transcode", "file": "video.mp4"}` to **Redis** (port `6379`).
3. **Instant Response:** FastAPI immediately returns `{"status": "queued", "task_id": "999"}` to the client (Response time: ~10ms).
4. **Execution:** The **Celery Worker** detects the new task in **Redis**, locks it, and begins the CPU-intensive transcoding process.
5. **Completion:** Once done, the Celery Worker updates the job status in a shared database or Redis, allowing the frontend client to poll and see that the video is ready.

<details>
<summary>📂 View docker-compose.yml</summary>

```yaml
version: '3.8'
services:
  web:
    build: ./app
    ports:
      - "8000:8000"
    environment:
      CELERY_BROKER_URL: redis://broker:6379/0
    depends_on:
      - broker
    networks:
      - task-net

  broker:
    image: redis:7-alpine
    networks:
      - task-net

  worker:
    build: ./app
    command: celery -A tasks worker --loglevel=info
    environment:
      CELERY_BROKER_URL: redis://broker:6379/0
    depends_on:
      - broker
    networks:
      - task-net

networks:
  task-net:
```
</details>

---

## 8. Secure API Gateway & Auth Service (Kong Gateway + JWT Auth)
A centralized gatekeeper pattern where all public traffic flows through a single API Gateway which validates authorization before routing to internal microservices.

### 🏗️ Architecture & Network Layout
```
               ┌────────────────────── API Gateway ───────────────────────┐
  Client Req   │                                                          │
 ────────────► │ [Kong API Gateway] ────(Validate Token)──► [Auth Service]│
 (JWT Token)   │        │                                                 │
               │        ├──(Route Request)──► [Service A]                 │
               │        └──(Route Request)──► [Service B]                 │
               └──────────────────────────────────────────────────────────┘
```

### ⚙️ How it Works
* **Kong API Gateway:** The single entry point for all API calls. It handles rate-limiting, routing, logging, and security plug-ins.
* **Auth Service:** A lightweight service that verifies user credentials and signs JWT (JSON Web Tokens).
* **Service A & B:** Microservices that are completely isolated and do not handle public authentication themselves.

### 🔄 Data Flow
1. **Authentication:** User logs in at `http://api.domain.com/auth/login` $\rightarrow$ **Kong Gateway** routes this to the **Auth Service** $\rightarrow$ Auth Service returns a signed JWT token to the client.
2. **Accessing Services:** User makes an API call to `http://api.domain.com/users` with the Header `Authorization: Bearer <JWT>`.
3. **Gateway Verification:** **Kong** intercepts the request and runs its built-in JWT verification plugin.
4. **Authorized Routing:**
   * **If invalid:** Kong rejects the request instantly with a `401 Unauthorized` response.
   * **If valid:** Kong strips the authorization header, injects user metadata (like `X-User-Id`), and proxies the request to **Service A**.
5. **Decoupled execution:** **Service A** executes the business logic knowing the request is pre-authenticated.

<details>
<summary>📂 View docker-compose.yml</summary>

```yaml
version: '3.8'
services:
  kong-database:
    image: postgres:13-alpine
    environment:
      POSTGRES_USER: kong
      POSTGRES_DB: kong
      POSTGRES_PASSWORD: kong
    volumes:
      - kong_data:/var/lib/postgresql/data
    networks:
      - gateway-net

  kong-migration:
    image: kong:3.3
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_PASSWORD: kong
    depends_on:
      - kong-database
    command: kong migrations bootstrap
    networks:
      - gateway-net

  gateway:
    image: kong:3.3
    ports:
      - "8000:8000" # Public API HTTP
      - "8443:8443" # Public API HTTPS
      - "8001:8001" # Internal Admin API
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_PASSWORD: kong
      KONG_PROXY_LISTEN: 0.0.0.0:8000, 0.0.0.0:8443 ssl
    depends_on:
      - kong-database
    networks:
      - gateway-net

  auth-service:
    build: ./auth-service
    networks:
      - gateway-net

  service-a:
    build: ./service-a
    networks:
      - gateway-net

volumes:
  kong_data:

networks:
  gateway-net:
```
</details>

---

## 9. Distributed Object Storage (MinIO S3 + Redis Cache)
A private cloud architecture utilizing compatible S3 object storage for asset management, cached with high-speed key-value stores for lightning-fast media querying.

### 🏗️ Architecture & Network Layout
```
               ┌───────────────────── Storage Cache ──────────────────────┐
  Client Req   │                                                          │
 ────────────► │ [Node.js App] ──(Metadata Cache)──► [Redis Cache]        │
               │       │                                                  │
               │       └──(Retrieve File)──────────► [MinIO S3 Server]    │
               │                                      (Object Data)       │
               └──────────────────────────────────────────────────────────┘
```

### ⚙️ How it Works
* **MinIO:** A high-performance, S3-compatible object storage server. It stores binary large objects (BLOs) like images, videos, and zip files.
* **Redis:** Caches signed download URLs and file metadata to avoid querying MinIO continuously.
* **Node.js App:** Mediates requests, verifies if the requester has permissions, fetches pre-signed URLs, and serves files.

### 🔄 Data Flow
1. **Retrieval Attempt:** Client requests a pre-signed download link for a private file `profile_99.png`.
2. **Metadata Cache Check:**
   * **Node.js** checks **Redis** for the pre-signed URL.
   * **Cache Hit:** URL exists $\rightarrow$ Node.js redirects client immediately to the temporary CDN download URL (**Response Time: ~2ms**).
   * **Cache Miss:** Node.js makes an SDK query to **MinIO** (port `9000`) requesting a secure pre-signed URL valid for 15 minutes.
3. **Caching:** Node.js writes the generated URL to **Redis** with an expiration time of 14 minutes.
4. **Download:** The client receives the URL and downloads the secure object directly from **MinIO**.

<details>
<summary>📂 View docker-compose.yml</summary>

```yaml
version: '3.8'
services:
  app:
    build: ./app
    ports:
      - "3000:3000"
    environment:
      S3_ENDPOINT: storage
      S3_ACCESS_KEY: admin_user
      S3_SECRET_KEY: admin_password
      REDIS_HOST: cache
    depends_on:
      - storage
      - cache
    networks:
      - storage-net

  storage:
    image: minio/minio:RELEASE.2023-05-18T00-15-31Z
    ports:
      - "9000:9000" # API
      - "9001:9001" # Web Console
    environment:
      MINIO_ROOT_USER: admin_user
      MINIO_ROOT_PASSWORD: admin_password
    command: server /data --console-address ":9001"
    volumes:
      - minio-data:/data
    networks:
      - storage-net

  cache:
    image: redis:7-alpine
    networks:
      - storage-net

volumes:
  minio-data:

networks:
  storage-net:
```
</details>

---

## 10. Self-Hosted CI/CD Runner (GitLab/GitHub Runner + Docker-in-Docker)
A secure automated building machine used to execute CI/CD workflows, compiling code and building new Docker images inside an isolated sandbox environment.

### 🏗️ Architecture & Network Layout
```
               ┌─────────────────────── CI/CD Sandbox ────────────────────────┐
  Git Push     │                                                              │
 ────────────► │ [GitHub Runner] ──(Request Build)──► [Docker-in-Docker (DinD)]│
 (Trigger Event)│                                        (Spins up temp containers)
               └──────────────────────────────────────────────────────────────┘
```

### ⚙️ How it Works
* **GitHub Runner:** A container that continuously polls GitHub for newly triggered pipeline jobs. It downloads the pipeline steps and executes them.
* **Docker-in-Docker (DinD):** A special Docker daemon running inside an isolated container, allowing the Runner to run `docker build` and `docker run` inside its own environment without mounting the host's actual `docker.sock`.

### 🔄 Data Flow
1. **Trigger:** A developer pushes code to GitHub $\rightarrow$ GitHub Actions registers a new workflow.
2. **Polling:** The **GitHub Runner** container polls GitHub (port `443`), detects the pending build job, and claims it.
3. **Build Execution:** The runner parses the build steps (e.g. `docker build -t my-app:latest .`).
4. **Daemon Interfacing:** The runner communicates with the **Docker-in-Docker (DinD)** container over TLS/TCP (port `2376`) to build the new image inside DinD's local cache.
5. **Testing/Publishing:** The runner runs unit tests on the newly built container inside DinD, and if successful, triggers a push command sending the image to Docker Hub.

<details>
<summary>📂 View docker-compose.yml</summary>

```yaml
version: '3.8'
services:
  runner:
    image: my-custom-github-runner:latest
    environment:
      DOCKER_HOST: tcp://dind:2376
      DOCKER_TLS_VERIFY: 1
      DOCKER_CERT_PATH: /certs/client
      RUNNER_TOKEN: "YOUR_GITHUB_RUNNER_REGISTRATION_TOKEN"
    volumes:
      - shared-certs:/certs/client
    depends_on:
      - dind
    networks:
      - ci-net

  dind:
    image: docker:24.0-dind
    privileged: true # Required for nested containerization
    environment:
      DOCKER_TLS_CERTDIR: /certs
    volumes:
      - shared-certs:/certs
    networks:
      - ci-net

volumes:
  shared-certs:

networks:
  ci-net:
```
</details>
