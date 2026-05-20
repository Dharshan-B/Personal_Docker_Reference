# Stage 1: Builder — installs all dependencies and compiles
FROM node:18-alpine AS builder

WORKDIR /app

# Copy only package files first (caching optimization)
COPY package*.json ./
RUN mkdir -p node_modules && npm install --omit=dev

# Copy source code
COPY . .

# Stage 2: Production — only copy what's needed
FROM node:18-alpine AS production

# Security: run as non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

WORKDIR /app

# Copy ONLY the built artifacts from builder stage
COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/index.js ./

EXPOSE 3000

CMD ["node", "index.js"]
