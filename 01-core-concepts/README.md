# 📦 Phase 1 — Core Concepts

## 🎯 Goal
Understand what Docker is, how it works, and get comfortable with basic CLI commands.

---

## 📖 Key Concepts

### What is Docker?
Docker is a platform that lets you **package, ship, and run applications in containers**.

> Think of a container like a lightweight, portable box that contains your app + everything it needs to run (code, runtime, libraries, settings).

### Containers vs Virtual Machines

| Feature       | Container             | Virtual Machine           |
|---            |---                    |---                        |
| Size          | MBs                   | GBs                       |
| Startup Time  | Seconds               | Minutes                   |
| OS            | Shares host OS kernel | Full OS inside            |
| Isolation     | Process-level         | Full hardware-level       |
| Use Case      | Microservices, apps   | Full OS environments      |

### Docker Architecture

```
┌─────────────────────────────────────┐
│           Docker Client (CLI)       │  ← You type commands here
│         docker run / build / push   │
└──────────────────┬──────────────────┘
                   │ REST API
┌──────────────────▼──────────────────┐
│           Docker Daemon (dockerd)   │  ← Does the actual work
│   Manages images, containers,       │
│   networks, volumes                 │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│           Docker Registry           │  ← Stores images
│       (Docker Hub / private)        │
└─────────────────────────────────────┘
```

### Key Terms

| Term           | Definition                                    |
|---             |---                                            |
| **Image**      | Read-only blueprint/template for a container  |
| **Container**  | A running instance of an image                |
| **Dockerfile** | A script of instructions to build an image    |
| **Registry**   | A storage for Docker images (e.g., Docker Hub)|
| **Volume**     | Persistent storage for container data         |
| **Network**    | Communication channel between containers      |

---

## 🛠️ Hands-on Exercises

### Exercise 1 — Run your first container
```bash
docker run hello-world
```
**What happened?**
1. Docker looked for `hello-world` image locally
2. Didn't find it → pulled from Docker Hub
3. Created a container from the image
4. Container ran, printed message, then stopped

### Exercise 2 — Run an interactive Ubuntu shell
```bash
docker run -it ubuntu bash

# Inside the container:
ls
cat /etc/os-release
echo "I am inside a container!"
exit
```

### Exercise 3 — Run nginx web server
```bash
# -d = detached (background), -p = port mapping (host:container)
docker run -d -p 8080:80 --name my-nginx nginx

# Visit: http://localhost:8080
```

### Exercise 4 — Container lifecycle
```bash
docker ps                    # See running containers
docker ps -a                 # See ALL containers (including stopped)
docker stop my-nginx         # Stop the container
docker start my-nginx        # Start it again
docker restart my-nginx      # Restart it
docker rm my-nginx           # Delete the container
docker rm -f my-nginx        # Force delete (even if running)
```

### Exercise 5 — Image management
```bash
docker images                       # List all local images
docker pull node:18-alpine          # Pull a specific image
docker inspect nginx                # Detailed info about an image
docker history nginx                # See image layers
docker rmi nginx                    # Remove image (must have no containers)
```

### Exercise 6 — Logs & Execute commands
```bash
docker run -d --name my-nginx nginx

docker logs my-nginx                # View container logs
docker logs -f my-nginx             # Follow (live) logs
docker exec -it my-nginx bash       # Open shell in running container
docker exec my-nginx ls /etc/nginx  # Run a one-off command
```

---

## 🧠 My Notes



### What I understood:


### What confused me:


### Commands I keep forgetting:

