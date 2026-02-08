# Unified Todo AI Chat Application

This repository contains a unified application that combines all phases of the Todo AI Chat system into a single backend. The unified application includes:

- **Phase 2**: Full-Stack Multi-User Web Application
- **Phase 3**: AI-Powered Todo Chat System
- **Phase 5**: Advanced Cloud Features (Recurring tasks, due dates, priorities, etc.)

## Features

- Multi-user authentication and authorization
- Task management with CRUD operations
- AI-powered chat interface
- Advanced task features (recurring, due dates, priorities, tags)
- Kafka event streaming
- Dapr integration for cloud-native deployment

## Prerequisites

- Python 3.7+
- PostgreSQL database
- Required Python packages (see requirements.txt)

## Running the Application

### Method 1: Using the Unified Backend (Recommended)

```bash
python unified_backend.py
```

Or use the starter script:

```bash
python start_unified_app.py
```

### Method 2: Using the Phase 5 Backend

```bash
python run_phase5_backend.py
```

## Accessing the Application

Once the server is running, you can access:

- **Application Root**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Phase Information**: http://localhost:8000/phases-info

## API Endpoints

### Phase 2 - Authentication & Basic Tasks
- `POST /auth/login` - User login
- `POST /auth/signup` - User registration
- `GET /basic-tasks` - List user's basic tasks
- `POST /basic-tasks` - Create a basic task

### Phase 3 - AI Chat System
- `POST /chat/start` - Start a new conversation
- `POST /chat/{user_id}/chat` - Send message to chat AI
- `GET /chat/{conversation_id}` - Get conversation history

### Phase 5 - Advanced Task Management
- `GET /tasks` - List user's advanced tasks (with filters, due dates, etc.)
- `POST /tasks` - Create an advanced task (with recurring, priority, etc.)
- `PUT /tasks/{id}` - Update an advanced task
- `DELETE /tasks/{id}` - Delete a task
- `POST /tasks/{id}/complete` - Mark task as complete

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost/database_name
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
DAPR_HTTP_PORT=3500
DAPR_GRPC_PORT=50001
```

## Frontend Integration

The unified backend serves all frontend needs for:
- Phase 2: Traditional web app interface
- Phase 3: Chatbot interface
- Phase 5: Advanced feature interfaces

Frontend applications can connect to the appropriate endpoints based on the feature they need to access.