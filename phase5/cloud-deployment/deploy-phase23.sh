#!/bin/bash
# deploy-phase23.sh - Deploy Phase 2+3: Web Application with AI Chat

set -e  # Exit on any error

echo "==========================================="
echo " 🚀 DEPLOYING PHASE 2+3: WEB APP WITH AI CHAT"
echo "==========================================="

echo ""
echo "Prerequisites check:"
echo "- OCI CLI installed and configured"
echo "- kubectl installed and connected to OKE cluster"
echo "- Docker installed and logged into OCIR"
echo "- PostgreSQL database ready"
echo "- OpenAI API key configured"
echo ""

read -p "Have you completed the prerequisites? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please complete the prerequisites first."
    exit 1
fi

echo ""
echo "Step 1: Building Phase 2+3 Docker image..."
docker build -t todo-phase23-backend:latest -f Dockerfile.phase23 .

echo ""
echo "Step 2: Tagging for OCIR..."
read -p "Enter your Oracle Cloud region (e.g., us-ashburn-1): " REGION
read -p "Enter your tenancy name: " TENANCY
docker tag todo-phase23-backend:latest ${REGION}.ocir.io/${TENANCY}/todo-phase23-backend:latest

echo ""
echo "Step 3: Pushing Phase 2+3 image to OCIR..."
docker push ${REGION}.ocir.io/${TENANCY}/todo-phase23-backend:latest

echo ""
echo "Step 4: Updating Phase 2+3 deployment with your image..."

# Create a temporary deployment file with actual values
TEMP_DEPLOYMENT=$(mktemp)
sed "s|<region>|${REGION}|g; s|<tenancy>|${TENANCY}|g" phase23-deployment.yaml > "$TEMP_DEPLOYMENT"

echo "Step 5: Applying Phase 2+3 Kubernetes manifests..."
kubectl apply -f "$TEMP_DEPLOYMENT"

echo ""
echo "Step 6: Waiting for Phase 2+3 deployment to be ready..."
kubectl rollout status deployment/todo-phase23-backend -n todo-app --timeout=300s

echo ""
echo "🎉 PHASE 2+3 DEPLOYMENT COMPLETED!"
echo ""
echo "Your Phase 2+3 application is now deployed to Oracle Cloud!"
echo "It includes authentication, task management, and AI chat features."
echo ""
echo "To check the status:"
echo "  kubectl get pods -n todo-app"
echo "  kubectl get services -n todo-app"
echo ""
echo "To access your Phase 2+3 application:"
echo "  kubectl get svc todo-phase23-service -n todo-app"
echo "  Use the EXTERNAL-IP to access your application"
echo ""

# Clean up temporary file
rm "$TEMP_DEPLOYMENT"