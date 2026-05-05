#!/bin/bash
# ─────────────────────────────────────────────────────
# Demo: PostgreSQL with persistent named volume
# Run this script step by step in your terminal
# ─────────────────────────────────────────────────────

echo "=== Step 1: Create a named volume ==="
docker volume create pg-data
docker volume ls

echo ""
echo "=== Step 2: Run PostgreSQL with the volume ==="
docker run -d \
  --name my-postgres \
  -e POSTGRES_DB=myapp \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret123 \
  -p 5432:5432 \
  -v pg-data:/var/lib/postgresql/data \
  postgres:15-alpine

echo "Waiting for PostgreSQL to start..."
sleep 5

echo ""
echo "=== Step 3: Create a table and insert data ==="
docker exec -it my-postgres psql -U admin -d myapp -c "
  CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
  );
  INSERT INTO users (name) VALUES ('Alice'), ('Bob'), ('Charlie');
  SELECT * FROM users;
"

echo ""
echo "=== Step 4: Remove the container (data stays in volume!) ==="
docker rm -f my-postgres
docker ps -a

echo ""
echo "=== Step 5: Create a NEW container using same volume ==="
docker run -d \
  --name my-postgres-new \
  -e POSTGRES_DB=myapp \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret123 \
  -p 5432:5432 \
  -v pg-data:/var/lib/postgresql/data \
  postgres:15-alpine

sleep 5

echo ""
echo "=== Step 6: Data is still there! ==="
docker exec -it my-postgres-new psql -U admin -d myapp -c "SELECT * FROM users;"

echo ""
echo "=== Cleanup ==="
docker rm -f my-postgres-new
docker volume rm pg-data
echo "Done!"
