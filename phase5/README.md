# Phase 5: Advanced Cloud Deployment

## Part A: Advanced Features Implementation

This phase implements advanced features for the Todo Chatbot application, focusing on enhancing the functionality with enterprise-grade capabilities.

### Features Implemented

#### Advanced Level Features
- **Recurring Tasks**: Tasks that repeat based on patterns (daily, weekly, monthly, yearly)
- **Due Dates & Reminders**: Tasks with deadlines and automated reminder notifications

#### Intermediate Level Features
- **Priorities**: Low, Medium, High, Urgent priority levels for tasks
- **Tags**: Ability to categorize tasks with multiple tags
- **Search**: Full-text search across task titles and descriptions
- **Filter**: Advanced filtering by status, priority, tags, and date ranges
- **Sort**: Sorting by creation date, due date, or priority

#### Infrastructure Features
- **Event-Driven Architecture**: Implemented with Apache Kafka for asynchronous processing
- **Dapr Integration**: Distributed Application Runtime for microservice patterns including pub/sub, state management, and bindings

### Architecture Overview

```
┌─────────────┐    Kafka     ┌─────────────┐
│   Frontend  │◄────────────►│   Kafka     │
└─────────────┘              └─────────────┘
       │                           │
       │                    Dapr   │
       ▼                   Client  ▼
┌─────────────┐              ┌─────────────┐
│   Backend   │◄────────────►│   Dapr      │
│   Service   │              │ Sidecar     │
└─────────────┘              └─────────────┘
       │
       ▼
┌─────────────┐
│ PostgreSQL  │
└─────────────┘
```

### Key Components

#### Backend Enhancements
- **Models**: Extended Task model with priority, tags, due_date, recurring fields
- **Services**: Advanced task service with filtering, sorting, and recurring logic
- **API**: Updated endpoints supporting all new features
- **MCP Tools**: Updated tools with advanced capabilities

#### Frontend Components
- **Task Filters**: Comprehensive filtering and sorting UI
- **Task Cards**: Display of all advanced features with visual indicators
- **Dashboard**: Statistics and insights for advanced features
- **Forms**: Creation/editing with all new fields

#### Event-Driven Architecture
- **Kafka Producer**: Publishes task events (creation, update, completion)
- **Kafka Consumer**: Processes events asynchronously
- **Topics**: task-events, reminder-events, notification-events

#### Dapr Integration
- **Pub/Sub**: Event publishing for task operations
- **State Management**: Distributed state for task data
- **Bindings**: External service integration points

### API Endpoints

#### Task Management
- `POST /tasks` - Create task with advanced features
- `GET /tasks` - List tasks with filtering, sorting, and search
- `GET /tasks/{id}` - Get specific task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `POST /tasks/{id}/complete` - Mark task as complete
- `GET /tasks/due-soon` - Get tasks due soon
- `GET /tasks/recurring` - Get recurring tasks

#### Filtering Parameters
- `completed`: Filter by completion status
- `priority`: Filter by priority level
- `tags`: Filter by tags
- `due_date_from`: Filter tasks with due date after
- `due_date_to`: Filter tasks with due date before
- `search_query`: Search in title and description
- `sort_by`: Field to sort by (created_at, due_date, priority)
- `sort_order`: Sort order (asc, desc)

### Running the Application

1. **Start Kafka**:
   ```bash
   docker-compose -f docker-compose.kafka.yml up -d
   ```

2. **Start Dapr**:
   ```bash
   dapr init
   dapr run --app-id todo-backend --app-port 8000 --dapr-http-port 3500 --dapr-grpc-port 50001
   ```

3. **Run Backend**:
   ```bash
   python run_backend.py
   ```

4. **Run Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

### Database Schema Changes

The existing tasks table is extended with:

```sql
ALTER TABLE tasks ADD COLUMN priority VARCHAR(20) DEFAULT 'medium';
ALTER TABLE tasks ADD COLUMN tags JSONB DEFAULT '[]';
ALTER TABLE tasks ADD COLUMN due_date TIMESTAMP WITH TIME ZONE;
ALTER TABLE tasks ADD COLUMN recurring BOOLEAN DEFAULT FALSE;
ALTER TABLE tasks ADD COLUMN recurrence_pattern VARCHAR(20);
ALTER TABLE tasks ADD COLUMN parent_task_id INTEGER REFERENCES tasks(id);
ALTER TABLE tasks ADD COLUMN reminder_sent BOOLEAN DEFAULT FALSE;
ALTER TABLE tasks ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE;
```

### Future Enhancements

- **Part B**: Local deployment on Minikube with full Dapr setup
- **Part C**: Production deployment on Azure/Google Cloud with managed Kafka
- **Additional Features**: Subtasks, task dependencies, advanced notifications
- **Monitoring**: Enhanced observability for event-driven architecture