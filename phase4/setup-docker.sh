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