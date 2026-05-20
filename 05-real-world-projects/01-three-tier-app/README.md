# 3️⃣ Three-Tier Web Application (React + Node.js/Express + PostgreSQL)

A classic enterprise architecture separating the user interface, backend business logic, and secure database storage.

## ⚙️ How It Works
* **Frontend (Nginx):** Nginx serves static HTML, CSS, and JS (simulating a built React SPA) and reverse proxies API requests under `/api/` to the backend Node.js server.
* **Backend (Node.js/Express):** Handles incoming REST API requests, runs business logic, and interacts with PostgreSQL.
* **Database (PostgreSQL):** Persists relational records securely on an isolated internal network.

## 🔄 Data Flow
1. User requests `http://localhost` $ightarrow$ Nginx serves the static HTML/JS web interface.
2. The browser JavaScript makes an asynchronous `fetch('/api/users')` call.
3. Nginx intercepts `/api/` and routes it to `http://api:5000/users` internally.
4. The Node.js server receives the request, queries PostgreSQL on port `5432` to fetch the timestamp, and returns a JSON user list.
5. The frontend dynamically updates to show database connectivity.

## 🛠️ Step-by-Step Commands

### 1. Start the Stack
Spin up the frontend, backend, and PostgreSQL database:
```bash
docker compose up -d
```

### 2. Verify Deployment
* Check container statuses:
  ```bash
  docker compose ps
  ```
* Open your browser and visit: `http://localhost` (You should see "API & DB Connected!" along with the database time).
* Alternatively, test using curl:
  ```bash
  curl http://localhost/api/users
  ```

### 3. Clean Up (Teardown)
Stop containers and clean up the environment:
```bash
docker compose down
```
*To also wipe the persistent PostgreSQL volume:*
```bash
docker compose down -v
```
