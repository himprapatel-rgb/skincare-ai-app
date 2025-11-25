# AI Skin-Care App

An advanced AI-powered skin analysis and personalized skincare recommendation application.

## Overview

This application uses computer vision and machine learning to analyze skin conditions, detect issues like acne, pigmentation, and wrinkles, and provide personalized skincare recommendations.

## Features

- Real-time skin analysis via camera
- Acne detection and severity classification
- Dark circles and pigmentation analysis
- Wrinkle depth mapping
- Skin-type classification (oily, dry, combination, sensitive)
- Personalized skincare routine builder
- Product recommendations based on skin analysis
- Progress tracking over time

## Project Structure

```
/backend          - FastAPI backend server
/mobile           - React Native mobile application
/ml               - Machine learning models and training
/docs             - Documentation
/infrastructure   - DevOps and deployment configs
```

## Tech Stack

- **Mobile**: React Native, TypeScript
- **Backend**: Python, FastAPI, PostgreSQL, Redis
- **ML/AI**: PyTorch, TensorFlow, OpenCV
- **DevOps**: Docker, Kubernetes, GitLab CI/CD

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose

### Quick Start

1. Clone the repository
2. Run `docker-compose up` for local development
3. Access the API at http://localhost:8000

## License

MIT License

## Contributing

Please read our contributing guidelines before submitting PRs.