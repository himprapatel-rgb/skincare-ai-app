# AI Skincare App - Backend API

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

A production-ready FastAPI backend for an AI-powered skincare analysis and recommendation platform. This application combines computer vision, machine learning, and dermatological expertise to provide personalized skincare solutions.

## 🌟 Features

### Core Functionality
- **AI Skin Analysis**: Upload facial images for ML-powered skin condition detection
- **Personalized Routine Builder**: Generate customized AM/PM skincare routines
- **Progress Tracking**: Visualize skin health improvements over time with trend analysis
- **Ingredient Scanner**: Barcode scanning with INCI ingredient analysis and safety ratings
- **Smart Recommendations**: AI-generated product suggestions based on skin analysis
- **JWT Authentication**: Secure user registration and login

### Technical Highlights
- ✅ **Async/Await**: Fully asynchronous API for optimal performance
- ✅ **Type Safety**: Complete type hints throughout codebase
- ✅ **Auto Documentation**: Interactive API docs at `/docs` (Swagger UI)
- ✅ **Database Migrations**: Alembic for version-controlled schema changes
- ✅ **Production Ready**: Comprehensive error handling and logging
- ✅ **ML Integration**: PyTorch and TensorFlow support for skin analysis models

## 🏗️ Architecture

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── routes/
│   │           ├── auth.py          # Authentication endpoints
│   │           ├── analysis.py      # Skin analysis API
│   │           ├── routine.py       # Routine builder API
│   │           ├── progress.py      # Progress tracking API
│   │           └── ingredients.py   # Ingredient scanner API
│   ├── core/
│   │   ├── config.py                # App configuration
│   │   └── database.py              # Database connection
│   ├── models/
│   │   ├── user.py                  # User model
│   │   ├── skin_analysis.py         # Analysis model
│   │   └── routine.py               # Routine models
│   └── main.py                      # FastAPI application
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 14+
- Virtual environment tool (venv, conda, etc.)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://gitlab.com/himprapatel-group/skincare-ai-app.git
   cd skincare-ai-app/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📝 Environment Variables

Create a `.env` file in the backend directory:

```env
# Application
APP_NAME="AI Skincare App"
APP_VERSION="1.0.0"
DEBUG=True

# Security
SECRET_KEY="your-secret-key-here-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/skincare_db"

# CORS
CORS_ORIGINS="http://localhost:3000,http://localhost:8080"

# ML Models (Optional)
MODEL_PATH="./models"
```

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login (returns JWT token)
- `GET /api/v1/auth/me` - Get current user profile

### Skin Analysis
- `POST /api/v1/analysis/upload` - Upload image for AI analysis
- `GET /api/v1/analysis/{analysis_id}` - Get analysis results
- `GET /api/v1/analysis/` - Get user's analysis history
- `DELETE /api/v1/analysis/{analysis_id}` - Delete analysis
- `GET /api/v1/analysis/compare/{id1}/{id2}` - Compare two analyses

### Routine Builder
- `POST /api/v1/routine/` - Create custom routine
- `POST /api/v1/routine/generate` - Generate AI-powered routine
- `GET /api/v1/routine/{routine_id}` - Get routine details
- `GET /api/v1/routine/` - List user's routines
- `PUT /api/v1/routine/{routine_id}` - Update routine
- `DELETE /api/v1/routine/{routine_id}` - Delete routine
- `POST /api/v1/routine/{routine_id}/complete` - Log completion
- `GET /api/v1/routine/{routine_id}/adherence` - Get adherence stats

### Progress Tracking
- `GET /api/v1/progress/timeline` - Get progress timeline
- `GET /api/v1/progress/trends/{concern_type}` - Track specific concern
- `GET /api/v1/progress/summary` - Get progress summary

### Ingredient Scanner
- `POST /api/v1/ingredients/scan/barcode` - Scan product barcode
- `GET /api/v1/ingredients/ingredient/{name}` - Look up ingredient
- `POST /api/v1/ingredients/analyze/custom` - Analyze custom ingredient list
- `GET /api/v1/ingredients/search` - Search products

## 🧪 Testing

Run tests with pytest:

```bash
pytest tests/ -v
pytest tests/ --cov=app  # With coverage
```

## 🔒 Security

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **CORS Protection**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## 🚀 Deployment

### Docker (Recommended)

```bash
docker build -t skincare-api .
docker run -p 8000:8000 skincare-api
```

### Production Considerations

1. Use environment variables for sensitive data
2. Enable HTTPS/TLS
3. Set up proper logging and monitoring
4. Use a production ASGI server (Gunicorn + Uvicorn)
5. Implement rate limiting
6. Set up database backups
7. Use a reverse proxy (Nginx)

## 📊 Database Schema

- **users**: User accounts and authentication
- **skin_analyses**: AI skin analysis results
- **skincare_routines**: User routines and product steps
- **routine_adherence**: Routine completion tracking
- **product_recommendations**: AI-generated recommendations

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🔗 Related Documentation

- [Software Requirements Specification](../docs/SOFTWARE_REQUIREMENTS_SPECIFICATION.md)
- [API Documentation](http://localhost:8000/docs)
- [Frontend Repository](../frontend/)

## 📧 Contact

For questions or support, please open an issue on GitLab.

---

**Built with ❤️ using FastAPI, PostgreSQL, and PyTorch**
