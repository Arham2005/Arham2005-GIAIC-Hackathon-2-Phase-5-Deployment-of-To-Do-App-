#!/bin/bash
# Deployment script for Todo Chatbot application on Minikube with Dapr

set -e

echo "Deploying Todo Chatbot application to Minikube with Dapr..."

# Apply Dapr components
echo "Applying Dapr components..."
kubectl apply -f ./dapr-components-minikube.yaml

# Create secrets
echo "Creating secrets..."
kubectl create secret generic todo-secrets \
  --from-literal=openai-api-key="YOUR_OPENAI_API_KEY_HERE" \
  --namespace=todo-app \
  --dry-run=client -o yaml | kubectl apply -f -

# Apply infrastructure
echo "Applying infrastructure..."
kubectl apply -f ./01-infrastructure.yaml

# Wait for PostgreSQL and Redis to be ready
echo "Waiting for infrastructure to be ready..."
kubectl wait --for=condition=ready pod -l app=postgresql -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n todo-app --timeout=300s

# Apply Kafka
echo "Applying Kafka..."
kubectl apply -f ./04-kafka.yaml

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."
kubectl wait --for=condition=ready pod -l app=zookeeper -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=kafka -n todo-app --timeout=300s

# Apply backend
echo "Applying backend..."
kubectl apply -f ./02-backend-dapr.yaml

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
kubectl wait --for=condition=ready pod -l app=backend -n todo-app --timeout=600s

# Apply frontend
echo "Applying frontend..."
kubectl apply -f ./03-frontend-dapr.yaml

# Wait for frontend to be ready
echo "Waiting for frontend to be ready..."
kubectl wait --for=condition=ready pod -l app=frontend -n todo-app --timeout=300s

# Apply ingress
echo "Applying ingress..."
kubectl apply -f ./05-ingress.yaml

# Get Minikube IP
MINIKUBE_IP=$(minikube ip)
echo "Minikube IP: $MINIKUBE_IP"

# Update /etc/hosts (requires sudo)
echo "Updating /etc/hosts..."
echo "$MINIKUBE_IP todo.local" | sudo tee -a /etc/hosts

echo "Deployment complete!"
echo "Access the application at: http://todo.local"
echo "Dapr dashboard: dapr dashboard"
echo "Kubernetes dashboard: minikube dashboard"