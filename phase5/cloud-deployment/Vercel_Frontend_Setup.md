# Phase 2 Frontend Deployment on Vercel

This guide will help you deploy the Phase 2 frontend to Vercel for easy access.

## Prerequisites
- Vercel account (sign up at https://vercel.com/)
- GitHub account (Vercel integrates with GitHub)
- Phase 2 frontend code (located at `phase2/frontend/`)

## Step 1: Prepare Frontend for Vercel Deployment

### Create Vercel Configuration File
Create `phase2/frontend/vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next",
      "config": {
        "buildCommand": "npm run build",
        "devCommand": "npm run dev"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/"
    }
  ],
  "env": {
    "NEXT_PUBLIC_API_BASE_URL": "https://your-backend-url.vercel.app"
  }
}
```

### Update Environment Variables
Create or update `phase2/frontend/.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.onrender.com
# Or whatever backend URL you choose
```

### Ensure Next.js Configuration
Create or update `phase2/frontend/next.config.js`:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/:path*`,
      },
    ]
  },
}

module.exports = nextConfig
```

## Step 2: Prepare Backend for Easy Hosting

### Create Backend Configuration for External Hosting
Create `phase2/backend/Dockerfile.simple`:
```dockerfile
# Dockerfile.simple
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (commonly used by hosting platforms)
EXPOSE 8000

# Run the Phase 2 application
CMD ["uvicorn", "phase2.backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create Backend Environment Configuration
Create `phase2/backend/.env.production`:
```env
DATABASE_URL=your_postgresql_connection_string_here
ENVIRONMENT=production
ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Step 3: Deployment Instructions

### Frontend Deployment to Vercel:
1. Push your `phase2/frontend` code to a GitHub repository
2. Go to https://vercel.com/
3. Click "New Project" → "Import Git Repository"
4. Select your frontend repository
5. Set environment variables:
   - `NEXT_PUBLIC_API_BASE_URL`: Your backend URL (e.g., https://your-backend.onrender.com)
6. Click "Deploy"

### Backend Deployment Options:

#### Option A: Render.com (Free Tier)
1. Go to https://render.com/
2. Click "New +" → "Web Service"
3. Connect to your GitHub repository containing the backend
4. Choose "Docker" as Runtime
5. Use `phase2/backend/Dockerfile.simple` as Dockerfile path
6. Set environment variables:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `ALLOWED_ORIGINS`: Your Vercel frontend URL
7. Click "Create Web Service"

#### Option B: Railway.app (Free Tier)
1. Go to https://railway.app/
2. Click "New Project"
3. Connect to your GitHub repository
4. Choose "Dockerfile" deployment
5. Use `phase2/backend/Dockerfile.simple`
6. Set environment variables in Railway dashboard

#### Option C: Heroku (Free Tier)
1. Install Heroku CLI
2. Create `phase2/backend/Procfile`:
   ```
   web: uvicorn phase2.backend.app.main:app --host=0.0.0.0 --port=${PORT:-8000}
   ```
3. Deploy using Heroku CLI

## Step 4: Update API Calls for Cross-Origin Requests

Ensure your frontend API calls are configured to work with your deployed backend. Update `phase2/frontend/lib/api.ts` if needed:

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

## Step 5: Test Your Deployment

1. Access your frontend at the Vercel URL
2. Register/login to test authentication
3. Create and manage tasks to test backend functionality
4. Check browser console and network tabs for any errors

## Benefits of This Approach:
- **Frontend on Vercel**: Fast global CDN, automatic HTTPS, instant deployments
- **Backend on Render/Railway**: Easy scaling, managed infrastructure, free tiers
- **Separation of concerns**: Frontend and backend can be scaled independently
- **Cost-effective**: Both platforms offer generous free tiers

Your Phase 2 application will be accessible via the Vercel frontend URL while connecting to your externally hosted backend.