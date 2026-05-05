# 🚀 Phase 5 — Real-World Projects

## 🎯 Goal
Apply everything learned by building real, complete applications with Docker.

---

## Projects

### Project 1: Flask + Redis Hit Counter
**Folder:** `flask-redis-app/`

A Python web app that counts page visits using Redis as a cache.

**Concepts practiced:**
- Custom Dockerfile for Python
- Multi-service Docker Compose
- Container networking (Flask talks to Redis by name)
- Environment variables

```bash
cd flask-redis-app
docker compose up -d
# Visit http://localhost:5000
# Refresh page — counter increments!
docker compose down
```

---

### Project 2: WordPress + MySQL
**Folder:** `wordpress-mysql/`

A full WordPress site with MySQL database — industry-standard setup.

**Concepts practiced:**
- Using official images (no Dockerfile needed!)
- Named volumes for persistent data
- Environment variable configuration

```bash
cd wordpress-mysql
docker compose up -d
# Visit http://localhost:8080
# Complete WordPress setup wizard
docker compose down
# Data persists in volumes!
docker compose down -v  # This removes data too
```

---

## 🧠 My Notes

<!-- Add project-specific notes here -->

### Flask + Redis Learnings:


### WordPress + MySQL Learnings:


### Ideas for my own projects to Dockerize:
