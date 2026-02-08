# Incremental Deployment Strategy for Todo Application

This document outlines how to deploy the Todo Application in incremental phases as requested:

## Phase 1: Deploy Phase 2 (Basic Web Application) Separately

### Step 1: Create Phase 2 Specific Dockerfile
Create `Dockerfile.phase2`:
```dockerfile
# Dockerfile.phase2
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

# Run Phase 2 application
CMD ["uvicorn", "phase2.backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Create Phase 2 Kubernetes Manifests
Create `phase2-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-phase2-backend
  namespace: todo-app
  labels:
    app: todo-phase2-backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todo-phase2-backend
  template:
    metadata:
      labels:
        app: todo-phase2-backend
    spec:
      containers:
      - name: backend
        image: <region>.ocir.io/<tenancy>/todo-phase2-backend:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: todo-app-config
        - secretRef:
            name: db-secret
        resources:
          requests:
            memory: "256Mi"
            cpu: "125m"
          limits:
            memory: "512Mi"
            cpu: "250m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: todo-phase2-service
  namespace: todo-app
spec:
  selector:
    app: todo-phase2-backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

### Step 3: Deploy Phase 2
```bash
# Build Phase 2 image
docker build -t todo-phase2-backend:latest -f Dockerfile.phase2 .

# Tag and push
docker tag todo-phase2-backend:latest <region>.ocir.io/<tenancy>/todo-phase2-backend:latest
docker push <region>.ocir.io/<tenancy>/todo-phase2-backend:latest

# Deploy to Kubernetes
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f phase2-deployment.yaml
```

## Phase 2: Deploy Phase 2 + Phase 3 on Docker

### Step 1: Create Phase 2+3 Dockerfile
Create `Dockerfile.phase23`:
```dockerfile
# Dockerfile.phase23
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

# Run Phase 2+3 application
CMD ["uvicorn", "phase3.backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Create Phase 2+3 Kubernetes Manifests
Create `phase23-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-phase23-backend
  namespace: todo-app
  labels:
    app: todo-phase23-backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todo-phase23-backend
  template:
    metadata:
      labels:
        app: todo-phase23-backend
    spec:
      containers:
      - name: backend
        image: <region>.ocir.io/<tenancy>/todo-phase23-backend:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: todo-app-config
        - secretRef:
            name: db-secret
        resources:
          requests:
            memory: "384Mi"
            cpu: "187m"
          limits:
            memory: "768Mi"
            cpu: "375m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: todo-phase23-service
  namespace: todo-app
spec:
  selector:
    app: todo-phase23-backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

### Step 3: Deploy Phase 2+3
```bash
# Build Phase 2+3 image
docker build -t todo-phase23-backend:latest -f Dockerfile.phase23 .

# Tag and push
docker tag todo-phase23-backend:latest <region>.ocir.io/<tenancy>/todo-phase23-backend:latest
docker push <region>.ocir.io/<tenancy>/todo-phase23-backend:latest

# Deploy to Kubernetes
kubectl apply -f phase23-deployment.yaml
```

## Phase 3: Deploy Phase 2 + Phase 3 + Phase 5 (Advanced Features) to Cloud

This is what we already have in the existing `Dockerfile.unified` and `deployment.yaml`:

### Current Phase 2+3+5 Dockerfile (already exists)
```dockerfile
# Dockerfile.unified (already created)
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

# Run the phase5 application (includes all phases)
CMD ["uvicorn", "phase5.backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Current Phase 2+3+5 Kubernetes Manifests (already exists)
Our existing `deployment.yaml` already deploys the full Phase 5 application which includes all features from Phases 2, 3, and 5.

### Deploy Full Application (Phase 2+3+5)
```bash
# Build the full application image (already done in Dockerfile.unified)
docker build -t todo-phase5-backend:latest -f Dockerfile.unified .

# Tag and push
docker tag todo-phase5-backend:latest <region>.ocir.io/<tenancy>/todo-phase5-backend:latest
docker push <region>.ocir.io/<tenancy>/todo-phase5-backend:latest

# Deploy the full application
kubectl apply -f deployment.yaml
```

## Deployment Scripts for Each Phase

### Phase 2 Deployment Script
Create `deploy-phase2.sh`:
```bash
#!/bin/bash
echo "🚀 Deploying Phase 2: Basic Web Application"

# Get user inputs
read -p "Enter your Oracle Cloud region: " REGION
read -p "Enter your tenancy name: " TENANCY

# Build, tag, and push Phase 2 image
docker build -t todo-phase2-backend:latest -f Dockerfile.phase2 .
docker tag todo-phase2-backend:latest ${REGION}.ocir.io/${TENANCY}/todo-phase2-backend:latest
docker push ${REGION}.ocir.io/${TENANCY}/todo-phase2-backend:latest

# Update deployment file with actual values
sed "s|<region>|${REGION}|g; s|<tenancy>|${TENANCY}|g" phase2-deployment.yaml > temp-phase2-deployment.yaml

# Deploy to Kubernetes
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f temp-phase2-deployment.yaml

# Wait for deployment
kubectl rollout status deployment/todo-phase2-backend -n todo-app --timeout=300s

echo "✅ Phase 2 deployed successfully!"
echo "Access at: $(kubectl get svc todo-phase2-service -n todo-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"
```

### Phase 2+3 Deployment Script
Create `deploy-phase23.sh`:
```bash
#!/bin/bash
echo "🚀 Deploying Phase 2+3: Web Application with AI Chat"

# Get user inputs
read -p "Enter your Oracle Cloud region: " REGION
read -p "Enter your tenancy name: " TENANCY

# Build, tag, and push Phase 2+3 image
docker build -t todo-phase23-backend:latest -f Dockerfile.phase23 .
docker tag todo-phase23-backend:latest ${REGION}.ocir.io/${TENANCY}/todo-phase23-backend:latest
docker push ${REGION}.ocir.io/${TENANCY}/todo-phase23-backend:latest

# Update deployment file with actual values
sed "s|<region>|${REGION}|g; s|<tenancy>|${TENANCY}|g" phase23-deployment.yaml > temp-phase23-deployment.yaml

# Deploy to Kubernetes
kubectl apply -f temp-phase23-deployment.yaml

# Wait for deployment
kubectl rollout status deployment/todo-phase23-backend -n todo-app --timeout=300s

echo "✅ Phase 2+3 deployed successfully!"
echo "Access at: $(kubectl get svc todo-phase23-service -n todo-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"
```

## Summary of Incremental Deployment

1. **Phase 2 Only**: Basic authentication and task management
2. **Phase 2+3**: Adds AI-powered chat functionality
3. **Phase 2+3+5**: Full application with advanced features (recurring tasks, due dates, priorities, tags, Kafka, Dapr)

Each phase builds upon the previous one, allowing for gradual feature rollout and testing.

To execute any phase, simply run the corresponding deployment script or follow the manual steps outlined above.