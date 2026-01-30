#!/bin/bash
# Azure deployment script for Todo Chatbot application on AKS with Dapr and managed services

set -e

RESOURCE_GROUP="todo-app-rg"
CLUSTER_NAME="todo-aks-cluster"
LOCATION="eastus"
DNS_PREFIX="todo-aks"
NODE_COUNT=3
VM_SIZE="Standard_D2_v2"

echo "Starting Azure deployment for Todo Chatbot application..."

# Login to Azure (uncomment if needed)
# az login

# Create resource group
echo "Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create AKS cluster
echo "Creating AKS cluster..."
az aks create \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME \
  --node-count $NODE_COUNT \
  --generate-ssh-keys \
  --dns-name-prefix $DNS_PREFIX \
  --enable-addons monitoring \
  --workspace-resource-id "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.OperationalInsights/workspaces/todo-logs" \
  --vm-set-type VirtualMachineScaleSets \
  --load-balancer-sku standard

# Get AKS credentials
echo "Getting AKS credentials..."
az aks get-credentials --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME

# Install Dapr in AKS
echo "Installing Dapr in AKS..."
dapr init -k

# Wait for Dapr to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=dapr-operator -n dapr-system --timeout=300s

# Create Cosmos DB account
echo "Creating Azure Cosmos DB..."
az cosmosdb create \
  --resource-group $RESOURCE_GROUP \
  --name todo-cosmosdb-account \
  --kind GlobalDocumentDB \
  --locations regionName=$LOCATION failoverPriority=0 isZoneRedundant=False

# Create PostgreSQL Flexible Server
echo "Creating Azure Database for PostgreSQL..."
az postgres flexible-server create \
  --resource-group $RESOURCE_GROUP \
  --name todopostgres \
  --location $LOCATION \
  --database-name todo_db \
  --admin-user postgres \
  --admin-password "SecurePassword123!" \
  --sku-name Standard_B1ms \
  --public-access none

# Create Azure Cache for Redis
echo "Creating Azure Cache for Redis..."
az redis create \
  --resource-group $RESOURCE_GROUP \
  --name todo-redis-cache \
  --location $LOCATION \
  --sku Basic \
  --vm-size C0

# Create Azure Key Vault
echo "Creating Azure Key Vault..."
az keyvault create \
  --name "todo-keyvault-$(date +%s)" \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# Create secrets in Key Vault (replace with actual values)
# az keyvault secret set --vault-name "todo-keyvault-$(date +%s)" --name "openai-api-key" --value "your-openai-key"
# az keyvault secret set --vault-name "todo-keyvault-$(date +%s)" --name "database-url" --value "your-db-url"

# Create secrets in Kubernetes
kubectl create secret generic todo-secrets \
  --from-literal=postgres-password="SecurePassword123!" \
  --from-literal=secret-key="your-very-long-secret-key-here" \
  --from-literal=openai-api-key="your-openai-api-key" \
  --from-literal=database-url="postgresql://postgres:SecurePassword123!@todopostgres.postgres.database.azure.com:5432/todo_db" \
  --namespace=todo-app \
  --dry-run=client -o yaml | kubectl apply -f -

# Deploy application
echo "Deploying application to AKS..."
kubectl apply -f ./01-infrastructure-cloud.yaml
kubectl apply -f ./dapr-components-cloud-standard.yaml
kubectl apply -f ./02-backend-cloud.yaml
kubectl apply -f ./03-frontend-cloud.yaml
kubectl apply -f ./05-ingress-cloud.yaml

echo "Azure deployment complete!"
echo "AKS Cluster: $CLUSTER_NAME"
echo "Resource Group: $RESOURCE_GROUP"
echo "Access the application via the ingress load balancer IP"