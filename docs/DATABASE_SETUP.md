# Database & Skin Analysis Service Setup Guide

This guide explains how to set up the PostgreSQL database and configure the skin analysis service for the Skincare AI App.

## Prerequisites

- Python 3.9+
- PostgreSQL 13+ (or a hosted service like Neon, Supabase, Railway)
- RapidAPI account (for skin analysis API - free tier available)

## 1. Database Setup

### Option A: Local PostgreSQL

```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE skincare_ai;
CREATE USER skincare_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE skincare_ai TO skincare_user;
\q
```

### Option B: Cloud PostgreSQL (Recommended for Production)

**Neon (Free tier available):**
1. Sign up at https://neon.tech
2. Create a new project
3. Copy the connection string

**Supabase:**
1. Sign up at https://supabase.com
2. Create a new project
3. Go to Settings > Database > Connection string

## 2. Environment Configuration

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/skincare_ai

# Skin Analysis API (RapidAPI)
RAPIDAPI_KEY=your_rapidapi_key_here

# Redis (optional, for caching)
REDIS_URL=redis://localhost:6379

# Application
DEBUG=true
SECRET_KEY=your_secret_key_here
```

## 3. Skin Analysis API Setup

### Get RapidAPI Key (Free Tier)

1. Go to https://rapidapi.com
2. Sign up for a free account
3. Search for "Skin Analyze" or "AILabTools Skin Analysis"
4. Subscribe to the free tier
5. Copy your API key from the dashboard

### Alternative: Local Analysis

If you don't have an API key, the service will use local analysis:
- Basic skin metrics calculation
- Rule-based recommendations
- Lower accuracy but no external dependencies

## 4. Running Migrations

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run migrations (using Alembic)
alembic upgrade head
```

## 5. Testing the Setup

### Test Database Connection

```python
from app.core.database import check_db_health
import asyncio

async def test():
    result = await check_db_health()
    print(f"Database healthy: {result}")

asyncio.run(test())
```

### Test Skin Analysis Service

```python
from app.services.skin_analysis_service import skin_analysis_service
import asyncio

async def test_analysis():
    result = await skin_analysis_service.analyze_skin(
        image_url="https://example.com/face.jpg"
    )
    print(f"Overall score: {result.overall_score}")
    print(f"Skin type: {result.skin_type}")
    print(f"Concerns: {[c.concern_type for c in result.concerns]}")

asyncio.run(test_analysis())
```

## 6. Database Schema

The skin analysis results are stored in the `skin_analyses` table:

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Foreign key to users |
| image_url | TEXT | URL of analyzed image |
| overall_score | FLOAT | 0-100 skin health score |
| skin_type | VARCHAR | oily/dry/combination/normal |
| detected_concerns | JSON | Array of detected issues |
| skin_metrics | JSON | Hydration, texture, etc. |
| created_at | TIMESTAMP | Analysis timestamp |

## 7. API Endpoints

### POST /api/v1/analysis/analyze

Analyze a skin image:

```json
{
  "image_url": "https://...",
  "user_id": "uuid"
}
```

Response:

```json
{
  "overall_score": 75.5,
  "skin_type": "combination",
  "concerns": [
    {
      "concern_type": "acne",
      "severity": "mild",
      "confidence": 0.85
    }
  ],
  "recommendations": [
    "Use a gentle cleanser with salicylic acid"
  ]
}
```

## Troubleshooting

### Database Connection Issues

- Verify DATABASE_URL format
- Check PostgreSQL is running
- Ensure firewall allows port 5432

### API Key Issues

- Verify RAPIDAPI_KEY is set correctly
- Check API subscription is active
- Service falls back to local analysis if API fails

## Support

For issues, create a GitLab issue or contact the development team.
