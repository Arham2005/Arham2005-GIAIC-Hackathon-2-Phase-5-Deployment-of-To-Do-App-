# Phase III - AI-Powered Todo Chat System

This is the Phase III implementation of the Todo application following the Spec-Driven Development approach. This phase converts the CRUD web app into an AI-native, conversational system where natural language triggers structured backend actions safely.

## Features

- **AI-Powered Chat Interface**: Natural language processing for task management
- **Conversational Task Management**: Add, list, update, complete, and delete tasks via chat
- **MCP Tool Integration**: AI safely interacts with backend through defined tools
- **Stateless Architecture**: Conversation history persisted in database
- **User Isolation**: All conversations are scoped to individual users

## Architecture

### Backend Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLModel
- **Authentication**: JWT with Bearer tokens
- **AI Agent**: Custom implementation with intent recognition
- **MCP Tools**: Defined interface for safe AI actions

### Frontend Stack
- **Framework**: Next.js
- **Styling**: Tailwind CSS
- **API Communication**: Fetch API

## AI Capabilities

The AI agent can understand and respond to various task management commands:

### Available Actions:
- **Add Task**: "Add a task to buy groceries" or "Create a task called 'meeting'"
- **List Tasks**: "Show me my tasks" or "What do I have to do?"
- **Update Task**: "Change task 1 to have title 'updated title'"
- **Complete Task**: "Mark task 2 as complete" or "Finish task 1"
- **Delete Task**: "Remove task 3" or "Delete task 1"

## Database Schema

### conversations table
- `id`: Primary Key
- `title`: Conversation title
- `user_id`: Foreign Key to users.id
- `created_at`: Timestamp

### messages table
- `id`: Primary Key
- `content`: Message content
- `role`: Message role (user/assistant)
- `conversation_id`: Foreign Key to conversations.id
- `user_id`: Foreign Key to users.id
- `created_at`: Timestamp

## API Endpoints

### Chat Endpoints
- `POST /chat/start` - Start new conversation
- `POST /chat/{conversation_id}/message` - Send message and get AI response
- `GET /chat/{conversation_id}` - Get conversation history

## Security Features

- All AI actions go through MCP tools (safe interface)
- User data isolation maintained at all levels
- Conversation privacy enforced
- No direct database access from AI

## Setup Instructions

### Backend Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Set up environment variables:
```bash
DATABASE_URL=postgresql://user:password@localhost/todo_db
SECRET_KEY=your-super-secret-key-change-this
```

3. Initialize the database:
```bash
python -m phase2.backend.app.database.init_db
```

4. Run the backend server:
```bash
uvicorn phase3.backend.app.main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd phase3/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file with:
```bash
NEXT_PUBLIC_CHAT_API_URL=http://localhost:8000/chat
```

4. Run the development server:
```bash
npm run dev
```

## MCP Tool Contract

The AI may only interact via the following tools:

- `add_task(title, description)` - Add a new task
- `list_tasks()` - List user's tasks
- `update_task(id, fields)` - Update a task
- `complete_task(id)` - Mark task as complete
- `delete_task(id)` - Delete a task

These tools reuse existing Phase II backend logic, ensuring consistency and safety.

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Individual database connection parameters

### Frontend
- `NEXT_PUBLIC_CHAT_API_URL`: Backend API URL for chat endpoints (defaults to http://localhost:8000/chat)

## API Documentation

After starting the backend server, API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Phase Transition

Phase III builds upon Phase II's foundation:
- Reuses user authentication system
- Leverages existing task management backend
- Maintains data isolation principles
- Adds conversational AI layer on top

## Future Enhancements

- Integration with OpenAI or other LLM providers
- Enhanced natural language understanding
- Richer conversation memory
- Advanced task management features