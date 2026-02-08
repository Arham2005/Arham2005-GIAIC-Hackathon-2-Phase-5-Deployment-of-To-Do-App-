#!/bin/bash
# oci-deploy-script.sh - Automated deployment script for Oracle Cloud

set -e  # Exit on any error

echo "==========================================="
echo " 🚀 TODO APP PHASE 5 DEPLOYMENT TO ORACLE CLOUD"
echo "==========================================="

echo ""
echo "Prerequisites check:"
echo "- OCI CLI installed and configured"
echo "- kubectl installed and connected to OKE cluster"
echo "- Docker installed and logged into OCIR"
echo ""

read -p "Have you completed the prerequisites? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please complete the prerequisites first."
    exit 1
fi

echo ""
echo "Step 1: Building Docker image..."
docker build -t todo-phase5-backend:latest -f Dockerfile.unified .

echo ""
echo "Step 2: Tagging for OCIR..."
read -p "Enter your Oracle Cloud region (e.g., us-ashburn-1): " REGION
read -p "Enter your tenancy name: " TENANCY
docker tag todo-phase5-backend:latest ${REGION}.ocir.io/${TENANCY}/todo-phase5-backend:latest

echo ""
echo "Step 3: Pushing to OCIR..."
docker push ${REGION}.ocir.io/${TENANCY}/todo-phase5-backend:latest

echo ""
echo "Step 4: Updating deployment with your image..."

# Create a temporary deployment file with actual values
TEMP_DEPLOYMENT=$(mktemp)
sed "s|<region>|${REGION}|g; s|<tenancy>|${TENANCY}|g" deployment.yaml > "$TEMP_DEPLOYMENT"

echo "Step 5: Applying Kubernetes manifests..."
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f "$TEMP_DEPLOYMENT"
kubectl apply -f ingress.yaml

echo ""
echo "Step 6: Waiting for deployment to be ready..."
kubectl rollout status deployment/todo-phase5-backend -n todo-app --timeout=300s

echo ""
echo "Deployment completed!"
echo ""
echo "To check status:"
echo "  kubectl get pods -n todo-app"
echo "  kubectl get services -n todo-app"
echo "  kubectl get ingress -n todo-app"
echo ""
echo "Access your application at the external IP from:"
echo "  kubectl get svc todo-phase5-service -n todo-app"
echo ""