# Phase 4 Docker Deployment (Phase 2 + Phase 3)

This guide will help you deploy Phase 2 + Phase 3 (Phase 4) using Docker for local development and testing.

## Prerequisites
- Docker Desktop installed (https://www.docker.com/products/docker-desktop/)
- Docker Compose
- PostgreSQL database (can be local or external)

## Step 1: Create Docker Compose File for Phase 4

Create `phase4/docker-compose.yml`:
```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15
    container_name: todo_phase4_db
    environment:
      POSTGRES_DB: todo_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - todo_network

  # Phase 4 Backend (Phase 2 + Phase 3)
  backend:
    build:
      context: ../
      dockerfile: phase4/Dockerfile.phase4
    container_name: todo_phase4_backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/todo_db
      - ENVIRONMENT=docker
      - ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
      - SECRET_KEY=your_docker_secret_key
      - ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
    networks:
      - todo_network

  # Phase 4 Frontend
  frontend:
    build:
      context: ../phase2/frontend
      dockerfile: Dockerfile
    container_name: todo_phase4_frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
    depends_on:
      - backend
    networks:
      - todo_network

volumes:
  postgres_data:

networks:
  todo_network:
    driver: bridge
```

## Step 2: Create Phase 4 Dockerfile

Create `phase4/Dockerfile.phase4`:
```dockerfile
# Dockerfile.phase4
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run Phase 2+3 application (Phase 4)
CMD ["uvicorn", "phase3.backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Step 3: Create Phase 4 Setup Script

Create `phase4/setup-docker.sh`:
```bash
#!/bin/bash
# setup-docker.sh - Setup script for Phase 4 Docker deployment

set -e

echo "==========================================="
echo " 🚀 SETUP PHASE 4: Phase 2 + Phase 3 (Docker)"
echo "==========================================="

echo ""
echo "Prerequisites check:"
echo "- Docker Desktop installed"
echo "- Docker Compose installed"
echo "- Internet connection"
echo ""

read -p "Continue with setup? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 1
fi

echo ""
echo "Step 1: Creating Phase 4 directory structure..."
mkdir -p phase4

echo ""
echo "Step 2: Checking if Docker is running..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
else
    echo "✅ Docker is running"
fi

echo ""
echo "Step 3: Setting up environment variables..."
if [ ! -f .env ]; then
    echo "Creating .env file with default settings..."
    cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EOF
    echo "⚠️  IMPORTANT: Please update .env with your actual OpenAI API key!"
fi

echo ""
echo "Step 4: Building and starting Phase 4 containers..."
cd phase4
docker-compose up -d --build

echo ""
echo "Step 5: Waiting for services to start..."
sleep 30

echo ""
echo "Step 6: Checking container status..."
docker-compose ps

echo ""
echo "🎉 PHASE 4 SETUP COMPLETED!"
echo ""
echo "Your Phase 4 application (Phase 2 + Phase 3) is now running in Docker!"
echo ""
echo "Access your applications:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "- Backend API Docs: http://localhost:8000/docs"
echo "- Database: localhost:5432 (todo_db)"
echo ""
echo "To stop the containers:"
echo "  cd phase4 && docker-compose down"
echo ""
echo "To restart the containers:"
echo "  cd phase4 && docker-compose up -d"
echo ""
echo "To view logs:"
echo "  cd phase4 && docker-compose logs -f"
echo ""