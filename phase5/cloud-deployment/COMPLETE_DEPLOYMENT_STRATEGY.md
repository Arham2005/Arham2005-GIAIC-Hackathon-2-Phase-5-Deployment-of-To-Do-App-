# Complete Deployment Strategy for Todo Application

This document outlines the complete deployment strategy for the Todo Application across all phases:

## Phase 1: Phase 2 (Frontend on Vercel, Backend on Easy Hosting)
- **Frontend**: Deploy to Vercel
- **Backend**: Deploy to Render.com, Railway.app, or Heroku
- **Purpose**: Easy access for testing and development

## Phase 2: Phase 4 (Phase 2 + Phase 3 on Docker)
- **Deployment**: Docker containers with docker-compose
- **Purpose**: Local development and testing of combined features
- **Components**: Frontend, Backend (Phase 2+3), Database

## Phase 3: Phase 5 (Full Application on Cloud)
- **Deployment**: Oracle Cloud Infrastructure (OKE Kubernetes)
- **Purpose**: Production deployment with advanced features
- **Components**: Full application with Kafka, Dapr, advanced features

---

## Detailed Instructions

### Phase 1: Vercel Frontend + External Backend

#### Frontend Deployment to Vercel:
1. Navigate to `phase2/frontend/`
2. Create a GitHub repository and push the frontend code
3. Go to https://vercel.com/
4. Import your GitHub repository
5. Set environment variable:
   - `NEXT_PUBLIC_API_BASE_URL`: Your backend URL (e.g., https://your-backend.onrender.com)
6. Deploy

#### Backend Deployment Options:

**Option A: Render.com**
1. Go to https://render.com/
2. Create a new Web Service
3. Connect to your GitHub repository
4. Use Docker deployment with `phase2/backend/Dockerfile.simple`
5. Set environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `ALLOWED_ORIGINS`: Your Vercel frontend URL
6. Deploy

**Option B: Railway.app**
1. Go to https://railway.app/
2. Create a new project
3. Connect to GitHub repository
4. Deploy using Dockerfile
5. Set environment variables in Railway dashboard

**Option C: Heroku**
1. Install Heroku CLI
2. Create `phase2/backend/Procfile`:
   ```
   web: uvicorn phase2.backend.app.main:app --host=0.0.0.0 --port=\${PORT:-8000}
   ```
3. Deploy using Heroku CLI

### Phase 2: Docker Deployment (Phase 4 - Phase 2 + Phase 3)

#### Quick Setup:
1. Navigate to the project root:
   ```bash
   cd C:\Users\DELL\Desktop\P3\
   ```

2. Make the setup script executable:
   ```bash
   chmod +x phase4/setup-docker.sh
   ```

3. Run the setup script:
   ```bash
   ./phase4/setup-docker.sh
   ```

#### Manual Setup:
1. Navigate to phase4 directory:
   ```bash
   cd phase4/
   ```

2. Ensure you have a `.env` file with your OpenAI API key:
   ```bash
   echo "OPENAI_API_KEY=your_actual_key_here" > .env
   ```

3. Start the services:
   ```bash
   docker-compose up -d --build
   ```

4. Access your applications:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Backend API Docs: http://localhost:8000/docs

#### Docker Compose Components:
- **Database**: PostgreSQL container with persistent volume
- **Backend**: Phase 2+3 application (Phase 4) with OpenAI integration
- **Frontend**: Next.js application connected to the backend

### Phase 3: Cloud Deployment (Phase 5 - Full Advanced Application)

#### Prerequisites:
1. Oracle Cloud Account (https://www.oracle.com/cloud/free/)
2. OCI CLI installed and configured
3. kubectl installed and connected to OKE cluster
4. Docker installed and logged into OCIR
5. PostgreSQL database (Neon or Oracle Autonomous DB)

#### Deployment Steps:
1. Navigate to the cloud deployment directory:
   ```bash
   cd phase5/cloud-deployment/
   ```

2. Deploy the full application using the existing scripts:
   - **Linux/Mac**: `./oci-deploy-script.sh` or `python deploy_to_oci.py`
   - **Windows**: `.\oci-deploy-script.ps1`

3. Follow the prompts to enter your Oracle Cloud region and tenancy name

4. Access your full application:
   ```bash
   kubectl get svc todo-phase5-service -n todo-app
   ```

#### Cloud Deployment Components:
- **Kubernetes**: Running on Oracle Kubernetes Engine (OKE)
- **Application**: Full Phase 5 with Kafka, Dapr, advanced features
- **Database**: External PostgreSQL (Neon or Oracle Autonomous DB)
- **Load Balancer**: Public access via external IP
- **Monitoring**: Built-in health checks and metrics

---

## Access Information by Phase

### Phase 1 (Vercel + External):
- **Frontend**: https://your-project.vercel.app
- **Backend API**: https://your-backend.onrender.com
- **API Docs**: https://your-backend.onrender.com/docs

### Phase 2 (Docker):
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432 (todo_db)

### Phase 3 (Cloud):
- **Application**: http://<EXTERNAL_IP>/
- **API Docs**: http://<EXTERNAL_IP>/docs
- **Health Check**: http://<EXTERNAL_IP>/health
- **Phase Info**: http://<EXTERNAL_IP>/phases-info

---

## Benefits of Each Phase

### Phase 1 (Vercel + External):
- ✅ Fast global CDN delivery
- ✅ Easy deployment and scaling
- ✅ Generous free tiers
- ✅ Great for development and demos

### Phase 2 (Docker):
- ✅ Consistent local development environment
- ✅ Easy to test integrated features
- ✅ Self-contained with all dependencies
- ✅ Good for CI/CD pipelines

### Phase 3 (Cloud):
- ✅ Production-ready infrastructure
- ✅ Advanced features (Kafka, Dapr)
- ✅ High availability and scalability
- ✅ Enterprise-grade security

Choose the phase that best fits your current needs and scale up as required!