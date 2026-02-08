# deploy-phase2.ps1 - Deploy Phase 2: Basic Web Application

Write-Host "===========================================" -ForegroundColor Green
Write-Host " 🚀 DEPLOYING PHASE 2: BASIC WEB APPLICATION" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

Write-Host ""
Write-Host "Prerequisites check:" -ForegroundColor Yellow
Write-Host "- OCI CLI installed and configured" -ForegroundColor Yellow
Write-Host "- kubectl installed and connected to OKE cluster" -ForegroundColor Yellow
Write-Host "- Docker installed and logged into OCIR" -ForegroundColor Yellow
Write-Host "- PostgreSQL database ready" -ForegroundColor Yellow
Write-Host ""

$continue = Read-Host "Have you completed the prerequisites? (y/n)"
if ($continue -notmatch "^y$|^Y$") {
    Write-Host "Please complete the prerequisites first." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 1: Building Phase 2 Docker image..." -ForegroundColor Cyan
docker build -t todo-phase2-backend:latest -f Dockerfile.phase2 .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2: Tagging for OCIR..." -ForegroundColor Cyan
$region = Read-Host "Enter your Oracle Cloud region (e.g., us-ashburn-1)"
$tenancy = Read-Host "Enter your tenancy name"
$imageName = "${region}.ocir.io/${tenancy}/todo-phase2-backend:latest"

docker tag todo-phase2-backend:latest $imageName

Write-Host ""
Write-Host "Step 3: Pushing Phase 2 image to OCIR..." -ForegroundColor Cyan
docker push $imageName

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker push failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 4: Updating Phase 2 deployment with your image..." -ForegroundColor Cyan

# Read the deployment file and replace placeholders
$deploymentContent = Get-Content phase2-deployment.yaml -Raw
$updatedDeployment = $deploymentContent -replace "<region>", $region
$updatedDeployment = $updatedDeployment -replace "<tenancy>", $tenancy

# Save the updated deployment
$tempDeploymentPath = "temp-phase2-deployment.yaml"
$updatedDeployment | Out-File -FilePath $tempDeploymentPath -Encoding UTF8

Write-Host "Step 5: Applying Phase 2 Kubernetes manifests..." -ForegroundColor Cyan
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f $tempDeploymentPath

Write-Host ""
Write-Host "Step 6: Waiting for Phase 2 deployment to be ready..." -ForegroundColor Cyan
kubectl rollout status deployment/todo-phase2-backend -n todo-app --timeout=300s

Write-Host ""
Write-Host "🎉 PHASE 2 DEPLOYMENT COMPLETED!" -ForegroundColor Green
Write-Host ""
Write-Host "Your Phase 2 application is now deployed to Oracle Cloud!" -ForegroundColor Green
Write-Host "It includes basic authentication and task management features." -ForegroundColor Green
Write-Host ""
Write-Host "To check the status:" -ForegroundColor Yellow
Write-Host "  kubectl get pods -n todo-app" -ForegroundColor Yellow
Write-Host "  kubectl get services -n todo-app" -ForegroundColor Yellow
Write-Host ""
Write-Host "To access your Phase 2 application:" -ForegroundColor Yellow
Write-Host "  kubectl get svc todo-phase2-service -n todo-app" -ForegroundColor Yellow
Write-Host "  Use the EXTERNAL-IP to access your application" -ForegroundColor Yellow
Write-Host ""

# Clean up temporary file
Remove-Item $tempDeploymentPath -Force