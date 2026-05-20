# 🚪 API Gateway & Authentication Gateway (Kong + PostgreSQL)

A centralized ingress gateway managing API routing, security boundaries, rate-limiting, and credentials validation at the edge of your microservices network.

## ⚙️ How It Works
* **Gateway (Kong):** Built on top of Nginx, Kong acts as a single gatekeeper entry point routing public traffic internally.
* **Database (PostgreSQL):** Kong's configuration storage, saving configured services, routes, and authentication plugins.
* **Migration Container:** A temporary service that automatically seeds database tables in Postgres before Kong boots.

## 🔄 Data Flow
1. Clients query a single public endpoint on port `8000`.
2. Kong interceptors inspect the header (e.g. searching for a API key or JWT token).
   * **If invalid:** Kong drops the connection directly, keeping internal microservices completely safe from malicious spikes.
   * **If valid:** Kong strips unnecessary headers and proxies the clean request to internal containers (like `auth-service` or `payment-service`).

## 🛠️ Step-by-Step Commands

### 1. Boot up database and run DB migrations
Kong requires PostgreSQL tables to be fully seeded before the gateway container starts up:
```bash
docker compose up -d kong-database
docker compose up kong-migration
```
*(Ensure the migration container prints database initialization success before starting Kong).*

### 2. Spin up the API Gateway
Now, start the main Kong Gateway engine:
```bash
docker compose up -d gateway
```

### 3. Verify Admin Console Connectivity
Kong's administrative REST API listens on port `8001`. Query it to ensure the gateway is operational:
```bash
curl http://localhost:8001/status
```

### 4. Clean Up
```bash
docker compose down -v
```
