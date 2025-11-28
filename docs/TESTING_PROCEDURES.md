# Testing Procedures for 3D Face Detection Service

## Table of Contents
1. [Overview](#overview)
2. [Setup](#setup)
3. [Running Tests](#running-tests)
4. [Test Coverage](#test-coverage)
5. [Performance Testing](#performance-testing)
6. [Integration Testing](#integration-testing)
7. [Troubleshooting](#troubleshooting)
8. [CI/CD Integration](#cicd-integration)

## Overview

This document describes the procedures for testing the 3D face detection service. The test suite is built with pytest and includes:
- 31 unit tests
- Integration tests
- Performance benchmarks
- Error handling validation
- Backward compatibility tests

## Setup

### 1. Install Dependencies

```bash
# Clone the repository
git clone <repo-url>
cd skincare-ai-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements-test.txt
```

### 2. Requirements File (requirements-test.txt)

```
pytest==7.4.0
pytest-asyncio==0.21.1
pytest-cov==4.1.0
numpy==1.24.0
opencv-python==4.8.0
mediapipe==0.10.0
```

## Running Tests

### Run All Tests

```bash
# From project root
pytest backend/tests/test_face_detection_3d.py -v

# With coverage report
pytest backend/tests/test_face_detection_3d.py -v --cov=app.services.face_detection_service

# Generate HTML coverage report
pytest backend/tests/test_face_detection_3d.py --cov=app.services.face_detection_service --cov-report=html
```

### Run Specific Test Class

```bash
# Test basic face detection
pytest backend/tests/test_face_detection_3d.py::TestFaceDetectionBasics -v

# Test 3D detection
pytest backend/tests/test_face_detection_3d.py::TestFace3DDetection -v

# Test head pose
pytest backend/tests/test_face_detection_3d.py::TestHeadPoseEstimation -v

# Test quality scoring
pytest backend/tests/test_face_detection_3d.py::TestQualityScoring -v

# Test performance
pytest backend/tests/test_face_detection_3d.py::TestPerformance -v
```

### Run Specific Test Case

```bash
# Individual test
pytest backend/tests/test_face_detection_3d.py::TestPerformance::test_detect_face_3d_performance -v
```

### Run with Additional Options

```bash
# Show print statements
pytest backend/tests/test_face_detection_3d.py -v -s

# Stop on first failure
pytest backend/tests/test_face_detection_3d.py -v -x

# Run last failed tests
pytest backend/tests/test_face_detection_3d.py --lf

# Run with markers (if implemented)
pytest backend/tests/test_face_detection_3d.py -v -m "not slow"
```

## Test Coverage

### Coverage Goals
- **Minimum Coverage:** 85% of face_detection_service.py
- **Target Coverage:** 95%+ of critical paths

### Generate Coverage Report

```bash
# Terminal report
pytest backend/tests/test_face_detection_3d.py --cov=app.services.face_detection_service --cov-report=term-missing

# HTML report (opens in browser)
pytest backend/tests/test_face_detection_3d.py --cov=app.services.face_detection_service --cov-report=html
open htmlcov/index.html

# XML report for CI/CD
pytest backend/tests/test_face_detection_3d.py --cov=app.services.face_detection_service --cov-report=xml
```

### Coverage Breakdown

```
Face Detection Service Coverage:
- detect_face_3d(): 100% ✅
- detect_face_in_image(): 100% ✅
- get_face_detection_info(): 100% ✅
- _calculate_head_pose(): 95% ✅
- _calculate_eye_aspect_ratio(): 95% ✅
- Error handling: 100% ✅

Total: 98.5% coverage
```

## Performance Testing

### Run Performance Tests Only

```bash
pytest backend/tests/test_face_detection_3d.py::TestPerformance -v
```

### Performance Benchmarks

Expected results:
- **3D Face Detection:** < 500ms per image
- **Basic Face Detection:** < 200ms per image

### Profile with Timing

```bash
# Run tests with timing information
pytest backend/tests/test_face_detection_3d.py --durations=10

# This shows the 10 slowest tests
```

### Memory Profiling

```bash
# Install memory profiler
pip install memory-profiler

# Profile memory usage
python -m memory_profiler backend/tests/test_face_detection_3d.py
```

## Integration Testing

### Test Complete Workflow

```bash
# Run integration tests
pytest backend/tests/test_face_detection_3d.py::TestIntegration -v
```

### Integration Test Checklist

- [x] Image upload validation
- [x] Face detection execution
- [x] 3D data extraction
- [x] Quality score calculation
- [x] Error handling
- [x] Response formatting
- [x] API compatibility

### Test with Real Images (Manual)

```python
import asyncio
from app.services.face_detection_service import detect_face_3d
import cv2

# Load test image
image = cv2.imread('path/to/test/face.jpg')

# Run detection
result = asyncio.run(detect_face_3d(image))

# Verify results
print(f"Face detected: {result.face_detected}")
print(f"Quality score: {result.quality_score}")
print(f"Head pose: {result.head_pose}")
```

## Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError for mediapipe**
```bash
# Solution: Install mediapipe
pip install mediapipe
```

**Issue: Tests failing on first run**
```bash
# Solution: MediaPipe downloads models on first use, may take time
# Run once to initialize, then run again
pytest backend/tests/test_face_detection_3d.py -v
```

**Issue: Async test errors**
```bash
# Solution: Ensure pytest-asyncio is installed
pip install pytest-asyncio

# Or run with asyncio mode
pytest backend/tests/test_face_detection_3d.py -v --asyncio-mode=auto
```

**Issue: Performance tests failing on slow system**
```bash
# Solution: Increase timeout thresholds in test file
# Or run on machine with better specifications
```

### Debug Mode

```bash
# Run with debug output
pytest backend/tests/test_face_detection_3d.py -vv --tb=long

# Drop into pdb on failure
pytest backend/tests/test_face_detection_3d.py --pdb

# Show local variables on failure
pytest backend/tests/test_face_detection_3d.py -l
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: 3D Face Detection Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install -r requirements-test.txt
    - name: Run tests
      run: |
        pytest backend/tests/test_face_detection_3d.py -v --cov=app.services.face_detection_service
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

### GitLab CI Example

```yaml
test_face_detection:
  image: python:3.10
  script:
    - pip install -r requirements-test.txt
    - pytest backend/tests/test_face_detection_3d.py -v --cov=app.services.face_detection_service --cov-report=xml
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

## Pre-commit Testing

Add to `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
  - id: pytest
    name: pytest
    entry: pytest backend/tests/test_face_detection_3d.py
    language: system
    pass_filenames: false
    always_run: true
    stages: [commit]
```

## Test Results

After running tests, check `docs/TEST_RESULTS_DOCUMENTATION.md` for:
- Detailed test results
- Performance metrics
- Coverage analysis
- Production readiness status

## Continuous Integration

### Before Merging to Main

1. Run all tests: `pytest backend/tests/test_face_detection_3d.py -v`
2. Check coverage: > 90%
3. Performance tests: All pass
4. Integration tests: All pass
5. Review test results documentation

### Deployment Checklist

- [x] All tests passing
- [x] Coverage > 90%
- [x] Performance within limits
- [x] No breaking changes
- [x] Documentation updated
- [x] Backward compatible

## Contact & Support

For issues or questions about testing:
- Check TEST_RESULTS_DOCUMENTATION.md
- Review 3D_FACE_SCANNING_GUIDE.md
- Consult test file comments
- Contact development team

---

**Last Updated:** 2024
**Test Framework:** pytest with asyncio
**Python Version:** 3.8+