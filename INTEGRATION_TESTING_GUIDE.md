# Backend-Frontend Integration Testing Guide

## Overview
This document provides a comprehensive guide for integrating backend features with the Flutter mobile frontend and performing end-to-end testing.

## Architecture

### Backend Services (FastAPI)
- **Authentication Service**: User registration, login, token management
- **Skin Analysis Service**: AI-powered skin condition analysis
- **Ingredient Scanner**: Product ingredient scanning and analysis
- **Progress Tracking**: User progress and improvement metrics
- **Skincare Routine Builder**: Personalized routine creation and management
- **User Profile Management**: User data and preferences
- **Notification Management**: Push notifications and alerts
- **Dermatologist Consultation**: Appointment booking and consultation management

### Frontend (Flutter/Dart)
- Authentication screens
- Skin analysis interface
- Product ingredient scanner
- Progress dashboard
- Routine management
- User profile
- Notifications
- Consultation booking

## Integration Checklist

### 1. Authentication Integration
- [ ] Frontend implements login screen with email/password
- [ ] Frontend calls POST /api/v1/auth/login with credentials
- [ ] Backend returns JWT token and user data
- [ ] Frontend stores token securely in device storage
- [ ] Frontend implements token refresh mechanism
- [ ] Frontend implements logout functionality
- [ ] Test: Login with valid credentials → Success
- [ ] Test: Login with invalid credentials → Error handling

### 2. Skin Analysis Integration
- [ ] Frontend implements camera/image upload interface
- [ ] Frontend calls POST /api/v1/analysis/analyze with image data
- [ ] Backend processes image with ML model
- [ ] Frontend displays analysis results (condition, recommendations, severity)
- [ ] Frontend allows saving analysis history
- [ ] Test: Upload image → Receive analysis
- [ ] Test: View analysis history

### 3. Ingredient Scanner Integration
- [ ] Frontend implements ingredient input interface
- [ ] Frontend calls POST /api/v1/ingredients/scan with product data
- [ ] Backend returns ingredient analysis (safety, benefits, warnings)
- [ ] Frontend displays ingredient details and ratings
- [ ] Test: Scan ingredients → Display results
- [ ] Test: Save to favorites

### 4. Progress Tracking Integration
- [ ] Frontend calls GET /api/v1/progress/metrics to fetch user progress
- [ ] Frontend displays progress charts and statistics
- [ ] Frontend calls POST /api/v1/progress/update to record new data
- [ ] Backend stores progress data with timestamps
- [ ] Frontend allows filtering by date range
- [ ] Test: View progress metrics
- [ ] Test: Add new progress entry

### 5. Routine Management Integration
- [ ] Frontend calls GET /api/v1/routine/user/{user_id} to fetch routines
- [ ] Frontend calls POST /api/v1/routine/create to create new routine
- [ ] Backend generates personalized recommendations
- [ ] Frontend displays routine steps with timing
- [ ] Frontend sends reminders based on routine schedule
- [ ] Test: Create routine → Receive recommendations
- [ ] Test: Update routine → Sync with backend

### 6. User Profile Integration
- [ ] Frontend calls GET /api/v1/users/{user_id} to fetch profile
- [ ] Frontend calls PUT /api/v1/users/{user_id} to update profile
- [ ] Backend validates and stores profile data
- [ ] Frontend displays and allows editing of skin type, concerns, preferences
- [ ] Test: View profile → Display data
- [ ] Test: Update profile → Verify changes

### 7. Notifications Integration
- [ ] Frontend calls GET /api/v1/notifications to fetch notifications
- [ ] Frontend calls POST /api/v1/notifications/push for push notifications
- [ ] Frontend implements notification handling
- [ ] Backend sends routine reminders
- [ ] Backend sends tips and recommendations
- [ ] Test: Receive notification → Display alert

### 8. Dermatologist Consultation Integration
- [ ] Frontend calls GET /api/v1/dermatologist/available to fetch available slots
- [ ] Frontend calls POST /api/v1/dermatologist/book to book consultation
- [ ] Backend stores consultation data
- [ ] Frontend displays consultation history
- [ ] Test: Book consultation → Receive confirmation
- [ ] Test: View consultation history

## API Endpoints Summary

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Token refresh
- `POST /api/v1/auth/logout` - User logout

### Analysis
- `POST /api/v1/analysis/analyze` - Skin analysis
- `GET /api/v1/analysis/history` - Analysis history

### Ingredients
- `POST /api/v1/ingredients/scan` - Ingredient scanning
- `GET /api/v1/ingredients/details/{ingredient_id}` - Ingredient details

### Progress
- `GET /api/v1/progress/metrics` - User progress metrics
- `POST /api/v1/progress/update` - Update progress

### Routine
- `GET /api/v1/routine/user/{user_id}` - User routines
- `POST /api/v1/routine/create` - Create routine
- `PUT /api/v1/routine/{routine_id}` - Update routine

### Users
- `GET /api/v1/users/{user_id}` - Get user profile
- `PUT /api/v1/users/{user_id}` - Update profile

### Notifications
- `GET /api/v1/notifications` - Get notifications
- `POST /api/v1/notifications/push` - Send notification

### Dermatologist
- `GET /api/v1/dermatologist/available` - Available slots
- `POST /api/v1/dermatologist/book` - Book consultation

## End-to-End Testing Scenarios

### Scenario 1: New User Journey
1. User opens app
2. User registers account
3. User completes skin profile
4. User takes skin analysis photo
5. App displays analysis results
6. App generates recommended routine
7. User saves routine
8. User receives reminder notification

### Scenario 2: Existing User Journey
1. User logs in
2. User views previous analysis results
3. User scans product ingredients
4. User views progress metrics
5. User updates routine
6. User books dermatologist consultation

### Scenario 3: Data Synchronization
1. User makes changes offline
2. Changes are queued locally
3. User goes online
4. Changes sync with backend
5. Backend confirms sync
6. User receives updated data

## Testing Tools and Frameworks

### Backend Testing
- pytest for unit tests
- httpx for API testing
- Postman/Insomnia for manual testing
- GitHub Actions for CI/CD

### Frontend Testing
- Flutter test framework
- Integration tests with Patrol
- Mockito for mocking backend
- WidgetTest for UI testing

## Error Handling

### HTTP Status Codes
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication failed
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Backend error

### Frontend Error Handling
- Display user-friendly error messages
- Implement retry logic for failed requests
- Log errors for debugging
- Implement offline mode with queuing

## Security Considerations

- Use HTTPS for all API calls
- Store JWT tokens securely (secure storage)
- Implement token expiration and refresh
- Validate all user inputs
- Use API rate limiting
- Implement CORS properly
- Hash sensitive data
- Use environment variables for secrets

## Performance Optimization

- Implement caching for frequently accessed data
- Use pagination for large datasets
- Compress images before uploading
- Implement lazy loading in UI
- Monitor API response times
- Use CDN for static assets

## Deployment

### Staging Environment
- Test all integrations before production
- Verify database connections
- Test payment processing (if applicable)

### Production Environment
- Monitor API performance
- Set up error tracking (Sentry, etc.)
- Implement backup strategies
- Use environment-specific configs

## Next Steps

1. Create detailed test cases for each endpoint
2. Implement integration tests in CI/CD pipeline
3. Set up monitoring and logging
4. Perform load testing
5. Create user documentation
6. Plan deployment strategy