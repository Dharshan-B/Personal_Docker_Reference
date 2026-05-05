# ☸️ Phase 7 — Bridge to Kubernetes

## 🎯 Goal
Connect your Docker knowledge to Kubernetes — understand how they work together.

---

## 🔗 Docker → Kubernetes: The Connection

You already have Kubernetes YAML files open! Here's how Docker and Kubernetes relate:

| Docker Concept | Kubernetes Equivalent |
|---|---|
| `docker build` → Image | Image (stored in registry) |
| `docker run` → Container | Container (inside a Pod) |
| `docker-compose` service | Deployment |
| `-p port:port` | Service (NodePort/LoadBalancer) |
| `-v volume:/path` | PersistentVolumeClaim |
| `--network mynet` | Service (ClusterIP) |
| `docker-compose.yml` | Multiple YAML manifests |
| Docker Hub | Container Registry |
| `.env` file | ConfigMap / Secret |

---

## 🏗️ The Flow: Docker → Kubernetes

```
1. Write your app code
        ↓
2. Write a Dockerfile
        ↓
3. Build the image:
   docker build -t myapp:v1 .
        ↓
4. Push to registry:
   docker push yourusername/myapp:v1
        ↓
5. Reference in Kubernetes:
   spec:
     containers:
       - name: myapp
         image: yourusername/myapp:v1   ← Your Docker image!
        ↓
6. Apply the manifest:
   kubectl apply -f deployment.yaml
```

---

## 📖 Your nginx-deployment.yaml — Explained

Looking at your Kubernetes YAML file — the `image: nginx` is a Docker image from Docker Hub!

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: nginx
          image: nginx:1.25    # ← This is a Docker image!
          ports:
            - containerPort: 80
```

Docker equivalent:
```bash
docker run -d -p 80:80 --name nginx nginx:1.25
```

---

## 🛠️ Hands-on Exercise

### Step 1: Push your Node.js app from Phase 2 to Docker Hub

```bash
# Build
cd ../02-dockerfiles/basic-node-app
docker build -t my-node-app .

# Tag with your Docker Hub username
docker tag my-node-app YOUR_USERNAME/my-node-app:v1

# Login and push
docker login
docker push YOUR_USERNAME/my-node-app:v1
```

### Step 2: Use it in a Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-node-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-node-app
  template:
    metadata:
      labels:
        app: my-node-app
    spec:
      containers:
        - name: my-node-app
          image: YOUR_USERNAME/my-node-app:v1   # ← Your Docker image!
          ports:
            - containerPort: 3000
          env:
            - name: PORT
              value: "3000"
---
apiVersion: v1
kind: Service
metadata:
  name: my-node-app-service
spec:
  selector:
    app: my-node-app
  type: NodePort
  ports:
    - port: 80
      targetPort: 3000
      nodePort: 30080
```

```bash
kubectl apply -f k8s-deployment.yaml
kubectl get pods
kubectl get services
```

---

## 🔑 Key Differences: Docker vs Kubernetes

| Aspect | Docker | Kubernetes |
|---|---|---|
| **Scope** | Single host | Multiple hosts (cluster) |
| **Scaling** | Manual | Automatic (HPA) |
| **Self-healing** | No | Yes (restarts failed pods) |
| **Load balancing** | Manual/Compose | Built-in (Services) |
| **Config management** | .env files | ConfigMaps & Secrets |
| **Storage** | Volumes | PersistentVolumes |
| **Networking** | Docker networks | Services & Ingress |

---

## 🧠 My Notes

<!-- Connect Docker concepts to what you've learned in Kubernetes -->

### Kubernetes concepts that now make more sense:


### How my ConfigMap/Secret YAMLs relate to Docker .env files:


### What I want to explore next in Kubernetes:
