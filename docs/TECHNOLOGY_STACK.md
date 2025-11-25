# Skincare AI App - Technology Stack

**Document:** `/docs/TECHNOLOGY_STACK.md`
**Version:** 1.0
**Last Updated:** November 25, 2025
**Based on:** Features roadmap + Zero-cost + No vendor lock-in requirements

---

## Core Requirements Met

✅ **Free Forever** - No paid tiers, no trials
✅ **Easy Migration** - Standard formats (SQL, Docker, REST)
✅ **GitLab Native** - Build, test, deploy iOS & Android on GitLab
✅ **All 14 Features** - Complete support for every feature
✅ **Fast & Responsive** - Native performance, <3s load times
✅ **Zero Cost** - $0/month for MVP (0-10K users)

---

## Technology Selection Principles

**NO Vendor Lock-in:**
- Standard SQL (not proprietary databases)
- Docker containers (portable)
- REST APIs (platform-agnostic)
- Open file formats (ONNX, TFLite)
- Git-based workflows

**Easy Migration Path:**
```
Current Platform → Export Data → Import to New Platform
- PostgreSQL dump → Any Postgres host
- Docker image → Any container platform
- Flutter code → Runs anywhere
- ML models (ONNX) → Platform-independent
```

---

## 1. Frontend: Flutter (Dart)

### Why Flutter?
[web:52][web:55][web:69]

**Performance:**
- Compiles to native ARM code
- 60fps animations guaranteed
- <3s app startup time
- Direct GPU access via Skia

**Migration Freedom:**
- Single codebase → iOS + Android
- No platform-specific code needed
- Export to web/desktop if needed
- Open-source (BSD license)

**GitLab CI/CD:**
- Free Linux runners for Android
- Free macOS runners for iOS (beta)
- 400 CI minutes/month free

### Stack

```yaml
Language: Dart 3.x
Framework: Flutter 3.24+
State Management: Riverpod 2.x
Architecture: Clean Architecture
Storage: SQLite (local) + Hive (cache)
```

### Key Packages (All Open-Source)

```yaml
Camera & Images:
  - camera: ^0.10.5
  - image_picker: ^1.0.5
  - image: ^4.1.3

ML/CV:
  - tflite_flutter: ^0.10.4
  - google_ml_kit: ^0.16.0
  - opencv_dart: ^1.0.4

Database:
  - sqflite: ^2.3.0
  - hive: ^2.2.3
  - drift: ^2.14.0

Networking:
  - dio: ^5.4.0
  - retrofit: ^4.0.3

UI/Charts:
  - fl_chart: ^0.65.0
  - syncfusion_flutter_charts: ^24.1.41

Security:
  - flutter_secure_storage: ^9.0.0
  - encrypt: ^5.0.3
```

---

## 2. Backend: FastAPI (Python)

### Why FastAPI?
[web:47][web:50]

**Performance:**
- Async/await (handles 1000+ concurrent requests)
- Faster than Django (2-3x)
- Auto API documentation (OpenAPI/Swagger)

**Migration Freedom:**
- Standard REST API
- Works with ANY frontend
- Docker containerized
- Environment-based config (12-factor)

**ML Integration:**
- Native Python (PyTorch, TensorFlow)
- NumPy, OpenCV, scikit-learn
- No language barriers

### Stack

```yaml
Language: Python 3.11+
Framework: FastAPI 0.110+
Server: Uvicorn (ASGI)
ORM: SQLAlchemy 2.x (async)
Migrations: Alembic
Authentication: JWT (python-jose)
Validation: Pydantic 2.x
```

### Dependencies

```txt
# Web
fastapi==0.110.0
uvicorn[standard]==0.27.0
pydantic==2.6.0

# Database (portable)
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9
pymongo==4.6.1
redis==5.0.1

# ML/CV
torch==2.2.0
torchvision==0.17.0
onnx==1.15.0
onnxruntime==1.17.0
opencv-python==4.9.0

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
```

---

## 3. Databases (Portable)

### PostgreSQL (Primary Database)

**Why:**
- Industry standard (no lock-in)
- Supports JSONB (flexible schemas)
- Full SQL compliance
- Easy backup/restore

**Migration:**
```bash
# Export from anywhere
pg_dump database > backup.sql

# Import to anywhere
psql new_database < backup.sql
```

**Free Hosting Options:**
```yaml
Supabase: 500 MB free (easy migration)
Neon.tech: 3 GB free (serverless Postgres)
ElephantSQL: 20 MB free
Railway: Free tier available
Self-hosted: Docker on any VPS
```

### MongoDB (Analytics)

**Why:**
- Time-series data (skin analysis logs)
- Flexible schema
- Standard export format (JSON)

**Migration:**
```bash
# Export
mongodump --db skincare --out /backup

# Import
mongorestore --db skincare /backup/skincare
```

**Free Hosting:**
```yaml
MongoDB Atlas: 512 MB free
Self-hosted: Docker container
```

### Redis (Caching)

**Why:**
- Fast in-memory cache
- Standard Redis protocol
- Easy to replace

**Migration:**
```bash
# Backup
redis-cli --rdb /backup/dump.rdb

# Restore
redis-cli --rdb /backup/dump.rdb
```

**Free Hosting:**
```yaml
Upstash: 10K commands/day free
Redis Cloud: 30 MB free
Self-hosted: Docker container
```

---

## 4. ML Pipeline (Portable)

### Training: PyTorch
[web:67][web:70]

**Why PyTorch:**
- Research-friendly
- Export to ONNX (standard format)
- Strong community
- No vendor lock-in

### Deployment: ONNX + TensorFlow Lite
[web:68][web:69][web:71]

**Why ONNX:**
- Platform-independent format
- Works with ANY framework
- Easy migration

**Conversion Pipeline:**
```
PyTorch (.pth) → ONNX (.onnx) → TFLite (.tflite)
```

### MLOps Tools (Open Source)

**MLflow:**[web:73][web:76][web:82]
```yaml
Experiment Tracking: Logs all training runs
Model Registry: Version control for models
Deployment: REST API serving
Storage: Local/S3/Any cloud
Migration: SQLite/PostgreSQL backend (portable)
```

**DVC (Data Version Control):**[web:73]
```yaml
Data Versioning: Git-like for datasets
Pipeline: Reproducible ML workflows
Storage: S3, Google Drive, SSH, local
Migration: Plain text config files
```

---

## 5. GitLab CI/CD (Complete Pipeline)

### Android Build & Test (FREE)

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  FLUTTER_VERSION: "3.24.0"

# Unit Tests
test_flutter:
  stage: test
  image: ghcr.io/cirruslabs/flutter:${FLUTTER_VERSION}
  tags:
    - saas-linux-medium-amd64
  script:
    - flutter pub get
    - flutter test
    - flutter test integration_test/
  coverage: '/lines\.+\s+(\d+\.\d+\%)/'

# Android Build
build_android:
  stage: build
  image: ghcr.io/cirruslabs/flutter:${FLUTTER_VERSION}
  tags:
    - saas-linux-medium-amd64
  script:
    - flutter pub get
    - flutter build apk --debug
    - flutter build appbundle --release
  artifacts:
    paths:
      - build/app/outputs/
    expire_in: 1 week
  only:
    - main
    - develop

# Backend Tests
test_backend:
  stage: test
  image: python:3.11-slim
  script:
    - cd backend
    - pip install -r requirements.txt
    - pytest tests/ --cov=app --cov-report=term
  coverage: '/TOTAL.+\s+(\d+%)'/

# ML Model Tests
test_ml_models:
  stage: test
  image: python:3.11
  script:
    - cd ml
    - pip install -r requirements.txt
    - pytest tests/
```

### iOS Build & Test (FREE)
[web:53][web:56]

```yaml
# iOS Build
build_ios:
  stage: build
  image: macos-14-xcode-15
  tags:
    - saas-macos-medium-m1
  script:
    # Install Flutter
    - git clone https://github.com/flutter/flutter.git -b stable --depth 1
    - export PATH="$PATH:`pwd`/flutter/bin"
    - flutter --version
    - flutter pub get
    
    # Install pods
    - cd ios && pod install && cd ..
    
    # Run tests
    - flutter test
    
    # Build iOS
    - flutter build ios --release --no-codesign
  artifacts:
    paths:
      - build/ios/
    expire_in: 1 week
  only:
    - main
  when: manual  # Save CI minutes
```

---

## 6. Complete Feature Implementation

### Mapping 14 Features to Our Stack

Based on FEATURES_ROADMAP.md[web:46], here's how each feature works:

#### **Phase 1: MVP Features (Months 1-4)**

**Feature 1: AI Skin Analysis Engine**
```yaml
Frontend:
  - Flutter camera plugin
  - TFLite for on-device inference
  - OpenCV for preprocessing
  
Backend:
  - FastAPI /api/v1/analyze endpoint
  - PyTorch model inference
  - Returns JSON with detected concerns
  
ML:
  - U-Net for segmentation
  - ResNet50 for classification
  - Trained on CelebAMask-HQ + Fitzpatrick17k
  - Exported to ONNX → TFLite
  
Performance:
  - <3s analysis time (on-device)
  - 90%+ accuracy target
  - Works offline

✅ Zero cost, fully portable, runs on GitLab
```

**Feature 2: Skin Segmentation & Face Mapping**
```yaml
Implementation:
  - DeepLabV3+ model
  - 11 facial zones
  - Custom Flutter painter for visualization
  - Interactive touch zones
  
Migration:
  - Model: ONNX format (portable)
  - Code: Standard Flutter
  
✅ Supported
```

**Feature 3: Progress Tracking & Timeline**
```yaml
Storage:
  - SQLite (local): Photo metadata
  - PostgreSQL (cloud): Sync across devices
  - CloudFlare R2: Photo storage
  
Visualization:
  - fl_chart: Progress graphs
  - syncfusion_flutter_charts: Timeline
  
Algorithms:
  - SSIM/PSNR for image comparison
  - Trend analysis
  
✅ All portable technologies
```

**Feature 4: AI Routine Builder**
```yaml
Backend:
  - Rule-based recommendation engine
  - FastAPI endpoints
  - PostgreSQL: Routines storage
  
Frontend:
  - Step-by-step wizard
  - Morning/evening toggle
  
✅ Standard REST API
```

**Feature 5: Ingredient Database**
```yaml
Database:
  - PostgreSQL: 500+ ingredients
  - Full-text search
  - Redis: Cache popular searches
  
Migration:
  - SQL dump (completely portable)
  
✅ Industry-standard database
```

**Feature 6: Privacy & Compliance**
```yaml
Implementation:
  - On-device ML (TFLite)
  - AES-256 encryption
  - JWT authentication
  - GDPR data export API
  
✅ Built-in, no third-party services
```

**Feature 7: Open-Source ML Pipeline**
```yaml
Tools:
  - MLflow: Experiment tracking
  - DVC: Data versioning
  - Git: Code versioning
  - Docker: Reproducible environments
  
✅ All open-source, portable
```

#### **Phase 2: Enhanced Features (Months 5-8)**

**Features 8-11:**
- Lifestyle Tracking: PostgreSQL time-series
- Dermatologist Verification: WebSocket + Queue
- AR Try-On: ARCore/ARKit (free SDKs)
- Predictive AI: LSTM models

✅ All supported with current stack

#### **Phase 3: Advanced Features (Months 9-12)**

**Features 12-14:**
- Community: PostgreSQL + Redis
- Male Focus: Same ML pipeline
- B2B SDK: Flutter package + REST API

✅ All supported

---

## 7. Zero-Cost Deployment Architecture

### Complete Free Hosting Strategy

```
┌─────────────────────────────────────────┐
│   Mobile Apps (Flutter)                 │
│   iOS + Android                         │
│   Built on GitLab CI/CD (FREE)          │
└──────────────┬──────────────────────────┘
               │
               │ HTTPS
               ▼
┌──────────────────────────────────────────┐
│   Backend API (FastAPI)                  │
│   Hosting Options (pick one):            │
│   - Render.com (750 hrs/mo FREE)         │
│   - Railway.app ($5 credit/mo)           │
│   - Fly.io (3 VMs FREE)                  │
│   - Self-hosted Docker (FREE)            │
└──────────────┬───────────────────────────┘
               │
      ┌────────┼────────┐
      │        │        │
  ┌───▼───┐ ┌─▼──┐ ┌───▼────┐
  │Postgre│ │Mongo│ │ Redis  │
  │SQL    │ │DB   │ │        │
  │500 MB │ │512MB│ │10K/day │
  │FREE   │ │FREE │ │ FREE   │
  └───────┘ └────┘ └────────┘
```

### Migration Example

**Scenario: Move from Render to Railway**

```bash
# 1. Export database
pg_dump $RENDER_DATABASE_URL > backup.sql

# 2. Push Docker image to registry
docker build -t skincare-backend .
docker push ghcr.io/yourorg/skincare-backend

# 3. Deploy to Railway
# - Connect GitLab repo
# - Import backup.sql
# - Set environment variables
# - Deploy

# Total downtime: <5 minutes
```

---

## 8. Performance Benchmarks

### Target Performance (All Achievable)

| Metric | Target | How We Achieve It |
|--------|--------|-------------------|
| App Startup | <3s | Flutter native compile, minimal splash |
| Analysis Time | <5s | On-device TFLite inference |
| API Response | <200ms | FastAPI async, Redis caching |
| Database Query | <100ms | Indexed queries, connection pooling |
| Image Upload | <2s | Cloudflare R2 CDN, image compression |
| UI Frame Rate | 60fps | Flutter Skia engine |
| Memory Usage | <150MB | Efficient state management |

### Load Testing

```bash
# Test API with Apache Bench
ab -n 1000 -c 100 https://api.skincare.app/health

# Expected: 1000+ requests/second
```

---

## 9. Development Workflow

### Local Setup (5 minutes)

```bash
# 1. Clone repo
git clone git@gitlab.com:himprapatel-group/skincare-ai-app.git
cd skincare-ai-app

# 2. Install Flutter
flutter doctor
flutter pub get

# 3. Start backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 4. Run app
flutter run

# 5. Run tests
flutter test
pytest backend/tests/
```

### GitLab Workflow

```
Developer → Push to GitLab → CI Pipeline Runs →
  ├─ Flutter tests (Linux runner)
  ├─ Backend tests (Python)
  ├─ ML model tests
  ├─ Build Android APK
  ├─ Build iOS (manual)
  └─ Deploy to staging (auto)

Merge to main → Production deploy
```

---

## 10. Migration Checklist

### Moving Platforms? Easy!

**Data Export:**
```bash
# PostgreSQL
pg_dump > backup.sql

# MongoDB
mongodump --out /backup

# Redis
redis-cli SAVE
cp /var/lib/redis/dump.rdb /backup/

# Files (R2/S3)
aws s3 sync s3://old-bucket /backup
```

**Code Migration:**
- ✅ Flutter: Runs anywhere (no changes)
- ✅ FastAPI: Standard Docker container
- ✅ ML Models: ONNX format (universal)

**New Platform Setup:**
1. Deploy Docker image (10 min)
2. Import database dumps (5 min)
3. Update environment variables (2 min)
4. Test endpoints (5 min)

**Total migration time: ~30 minutes**

---

## 11. Cost Scaling Plan

| Users | Monthly Cost | What Changes |
|-------|--------------|
| 0-1K | **$0** | Everything on free tiers |
| 1K-5K | **$0** | Still within free limits |
| 5K-10K | **$0** | Max out free tiers |
| 10K-25K | **$32/mo** | Render $7, Supabase $25 |
| 25K-50K | **$82/mo** | + MongoDB $25, Redis $10, R2 $15 |
| 50K-100K | **$197/mo** | Scale databases, add CDN |

**Key Point:** First 10K users = $0/month!

---

## 12. Final Summary

### Stack Overview

```yaml
Frontend:
  Framework: Flutter 3.24+
  Language: Dart
  Platforms: iOS, Android
  Build: GitLab CI/CD (free)
  
Backend:
  Framework: FastAPI 0.110+
  Language: Python 3.11+
  Server: Uvicorn (ASGI)
  Deployment: Docker container
  Hosting: Render/Railway/Fly (free tiers)
  
Databases:
  Primary: PostgreSQL (Supabase 500MB free)
  Analytics: MongoDB Atlas (512MB free)
  Cache: Redis (Upstash 10K cmd/day free)
  
ML/AI:
  Training: PyTorch 2.2+
  Format: ONNX (portable)
  Mobile: TensorFlow Lite
  MLOps: MLflow + DVC (open-source)
  
Storage:
  Files: Cloudflare R2 (10GB free)
  Local: SQLite + Hive
  
CI/CD:
  Platform: GitLab (400 min/month free)
  Android: Linux runners
  iOS: macOS runners (beta)
  Testing: Automated on every push
```

### Why This Stack?

✅ **Zero Vendor Lock-in**
- Standard SQL, REST APIs, Docker
- Export/import in minutes
- ONNX models work anywhere

✅ **Free Forever**
- No trials, no credit cards needed
- Support 0-10K users at $0/month
- Scale gradually

✅ **GitLab Native**
- Build iOS & Android on GitLab
- Run all tests on GitLab
- Deploy from GitLab

✅ **Fast & Responsive**
- Native Flutter performance
- Async FastAPI backend
- Redis caching
- On-device ML inference

✅ **All Features Supported**
- Every one of our 14 features works
- No compromises
- Production-ready

### Next Steps

1. **Setup GitLab Repository** (Done ✓)
2. **Create Flutter Project**
   ```bash
   flutter create skincare_ai_app
   cd skincare_ai_app
   flutter pub add riverpod dio tflite_flutter
   ```

3. **Setup Backend**
   ```bash
   mkdir backend
   cd backend
   pip install fastapi uvicorn sqlalchemy
   # Create main.py
   ```

4. **Configure GitLab CI/CD**
   - Copy `.gitlab-ci.yml` from this document
   - Add CI/CD variables
   - Push to trigger first build

5. **Deploy Free Hosting**
   - Sign up for Supabase (PostgreSQL)
   - Sign up for MongoDB Atlas
   - Sign up for Render.com (backend)
   - Deploy!

---

## 13. Complete .gitlab-ci.yml

**Copy this file to your repository root:**

```yaml
# .gitlab-ci.yml
# Complete CI/CD pipeline for iOS & Android

stages:
  - test
  - build
  - deploy

variables:
  FLUTTER_VERSION: "3.24.0"
  PYTHON_VERSION: "3.11"

# Cache dependencies
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .pub-cache/
    - backend/.venv/

###################
# TEST STAGE
###################

test_flutter:
  stage: test
  image: ghcr.io/cirruslabs/flutter:${FLUTTER_VERSION}
  tags:
    - saas-linux-medium-amd64
  script:
    - flutter pub get
    - flutter analyze
    - flutter test --coverage
    - flutter test integration_test/
  coverage: '/lines\.+\s+(\d+\.\d+\%)'/
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura.xml

test_backend:
  stage: test
  image: python:${PYTHON_VERSION}-slim
  tags:
    - saas-linux-medium-amd64
  script:
    - cd backend
    - pip install -r requirements.txt
    - pytest tests/ --cov=app --cov-report=term --cov-report=xml
  coverage: '/TOTAL.+\s+(\d+%)'/
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: backend/coverage.xml

test_ml_models:
  stage: test
  image: python:${PYTHON_VERSION}
  tags:
    - saas-linux-medium-amd64
  script:
    - cd ml
    - pip install -r requirements.txt
    - pytest tests/
  only:
    - main
    - develop

###################
# BUILD STAGE
###################

build_android_debug:
  stage: build
  image: ghcr.io/cirruslabs/flutter:${FLUTTER_VERSION}
  tags:
    - saas-linux-medium-amd64
  script:
    - flutter pub get
    - flutter build apk --debug
  artifacts:
    paths:
      - build/app/outputs/apk/debug/app-debug.apk
    expire_in: 1 week
  only:
    - develop
    - merge_requests

build_android_release:
  stage: build
  image: ghcr.io/cirruslabs/flutter:${FLUTTER_VERSION}
  tags:
    - saas-linux-medium-amd64
  script:
    # Decode signing key
    - echo $ANDROID_KEYSTORE_BASE64 | base64 -d > android/app/upload-keystore.jks
    
    # Create key.properties
    - |
      cat > android/key.properties <<EOF
      storePassword=$KEYSTORE_PASSWORD
      keyPassword=$KEY_PASSWORD
      keyAlias=$KEY_ALIAS
      storeFile=upload-keystore.jks
      EOF
    
    # Build release
    - flutter pub get
    - flutter build appbundle --release
  artifacts:
    paths:
      - build/app/outputs/bundle/release/app-release.aab
    expire_in: 1 month
  only:
    - main
    - tags

build_ios:
  stage: build
  image: macos-14-xcode-15
  tags:
    - saas-macos-medium-m1
  script:
    # Install Flutter
    - git clone https://github.com/flutter/flutter.git -b stable --depth 1
    - export PATH="$PATH:`pwd`/flutter/bin"
    - flutter --version
    - flutter pub get
    
    # Install CocoaPods
    - cd ios
    - pod install
    - cd ..
    
    # Build iOS
    - flutter build ios --release --no-codesign
  artifacts:
    paths:
      - build/ios/iphoneos/
    expire_in: 1 week
  only:
    - main
  when: manual  # Manual trigger to save CI minutes

###################
# DEPLOY STAGE
###################

deploy_backend_staging:
  stage: deploy
  image: curlimages/curl:latest
  tags:
    - saas-linux-small-amd64
  script:
    - curl -X POST $RENDER_DEPLOY_HOOK_STAGING
  only:
    - develop
  when: manual

deploy_backend_production:
  stage: deploy
  image: curlimages/curl:latest
  tags:
    - saas-linux-small-amd64
  script:
    - curl -X POST $RENDER_DEPLOY_HOOK_PRODUCTION
  only:
    - main
  when: manual

deploy_android_internal:
  stage: deploy
  image: ruby:3.2-slim
  tags:
    - saas-linux-medium-amd64
  script:
    - gem install fastlane
    - cd android
    - fastlane deploy_internal
  dependencies:
    - build_android_release
  only:
    - tags
  when: manual
```

---

## 14. Environment Variables (GitLab CI/CD)

**Settings → CI/CD → Variables:**

```yaml
# Android Signing
ANDROID_KEYSTORE_BASE64: [base64 encoded keystore]
KEYSTORE_PASSWORD: [your keystore password]
KEY_PASSWORD: [your key password]
KEY_ALIAS: upload

# Backend Deployment
RENDER_DEPLOY_HOOK_STAGING: [Render webhook URL]
RENDER_DEPLOY_HOOK_PRODUCTION: [Render webhook URL]

# Databases
DATABASE_URL: postgresql://user:pass@host:5432/db
MONGODB_URL: mongodb+srv://user:pass@cluster.mongodb.net
REDIS_URL: redis://default:pass@host:6379

# API Keys (if needed)
OPENWEATHER_API_KEY: [for weather integration]
CLOUDFLARE_R2_ACCESS_KEY: [for file storage]
CLOUDFLARE_R2_SECRET_KEY: [for file storage]

# Play Store (for deployment)
PLAY_STORE_JSON_KEY: [service account JSON]
```

---

## 15. Dockerfile (Backend)

**backend/Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Conclusion

✅ **Free Forever:** $0/month for 0-10K users
✅ **No Lock-In:** Migrate platforms in 30 minutes
✅ **GitLab Native:** Build, test, deploy iOS & Android
✅ **All Features:** Complete support for 14 features
✅ **Fast:** <3s startup, 60fps, <5s analysis
✅ **Open Source:** Every technology is open-source
✅ **Production Ready:** Battle-tested stack

**Ready to start building! 🚀**

---

**Document Status:** ✅ Complete
**Next Action:** Begin Phase 1 development
**Est. Time to MVP:** 4 months

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        SKINCARE AI APP                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    MOBILE APP (Flutter)                  │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │   │
│  │  │ Camera  │  │Analysis │  │Routines │  │Progress │    │   │
│  │  │ Module  │  │ Screen  │  │ Builder │  │ Tracker │    │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘    │   │
│  │       └────────────┴────────────┴────────────┘         │   │
│  │                         │                               │   │
│  │              ┌──────────┴──────────┐                   │   │
│  │              │   State Management  │                   │   │
│  │              │   (Provider/Bloc)   │                   │   │
│  │              └──────────┬──────────┘                   │   │
│  └──────────────────────────┼──────────────────────────────┘   │
│                             │                                   │
│  ┌──────────────────────────┴──────────────────────────────┐   │
│  │                   ON-DEVICE ML (TFLite)                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │   │
│  │  │ Skin Type    │  │ Concern      │  │ Health       │   │   │
│  │  │ Classifier   │  │ Detector     │  │ Scorer       │   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                             │                                   │
│                       HTTPS/REST                                │
│                             │                                   │
│  ┌──────────────────────────┴──────────────────────────────┐   │
│  │                    BACKEND (FastAPI)                     │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │   │
│  │  │  Auth   │  │  User   │  │ Product │  │Analytics│    │   │
│  │  │ Service │  │ Service │  │ Service │  │ Service │    │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘    │   │
│  └───────┼────────────┼────────────┼────────────┼──────────┘   │
│          │            │            │            │               │
│  ┌───────┴────────────┴────────────┴────────────┴──────────┐   │
│  │                      DATA LAYER                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐               │   │
│  │  │PostgreSQL│  │ MongoDB  │  │  Redis   │               │   │
│  │  │ (Users)  │  │(Products)│  │ (Cache)  │               │   │
│  │  └──────────┘  └──────────┘  └──────────┘               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## API Endpoints Overview

### Authentication APIs
| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/auth/register | POST | User registration |
| /api/v1/auth/login | POST | User login |
| /api/v1/auth/refresh | POST | Refresh token |
| /api/v1/auth/logout | POST | User logout |

### Skin Analysis APIs
| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/analysis/scan | POST | Submit skin photo |
| /api/v1/analysis/{id} | GET | Get analysis results |
| /api/v1/analysis/history | GET | User analysis history |

### Routine APIs
| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/routines/generate | POST | Generate routine |
| /api/v1/routines/{id} | GET | Get routine details |
| /api/v1/routines/{id}/complete | POST | Mark step complete |

---

## Environment Configuration

### Development
```env
ENVIRONMENT=development
DEBUG=true
API_URL=http://localhost:8000
DB_HOST=localhost
REDIS_HOST=localhost
```

### Production
```env
ENVIRONMENT=production
DEBUG=false
API_URL=https://api.skincare-ai.app
DB_HOST=db.internal
REDIS_HOST=cache.internal
```

---

## Security Requirements

- All API calls over HTTPS
- JWT tokens with 15min expiry
- Refresh tokens with 7-day expiry
- Password hashing with bcrypt
- Rate limiting: 100 req/min per user
- CORS configured for app domains only
- Data encryption at rest (AES-256)
- GDPR/CCPA compliance built-in

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 25, 2025 | Initial technology stack |
| 2.0 | Nov 25, 2025 | Added architecture diagram, API overview, security |

---

*Document maintained by Skincare AI Development Team*