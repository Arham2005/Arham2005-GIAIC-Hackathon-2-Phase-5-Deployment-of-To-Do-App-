# Todo Application Phase 5 - Oracle Cloud Deployment Guide

This guide provides instructions for deploying the Todo Application Phase 5 (with advanced features) to Oracle Cloud Infrastructure (OCI) using Oracle Kubernetes Engine (OKE).

## Prerequisites

Before deploying, ensure you have:

1. **Oracle Cloud Account** - Sign up at https://www.oracle.com/cloud/free/
2. **OCI CLI** - Install and configure with your credentials
3. **kubectl** - Install and connect to your OKE cluster
4. **Docker** - Install and ready for container builds
5. **External PostgreSQL Database** - Recommended: Neon PostgreSQL (free tier available)

## Architecture Overview

The application consists of:
- **Phase 2**: Full-stack multi-user web application with authentication
- **Phase 3**: AI-powered chat system with MCP tools
- **Phase 5**: Advanced features (recurring tasks, due dates, priorities, etc.)

All phases are unified in a single backend application served on port 8000.

## Deployment Steps

### Step 1: Set Up Oracle Cloud Environment

1. **Sign up for Oracle Cloud Free Tier**
   - Visit https://www.oracle.com/cloud/free/
   - Complete registration (no credit card required for Always Free tier)

2. **Install OCI CLI**
   ```bash
   # On Windows, download from: https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm
   # Or use PowerShell:
   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.ps1" -OutFile install.ps1
   .\install.ps1
   ```

3. **Install kubectl**
   ```bash
   # On Windows with Chocolatey
   choco install kubernetes-cli

   # Or manually download from https://kubernetes.io/docs/tasks/tools/
   ```

4. **Configure OCI CLI**
   ```bash
   oci setup config
   # Follow the prompts to enter your tenancy OCID, user OCID, etc.
   ```

### Step 2: Create OKE Cluster

1. **Create OKE cluster with Always Free eligible resources**
   ```bash
   # Create cluster with 4 OCPUs and 24GB RAM (within Always Free limits)
   oci ce cluster create --name todo-app-cluster \
     --kubernetes-version v1.28.2 \
     --vcn-id <your_vcn_id> \
     --service-lb-subnet-ids <subnet_id_1> <subnet_id_2> \
     --compartment-id <your_compartment_id>
   ```

2. **Get Kubeconfig**
   ```bash
   oci ce cluster create-kubeconfig --cluster-id <cluster_id> --file ~/.kube/config --region us-ashburn-1
   ```

3. **Verify cluster connectivity**
   ```bash
   kubectl get nodes
   ```

### Step 3: Set Up Database

1. **Set up Neon PostgreSQL (recommended)**
   - Go to https://neon.tech/
   - Create a free project
   - Get your connection string: `postgresql://username:password@ep-xxx.region.aws.neon.tech/neondb`

2. **Alternatively, use Oracle Autonomous Database**
   - Create Autonomous Transaction Processing (ATP) instance in OCI
   - Download wallet and connection string

3. **Store database credentials in Kubernetes Secret**
   ```bash
   kubectl create secret generic db-secret \
     --from-literal=DATABASE_URL='postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/neondb' \
     --namespace todo-app
   ```

### Step 4: Prepare Container Image

1. **Log in to Oracle Cloud Infrastructure Registry (OCIR)**
   ```bash
   # Format: <region>.ocir.io/<tenancy>/<repo>:<tag>
   # Example: us-ashburn-1.ocir.io/mytenant/todo-repo:latest
   docker login <region>.ocir.io
   # Username: <tenancy_namespace>/<username>
   # Password: Your OCI auth token (generate in OCI Console -> User Settings -> Auth Tokens)
   ```

2. **Build and push Docker image**
   ```bash
   # Using the provided deployment script:
   # On Windows PowerShell:
   .\oci-deploy-script.ps1

   # Or manually:
   docker build -t todo-phase5-backend:latest -f Dockerfile.unified .
   docker tag todo-phase5-backend:latest <region>.ocir.io/<tenancy>/todo-phase5-backend:latest
   docker push <region>.ocir.io/<tenancy>/todo-phase5-backend:latest
   ```

### Step 5: Deploy to Kubernetes

1. **Apply Kubernetes manifests**
   ```bash
   kubectl apply -f namespace.yaml
   kubectl apply -f configmap.yaml
   # Update deployment.yaml with your actual region and tenancy before applying
   kubectl apply -f deployment.yaml
   kubectl apply -f ingress.yaml
   ```

2. **Monitor deployment**
   ```bash
   kubectl get pods -n todo-app
   kubectl get services -n todo-app
   kubectl get ingress -n todo-app
   ```

### Step 6: Configure Frontend (Next.js)

The frontend can be deployed separately using Oracle Cloud Application Container or a static hosting service.

## Environment Variables

Update the configmap.yaml with your actual values:
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: Your OpenAI API key for AI features
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS
- `ENVIRONMENT`: Set to "production"

## Accessing the Application

1. **Get the external IP**
   ```bash
   kubectl get svc todo-phase5-service -n todo-app
   ```

2. **Access the application**
   - API: `http://<EXTERNAL_IP>/`
   - API Documentation: `http://<EXTERNAL_IP>/docs`
   - Health check: `http://<EXTERNAL_IP>/health`
   - Phase info: `http://<EXTERNAL_IP>/phases-info`

## Scaling and Management

1. **Scale the application**
   ```bash
   kubectl scale deployment todo-phase5-backend -n todo-app --replicas=3
   ```

2. **Update the application**
   ```bash
   # Build new image with new tag
   docker build -t todo-phase5-backend:v2 -f Dockerfile.unified .
   docker tag todo-phase5-backend:v2 <region>.ocir.io/<tenancy>/todo-phase5-backend:v2
   docker push <region>.ocir.io/<tenancy>/todo-phase5-backend:v2

   # Update deployment
   kubectl set image deployment/todo-phase5-backend backend=<region>.ocir.io/<tenancy>/todo-phase5-backend:v2 -n todo-app
   ```

3. **View logs**
   ```bash
   kubectl logs -n todo-app deployment/todo-phase5-backend -f
   ```

## Troubleshooting

1. **Check pod status**
   ```bash
   kubectl get pods -n todo-app
   kubectl describe pod <pod-name> -n todo-app
   ```

2. **Check service status**
   ```bash
   kubectl get svc -n todo-app
   kubectl describe svc todo-phase5-service -n todo-app
   ```

3. **Test connectivity**
   ```bash
   # Port forward for testing
   kubectl port-forward -n todo-app service/todo-phase5-service 8080:80
   # Then visit http://localhost:8080
   ```

## Security Considerations

1. **Network policies** - Restrict traffic between services
2. **Secrets management** - Use sealed-secrets for sensitive data
3. **RBAC** - Configure proper role-based access control
4. **TLS/SSL** - Use cert-manager for automatic certificate provisioning

## Cleanup

To remove the deployment:
```bash
kubectl delete namespace todo-app
```

To remove the OKE cluster:
```bash
oci ce cluster delete --cluster-id <cluster_id> --force
```