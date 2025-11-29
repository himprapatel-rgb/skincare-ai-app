# AI Skin-Care App

[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/himprapatel-rgb/skincare-ai-app/pages/pages-build-deployment?label=Pages%20Deploy)](https://github.com/himprapatel-rgb/skincare-ai-app/actions)
[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-brightgreen)](https://himprapatel-rgb.github.io/skincare-ai-app/)

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
- Web (GitHub Pages deployment)

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

### Machine Learning / AI
- **Frameworks**: PyTorch, TensorFlow
- **Computer Vision**: OpenCV, MediaPipe
- **Models**: Custom CNN for skin analysis
- **Face Detection**: MediaPipe Face Mesh (3D)

### DevOps & Infrastructure
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Hosting**: GitHub Pages (Frontend)

---

## Getting Started

### Prerequisites
- Python 3.11+
- Flutter SDK 3.x
- Docker & Docker Compose
- Git

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/himprapatel-rgb/skincare-ai-app.git
cd skincare-ai-app
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

3. **Mobile App Setup**
```bash
cd mobile
flutter pub get
flutter run
```

---

## Live Demo

🌐 **Web App**: [https://himprapatel-rgb.github.io/skincare-ai-app/](https://himprapatel-rgb.github.io/skincare-ai-app/)

---

## Project Status

| Component | Status | Progress |
|-----------|--------|----------|
| Backend API | ✅ Complete | 100% |
| Mobile App | ✅ Complete | 100% |
| ML Models | ✅ Complete | 100% |
| Documentation | ✅ Complete | 100% |
| CI/CD Pipeline | ✅ Active | 100% |
| GitHub Pages | ✅ Live | 100% |

---

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](docs/CONTRIBUTING.md) before submitting PRs.

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Contact

**Project Maintainer**: Himanshu Prakashbhai Patel
**GitHub**: [@himprapatel-rgb](https://github.com/himprapatel-rgb)

---

*Built with ❤️ using Flutter, FastAPI, and AI*
*Now hosted on GitHub with unlimited free CI/CD!*
