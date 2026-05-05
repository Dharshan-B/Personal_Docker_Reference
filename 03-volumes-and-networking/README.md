# 💾 Phase 3 — Volumes & Networking

## 🎯 Goal
Learn how to persist data beyond container lifecycles and connect containers to each other.

---

## 📖 Part 1: Volumes

### Why Volumes?

By default, containers are **stateless** — all data inside is lost when the container is removed.

```bash
docker run -it ubuntu bash
echo "hello" > /data/myfile.txt
exit
docker rm <container-id>
# ❌ /data/myfile.txt is GONE!
```

Volumes solve this by storing data **outside** the container.

---

### Types of Storage

| Type | Syntax | Use Case |
|---|---|---|
| **Named Volume** | `-v mydata:/app/data` | Recommended for production data |
| **Bind Mount** | `-v /host/path:/container/path` | Dev: sync code from host |
| **tmpfs Mount** | `--tmpfs /tmp` | In-memory, temporary data |

---

### Named Volumes (Recommended)

```bash
# Create a volume
docker volume create mydata

# Use it in a container
docker run -d \
  --name postgres-db \
  -e POSTGRES_PASSWORD=secret \
  -v mydata:/var/lib/postgresql/data \
  postgres:15

# Stop and remove the container
docker rm -f postgres-db

# Start a NEW container — data is still there!
docker run -d \
  --name postgres-db-new \
  -e POSTGRES_PASSWORD=secret \
  -v mydata:/var/lib/postgresql/data \
  postgres:15
```

### Bind Mounts (Development)

```bash
# Map current directory to /app in container
# Changes on host reflect INSTANTLY in container
docker run -d \
  -p 3000:3000 \
  -v ${PWD}:/app \
  -w /app \
  node:18-alpine \
  node index.js
```

---

## 📖 Part 2: Networking

### Docker Network Types

| Type | Description |
|---|---|
| `bridge` | Default network. Containers can communicate via IP |
| `host` | Container shares the host's network directly |
| `none` | No network access |
| **Custom bridge** | Best practice — containers find each other by **name** |

---

### Why Custom Networks?

On the default `bridge` network, containers can only reach each other by IP (which changes!).

On a **custom bridge network**, containers discover each other by **container name** automatically.

```bash
# ❌ Default bridge — need IP address
docker run -d --name db postgres
# Must use IP to connect — fragile!

# ✅ Custom network — use container name
docker network create myapp-network
docker run -d --name db --network myapp-network postgres
docker run -d --name api --network myapp-network my-api
# Inside 'api', connect to 'db' by name → postgresql://db:5432/mydb
```

---

## 🛠️ Exercises

### Exercise 1 — Volume persistence test
```bash
# Create a volume
docker volume create testdata

# Write data into it
docker run --rm -v testdata:/data alpine sh -c "echo 'Hello Volume!' > /data/test.txt"

# Read it back from a NEW container
docker run --rm -v testdata:/data alpine cat /data/test.txt
# Output: Hello Volume!

# Cleanup
docker volume rm testdata
```

### Exercise 2 — PostgreSQL with named volume
See `examples/postgres-with-volume.sh`

### Exercise 3 — Custom network communication
```bash
# Create network
docker network create demo-network

# Start a server container
docker run -d --name server --network demo-network nginx

# Start a client container and reach the server BY NAME
docker run --rm --network demo-network alpine wget -qO- http://server
# Returns nginx HTML — containers are talking!

# Cleanup
docker rm -f server
docker network rm demo-network
```

### Exercise 4 — Inspect network
```bash
docker network inspect bridge
docker network inspect demo-network
```

---

## 🧠 My Notes

<!-- Add your personal notes here -->

### What I understood:


### What confused me:


### Real-world scenarios I can think of:
