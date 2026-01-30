#!/bin/bash
# Setup script for deploying the Todo Chatbot application to Minikube with Dapr

set -e

echo "Setting up Minikube and Dapr for Todo Chatbot application..."

# Install Minikube if not installed
if ! command -v minikube &> /dev/null; then
    echo "Installing Minikube..."
    # This assumes a Linux/Mac environment - adjust for Windows if needed
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
fi

# Install kubectl if not installed
if ! command -v kubectl &> /dev/null; then
    echo "Installing kubectl..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install kubectl /usr/local/bin/kubectl
fi

# Install Dapr CLI if not installed
if ! command -v dapr &> /dev/null; then
    echo "Installing Dapr CLI..."
    wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
fi

# Start Minikube with sufficient resources
echo "Starting Minikube..."
minikube start --memory=4096 --cpus=4

# Enable required Minikube addons
minikube addons enable ingress
minikube addons enable metrics-server

# Initialize Dapr in Kubernetes
echo "Installing Dapr in Minikube..."
dapr init -k

# Wait for Dapr to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=dapr-operator --timeout=300s

echo "Minikube and Dapr setup complete!"