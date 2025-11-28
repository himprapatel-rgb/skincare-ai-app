# Skincare AI Backend - Complete Implementation Guide

## Project Overview

The Skincare AI backend is built with **FastAPI** and **Python 3.11+**, providing a robust, scalable, and production-ready API for the skincare analysis mobile application.

### Tech Stack
- **Framework**: FastAPI (async)
- **Database**: PostgreSQL with async SQLAlchemy
- **Cache**: Redis
- **Authentication**: JWT (JSON Web Tokens)
- **Email**: SMTP
- **Documentation**: Swagger UI (Automatic)

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry point
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── routes/
│   │           ├── __init__.py
│   │           ├── auth.py          # Authentication endpoints
│   │           ├── users.py         # User profile management
│   │           ├── analysis.py      # Skin analysis endpoints
│   │           ├── routine.py       # Skincare routine
│   │           ├── progress.py      # Progress tracking
│   │           ├── ingredients.py   # Product ingredients
│   │           ├── notifications.py # Push notifications
│   │           └── dermatologist.py # Dermatologist consultation
│   ├── core/
│   │   ├── config.py               # Configuration & settings
│   │   ├── database.py             # Database setup & session
│   │   ├── security.py             # JWT & authentication
│   │   ├── logging.py              # Logging configuration
│   │   ├── cache.py                # Redis cache management
│   │   └── monitoring.py           # Application monitoring
│   ├── models/
│   │   ├── user.py                 # User ORM model
│   │   ├── analysis_result.py      # Analysis ORM model
│   │   ├── routine.py              # Routine ORM model
│   │   └── notification.py         # Notification ORM model
│   └── schemas/
│       ├── user.py                 # User Pydantic schemas
│       ├── analysis.py             # Analysis request/response schemas
│       └── routine.py              # Routine schemas
├── alembic/                         # Database migrations
├── tests/                           # Unit & integration tests
├── requirements.txt
├── .env.example
└── Dockerfile
```

## Key Features Implemented

### 1. Authentication System
- JWT-based token authentication
- Bcrypt password hashing
- Secure token refresh mechanism
- Email verification support
- Role-based access control (RBAC)

### 2. User Management
- User registration and login
- Profile management
- Preference settings
- Account deletion (soft delete)
- User statistics and analytics

### 3. Skin Analysis Engine
- Image upload and processing
- AI-powered skin analysis
- Skin metrics calculation (hydration, oiliness, elasticity, pores)
- Condition detection (acne, dryness, sensitivity, etc.)
- Personalized recommendations

### 4. Skincare Routines
- Morning & evening routine generation
- Step-by-step instructions
- Product recommendations
- Routine adherence tracking

### 5. Progress Tracking
- Historical analysis storage
- Progress visualization data
- Trend analysis
- Routine compliance metrics

### 6. Notifications
- Push notification management
- Reminder scheduling
- Notification preferences
- Email notifications

### 7. Dermatologist Consultation
- Consultation request creation
- Question & image submission
- Response management
- Rating system

### 8. Skin Scan (AI-Powered)
- Image upload analysis (JPEG, PNG)
- URL-based image analysis
- AI skin type classification (oily, dry, combination, normal, sensitive)
- Skin concern detection (acne, wrinkles, dark spots, redness, etc.)
- Comprehensive skin metrics (hydration, oiliness, texture, elasticity, pore size)
- Personalized recommendations based on analysis
- Health check endpoint for service monitoring

## API Endpoints

### Authentication
```
POST   /api/v1/auth/register      - User registration
POST   /api/v1/auth/login         - User login
POST   /api/v1/auth/refresh       - Refresh token
POST   /api/v1/auth/logout        - User logout
POST   /api/v1/auth/verify-email  - Email verification
```

### Users
```
GET    /api/v1/users/me            - Get current user profile
PUT    /api/v1/users/me            - Update profile
DELETE /api/v1/users/me            - Delete account
GET    /api/v1/users/me/statistics - Get user statistics
GET    /api/v1/users/me/preferences - Get preferences
PUT    /api/v1/users/me/preferences - Update preferences
```

### Skin Analysis
```
POST   /api/v1/analysis           - Submit skin analysis
GET    /api/v1/analysis/{id}      - Get analysis result
GET    /api/v1/analysis           - List user analyses
DELETE /api/v1/analysis/{id}      - Delete analysis
```

### Routines
```
GET    /api/v1/routine            - Get current routine
POST   /api/v1/routine            - Generate new routine
PUT    /api/v1/routine            - Update routine
GET    /api/v1/routine/history    - Routine history
```

### Progress
```
GET    /api/v1/progress           - Get progress data
GET    /api/v1/progress/charts    - Chart data
POST   /api/v1/progress/log       - Log routine completion
```

### Notifications
```
GET    /api/v1/notifications      - List notifications
POST   /api/v1/notifications/{id}/read - Mark as read
DELETE /api/v1/notifications/{id} - Delete notification
```

### Dermatologist
```
POST   /api/v1/dermatologist/consult           - Create consultation
GET    /api/v1/dermatologist/consultations    - List consultations
GET    /api/v1/dermatologist/consultations/{id} - Get consultation
POST   /api/v1/dermatologist/consultations/{id}/rate - Rate response

### Skin Scan
```
POST   /api/v1/skin-scan/analyze      - Analyze skin from uploaded image
POST   /api/v1/skin-scan/analyze-url  - Analyze skin from image URL
GET    /api/v1/skin-scan/health       - Health check for skin scan service
```
```

## Setup Instructions

### 1. Installation

```bash
# Clone repository
git clone https://gitlab.com/himprapatel-group/skincare-ai-app.git
cd skincare-ai-app/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
# Required variables:
# DATABASE_URL=postgresql+asyncpg://user:password@localhost/skincare_db
# REDIS_URL=redis://localhost:6379/0
# JWT_SECRET_KEY=your-secret-key
# JWT_ALGORITHM=HS256
```

### 3. Database Setup

```bash
# Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE skincare_db;"

# Run migrations
alembic upgrade head
```

### 4. Run Development Server

```bash
# Start server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access Swagger documentation
http://localhost:8000/api/v1/docs
```

## Database Migrations

### Create New Migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migration
```bash
alembic downgrade -1
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py
```

## Deployment

### Docker Build
```bash
docker build -t skincare-ai-backend .
docker run -p 8000:8000 --env-file .env skincare-ai-backend
```

### Production Deployment
```bash
# Using Gunicorn + Uvicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Monitoring & Logging

- Structured logging with Python logging module
- Application metrics via Prometheus
- Request tracing with X-Request-ID
- Health check endpoints: `/health` and `/health/detailed`

## Performance Optimization

- Async/await for non-blocking operations
- Redis caching for frequently accessed data
- Database connection pooling
- Query optimization with proper indexing
- GZip compression for responses

## Security Best Practices

- CORS configuration for mobile app
- Rate limiting on endpoints
- Input validation with Pydantic
- SQL injection prevention (ORM)
- Password hashing with bcrypt
- HTTPS enforcement in production
- Secure token storage

## Contributing Guidelines

1. Create feature branch from `main`
2. Follow PEP 8 style guide
3. Add tests for new features
4. Create merge request with description
5. Code review before merging

## Support & Documentation

- API Documentation: `/api/v1/docs` (Swagger)
- ReDoc Documentation: `/api/v1/redoc`
- Additional docs: `docs/` folder

## License

All rights reserved - Himanshu Prakashbhai Patel Group
