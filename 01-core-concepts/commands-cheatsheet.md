# 🐳 Docker CLI Cheat Sheet

> Quick reference for all essential Docker commands.

---

## 🖼️ Images

```bash
docker images                        # List all local images
docker pull <image>                  # Download image from registry
docker pull nginx:1.25               # Pull specific version/tag
docker build -t <name>:<tag> .       # Build image from Dockerfile
docker tag <image> <new-name>        # Rename/tag an image
docker rmi <image>                   # Remove image
docker rmi -f <image>                # Force remove image
docker image prune                   # Remove all unused images
docker inspect <image>               # Detailed image info (JSON)
docker history <image>               # Show image layers
docker save -o file.tar <image>      # Export image to tar file
docker load -i file.tar              # Import image from tar file
```

---

## 📦 Containers

```bash
# Run
docker run <image>                   # Run a container
docker run -d <image>                # Run detached (background)
docker run -it <image> bash          # Run interactive with terminal
docker run --name myapp <image>      # Give container a name
docker run -p 8080:80 <image>        # Map host:container port
docker run -e VAR=value <image>      # Set environment variable
docker run --rm <image>              # Auto-remove when stopped

# Manage
docker ps                            # List running containers
docker ps -a                         # List all containers
docker stop <container>              # Gracefully stop
docker start <container>             # Start a stopped container
docker restart <container>           # Restart container
docker rm <container>                # Remove stopped container
docker rm -f <container>             # Force remove running container
docker container prune               # Remove all stopped containers

# Inspect & Debug
docker logs <container>              # View logs
docker logs -f <container>           # Follow logs (live)
docker logs --tail 50 <container>    # Last 50 log lines
docker exec -it <container> bash     # Enter running container shell
docker exec <container> <cmd>        # Run command in container
docker inspect <container>           # Detailed container info
docker top <container>               # Show running processes
docker stats                         # Live resource usage (CPU/RAM)
docker cp <container>:/path ./local  # Copy file FROM container
docker cp ./local <container>:/path  # Copy file TO container
```

---

## 💾 Volumes

```bash
docker volume create <name>          # Create a named volume
docker volume ls                     # List all volumes
docker volume inspect <name>         # Detailed volume info
docker volume rm <name>              # Remove a volume
docker volume prune                  # Remove all unused volumes

# Use volumes when running containers
docker run -v <volume>:/path <image>         # Named volume
docker run -v /host/path:/container/path <image>  # Bind mount
docker run -v $(pwd):/app <image>            # Current dir bind mount
```

---

## 🌐 Networks

```bash
docker network ls                    # List networks
docker network create <name>         # Create custom network
docker network rm <name>             # Remove network
docker network inspect <name>        # Detailed network info
docker network prune                 # Remove unused networks

# Connect containers to network
docker run --network <name> <image>
docker network connect <network> <container>     # Add running container
docker network disconnect <network> <container>  # Remove from network
```

---

## 🎼 Docker Compose

```bash
docker compose up                    # Start all services
docker compose up -d                 # Start detached (background)
docker compose up --build            # Rebuild images before starting
docker compose down                  # Stop and remove containers
docker compose down -v               # Also remove volumes
docker compose ps                    # List compose services
docker compose logs                  # View all service logs
docker compose logs -f <service>     # Follow specific service logs
docker compose exec <service> bash   # Shell into a service
docker compose build                 # Build/rebuild images only
docker compose pull                  # Pull latest images
docker compose restart <service>     # Restart specific service
docker compose stop                  # Stop without removing
docker compose start                 # Start stopped services
```

---

## 🏷️ Registry & Docker Hub

```bash
docker login                         # Login to Docker Hub
docker logout                        # Logout

docker tag myapp yourusername/myapp:v1        # Tag for push
docker push yourusername/myapp:v1             # Push to Docker Hub
docker pull yourusername/myapp:v1             # Pull from Docker Hub
```

---

## 🧹 Cleanup (System Prune)

```bash
docker system df                     # Show disk usage
docker system prune                  # Remove all unused resources
docker system prune -a               # Also remove unused images
docker system prune -a --volumes     # Also remove volumes (CAREFUL!)
```

---

## 🔍 Useful Flags Reference

| Flag | Short | Meaning |
|------|-------|---------|
| `--detach` | `-d` | Run in background |
| `--interactive` | `-i` | Keep STDIN open |
| `--tty` | `-t` | Allocate a terminal |
| `--publish` | `-p` | Publish port (host:container) |
| `--volume` | `-v` | Mount volume |
| `--env` | `-e` | Set environment variable |
| `--name` | | Assign container name |
| `--network` | | Connect to a network |
| `--rm` | | Auto-remove when stopped |
| `--build` | | Rebuild image (compose) |

---

## 💡 Common Patterns

```bash
# Enter a running container to debug
docker exec -it <container> bash

# See what's inside an image without running it
docker run --rm -it <image> ls /

# Follow logs of a specific service in compose
docker compose logs -f api

# Run a one-off command in compose service
docker compose run --rm api python manage.py migrate

# Remove EVERYTHING (nuclear option)
docker system prune -a --volumes
```
