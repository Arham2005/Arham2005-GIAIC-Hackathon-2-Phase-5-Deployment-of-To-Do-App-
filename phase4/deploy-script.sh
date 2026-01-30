#!/bin/bash

# Deployment script for Todo Chatbot on Kubernetes
# This script automates the deployment process using Helm

set -e  # Exit on any error

echo "🚀 Starting Todo Chatbot deployment..."

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v minikube &> /dev/null; then
    echo "❌ minikube is not installed. Please install minikube first."
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "❌ helm is not installed. Please install helm first."
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Start Minikube cluster
echo "🔄 Starting Minikube cluster..."
minikube start --driver=docker

# Wait for cluster to be ready
echo "⏳ Waiting for cluster to be ready..."
kubectl wait --for=condition=Ready nodes --all --timeout=120s

# Enable ingress addon in Minikube
echo "🔌 Enabling ingress addon..."
minikube addons enable ingress

# Wait for ingress controller to be ready
echo "⏳ Waiting for ingress controller to be ready..."
kubectl wait --for=condition=Ready pods --namespace=kube-system -l name=nginx-ingress-controller --timeout=120s

# Build Docker images (if not already built)
echo "📦 Building Docker images..."
docker build -f ./phase4/backend.Dockerfile -t todo-backend:latest .
docker build -f ./phase4/frontend.Dockerfile -t todo-frontend:latest .

# Load images into Minikube
echo "📥 Loading images into Minikube..."
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Update Helm dependencies
echo "🔄 Updating Helm dependencies..."
helm repo update

# Install the Todo Chatbot application
echo "⚙️ Installing Todo Chatbot application..."
helm upgrade --install todo-chatbot ./phase4/helm-chart/todo-chatbot \
  --namespace todo-app \
  --create-namespace \
  --set backend.image.tag=latest \
  --set frontend.image.tag=latest

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=Ready pods --namespace=todo-app --selector=app.kubernetes.io/component=backend --timeout=300s
kubectl wait --for=condition=Ready pods --namespace=todo-app --selector=app.kubernetes.io/component=frontend --timeout=300s

# Get Minikube IP for ingress
MINIKUBE_IP=$(minikube ip)
echo "🌐 Minikube IP: $MINIKUBE_IP"

# Add entry to hosts file (requires sudo)
echo "$MINIKUBE_IP todo.local" | sudo tee -a /etc/hosts

echo "✅ Todo Chatbot deployment completed successfully!"
echo ""
echo "📋 Access the application:"
echo "   Frontend: http://todo.local"
echo "   Backend API: http://todo.local/api"
echo "   Backend Health Check: http://todo.local/health"
echo ""
echo "🔧 To access the application in your browser, make sure to add the following entry to your hosts file:"
echo "   $MINIKUBE_IP todo.local"
echo ""
echo "📊 To monitor the deployment:"
echo "   kubectl get pods -n todo-app"
echo "   kubectl get services -n todo-app"
echo "   kubectl get ingress -n todo-app"
echo ""
echo "🔄 To update the application:"
echo "   # Make changes to the code"
echo "   # Rebuild the Docker images"
echo "   docker build -f ./phase4/backend.Dockerfile -t todo-backend:latest ."
echo "   docker build -f ./phase4/frontend.Dockerfile -t todo-frontend:latest ."
echo "   minikube image load todo-backend:latest"
echo "   minikube image load todo-frontend:latest"
echo "   helm upgrade todo-chatbot ./phase4/helm-chart/todo-chatbot --namespace todo-app"
echo ""
echo "🗑️ To uninstall the application:"
echo "   helm uninstall todo-chatbot -n todo-app"
echo "   kubectl delete namespace todo-app"
echo ""
echo "🐳 To stop Minikube:"
echo "   minikube stop"