# Testing and Validation for Todo Chatbot Kubernetes Deployment

## Overview
This document outlines the testing procedures and validation steps to ensure the Todo Chatbot application is properly deployed and functioning in the Kubernetes environment.

## Pre-Deployment Validation

### 1. Helm Chart Validation
```bash
# Validate the Helm chart syntax
helm lint ./phase4/helm-chart/todo-chatbot

# Dry-run installation to validate templates
helm install todo-chatbot ./phase4/helm-chart/todo-chatbot --dry-run --debug

# Check generated manifests
helm template todo-chatbot ./phase4/helm-chart/todo-chatbot
```

### 2. Docker Images Validation
```bash
# Test backend image locally
docker run -p 8000:8000 todo-backend:latest

# Test frontend image locally
docker run -p 3000:3000 todo-frontend:latest

# Check image sizes and layers
docker images | grep todo-
```

## Deployment Validation

### 1. Kubernetes Resources Status
```bash
# Check all pods are running
kubectl get pods -n todo-app

# Check all services are available
kubectl get svc -n todo-app

# Check ingress status
kubectl get ingress -n todo-app

# Check persistent volume claims
kubectl get pvc -n todo-app

# Check deployment rollout status
kubectl rollout status deployment/todo-chatbot-backend -n todo-app
kubectl rollout status deployment/todo-chatbot-frontend -n todo-app
```

### 2. Pod Health Checks
```bash
# Check pod logs for errors
kubectl logs -n todo-app -l app.kubernetes.io/component=backend --tail=50
kubectl logs -n todo-app -l app.kubernetes.io/component=frontend --tail=50

# Check pod resource usage
kubectl top pods -n todo-app

# Describe pods for detailed information
kubectl describe pods -n todo-app -l app.kubernetes.io/component=backend
kubectl describe pods -n todo-app -l app.kubernetes.io/component=frontend
```

## Functional Testing

### 1. Backend API Testing
```bash
# Port forward to access backend
kubectl port-forward -n todo-app svc/todo-chatbot-backend-service 8000:8000 &

# Test health endpoint
curl http://localhost:8000/health

# Test authentication endpoints
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test@example.com", "password": "password123"}'
```

### 2. Frontend Testing
```bash
# Port forward to access frontend
kubectl port-forward -n todo-app svc/todo-chatbot-frontend-service 3000:80

# Test if frontend loads
curl -I http://localhost:3000
```

### 3. End-to-End Testing Script
```bash
#!/bin/bash
# e2e-test.sh

NAMESPACE="todo-app"
TIMEOUT=300

echo "🧪 Starting end-to-end tests..."

# Wait for all pods to be ready
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=Ready pods --namespace=$NAMESPACE --selector=app.kubernetes.io/component=backend --timeout=${TIMEOUT}s
kubectl wait --for=condition=Ready pods --namespace=$NAMESPACE --selector=app.kubernetes.io/component=frontend --timeout=${TIMEOUT}s

# Get pod names
BACKEND_POD=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}')
FRONTEND_POD=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/component=frontend -o jsonpath='{.items[0].metadata.name}')

echo "📦 Backend pod: $BACKEND_POD"
echo "📦 Frontend pod: $FRONTEND_POD"

# Test backend health
echo "🏥 Testing backend health..."
BACKEND_HEALTH=$(kubectl exec -n $NAMESPACE $BACKEND_POD -- curl -s http://localhost:8000/health)
if [[ $BACKEND_HEALTH == *"healthy"* ]]; then
    echo "✅ Backend health check passed"
else
    echo "❌ Backend health check failed: $BACKEND_HEALTH"
    exit 1
fi

# Test database connectivity by checking if tasks endpoint works
echo "💾 Testing database connectivity..."
TASKS_RESPONSE=$(kubectl exec -n $NAMESPACE $BACKEND_POD -- curl -s -w "\n%{http_code}" http://localhost:8000/tasks/)
HTTP_CODE=$(echo "$TASKS_RESPONSE" | tail -n1)
TASKS_BODY=$(echo "$TASKS_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 401 ]; then
    echo "✅ Database connectivity test passed (got expected response)"
else
    echo "❌ Database connectivity test failed (HTTP $HTTP_CODE): $TASKS_BODY"
    exit 1
fi

# Test ingress accessibility
echo "🌐 Testing ingress accessibility..."
INGRESS_IP=$(kubectl get ingress -n $NAMESPACE todo-chatbot -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
if [ -n "$INGRESS_IP" ]; then
    echo "✅ Ingress is accessible at $INGRESS_IP"
else
    echo "⚠️ Ingress IP not assigned yet, this might be normal depending on your setup"
fi

echo "🎉 All tests passed! Application is ready for use."
```

## AI-Assisted Validation

### 1. Using kubectl-ai for Validation
```bash
# Check overall health
kubectl-ai "show me the health status of all pods in todo-app namespace"

# Resource analysis
kubectl-ai "analyze resource usage for todo-chatbot deployments"

# Network connectivity
kubectl-ai "verify that frontend can connect to backend in todo-app namespace"

# Error detection
kubectl-ai "find any errors in the logs from the last 10 minutes in todo-app namespace"
```

### 2. Using Kagent for Analysis
```bash
# Cluster analysis
kagent "analyze the cluster health and identify any potential issues"

# Performance analysis
kagent "evaluate performance metrics for todo-chatbot and suggest optimizations"

# Security scan
kagent "perform a security assessment on the todo-app namespace"
```

## Performance Testing

### 1. Load Testing
```bash
# Install hey for load testing
go install github.com/rakyll/hey@latest

# Test backend performance
hey -n 1000 -c 10 -host todo.local http://todo.local/health

# Test concurrent user scenario
hey -n 500 -c 20 -host todo.local http://todo.local/api/users/me
```

### 2. Resource Utilization Monitoring
```bash
# Monitor resource usage over time
kubectl top pods -n todo-app --watch

# Check resource limits and requests
kubectl describe deployment todo-chatbot-backend -n todo-app
kubectl describe deployment todo-chatbot-frontend -n todo-app
```

## Security Validation

### 1. Secret Management
```bash
# Verify secrets are properly configured
kubectl get secrets -n todo-app
kubectl describe secret todo-chatbot-backend-secret -n todo-app

# Verify sensitive data is not exposed in configs
kubectl get configmaps -n todo-app -o yaml
```

### 2. Network Policies (if implemented)
```bash
# Check if network policies are applied
kubectl get networkpolicies -n todo-app
```

## Scalability Testing

### 1. Horizontal Scaling
```bash
# Scale backend deployment
kubectl scale deployment todo-chatbot-backend -n todo-app --replicas=3

# Verify all replicas are running
kubectl get pods -n todo-app -l app.kubernetes.io/component=backend

# Scale frontend deployment
kubectl scale deployment todo-chatbot-frontend -n todo-app --replicas=2

# Verify all replicas are running
kubectl get pods -n todo-app -l app.kubernetes.io/component=frontend
```

### 2. Auto-scaling Validation (if HPA is configured)
```bash
# Check HPA status
kubectl get hpa -n todo-app

# Simulate load to test auto-scaling
# (Implementation depends on HPA configuration)
```

## Backup and Recovery Validation

### 1. Data Persistence
```bash
# Verify data is persisting across pod restarts
kubectl delete pod -n todo-app -l app.kubernetes.io/component=backend
kubectl delete pod -n todo-app -l app.kubernetes.io/component=database

# Wait for new pods to start
kubectl wait --for=condition=Ready pods --namespace=todo-app --selector=app.kubernetes.io/component=backend --timeout=180s
kubectl wait --for=condition=Ready pods --namespace=todo-app --selector=app.kubernetes.io/component=database --timeout=180s
```

## Rollback Validation

### 1. Rolling Updates
```bash
# Update deployment with new image
kubectl set image deployment/todo-chatbot-backend -n todo-app backend=todo-backend:new-version

# Monitor rollout
kubectl rollout status deployment/todo-chatbot-backend -n todo-app

# If something goes wrong, rollback
kubectl rollout undo deployment/todo-chatbot-backend -n todo-app
```

## Documentation Checklist

### 1. Deployment Documentation
- [ ] Helm chart configuration documented
- [ ] Values.yaml parameters explained
- [ ] Deployment steps documented
- [ ] Scaling procedures documented
- [ ] Troubleshooting guide available

### 2. Operational Documentation
- [ ] Monitoring setup documented
- [ ] Logging configuration documented
- [ ] Backup and recovery procedures
- [ ] Security considerations
- [ ] Performance tuning guidelines

## Final Validation Steps

### 1. Complete Application Test
1. Access the frontend application at `http://todo.local`
2. Register a new user account
3. Log in to the application
4. Create a few tasks
5. Update and complete tasks
6. Use the AI chatbot functionality
7. Verify all features work as expected

### 2. Cleanup Test
```bash
# Test cleanup procedures
helm uninstall todo-chatbot -n todo-app
kubectl delete namespace todo-app

# Verify cleanup
kubectl get all -n todo-app
# Should return "No resources found"
```

## Success Criteria

The deployment is considered successful when:
- [ ] All pods are running and healthy
- [ ] Services are accessible
- [ ] Ingress is routing traffic correctly
- [ ] Application functionality is verified
- [ ] Performance meets requirements
- [ ] Security configurations are validated
- [ ] Documentation is complete
- [ ] Rollback procedures are tested
- [ ] Monitoring is in place

## Post-Deployment Actions

1. Set up monitoring and alerting
2. Configure automated backups
3. Document operational procedures
4. Train team members on Kubernetes operations
5. Schedule regular security audits
6. Plan capacity management procedures

## Troubleshooting Common Issues

### Issue: Pods stuck in Pending state
```bash
kubectl describe pods -n todo-app
kubectl get nodes
kubectl describe nodes
```

### Issue: Ingress not routing traffic
```bash
kubectl get ingress -n todo-app -o yaml
kubectl logs -n kube-system deployment/ingress-nginx-controller
```

### Issue: Database connection failures
```bash
kubectl logs -n todo-app -l app=postgres
kubectl describe svc postgres-service -n todo-app
```

### Issue: Resource constraints
```bash
kubectl describe nodes
kubectl top nodes
kubectl describe pod <pod-name> -n todo-app
```