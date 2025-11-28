# AI Skin-Care App

[![Pipeline Status](https://gitlab.com/himprapatel-group/skincare-ai-app/badges/main/pipeline.svg)](https://gitlab.com/himprapatel-group/skincare-ai-app/-/pipelines)
[![GitLab Pages](https://img.shields.io/badge/GitLab-Pages-orange)](https://himprapatel-project-20fc64.gitlab.io/)

An advanced AI-powered skin analysis and personalized skincare recommendation application built with Flutter, FastAPI, and machine learning.

## Overview

This application uses computer vision and machine learning to analyze skin conditions, detect issues like acne, pigmentation, and wrinkles, and provide personalized skincare recommendations. The app supports iOS, Android, and Web platforms.

## Key Features

### Skin Analysis
- Real-time skin analysis via camera
- Acne detection and severity classification
- Dark circles and pigmentation analysis
- Wrinkle depth mapping
- Skin-type classification (oily, dry, combination, sensitive)
- Pore analysis and detection

### Personalization
- Personalized skincare routine builder
- Product recommendations based on skin analysis
- Progress tracking over time
- Custom treatment plans

### Platform Support
- iOS (App Store ready)
- Android (Google Play ready)
- Web (GitLab Pages deployment)

---

## Repository Structure

```
skincare-ai-app/
├── backend/                    # FastAPI Backend Server
│   ├── app/                    # Main application code
│   ├── tests/                  # Backend test suite
│   ├── Dockerfile              # Docker containerization
│   ├── requirements.txt        # Python dependencies
│   ├── BACKEND_README.md       # Backend documentation
│   ├── COMPLETE_IMPLEMENTATION_GUIDE.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── WORKING_DOCUMENT.md
│   └── .env.example            # Environment variables template
│
├── mobile/                     # Flutter Mobile Application
│   ├── lib/                    # Dart source code
│   ├── web/                    # Web platform files
│   ├── integration_test/       # E2E integration tests
│   ├── scripts/                # Build & deployment scripts
│   ├── pubspec.yaml            # Flutter dependencies
│   ├── README.md               # Mobile app documentation
│   └── SETUP_IOS_ANDROID.md    # iOS/Android setup guide
│
├── ml/                         # Machine Learning Models
│   ├── models/                 # Trained ML models
│   │   ├── FaceDetector        # Face detection model
│   │   └── SkinSegmenter       # Skin segmentation model
│   └── requirements.txt        # ML dependencies
│
├── docs/                       # Project Documentation
│   ├── Technical doc/          # Technical documentation
│   ├── ai-systems/             # AI system documentation
│   ├── compliance/             # Compliance & regulations
│   ├── cv-ml/                  # Computer vision & ML docs
│   ├── data/                   # Data documentation
│   ├── research/               # Research materials
│   ├── skin research/          # Skin analysis research
│   ├── BACKEND_CODE_SAMPLES.md
│   ├── ARCHITECTURE_DIAGRAM.md
│   ├── BACKEND_IMPLEMENTATION_GUIDE.md
│   ├── CHANGELOG.md
│   ├── CODE_REVIEW_CHECKLIST.md
│   ├── CONTRIBUTING.md
│   ├── DEVELOPMENT_WORKFLOW.md
│   ├── ENVIRONMENT_SETUP_SUMMARY.md
│   ├── ENVIRONMENT_TEST_RESULTS.md
│   ├── FEATURES_ROADMAP.md
│   ├── MOBILE_ARCHITECTURE.md
│   ├── NON_NEGOTIABLE_RULES.md
│   ├── SOFTWARE_REQUIREMENTS_SPECIFICATION.md
│   ├── TECHNOLOGY_STACK.md
│   ├── TESTING_DEPLOYMENT.md
│   ├── UI_UX_DESIGN.md
│   └── UI_WIREFRAMES.md
│
├── infrastructure/             # DevOps & Deployment
│   └── (Kubernetes, Docker configs)
│
├── .gitlab-ci.yml              # GitLab CI/CD Pipeline
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
│
├── # Project Management Files
├── DEPLOYMENT_VERIFICATION_REPORT.md
├── FINAL_DEPLOYMENT_APPROVAL.md
├── GITLAB_CICD_EXECUTION_REPORT.md
├── INTEGRATION_TESTING_GUIDE.md
├── PROGRESS_TRACKER.md
└── PROJECT_COMPLETION_SUMMARY.md
```

---

## Tech Stack

### Frontend (Mobile)
- **Framework**: Flutter 3.x
- **Language**: Dart
- **State Management**: Provider/Riverpod
- **Platforms**: iOS, Android, Web

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Authentication**: JWT, OAuth2
- **API Documentation**: OpenAPI/Swagger

### Machine Learning / AI
- **Frameworks**: PyTorch, TensorFlow
- **Computer Vision**: OpenCV
- **Models**: Custom CNN for skin analysis
- **Face Detection**: MTCNN/MediaPipe

### DevOps & Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitLab CI/CD
- **Hosting**: GitLab Pages (Frontend), Cloud (Backend)
- **Monitoring**: Firebase Analytics

---

## Getting Started

### Prerequisites

- Python 3.11+
- Flutter SDK 3.x
- Node.js 20+
- Docker & Docker Compose
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://gitlab.com/himprapatel-group/skincare-ai-app.git
   cd skincare-ai-app
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   uvicorn app.main:app --reload
   ```

3. **Mobile App Setup**
   ```bash
   cd mobile
   flutter pub get
   flutter run
   ```

4. **Docker Setup (Full Stack)**
   ```bash
   docker-compose up
   ```

5. **Access the Application**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Web App: http://localhost:3000

---

## CI/CD Pipeline

The project uses GitLab CI/CD with the following stages:

| Stage | Job | Description |
|-------|-----|-------------|
| Build | `build_web` | Flutter web build |
| Build | `build_backend` | Docker backend build |
| Build | `test_backend` | Backend tests |
| Deploy | `pages` | Deploy to GitLab Pages |

---

## Documentation

Comprehensive documentation is available in the `/docs` directory:

- **[Architecture Diagram](docs/ARCHITECTURE_DIAGRAM.md)** - System architecture overview
- **[Technology Stack](docs/TECHNOLOGY_STACK.md)** - Complete tech stack details
- **[UI/UX Design](docs/UI_UX_DESIGN.md)** - Design guidelines and wireframes
- **[Development Workflow](docs/DEVELOPMENT_WORKFLOW.md)** - Development processes
- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute
- **[Features Roadmap](docs/FEATURES_ROADMAP.md)** - Planned features

---

## Project Status

| Component | Status | Progress |
|-----------|--------|----------|
| Backend API | ✅ Complete | 100% |
| Mobile App | ✅ Complete | 100% |
| ML Models | ✅ Complete | 100% |
| Documentation | ✅ Complete | 100% |
| CI/CD Pipeline | ✅ Active | 100% |
| iOS Deployment | ✅ Ready | 100% |
| Android Deployment | ✅ Ready | 100% |

---

## Live Demo

🌐 **Web App**: [https://himprapatel-project-20fc64.gitlab.io/](https://himprapatel-project-20fc64.gitlab.io/)

---

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](docs/CONTRIBUTING.md) before submitting PRs.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Merge Request

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Contact

**Project Maintainer**: Himanshu Prakashbhai Patel

**GitLab**: [@himprapatel](https://gitlab.com/himprapatel)

---

*Built with ❤️ using Flutter, FastAPI, and AI*