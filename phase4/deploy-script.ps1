# PowerShell deployment script for Todo Chatbot on Kubernetes
# This script automates the deployment process using Helm

Write-Host "🚀 Starting Todo Chatbot deployment..." -ForegroundColor Green

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow

# Check if minikube is installed
if (!(Get-Command minikube -ErrorAction SilentlyContinue)) {
    Write-Host "❌ minikube is not installed. Please install minikube first." -ForegroundColor Red
    exit 1
}

# Check if helm is installed
if (!(Get-Command helm -ErrorAction SilentlyContinue)) {
    Write-Host "❌ helm is not installed. Please install helm first." -ForegroundColor Red
    exit 1
}

# Check if kubectl is installed
if (!(Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "❌ kubectl is not installed. Please install kubectl first." -ForegroundColor Red
    exit 1
}

# Start Minikube cluster
Write-Host "🔄 Starting Minikube cluster..." -ForegroundColor Yellow
minikube start --driver=docker

# Wait for cluster to be ready
Write-Host "⏳ Waiting for cluster to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=Ready nodes --all --timeout=120s

# Enable ingress addon in Minikube
Write-Host "🔌 Enabling ingress addon..." -ForegroundColor Yellow
minikube addons enable ingress

# Wait for ingress controller to be ready
Write-Host "⏳ Waiting for ingress controller to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=Ready pods --namespace=kube-system -l name=nginx-ingress-controller --timeout=120s

# Build Docker images (if not already built)
Write-Host "📦 Building Docker images..." -ForegroundColor Yellow
docker build -f ./phase4/backend.Dockerfile -t todo-backend:latest .
docker build -f ./phase4/frontend.Dockerfile -t todo-frontend:latest .

# Load images into Minikube
Write-Host "📥 Loading images into Minikube..." -ForegroundColor Yellow
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Update Helm dependencies
Write-Host "🔄 Updating Helm dependencies..." -ForegroundColor Yellow
helm repo update

# Install the Todo Chatbot application
Write-Host "⚙️ Installing Todo Chatbot application..." -ForegroundColor Yellow
helm upgrade --install todo-chatbot ./phase4/helm-chart/todo-chatbot `
  --namespace todo-app `
  --create-namespace `
  --set backend.image.tag=latest `
  --set frontend.image.tag=latest

# Wait for deployments to be ready
Write-Host "⏳ Waiting for deployments to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=Ready pods --namespace=todo-app --selector=app.kubernetes.io/component=backend --timeout=300s
kubectl wait --for=condition=Ready pods --namespace=todo-app --selector=app.kubernetes.io/component=frontend --timeout=300s

# Get Minikube IP for ingress
$minikubeIP = $(minikube ip)
Write-Host "🌐 Minikube IP: $minikubeIP" -ForegroundColor Green

# Add entry to hosts file (requires administrator privileges)
$hostsEntry = "$minikubeIP todo.local"
$hostsPath = "C:\Windows\System32\drivers\etc\hosts"

# Check if the entry already exists
$hostsContent = Get-Content $hostsPath
$entryExists = $hostsContent -match "todo.local"

if (-not $entryExists) {
    # Add the entry to hosts file (requires running as administrator)
    try {
        Add-Content -Path $hostsPath -Value $hostsEntry -Force
        Write-Host "✅ Added entry to hosts file: $hostsEntry" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️ Could not add entry to hosts file. Please add manually: $hostsEntry" -ForegroundColor Yellow
        Write-Host "💡 Run PowerShell as Administrator to add the entry automatically" -ForegroundColor Cyan
    }
} else {
    Write-Host "✅ Entry already exists in hosts file" -ForegroundColor Green
}

Write-Host "✅ Todo Chatbot deployment completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Access the application:" -ForegroundColor Cyan
Write-Host "   Frontend: http://todo.local"
Write-Host "   Backend API: http://todo.local/api"
Write-Host "   Backend Health Check: http://todo.local/health"
Write-Host ""
Write-Host "🔧 To access the application in your browser, make sure todo.local resolves to $minikubeIP" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 To monitor the deployment:" -ForegroundColor Cyan
Write-Host "   kubectl get pods -n todo-app"
Write-Host "   kubectl get services -n todo-app"
Write-Host "   kubectl get ingress -n todo-app"
Write-Host ""
Write-Host "🔄 To update the application:" -ForegroundColor Cyan
Write-Host "   # Make changes to the code" -ForegroundColor Gray
Write-Host "   # Rebuild the Docker images" -ForegroundColor Gray
Write-Host "   docker build -f ./phase4/backend.Dockerfile -t todo-backend:latest ." -ForegroundColor Gray
Write-Host "   docker build -f ./phase4/frontend.Dockerfile -t todo-frontend:latest ." -ForegroundColor Gray
Write-Host "   minikube image load todo-backend:latest" -ForegroundColor Gray
Write-Host "   minikube image load todo-frontend:latest" -ForegroundColor Gray
Write-Host "   helm upgrade todo-chatbot ./phase4/helm-chart/todo-chatbot --namespace todo-app" -ForegroundColor Gray
Write-Host ""
Write-Host "🗑️ To uninstall the application:" -ForegroundColor Cyan
Write-Host "   helm uninstall todo-chatbot -n todo-app" -ForegroundColor Gray
Write-Host "   kubectl delete namespace todo-app" -ForegroundColor Gray
Write-Host ""
Write-Host "🐳 To stop Minikube:" -ForegroundColor Cyan
Write-Host "   minikube stop" -ForegroundColor Gray