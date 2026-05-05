# 🎼 Phase 4 — Docker Compose

## 🎯 Goal
Define and run multi-container applications with a single YAML file.

---

## 📖 What is Docker Compose?

Docker Compose lets you define your **entire application stack** (multiple services, networks, volumes) in a single `docker-compose.yml` file.

```
Without Compose:
  docker network create mynet
  docker run -d --name db --network mynet -e POSTGRES_PASSWORD=... postgres
  docker run -d --name api --network mynet -p 3000:3000 my-api
  docker run -d --name frontend --network mynet -p 8080:80 my-frontend

With Compose:
  docker compose up -d  ← One command does EVERYTHING!
```

---

## 📋 docker-compose.yml Structure

```yaml
version: '3.8'           # Compose file format version

services:                # Your containers (services)
  service-name:
    image: nginx         # Use a pre-built image, OR
    build: ./app         # Build from a Dockerfile
    ports:
      - "host:container"
    environment:
      KEY: value
    volumes:
      - volume-name:/path
    networks:
      - my-network
    depends_on:
      - other-service    # Start this AFTER other-service
    restart: unless-stopped

volumes:                 # Define named volumes
  volume-name:

networks:                # Define custom networks
  my-network:
```

---

## 🔑 Key Concepts

### `depends_on`
Controls startup **order** — but does NOT wait for the service to be **ready**.
For DB readiness, use `healthcheck` or a wait script.

### `restart` policies

| Policy | Behaviour |
|---|---|
| `no` | Never restart (default) |
| `always` | Always restart |
| `on-failure` | Restart only on error exit |
| `unless-stopped` | Always restart unless manually stopped |

### Environment variables
```yaml
# Inline
environment:
  DB_HOST: db
  DB_PORT: 5432

# From .env file (recommended for secrets)
env_file:
  - .env
```

---

## 🛠️ Exercises

### Exercise 1 — Simple Webapp with Nginx
See `simple-webapp/docker-compose.yml`
```bash
cd simple-webapp
docker compose up -d
# Visit http://localhost:8080
docker compose logs
docker compose down
```

### Exercise 2 — Full Stack App
See `fullstack-app/docker-compose.yml`
```bash
cd fullstack-app
docker compose up -d
docker compose ps
docker compose logs -f backend
docker compose down -v
```

### Exercise 3 — Override for development
```bash
# Use multiple compose files
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

---

## 🧠 My Notes

<!-- Add your personal notes here -->

### What I understood:


### What confused me:


### Use cases I can see for my projects:
