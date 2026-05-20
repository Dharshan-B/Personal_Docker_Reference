# ⚡ Reverse Proxy & Caching CDN (Nginx + Redis + Node.js)

A performance-first cache pattern that stores slow database query responses in high-speed RAM, protecting backend servers from high-concurrency request spikes.

## ⚙️ How It Works
* **Proxy (Nginx):** Acts as the ingress gateway, forwarding traffic to the Node.js application.
* **Web (Node.js/Express):** Checks if the requested dataset is cached inside Redis. If not, it simulates a slow database retrieval, saves the response to Redis, and returns the result.
* **Cache (Redis):** An in-memory key-value database that stores ephemeral product caches.

## 🔄 Data Flow
1. User requests `http://localhost/data`.
2. **Nginx** proxies the request to the **Node.js** app container.
3. **Node.js** checks **Redis** (`GET product_data`).
   * **Cache Miss (First Run):** Redis has no data $ightarrow$ Node.js simulates a slow 1.5-second DB fetch $ightarrow$ Saves results to Redis for 60 seconds (`SETEX`) $ightarrow$ Responds to user.
   * **Cache Hit (Subsequent Runs):** Redis immediately returns the product in RAM $ightarrow$ Responds to user in less than 5ms.

## 🛠️ Step-by-Step Commands

### 1. Start the Stack
Spin up the proxy, app server, and Redis:
```bash
docker compose up -d
```

### 2. Verify Cache Performance
* **First Run (Cache Miss - Slow):**
  ```bash
  curl http://localhost/data
  ```
  *(Notice the 1.5s delay. Output will state `"source": "Cache Miss (Slow DB Run)"`).*
* **Second Run (Cache Hit - Instant):**
  ```bash
  curl http://localhost/data
  ```
  *(Output returns instantly. Output will state `"source": "Cache Hit (Redis)"` and `timeTakenMs` will be close to 0).*

### 3. Inspect Redis Directly
Open the Redis CLI inside the container to see the cached key:
```bash
docker compose exec cache redis-cli keys "*"
```

### 4. Clean Up
```bash
docker compose down
```
