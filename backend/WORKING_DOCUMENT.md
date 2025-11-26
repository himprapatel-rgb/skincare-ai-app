# Skincare AI Backend - Working Document

## Project Status: November 26, 2025

This document serves as a comprehensive working reference for the Skincare AI Backend development project.

### Quick Project Facts
- **Repository**: https://gitlab.com/himprapatel-group/skincare-ai-app
- **Framework**: FastAPI 0.104.1 with Python 3.11+
- **Database**: PostgreSQL with async SQLAlchemy + Redis cache
- **Authentication**: JWT (JSON Web Tokens) with Bcrypt
- **Status**: Ready for Development Phase
- **Total API Endpoints**: 37+ fully documented endpoints
- **Microservices**: 8 route modules (auth, users, analysis, routine, progress, ingredients, notifications, dermatologist)

## Core Architecture

### Technology Stack
- **Web Framework**: FastAPI with Uvicorn ASGI server
- **Database**: PostgreSQL + SQLAlchemy (async)
- **Caching**: Redis
- **ML/AI**: PyTorch, TensorFlow, OpenCV, NumPy, Scikit-learn
- **Testing**: Pytest with async support
- **Code Quality**: Black, Flake8, MyPy
- **Logging**: Loguru

### Project Structure
```
app/
├── main.py              # FastAPI entry point
├── api/v1/routes/       # All microservice routes
│   ├── auth.py         # Authentication
│   ├── users.py        # User management (6 endpoints)
│   ├── analysis.py     # Skin analysis
│   ├── routine.py      # Skincare routines
│   ├── progress.py     # Progress tracking
│   ├── ingredients.py  # Ingredient database
│   ├── notifications.py # Notifications (7 endpoints)
│   └── dermatologist.py # Consultations (6 endpoints)
├── core/                # Core modules
│   ├── config.py       # Configuration management
│   ├── database.py     # Database setup
│   ├── security.py     # JWT & authentication
│   ├── cache.py        # Redis caching
│   ├── logging.py      # Logging setup
│   └── monitoring.py   # Monitoring
├── models/              # SQLAlchemy ORM models
│   ├── user.py
│   ├── analysis_result.py
│   ├── routine.py
│   └── notification.py
└── schemas/             # Pydantic request/response schemas
    ├── user.py
    ├── analysis.py
    └── routine.py
```

## Implementation Roadmap

### Phase 1: Core Infrastructure (CURRENT)
- [x] FastAPI application setup with lifespan management
- [x] CORS, GZip, exception handlers configured
- [x] Documentation endpoints (Swagger, ReDoc)
- [x] Health check endpoints
- [ ] Database models implementation
- [ ] Configuration system setup
- [ ] Security/JWT utilities

### Phase 2: Authentication & Database
- [ ] User model with soft delete
- [ ] Auth routes (register, login, refresh token)
- [ ] Database migrations with Alembic
- [ ] Connection pooling configuration
- [ ] Redis cache integration

### Phase 3: Core Endpoints
- [ ] User profile management (6 endpoints)
- [ ] Skin analysis endpoints
- [ ] Skincare routine generation
- [ ] Progress tracking endpoints

### Phase 4: Advanced Features
- [ ] Notifications system (7 endpoints)
- [ ] Dermatologist consultation (6 endpoints)
- [ ] Ingredient database integration
- [ ] AI model integration

### Phase 5: Testing & Deployment
- [ ] Unit tests for all endpoints
- [ ] Integration tests
- [ ] Docker containerization
- [ ] CI/CD pipeline setup
- [ ] Production deployment

## Key API Endpoints

### Authentication (5)
- POST /api/v1/auth/register
- POST /api/v1/auth/login  
- POST /api/v1/auth/refresh
- POST /api/v1/auth/logout
- POST /api/v1/auth/verify-email

### Users (6)
- GET /api/v1/users/me
- PUT /api/v1/users/me
- DELETE /api/v1/users/me
- GET /api/v1/users/me/statistics
- GET /api/v1/users/me/preferences
- PUT /api/v1/users/me/preferences

### Notifications (7)
- GET /api/v1/notifications
- POST /api/v1/notifications/{id}/read
- DELETE /api/v1/notifications/{id}
- POST /api/v1/notifications/read-all
- GET /api/v1/notifications/preferences
- PUT /api/v1/notifications/preferences

### Dermatologist (6)
- POST /api/v1/dermatologist/consult
- GET /api/v1/dermatologist/consultations
- GET /api/v1/dermatologist/consultations/{id}
- POST /api/v1/dermatologist/consultations/{id}/rate
- POST /api/v1/dermatologist/consultations/{id}/cancel
- GET /api/v1/dermatologist/dermatologists

## Development Notes

### Main Application (main.py)
- Fully async lifespan management
- Graceful startup/shutdown event handling
- Comprehensive exception handling (HTTP, Validation, General)
- All routers included with proper prefixes
- Auto-generated OpenAPI/Swagger documentation

### Environment Configuration
Required .env variables:
```
APP_NAME=Skincare AI App
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-secret-key-min-32-chars
DATABASE_URL=postgresql+asyncpg://user:password@localhost/skincare_ai_db
REDIS_URL=redis://localhost:6379/0
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Next Steps

1. **Create config.py** - Settings management with Pydantic
2. **Create database.py** - Async database connection
3. **Create security.py** - JWT token utilities
4. **Implement ORM models** - User, Analysis, Notification, Routine
5. **Write test file** - Auth routes testing

---

*Last Updated: November 26, 2025*