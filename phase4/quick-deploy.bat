@echo off
echo.
echo 🚀 Quick Deploy: Todo Chatbot on Kubernetes
echo ============================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Please run this script as Administrator!
    pause
    exit /b 1
)

echo.
echo 1/5 🔄 Starting Minikube...
minikube start --driver=docker --cpus=2 --memory=4096
if %errorlevel% neq 0 (echo ❌ Failed to start Minikube & pause & exit /b 1)

echo.
echo 2/5 🔌 Enabling Ingress...
minikube addons enable ingress

echo.
echo 3/5 📦 Building Docker Images...
docker build -f ./phase4/backend.Dockerfile -t todo-backend:latest . --quiet
docker build -f ./phase4/frontend.Dockerfile -t todo-frontend:latest . --quiet

echo.
echo 4/5 📥 Loading Images to Minikube...
minikube image load todo-backend:latest --daemon
minikube image load todo-frontend:latest --daemon

echo.
echo 5/5 ⚙️ Deploying Application...
helm upgrade --install todo-chatbot ./phase4/helm-chart/todo-chatbot ^
  --namespace todo-app ^
  --create-namespace ^
  --set backend.image.tag=latest ^
  --set frontend.image.tag=latest ^
  --wait ^
  --timeout=5m

if %errorlevel% neq 0 (
    echo ❌ Deployment failed!
    pause
    exit /b 1
)

REM Get Minikube IP and update hosts file
for /f "tokens=*" %%i in ('minikube ip') do set IP=%%i
echo %IP% todo.local >> C:\Windows\System32\drivers\etc\hosts

echo.
echo 🎉 SUCCESS! Application deployed!
echo ================================
echo Access at: http://todo.local
echo.
echo To verify: kubectl get pods -n todo-app
echo To monitor: kubectl logs -n todo-app deployment/todo-chatbot-backend -f
echo.
pause