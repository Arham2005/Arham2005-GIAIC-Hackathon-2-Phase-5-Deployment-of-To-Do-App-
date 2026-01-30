#!/bin/bash
# Google Cloud deployment script for Todo Chatbot application on GKE with Dapr and managed services

set -e

PROJECT_ID="your-project-id"
CLUSTER_NAME="todo-gke-cluster"
ZONE="us-central1-a"
NODE_POOL="todo-node-pool"
MACHINE_TYPE="e2-standard-2"
NUM_NODES=3

echo "Starting Google Cloud deployment for Todo Chatbot application..."

# Login to Google Cloud (uncomment if needed)
# gcloud auth login

# Set project
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable container.googleapis.com
gcloud services enable redis.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable secretmanager.googleapis.com

# Create GKE cluster
echo "Creating GKE cluster..."
gcloud container clusters create $CLUSTER_NAME \
  --zone=$ZONE \
  --num-nodes=$NUM_NODES \
  --machine-type=$MACHINE_TYPE \
  --enable-autorepair \
  --enable-autoupgrade \
  --enable-cloud-logging \
  --enable-cloud-monitoring

# Get GKE credentials
echo "Getting GKE credentials..."
gcloud container clusters get-credentials $CLUSTER_NAME --zone=$ZONE

# Install Dapr in GKE
echo "Installing Dapr in GKE..."
dapr init -k

# Wait for Dapr to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=dapr-operator -n dapr-system --timeout=300s

# Create Cloud SQL instance for PostgreSQL
echo "Creating Cloud SQL for PostgreSQL..."
gcloud sql instances create todo-postgres-instance \
  --database-version=POSTGRES_13 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=SecurePassword123!

# Create database
gcloud sql databases create todo_db --instance=todo-postgres-instance

# Create Memorystore for Redis
echo "Creating Cloud Memorystore for Redis..."
gcloud redis instances create todo-redis-instance \
  --size=1 \
  --region=us-central1 \
  --zone=us-central1-a \
  --redis-version=redis_6_x

# Create Secret Manager secrets
echo "Creating secrets in Secret Manager..."
echo -n "SecurePassword123!" | gcloud secrets create postgres-password --data-file=-
echo -n "your-very-long-secret-key-here" | gcloud secrets create secret-key --data-file=-
echo -n "your-openai-api-key" | gcloud secrets create openai-api-key --data-file=-

# Get Redis IP address
REDIS_IP=$(gcloud redis instances describe todo-redis-instance --region=us-central1 --format="value(host)")

# Get Cloud SQL connection name
CONNECTION_NAME=$(gcloud sql instances describe todo-postgres-instance --format="value(connectionName)")

# Create secrets in Kubernetes
kubectl create secret generic todo-secrets \
  --from-literal=postgres-password="SecurePassword123!" \
  --from-literal=secret-key="your-very-long-secret-key-here" \
  --from-literal=openai-api-key="your-openai-api-key" \
  --from-literal=database-url="postgresql://postgres:SecurePassword123!@$(gcloud sql instances describe todo-postgres-instance --format="value(ipAddresses.ip_address)"):5432/todo_db" \
  --namespace=todo-app \
  --dry-run=client -o yaml | kubectl apply -f -

# Deploy application
echo "Deploying application to GKE..."
kubectl apply -f ./01-infrastructure-cloud.yaml
kubectl apply -f ./dapr-components-cloud-standard.yaml
kubectl apply -f ./02-backend-cloud.yaml
kubectl apply -f ./03-frontend-cloud.yaml
kubectl apply -f ./05-ingress-cloud.yaml

echo "Google Cloud deployment complete!"
echo "GKE Cluster: $CLUSTER_NAME"
echo "Project: $PROJECT_ID"
echo "Access the application via the ingress load balancer IP"