# Phase 5: Advanced Cloud Deployment

## Part B: Local Deployment on Minikube with Full Dapr

This section describes how to deploy the Todo Chatbot application to Minikube with complete Dapr integration.

### Prerequisites

- Minikube
- kubectl
- Dapr CLI
- Docker

### Setup and Deployment

1. **Start Minikube with Dapr:**
   ```bash
   cd deploy/local
   chmod +x minikube-setup.sh
   ./minikube-setup.sh
   ```

2. **Deploy the application:**
   ```bash
   chmod +x deploy-minikube.sh
   ./deploy-minikube.sh
   ```

3. **Access the application:**
   - Frontend: http://todo.local
   - Dapr dashboard: `dapr dashboard`
   - Kubernetes dashboard: `minikube dashboard`

### Dapr Components Deployed

- **Pub/Sub**: Redis-based publish/subscribe for task events
- **State Management**: Redis-based state store for distributed state
- **Bindings**: Cron binding for scheduled tasks and reminders
- **Secrets**: Local file-based secret store
- **Service Invocation**: Direct service-to-service communication via Dapr

### Architecture Overview

```
┌─────────────┐    HTTP     ┌─────────────┐
│   Frontend  │────────────▶│   Dapr      │
│             │             │ Sidecar     │
└─────────────┘             └─────────────┘
                                 │
                                 ▼
┌─────────────┐             ┌─────────────┐
│   Backend   │────────────▶│   Dapr      │
│             │             │ Sidecar     │
└─────────────┘             └─────────────┘
                                 │
                                 ▼
                       ┌─────────────┐
                       │   Redis     │
                       │ (State/Pub) │
                       └─────────────┘
                                 │
                                 ▼
                       ┌─────────────┐
                       │ PostgreSQL  │
                       └─────────────┘
```

## Part C: Cloud Deployment on Azure (AKS) / Google Cloud (GKE)

This section describes how to deploy the Todo Chatbot application to cloud platforms with managed services and full Dapr integration.

### Azure Deployment (AKS)

#### Prerequisites

- Azure CLI
- Dapr CLI
- kubectl

#### Deployment Steps

1. **Update the Azure deployment script** with your subscription details:
   ```bash
   # Edit azure-deploy.sh and update:
   # - RESOURCE_GROUP
   # - SUBSCRIPTION_ID
   # - LOCATION
   # - Add your actual values for secrets
   ```

2. **Run the deployment:**
   ```bash
   cd deploy/cloud
   chmod +x azure-deploy.sh
   ./azure-deploy.sh
   ```

#### Services Used

- **AKS**: Managed Kubernetes service
- **Azure Cosmos DB**: Managed NoSQL database for state
- **Azure Database for PostgreSQL**: Managed PostgreSQL for main database
- **Azure Cache for Redis**: Managed Redis for caching/pub-sub
- **Azure Key Vault**: Managed secrets storage
- **Azure Container Registry**: Container image registry

### Google Cloud Deployment (GKE)

#### Prerequisites

- Google Cloud CLI
- Dapr CLI
- kubectl

#### Deployment Steps

1. **Update the GKE deployment script** with your project details:
   ```bash
   # Edit gke-deploy.sh and update:
   # - PROJECT_ID
   # - REGION
   # - Add your actual values for secrets
   ```

2. **Run the deployment:**
   ```bash
   cd deploy/cloud
   chmod +x gke-deploy.sh
   ./gke-deploy.sh
   ```

#### Services Used

- **GKE**: Managed Kubernetes Engine
- **Cloud SQL**: Managed PostgreSQL database
- **Cloud Memorystore**: Managed Redis service
- **Secret Manager**: Managed secrets storage
- **Artifact Registry**: Container image registry

### Dapr Components in Cloud

Both cloud deployments include:

- **Pub/Sub**: Managed message queuing (Azure Service Bus / Google Pub/Sub)
- **State Management**: Managed document database (Cosmos DB / Firestore)
- **Bindings**: Cron and external service bindings
- **Secrets**: Managed key vault (Key Vault / Secret Manager)
- **Service Invocation**: Dapr-enabled service-to-service communication

### Kafka Integration

For event-driven architecture, the system integrates with:

- **Confluent Cloud** or **Redpanda Cloud** for managed Kafka
- **Topic Management**: Automated topic creation for task events, reminders, and notifications
- **Consumer Groups**: Properly configured consumer groups for reliable message processing

### CI/CD Pipeline

GitHub Actions workflows are provided for both platforms:

- **Azure**: `.github/workflows/ci-cd-azure.yml`
- **GKE**: `.github/workflows/ci-cd-gke.yml`

The pipelines include:
- Automated builds and container image pushes
- Security scanning
- Deployment to production
- Health checks and rollbacks

### Monitoring and Observability

- **Dapr Observability**: Built-in metrics, tracing, and health checks
- **Cloud Monitoring**: Platform-native monitoring and alerting
- **Logging**: Structured logging with correlation IDs
- **Performance Metrics**: Response times, throughput, and error rates

### Security Considerations

- **Network Policies**: Restrict traffic between services
- **RBAC**: Role-based access control for Kubernetes resources
- **Secret Management**: Never expose secrets in code or configuration
- **TLS**: Encrypted communication between all services
- **Authentication**: JWT-based authentication for all API calls

### Scaling Configuration

- **Horizontal Pod Autoscaling**: Automatic scaling based on CPU/memory
- **Cluster Autoscaling**: Node pool scaling based on demand
- **Database Connection Pooling**: Efficient database connection management
- **Redis Clustering**: Distributed caching for high availability