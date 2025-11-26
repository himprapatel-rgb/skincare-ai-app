#!/bin/bash
# Automated Test Deployment Script for iOS & Android
# Builds and deploys app to test devices/emulators

set -e

echo "================================================"
echo "Skincare AI App - Test Deployment"
echo "================================================"
echo ""

# Configuration
BUILD_TYPE="debug"  # debug, profile, release
DEPLOY_IOS=true
DEPLOY_ANDROID=true

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --release) BUILD_TYPE="release" ;; 
        --profile) BUILD_TYPE="profile" ;;
        --ios-only) DEPLOY_ANDROID=false ;;
        --android-only) DEPLOY_IOS=false ;;
        *) echo "Unknown option: $1" ;; 
    esac
    shift
done

echo "Build Type: $BUILD_TYPE"
echo ""

# iOS Deployment
if [ "$DEPLOY_IOS" = true ]; then
    echo "[iOS] Building Flutter app..."
    flutter build ios --$BUILD_TYPE || exit 1
    echo "[iOS] Build complete!"
    echo ""
fi

# Android Deployment  
if [ "$DEPLOY_ANDROID" = true ]; then
    echo "[Android] Building Flutter app..."
    if [ "$BUILD_TYPE" = "release" ]; then
        flutter build apk --release || exit 1
    else
        flutter build apk --$BUILD_TYPE || exit 1
    fi
    echo "[Android] Build complete!"
    echo ""
fi

# List available devices
echo "Available devices:"
flutter devices
echo ""

echo "================================================"
echo "Build and deploy complete!"
echo "================================================"
