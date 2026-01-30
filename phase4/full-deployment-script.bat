@echo off
echo.
echo 🚀 Starting Todo Chatbot Kubernetes Deployment
echo =================================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ This script must be run as Administrator!
    echo Right-click on this file and select "Run as administrator"
    pause
    exit /b 1
)

echo ✅ Running as Administrator

REM Check prerequisites
echo.
echo 🔍 Checking Prerequisites...
echo ---------------------------

where /q kubectl
if %errorlevel% neq 0 (
    echo ❌ kubectl is not installed or not in PATH
    pause
    exit /b 1
) else (
    echo ✅ kubectl found
    kubectl version --client
)

where /q helm
if %errorlevel% neq 0 (
    echo ❌ helm is not installed or not in PATH
    pause
    exit /b 1
) else (
    echo ✅ helm found
    helm version
)

where /q docker
if %errorlevel% neq 0 (
    echo ❌ docker is not installed or not in PATH
    pause
    exit /b 1
) else (
    echo ✅ docker found
    docker --version
)

REM Check if Minikube is available
where /q minikube
if %errorlevel% neq 0 (
    echo ❌ minikube is not installed or not in PATH
    echo Download from: https://minikube.sigs.k8s.io/docs/start/
    pause
    exit /b 1
) else (
    echo ✅ minikube found
    minikube version
)

echo.
echo 🔄 Starting Minikube Cluster...
echo -------------------------------
minikube start --driver=docker --cpus=2 --memory=4096
if %errorlevel% neq 0 (
    echo ❌ Failed to start Minikube
    pause
    exit /b 1
)

echo ✅ Minikube cluster started successfully

echo.
echo 🔧 Enabling Ingress Controller...
echo --------------------------------
minikube addons enable ingress
if %errorlevel% neq 0 (
    echo ⚠️ Warning: Failed to enable ingress addon
) else (
    echo ✅ Ingress controller enabled
)

echo.
echo 📦 Building Docker Images...
echo ----------------------------
echo Building backend image...
docker build -f ./phase4/backend.Dockerfile -t todo-backend:latest . --no-cache
if %errorlevel% neq 0 (
    echo ❌ Failed to build backend image
    pause
    exit /b 1
)

echo Building frontend image...
docker build -f ./phase4/frontend.Dockerfile -t todo-frontend:latest . --no-cache
if %errorlevel% neq 0 (
    echo ❌ Failed to build frontend image
    pause
    exit /b 1
)

echo.
echo 📥 Loading Images into Minikube...
echo ----------------------------------
minikube image load todo-backend:latest
if %errorlevel% neq 0 (
    echo ⚠️ Warning: Failed to load backend image into minikube
)

minikube image load todo-frontend:latest
if %errorlevel% neq 0 (
    echo ⚠️ Warning: Failed to load frontend image into minikube
)

echo.
echo ⚙️ Installing Todo Chatbot Application...
echo -----------------------------------------
helm upgrade --install todo-chatbot ./phase4/helm-chart/todo-chatbot ^
  --namespace todo-app ^
  --create-namespace ^
  --set backend.image.tag=latest ^
  --set frontend.image.tag=latest ^
  --wait ^
  --timeout=10m

if %errorlevel% neq 0 (
    echo ❌ Failed to install Todo Chatbot application
    pause
    exit /b 1
)

echo.
echo ⏳ Waiting for Deployments to be Ready...
echo ----------------------------------------
kubectl wait --for=condition=Ready pods --namespace=todo-app --selector=app.kubernetes.io/component=backend --timeout=300s
if %errorlevel% neq 0 (
    echo ⚠️ Backend pods may not be ready yet
) else (
    echo ✅ Backend pods are ready
)

kubectl wait --for=condition=Ready pods --namespace=todo-app --selector=app.kubernetes.io/component=frontend --timeout=300s
if %errorlevel% neq 0 (
    echo ⚠️ Frontend pods may not be ready yet
) else (
    echo ✅ Frontend pods are ready
)

echo.
echo 🌐 Getting Minikube IP Address...
echo ----------------------------------
for /f "tokens=*" %%i in ('minikube ip') do set MINIKUBE_IP=%%i
echo Minikube IP: %MINIKUBE_IP%

echo.
echo 🔧 Configuring Hosts File...
echo ---------------------------
set HOSTS_ENTRY=%MINIKUBE_IP% todo.local

REM Check if entry already exists
findstr /c:"todo.local" "C:\Windows\System32\drivers\etc\hosts" >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️ todo.local entry already exists in hosts file
) else (
    REM Add entry to hosts file
    echo %HOSTS_ENTRY% >> "C:\Windows\System32\drivers\etc\hosts"
    if %errorlevel% equ 0 (
        echo ✅ Added todo.local to hosts file
    ) else (
        echo ⚠️ Failed to add entry to hosts file
        echo Manual step: Add "%HOSTS_ENTRY%" to C:\Windows\System32\drivers\etc\hosts
    )
)

echo.
echo 📋 Verifying Deployment...
echo -------------------------
echo Checking pods:
kubectl get pods -n todo-app

echo.
echo Checking services:
kubectl get svc -n todo-app

echo.
echo Checking ingress:
kubectl get ingress -n todo-app

echo.
echo 🎉 Deployment Completed Successfully!
echo =====================================
echo.
echo 🌍 Access the application at: http://todo.local
echo 📊 Backend API: http://todo.local/api
echo 🏥 Health Check: http://todo.local/health
echo.
echo 📝 Notes:
echo   - If the site doesn't load, refresh your browser
echo   - The first load may take a moment as pods initialize
echo   - Check http://todo.local/health to verify backend is running
echo.
echo 🔧 To monitor the deployment:
echo   kubectl get pods -n todo-app
echo   kubectl get svc -n todo-app
echo   kubectl logs -n todo-app deployment/todo-chatbot-backend -f
echo.
echo 🗑️ To uninstall:
echo   helm uninstall todo-chatbot -n todo-app
echo.
pause