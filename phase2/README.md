# Phase II - Full-Stack Multi-User Web Application

This is the Phase II implementation of the Todo application following the Spec-Driven Development approach. This phase transforms the CLI-based application into a production-grade, authenticated, multi-user web system.

## Features

- **User Authentication**: JWT-based authentication system
- **Multi-User Support**: Each user has isolated data
- **Persistent Storage**: PostgreSQL database
- **RESTful API**: Well-defined API endpoints
- **Modern Frontend**: Next.js-based user interface

## Architecture

### Backend Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLModel
- **Authentication**: JWT with Bearer tokens
- **Password Hashing**: bcrypt

### Frontend Stack
- **Framework**: Next.js
- **Styling**: Tailwind CSS
- **API Communication**: Fetch API

## Database Schema

### users table
- `id`: Primary Key
- `email`: Unique, Non-null
- `hashed_password`: Non-null
- `created_at`: Timestamp

### tasks table
- `id`: Primary Key
- `title`: Non-null
- `description`: Optional
- `completed`: Boolean, default false
- `user_id`: Foreign Key to users.id
- `created_at`: Timestamp

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Tasks
- `POST /tasks` - Create task
- `GET /tasks` - List user tasks
- `GET /tasks/{id}` - Get single task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `POST /tasks/{id}/complete` - Mark task complete

## Security Features

- JWT token-based authentication
- User data isolation (each request is scoped by user_id)
- Password hashing with bcrypt
- Input validation and sanitization

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
uvicorn phase2.backend.app.main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd phase2/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The application will be accessible at `http://localhost:3000`.

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Individual database connection parameters

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API URL (defaults to http://localhost:8000)

## API Documentation

After starting the backend server, API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run backend tests with:
```bash
pytest
```

## Deployment

For production deployment:
1. Use a production-ready database (not SQLite)
2. Configure proper CORS settings
3. Use environment-specific configuration
4. Set up SSL certificates
5. Use a reverse proxy (nginx) in front of the application

## Phase III Preparation

This implementation is designed to support Phase III requirements:
- AI-powered chat interface
- MCP (Model Context Protocol) tools
- Conversational task management

The clean separation of concerns and well-defined API endpoints make it easy to add AI capabilities in Phase III.