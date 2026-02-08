# oci-deploy-script.ps1 - Automated deployment script for Oracle Cloud

Write-Host "===========================================" -ForegroundColor Green
Write-Host " 🚀 TODO APP PHASE 5 DEPLOYMENT TO ORACLE CLOUD" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

Write-Host ""
Write-Host "Prerequisites check:" -ForegroundColor Yellow
Write-Host "- OCI CLI installed and configured" -ForegroundColor Yellow
Write-Host "- kubectl installed and connected to OKE cluster" -ForegroundColor Yellow
Write-Host "- Docker installed and logged into OCIR" -ForegroundColor Yellow
Write-Host ""

$continue = Read-Host "Have you completed the prerequisites? (y/n)"
if ($continue -notmatch "^y$|^Y$") {
    Write-Host "Please complete the prerequisites first." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 1: Building Docker image..." -ForegroundColor Cyan
docker build -t todo-phase5-backend:latest -f Dockerfile.unified .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2: Tagging for OCIR..." -ForegroundColor Cyan
$region = Read-Host "Enter your Oracle Cloud region (e.g., us-ashburn-1)"
$tenancy = Read-Host "Enter your tenancy name"
$imageName = "${region}.ocir.io/${tenancy}/todo-phase5-backend:latest"

docker tag todo-phase5-backend:latest $imageName

Write-Host ""
Write-Host "Step 3: Pushing to OCIR..." -ForegroundColor Cyan
docker push $imageName

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker push failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 4: Updating deployment with your image..." -ForegroundColor Cyan

# Read the deployment file and replace placeholders
$deploymentContent = Get-Content deployment.yaml -Raw
$updatedDeployment = $deploymentContent -replace "<region>", $region
$updatedDeployment = $updatedDeployment -replace "<tenancy>", $tenancy

# Save the updated deployment
$tempDeploymentPath = "temp-deployment.yaml"
$updatedDeployment | Out-File -FilePath $tempDeploymentPath -Encoding UTF8

Write-Host "Step 5: Applying Kubernetes manifests..." -ForegroundColor Cyan
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f $tempDeploymentPath
kubectl apply -f ingress.yaml

Write-Host ""
Write-Host "Step 6: Waiting for deployment to be ready..." -ForegroundColor Cyan
kubectl rollout status deployment/todo-phase5-backend -n todo-app --timeout=300s

Write-Host ""
Write-Host "Deployment completed!" -ForegroundColor Green
Write-Host ""
Write-Host "To check status:" -ForegroundColor Yellow
Write-Host "  kubectl get pods -n todo-app" -ForegroundColor Yellow
Write-Host "  kubectl get services -n todo-app" -ForegroundColor Yellow
Write-Host "  kubectl get ingress -n todo-app" -ForegroundColor Yellow
Write-Host ""
Write-Host "Access your application at the external IP from:" -ForegroundColor Yellow
Write-Host "  kubectl get svc todo-phase5-service -n todo-app" -ForegroundColor Yellow
Write-Host ""

# Clean up temporary file
Remove-Item $tempDeploymentPath -Force