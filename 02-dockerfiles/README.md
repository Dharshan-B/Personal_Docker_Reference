# 🖼️ Phase 2 — Dockerfiles & Images

## 🎯 Goal
Learn to write Dockerfiles and build your own custom Docker images.

---

## 📖 What is a Dockerfile?

A `Dockerfile` is a text file with a sequence of instructions that Docker uses to **build an image automatically**.

```
Dockerfile (instructions) → docker build → Image → docker run → Container
```

---

## 📋 Dockerfile Instructions

| Instruction | Purpose | Example |
|---|---|---|
| `FROM` | Base image (always first) | `FROM node:18-alpine` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `COPY` | Copy files from host to image | `COPY . .` |
| `ADD` | Like COPY but supports URLs & tar | `ADD app.tar.gz /app` |
| `RUN` | Run commands during **build** | `RUN npm install` |
| `ENV` | Set environment variables | `ENV PORT=3000` |
| `EXPOSE` | Document which port app uses | `EXPOSE 3000` |
| `CMD` | Default command on **start** | `CMD ["node", "index.js"]` |
| `ENTRYPOINT` | Fixed command (can't be overridden) | `ENTRYPOINT ["python"]` |
| `ARG` | Build-time variable | `ARG VERSION=1.0` |
| `VOLUME` | Create a mount point | `VOLUME /data` |
| `USER` | Set user for RUN/CMD | `USER node` |
| `LABEL` | Add metadata | `LABEL version="1.0"` |

---

## 🔑 CMD vs ENTRYPOINT

```dockerfile
# CMD — default command, can be overridden at runtime
CMD ["node", "index.js"]
# docker run myapp              → runs: node index.js
# docker run myapp bash         → runs: bash (overrides CMD)

# ENTRYPOINT — fixed command, args are appended
ENTRYPOINT ["python"]
CMD ["app.py"]
# docker run myapp              → runs: python app.py
# docker run myapp manage.py    → runs: python manage.py
```

---

## 🏗️ Image Layers

Each instruction in a Dockerfile creates a **layer**. Layers are cached:

```dockerfile
FROM node:18-alpine          # Layer 1
WORKDIR /app                 # Layer 2
COPY package.json .          # Layer 3  ← If unchanged, cache hits here
RUN npm install              # Layer 4  ← Only re-runs if layer 3 changed
COPY . .                     # Layer 5  ← Changes often
CMD ["node", "index.js"]     # Layer 6
```

> ✅ **Best Practice**: Copy `package.json` and install dependencies BEFORE copying all source code. This way, `npm install` is cached unless dependencies change.

---

## 🛠️ Exercises

### Exercise 1 — Basic Node.js App
See the `basic-node-app/` folder.
```bash
cd basic-node-app
docker build -t my-node-app .
docker run -d -p 3000:3000 --name nodeapp my-node-app
# Visit http://localhost:3000
docker logs nodeapp
docker rm -f nodeapp
```

### Exercise 2 — Multi-Stage Build
See the `multi-stage-build/` folder.
```bash
cd multi-stage-build
docker build -t my-app-optimized .
docker images  # Compare the size!
```

### Exercise 3 — Build with arguments
```bash
docker build --build-arg NODE_ENV=production -t my-app .
```

### Exercise 4 — Tag and push to Docker Hub
```bash
docker build -t my-node-app .
docker tag my-node-app YOUR_DOCKERHUB_USERNAME/my-node-app:v1
docker push YOUR_DOCKERHUB_USERNAME/my-node-app:v1
```

---

## 🧠 My Notes

<!-- Add your personal notes here -->

### What I understood:


### What confused me:


### Dockerfile patterns I found useful:
