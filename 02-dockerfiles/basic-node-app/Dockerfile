# ─────────────────────────────────────────────
# Basic Node.js App — Dockerfile
# ─────────────────────────────────────────────

# 1. Base image — alpine is lightweight (~5MB vs ~900MB for full node)
FROM node:18-alpine

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy package.json FIRST — so npm install is cached
#    (only re-runs when package.json changes, not when code changes)
COPY package.json .

# 4. Install dependencies
RUN npm install

# 5. Copy rest of the source code
COPY . .

# 6. Document which port the app listens on (informational)
EXPOSE 3000

# 7. Set environment variables with defaults
ENV PORT=3000
ENV APP_NAME="Docker Learning App"

# 8. Command to run when container starts
CMD ["node", "index.js"]
