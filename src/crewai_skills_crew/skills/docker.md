# Skill: docker

## Purpose
Build, run, and manage Docker containers and images.

## When to use
- Building container images from Dockerfiles
- Running, stopping, or debugging containers
- Managing Docker Compose multi-service stacks
- Pushing images to registries (Docker Hub, ACR, ECR, GCR)
- Inspecting logs, networking, or volumes

## Prerequisites
- Docker installed and running: `docker --version`
- Docker Compose: `docker compose version`

## How to execute

**Build an image:**
```bash
docker build -t myapp:latest .
docker build -t myapp:v1.0 -f Dockerfile.prod .
```

**Run a container:**
```bash
# Basic run
docker run -d --name myapp -p 8080:80 myapp:latest

# With env vars and volume
docker run -d --name myapp \
  -p 8080:80 \
  -e DATABASE_URL="postgres://..." \
  -v $(pwd)/data:/app/data \
  myapp:latest
```

**List containers and images:**
```bash
docker ps -a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

**View logs:**
```bash
docker logs myapp --tail 50
docker logs myapp -f   # follow/stream
```

**Execute command inside container:**
```bash
docker exec -it myapp /bin/sh
docker exec myapp ls /app
```

**Stop and remove:**
```bash
docker stop myapp && docker rm myapp
docker rmi myapp:latest
```

**Docker Compose:**
```bash
# Start all services
docker compose up -d

# Rebuild and start
docker compose up -d --build

# View logs
docker compose logs -f --tail 50

# Stop all
docker compose down

# Stop and remove volumes
docker compose down -v
```

**Create a Dockerfile:**
```bash
cat > Dockerfile << 'EOF'
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
```

**Create a docker-compose.yml:**
```bash
cat > docker-compose.yml << 'EOF'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
EOF
```

**Push to a registry:**
```bash
# Docker Hub
docker tag myapp:latest username/myapp:latest
docker push username/myapp:latest

# ACR (Azure Container Registry)
az acr login --name myregistry
docker tag myapp:latest myregistry.azurecr.io/myapp:latest
docker push myregistry.azurecr.io/myapp:latest
```

**System cleanup:**
```bash
docker system prune -f            # Remove unused containers, networks, images
docker volume prune -f             # Remove unused volumes
docker system df                   # Show disk usage
```

**Inspect container:**
```bash
docker inspect myapp --format '{{.State.Status}}'
docker stats --no-stream
```

## Output contract
- stdout: command output
- exit_code 0: success
- exit_code 1+: build error, container not found, or permission issue

## Evaluate output
If build fails: read the error line — usually a missing file in COPY, bad RUN command, or wrong base image.
If port conflict: check `docker ps` for existing containers on that port.
If "permission denied": check Docker daemon is running and user has access.
