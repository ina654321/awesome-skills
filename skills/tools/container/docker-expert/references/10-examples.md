# Examples

## 10.1 Dockerfiles

### Node.js Production Dockerfile

```dockerfile
# syntax=docker/dockerfile:1.4
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies first (cache layer)
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY src/ ./src/
COPY tsconfig.json ./
COPY package*.json ./

# Build
RUN npm run build

# Production image
FROM node:20-alpine

WORKDIR /app

# Security: create non-root user
RUN addgroup -g 1000 -S appgroup && \
    adduser -u 1000 -S appuser -G appgroup

# Copy from builder
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/package.json ./

# Set environment
ENV NODE_ENV=production \
    PORT=8080

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:8080/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

EXPOSE 8080

CMD ["node", "dist/index.js"]
```

### Python Flask API Dockerfile

```dockerfile
FROM python:3.11-slim AS builder

WORKDIR /app

# Install pip and dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Create user
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -s /bin/sh appuser

# Copy installed packages
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY --chown=appuser:appgroup . .

USER appuser

ENV FLASK_APP=app.py \
    FLASK_ENV=production

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
```

### Go Application Dockerfile

```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder

RUN apk add --no-cache git

WORKDIR /app

# Copy go mod files first for caching
COPY go.mod go.sum ./
RUN go mod download

# Copy source
COPY . .

# Build
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/main .

# Production - distroless
FROM gcr.io/distroless/base:nonroot

WORKDIR /app

COPY --from=builder /app/main .

USER nonroot

EXPOSE 8080

ENTRYPOINT ["/app/main"]
```

### React Application Dockerfile

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production - nginx
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/build /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Add non-root user
RUN adduser -D -u 1000 nginx && \
    chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

USER nginx

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
```

## 10.2 Docker Compose Files

### Full-stack Application

```yaml
version: '3.8'

services:
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://user:password@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    networks:
      - backend

  web:
    build:
      context: ./web
      dockerfile: Dockerfile
    ports:
      - "8080:80"
    depends_on:
      - api
    networks:
      - frontend
      - backend

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - backend

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

## 10.3 kubectl Commands

### Basic Operations

```bash
# Build and push image
docker build -t myregistry.io/myapp:v1.0.0 .
docker push myregistry.io/myapp:v1.0.0

# Run container locally
docker run -d -p 8080:8080 --name myapp myregistry.io/myapp:v1.0.0

# View logs
docker logs -f myapp
docker logs --tail 100 myapp

# Interactive shell
docker exec -it myapp sh

# Inspect container
docker inspect myapp

# Check resource usage
docker stats

# Clean up
docker system prune -a
```

### Docker Compose Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Rebuild services
docker-compose up -d --build

# Scale service
docker-compose up -d --scale api=3

# Stop all services
docker-compose down

# Remove volumes too
docker-compose down -v

# Pull latest images
docker-compose pull

# Run a command in service
docker-compose exec api sh
```

### Multi-platform Build

```bash
# Enable buildx
docker buildx install
docker buildx create --name mybuilder
docker buildx use mybuilder

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myregistry.io/myapp:latest \
  --push .

# Build and load locally (arm64 on amd64 machine)
docker buildx build --platform linux/arm64 -t myapp:arm64 --load
```