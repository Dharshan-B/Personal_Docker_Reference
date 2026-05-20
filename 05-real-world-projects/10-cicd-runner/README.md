# 🏃 Self-Hosted CI/CD Builder (Runner + Docker-in-Docker)

A secure, isolated pipeline execution container that runs standard CI/CD build scripts, compiling code and executing nested `docker build` commands inside a sandbox.

## ⚙️ How It Works
* **Runner (GitLab):** A background worker daemon that queries GitLab/GitHub for pending build jobs.
* **DinD (Docker-in-Docker):** A secure, nested Docker daemon running inside its own container. Rather than sharing the host's `/var/run/docker.sock` (which gives root shell host access), the runner communicates with this isolated daemon via internal TLS/TCP (port `2376`).

## 🔄 Data Flow
1. Developer pushes code to GitLab/GitHub.
2. The **Runner** detects the trigger and fetches pipeline instructions.
3. The Runner executes `docker build` or `docker run` inside the pipeline.
4. The instructions are securely routed to the **DinD** sidecar container on port `2376`.
5. The DinD container spins up nested, ephemeral testing containers inside itself, safe from the host machine.

## 🛠️ Step-by-Step Commands

### 1. Start the Runner & Sandbox Daemon
Spin up the runner and the isolated nested Docker daemon:
```bash
docker compose up -d
```

### 2. Verify Nested Docker Connectivity
Log into the runner container and test if it has nested access to the sibling `dind` container:
```bash
docker compose exec runner docker info
```
*(This output will prove the runner can query the DinD container's engine over the network, ready to build nested images!)*

### 3. Clean Up
```bash
docker compose down -v
```
