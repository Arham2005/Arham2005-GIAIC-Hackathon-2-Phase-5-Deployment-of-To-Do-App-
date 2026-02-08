# Complete Incremental Deployment Guide for Todo Application

This guide provides step-by-step instructions for deploying the Todo Application in three incremental phases:

## Phase 1: Deploy Phase 2 (Basic Web Application) Separately

### What's Included:
- User authentication system
- Basic task management (CRUD operations)
- Multi-user isolation
- PostgreSQL database integration

### Deployment Steps:
1. Navigate to the deployment directory:
   ```bash
   cd phase5/cloud-deployment/
   ```

2. Deploy Phase 2 using the appropriate script:
   - **Linux/Mac**: `./deploy-phase2.sh`
   - **Windows**: `.\deploy-phase2.ps1`

3. Follow the prompts to enter your Oracle Cloud region and tenancy name

4. Access your Phase 2 application:
   ```bash
   kubectl get svc todo-phase2-service -n todo-app
   ```

## Phase 2: Deploy Phase 2 + Phase 3 on Docker

### What's Included:
- All Phase 2 features
- AI-powered chat system
- Natural language processing
- MCP tools integration

### Deployment Steps:
1. Ensure Phase 2 is running (or tear it down if needed):
   ```bash
   kubectl delete deployment todo-phase2-backend -n todo-app
   ```

2. Deploy Phase 2+3 using the appropriate script:
   - **Linux/Mac**: `./deploy-phase23.sh`
   - **Windows**: `.\deploy-phase23.ps1`

3. Follow the prompts to enter your Oracle Cloud region and tenancy name

4. Access your Phase 2+3 application:
   ```bash
   kubectl get svc todo-phase23-service -n todo-app
   ```

## Phase 3: Deploy Phase 2 + Phase 3 + Phase 5 (Advanced Features) to Cloud

### What's Included:
- All Phase 2 features (authentication, task management)
- All Phase 3 features (AI chat)
- Advanced features:
  - Recurring tasks
  - Due dates & reminders
  - Priorities and tags
  - Search, filter, sort capabilities
  - Kafka event streaming
  - Dapr integration
  - Advanced cloud deployment features

### Deployment Steps:
1. Ensure previous phases are torn down if needed:
   ```bash
   kubectl delete deployment todo-phase23-backend -n todo-app
   ```

2. Deploy the full application using the existing scripts:
   - **Linux/Mac**: `./oci-deploy-script.sh` or run `python deploy_to_oci.py`
   - **Windows**: `.\oci-deploy-script.ps1`

3. Follow the prompts to enter your Oracle Cloud region and tenancy name

4. Access your full application:
   ```bash
   kubectl get svc todo-phase5-service -n todo-app
   ```

## Verification Commands for Each Phase

### Check deployment status:
```bash
kubectl get pods -n todo-app
kubectl get services -n todo-app
kubectl get ingress -n todo-app
```

### Check application health:
```bash
# Replace service name based on phase
kubectl exec -it deployment/todo-phase2-backend -n todo-app -- curl localhost:8000/health
kubectl exec -it deployment/todo-phase23-backend -n todo-app -- curl localhost:8000/health
kubectl exec -it deployment/todo-phase5-backend -n todo-app -- curl localhost:8000/health
```

### View application logs:
```bash
# Replace deployment name based on phase
kubectl logs -n todo-app deployment/todo-phase2-backend -f
kubectl logs -n todo-app deployment/todo-phase23-backend -f
kubectl logs -n todo-app deployment/todo-phase5-backend -f
```

## Rolling Back Between Phases

If you need to rollback between phases:

1. **From Phase 3 to Phase 2+3**:
   ```bash
   kubectl delete deployment todo-phase5-backend -n todo-app
   # Then deploy Phase 2+3
   ```

2. **From Phase 2+3 to Phase 2**:
   ```bash
   kubectl delete deployment todo-phase23-backend -n todo-app
   # Then deploy Phase 2
   ```

3. **Complete cleanup**:
   ```bash
   kubectl delete namespace todo-app
   ```

## Resource Utilization

- **Phase 2**: Minimal resources (1 replica, 256Mi memory)
- **Phase 2+3**: Moderate resources (1 replica, 384Mi memory)
- **Phase 2+3+5**: Full resources (2 replicas, 512Mi+ memory each)

All deployments are designed to work within Oracle Cloud's Always Free tier limits.

## API Endpoints by Phase

- **Phase 2**:
  - Authentication: `/auth/*`
  - Tasks: `/tasks/*`

- **Phase 2+3**:
  - All Phase 2 endpoints
  - Chat: `/chat/*`

- **Phase 2+3+5**:
  - All previous endpoints
  - Advanced task features: `/tasks/*` (enhanced)
  - Health check: `/health`
  - Phase info: `/phases-info`
  - API docs: `/docs`