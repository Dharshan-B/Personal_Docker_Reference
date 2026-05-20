# 📦 Private Cloud S3 Object Storage (MinIO + Redis Cache + Node.js)

An enterprise-ready media asset architecture deploying private, locally hosted S3-compatible cloud storage, cached dynamically with Redis.

## ⚙️ How It Works
* **App (Node.js):** The secure gateway connecting the client to storage. It verifies permissions, registers URLs, and caches metadata.
* **Storage (MinIO):** A high-performance, S3-compatible object storage server. Includes an interactive web interface on port `9001`.
* **Cache (Redis):** Caches pre-signed storage URLs to avoid contacting MinIO for every single object request.

## 🔄 Data Flow
1. User requests a media URL through the Node.js API.
2. The Node.js app checks Redis.
   * **Cache Hit:** URL exists $ightarrow$ Node.js redirects user immediately to download target.
   * **Cache Miss:** Node.js contacts MinIO over S3 SDK $ightarrow$ MinIO signs a secure download URL valid for 15m $ightarrow$ Node.js saves the URL in Redis cache for 14m $ightarrow$ Redirects user to download.

## 🛠️ Step-by-Step Commands

### 1. Start the Stack
Start the S3 server, Redis cache, and application:
```bash
docker compose up -d --build
```

### 2. Access the MinIO Web UI
1. Open your browser and visit: `http://localhost:9001`.
2. Log in with the credentials:
   * **Username:** `admin_user`
   * **Password:** `admin_password`
3. You can now visually create storage buckets, upload files, and configure S3 policies!

### 3. Verify Application Interface
Check the application entry point to ensure it's running:
```bash
curl http://localhost:3000
```

### 4. Clean Up
```bash
docker compose down -v
```
