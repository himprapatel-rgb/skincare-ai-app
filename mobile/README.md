# Skincare AI App - Mobile Frontend

## Overview

Flutter-based mobile application for iOS and Android platforms for skincare analysis and personalized recommendations.

## Features

- **Camera Integration**: Capture skin images for analysis
- **Image Upload**: Upload existing skin photos
- **AI Analysis**: Real-time skin condition detection
- **Recommendations**: Personalized skincare product suggestions
- **History**: Track skin analysis history
- **Offline Support**: Core functionality works offline

## Quick Start

### Prerequisites

- Flutter 3.13+
- Dart 3.0+
- iOS 12.0+ (for iPhone)
- Android API 21+ (for Android phones)

### Setup

```bash
# Install dependencies
flutter pub get

# Run app
flutter run
```

### Development

```bash
# Run tests
flutter test

# Build debug APK
flutter build apk --debug

# Build release APK
flutter build apk --release

# Build iOS
flutter build ios
```

## Project Structure

```
lib/
├── main.dart              # Entry point
├── screens/               # UI screens
├── widgets/               # Reusable widgets
├── models/                # Data models
├── services/              # API & business logic
├── providers/             # State management
└── utils/                 # Utilities

test/
├── widget_test.dart       # Widget tests
└── unit_test/             # Unit tests
```

## Architecture

- **State Management**: Provider pattern
- **API Client**: Dio with Retrofit
- **Local Storage**: SQLite + Hive
- **Navigation**: Named routing

## Testing

```bash
# Run all tests
flutter test

# Run with coverage
flutter test --coverage
```

## Deployment

### iOS
```bash
flutter build ios --release
```

### Android
```bash
flutter build appbundle --release
```

## Documentation

See parent project README for full documentation.

## Status

**Current Version**: 0.1.0 (Beta)  
**Last Updated**: 2025-11-26  
**Status**: Active Development
