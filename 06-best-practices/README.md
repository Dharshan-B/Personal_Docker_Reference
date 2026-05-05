# 🏆 Phase 6 — Best Practices

## 🎯 Goal
Write production-quality, secure, optimized Dockerfiles and Compose files.

---

## ✅ Best Practice Checklist

### Dockerfile Best Practices

- [ ] **Use specific image tags** — Never use `latest` in production
  ```dockerfile
  # ❌ Bad
  FROM node:latest
  
  # ✅ Good
  FROM node:18.19-alpine3.19
  ```

- [ ] **Use alpine variants** — Much smaller images
  ```dockerfile
  FROM python:3.11-slim    # ~130MB vs ~900MB full image
  FROM node:18-alpine      # ~50MB vs ~350MB full image
  ```

- [ ] **Optimize layer caching** — Copy dependencies BEFORE source code
  ```dockerfile
  # ✅ Efficient — npm install is cached unless package.json changes
  COPY package.json package-lock.json ./
  RUN npm ci
  COPY . .
  ```

- [ ] **Use multi-stage builds** — Keep final image lean
  ```dockerfile
  FROM node:18-alpine AS builder
  RUN npm run build
  
  FROM nginx:alpine AS production
  COPY --from=builder /app/dist /usr/share/nginx/html
  ```

- [ ] **Run as non-root user** — Security
  ```dockerfile
  RUN addgroup -S appgroup && adduser -S appuser -G appgroup
  USER appuser
  ```

- [ ] **Use .dockerignore** — Don't copy unnecessary files
  ```
  node_modules
  .env
  .git
  *.log
  ```

- [ ] **Set WORKDIR explicitly** — Don't work in root `/`
  ```dockerfile
  WORKDIR /app
  ```

- [ ] **Use COPY instead of ADD** — ADD has hidden magic, COPY is explicit
  ```dockerfile
  COPY . .   # ✅ Explicit
  ADD . .    # ❌ Avoid unless you need tar extraction or URL
  ```

- [ ] **Use ENV for configuration** — Makes images configurable
  ```dockerfile
  ENV PORT=3000
  ENV NODE_ENV=production
  ```

- [ ] **Add HEALTHCHECK** — Let Docker know when your app is ready
  ```dockerfile
  HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1
  ```

---

### Docker Compose Best Practices

- [ ] **Never hardcode secrets** — Use `.env` files or secrets
  ```yaml
  # .env file (never commit this!)
  DB_PASSWORD=mysecretpassword
  
  # docker-compose.yml
  environment:
    DB_PASSWORD: ${DB_PASSWORD}
  ```

- [ ] **Use healthchecks with depends_on** — Ensure services are ready
  ```yaml
  depends_on:
    db:
      condition: service_healthy
  ```

- [ ] **Set restart policies** — For production resilience
  ```yaml
  restart: unless-stopped
  ```

- [ ] **Use named volumes** — Not anonymous volumes
  ```yaml
  volumes:
    mydata:   # Named — survives docker compose down
  ```

- [ ] **Pin image versions** — Reproducible builds
  ```yaml
  image: postgres:15.4-alpine
  ```

- [ ] **Use custom networks** — Don't rely on default bridge
  ```yaml
  networks:
    backend:
    frontend:
  ```

---

## 📊 Image Size Optimization

Before and after comparison:

| Approach | Image Size |
|---|---|
| `FROM node:18` (full) | ~950 MB |
| `FROM node:18-slim` | ~240 MB |
| `FROM node:18-alpine` | ~170 MB |
| Multi-stage build | ~50–80 MB |

---

## 🔒 Security Tips

1. **Never put secrets in Dockerfiles** — They're visible in image history
2. **Use Docker secrets or environment variables** for sensitive data
3. **Scan images for vulnerabilities:**
   ```bash
   docker scout cves my-image:latest
   ```
4. **Keep base images updated** — Security patches
5. **Don't expose unnecessary ports**

---

## 🧠 My Notes

<!-- Add your best practice learnings here -->

### Optimizations I applied to my projects:


### Security issues I discovered:
