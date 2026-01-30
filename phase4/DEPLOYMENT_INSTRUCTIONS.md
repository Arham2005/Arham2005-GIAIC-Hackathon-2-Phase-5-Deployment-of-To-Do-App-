# Todo Chatbot Deployment Instructions

## Prerequisites

Before running the deployment, ensure you have the following installed:

1. **Docker Desktop** with Kubernetes enabled OR **Minikube**
2. **Helm** (version 3.x)
3. **kubectl**
4. **Administrator access** to your computer (needed for hosts file modification)

## Installation Links

- Docker Desktop: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- Minikube: [https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/)
- Helm: [https://helm.sh/docs/intro/install/](https://helm.sh/docs/intro/install/)

## Quick Deployment (Recommended)

1. **Right-click** on `quick-deploy.bat` and select **"Run as administrator"**
2. Wait for the deployment to complete (takes 5-10 minutes)
3. Access the application at: `http://todo.local`

## Alternative: Manual Deployment

If you prefer to run commands manually:

### 1. Start Minikube
```bash
minikube start --driver=docker --cpus=2 --memory=4096
```

### 2. Enable Ingress
```bash
minikube addons enable ingress
```

### 3. Build Docker Images
```bash
docker build -f ./phase4/backend.Dockerfile -t todo-backend:latest .
docker build -f ./phase4/frontend.Dockerfile -t todo-frontend:latest .
```

### 4. Load Images to Minikube
```bash
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### 5. Deploy with Helm
```bash
helm upgrade --install todo-chatbot ./phase4/helm-chart/todo-chatbot \
  --namespace todo-app \
  --create-namespace \
  --set backend.image.tag=latest \
  --set frontend.image.tag=latest \
  --wait \
  --timeout=5m
```

### 6. Update Hosts File
Add this line to your hosts file (`C:\Windows\System32\drivers\etc\hosts`):
```
<minikube-ip> todo.local
```

Get the Minikube IP with: `minikube ip`

## Accessing the Application

After deployment, access the application at:
- **Frontend**: `http://todo.local`
- **Backend API**: `http://todo.local/api`
- **Health Check**: `http://todo.local/health`

## Verification Commands

Check if deployment was successful:
```bash
# Check pods
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check ingress
kubectl get ingress -n todo-app

# Check logs
kubectl logs -n todo-app deployment/todo-chatbot-backend -f
```

## Troubleshooting

### Common Issues:

1. **Permission Error**: Make sure to run as Administrator
2. **Image Pull Error**: Ensure images were built and loaded to Minikube
3. **Hosts File Error**: Manually add the IP address to your hosts file
4. **Timeout Errors**: Wait a few more minutes for pods to start

### Reset Deployment:
```bash
helm uninstall todo-chatbot -n todo-app
kubectl delete namespace todo-app
```

## OpenAI API Key (Optional)

To enable AI functionality, update the Helm values with your OpenAI API key:
```bash
helm upgrade --install todo-chatbot ./phase4/helm-chart/todo-chatbot \
  --namespace todo-app \
  --create-namespace \
  --set backend.image.tag=latest \
  --set frontend.image.tag=latest \
  --set backend.env.OPENAI_API_KEY="your-api-key-here"
```

## Cleanup

To remove the deployment:
```bash
helm uninstall todo-chatbot -n todo-app
kubectl delete namespace todo-app
minikube stop
```

## Support

If you encounter issues:
1. Check all prerequisites are installed
2. Ensure you're running as Administrator
3. Verify Docker Desktop/Minikube is running
4. Check the logs: `kubectl logs -n todo-app deployment/todo-chatbot-backend`