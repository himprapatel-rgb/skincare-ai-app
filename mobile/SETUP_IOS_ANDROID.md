# iOS & Android Test Environment Setup

## Quick Start - Complete Setup in 5 Minutes

**Status:** Production Ready  
**Last Updated:** 2025-11-26  
**Authority:** Mobile Development Team

---

## Prerequisites Checklist

### All Platforms
- [ ] Flutter 3.13+ installed
- [ ] Git configured
- [ ] 10GB free disk space minimum
- [ ] Xcode 14+ (macOS only, for iOS)
- [ ] Android Studio 2022+ (for Android)

### iOS Requirements
- [ ] macOS 12.0+
- [ ] Xcode Command Line Tools
- [ ] CocoaPods installed: `sudo gem install cocoapods`
- [ ] iOS 12.0+ deployment target

### Android Requirements
- [ ] Android SDK API 21+ (recommended API 33+)
- [ ] Android NDK for native code
- [ ] Java 11+ (OpenJDK or Oracle JDK)
- [ ] ANDROID_HOME environment variable set

---

## One-Command Setup

### macOS/Linux
```bash
#!/bin/bash
cd mobile
chmod +x setup.sh
./setup.sh
```

### Windows
```cmd
cd mobile
setup.bat
```

---

## Manual Setup Guide

### Step 1: Install Flutter (All Platforms)

```bash
# macOS/Linux
git clone https://github.com/flutter/flutter.git -b stable
export PATH="$PATH:`pwd`/flutter/bin"
flutter doctor

# Windows
git clone https://github.com/flutter/flutter.git -b stable
Set PATH=%PATH%;%cd%\flutter\bin
flutter doctor
```

### Step 2: iOS Setup (macOS Only)

```bash
# Install dependencies
sudo gem install cocoapods

# Navigate to iOS project
cd mobile/ios

# Install pods
pod install

# Update deployment target to iOS 12.0
cd ..
flutter pub get

# Verify iOS setup
flutter doctor -v
```

### Step 3: Android Setup (All Platforms)

```bash
# Set environment variables
export ANDROID_HOME=$HOME/Library/Android/sdk  # macOS
export ANDROID_HOME=/opt/android-sdk           # Linux
set ANDROID_HOME=C:\Android\sdk                 # Windows

# Add to PATH
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools

# Accept Android licenses
flutter config --android-sdk $ANDROID_HOME
flutter doctor --android-licenses

# Verify setup
flutter doctor -v
```

---

## Running Tests Locally

### iOS Simulator

```bash
# List available iOS simulators
flutter emulators

# Launch iOS simulator
open -a Simulator

# OR use Flutter command
flutter emulators --launch apple_ios_simulator

# Run app on iOS
cd mobile
flutter run
```

### Android Emulator

```bash
# List available Android emulators
flutter emulators

# Launch Android emulator (create one first if needed)
flutter emulators --launch Pixel_5_API_33

# Run app on Android
cd mobile
flutter run
```

### Physical Devices

#### iOS Physical Device
```bash
# Connect iPhone via USB
# Trust the device when prompted
flutter devices  # Verify connection
flutter run -d <device-id>
```

#### Android Physical Device
```bash
# Enable USB debugging on device
# Connect via USB
flutter devices  # Verify connection
flutter run -d <device-id>
```

---

## Running Tests

### Unit Tests
```bash
cd mobile
flutter test
```

### Widget Tests (UI Tests)
```bash
flutter test test/widget_test.dart
```

### Integration Tests
```bash
flutter test integration_test/
```

### Run All Tests with Coverage
```bash
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
```

---

## Build for Testing

### iOS Test Build

```bash
# Debug build (fastest)
flutter build ios --debug

# Profile build (optimized)
flutter build ios --profile

# Release build (production)
flutter build ios --release
```

### Android Test Build

```bash
# Debug APK
flutter build apk --debug

# Profile APK
flutter build apk --profile

# Release APK
flutter build apk --release

# AAB (Google Play)
flutter build appbundle --release
```

---

## Deployment to Test Devices

### Automated Deployment Script

See `deploy_test.sh` for automated deployment.

### Manual Deployment

#### iOS
```bash
# Use Xcode
open ios/Runner.xcworkspace

# OR command line
flutter run -d <ios-device-id>
```

#### Android
```bash
# Direct installation
flutter install -d <android-device-id>

# OR via adb
adb install build/app/outputs/apk/debug/app-debug.apk
```

---

## Troubleshooting

### iOS Issues

**Pod install fails:**
```bash
cd ios
rm Podfile.lock
pod install --repo-update
cd ..
```

**Code signing errors:**
- Open `ios/Runner.xcworkspace` in Xcode
- Go to Build Settings
- Fix signing team and provisioning profile

**iOS Simulator won't start:**
```bash
killall "iOS Simulator"
open -a Simulator
```

### Android Issues

**Gradle build fails:**
```bash
cd android
./gradlew clean build
cd ..
```

**ADB not found:**
```bash
export PATH=$PATH:$ANDROID_HOME/platform-tools
adb devices
```

**Emulator won't start:**
```bash
flutter emulators
flutter emulators --launch <emulator-name>
```

---

## CI/CD Integration

### GitHub Actions Example

See `.github/workflows/test.yml` for automated testing pipeline.

### Local Testing Before Push

```bash
# Run all tests
flutter test

# Build both platforms
flutter build ios --debug
flutter build apk --debug

# Then commit
git add .
git commit -m "feat: add feature X"
git push
```

---

## Performance Benchmarking

```bash
# Run performance tests
flutter run --profile

# Monitor frame rates
flutter run --profile --trace-startup
```

---

## Device-Specific Configurations

### iOS Configuration

**File:** `ios/Podfile`
```ruby
post_install do |installer|
  installer.pods_project.targets.each do |target|
    flutter_additional_ios_build_settings(target)
    target.build_configurations.each do |config|
      config.build_settings['GCC_PREPROCESSOR_DEFINITIONS'] ||= [
        '$(inherited)',
        'FLUTTER_ROOT=\"#{flutter_root}\"',
      ]
    end
  end
end
```

### Android Configuration

**File:** `android/app/build.gradle`
```gradle
android {
    compileSdkVersion 33
    
    defaultConfig {
        applicationId "com.skincareai.app"
        minSdkVersion 21
        targetSdkVersion 33
        versionCode 1
        versionName "0.1.0"
    }
}
```

---

## Testing Checklist

- [ ] Flutter doctor shows no issues
- [ ] iOS simulator/device runs app
- [ ] Android emulator/device runs app
- [ ] All unit tests pass
- [ ] All widget tests pass
- [ ] Integration tests pass
- [ ] App builds for iOS release
- [ ] App builds for Android release
- [ ] App launches without crashes
- [ ] UI renders correctly
- [ ] Camera integration works (physical devices)
- [ ] Image upload/processing works
- [ ] API calls succeed
- [ ] Database operations work
- [ ] Performance acceptable (60 FPS)

---

## Next Steps

1. Complete all prerequisites
2. Run one-command setup
3. Launch emulator/simulator
4. Run `flutter run`
5. Test all features
6. Build release versions
7. Deploy to test devices
8. Begin development

---

## Support & Documentation

- Flutter Docs: https://flutter.dev/docs
- iOS Development: https://developer.apple.com/ios
- Android Development: https://developer.android.com
- Project Docs: See `/docs` folder

---

**Status:** Ready for Testing & Development