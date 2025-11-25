# Software Requirements Specification (SRS)
# Skincare AI App - Industry-Standard Development Requirements

**Document:** `/docs/SOFTWARE_REQUIREMENTS_SPECIFICATION.md`  
**Version:** 1.0  
**Last Updated:** November 25, 2025  
**Status:** Active Development  
**Technology Stack:** Flutter + FastAPI + PyTorch/TFLite + PostgreSQL/MongoDB/Redis

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0 | Nov 25, 2025 | AI Engineering Team | Initial SRS document |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Overview](#2-system-overview)
3. [Functional Requirements](#3-functional-requirements)
4. [Non-Functional Requirements](#4-non-functional-requirements)
5. [System Architecture](#5-system-architecture)
6. [Data Requirements](#6-data-requirements)
7. [API Specifications](#7-api-specifications)
8. [ML/AI Model Requirements](#8-mlai-model-requirements)
9. [Security Requirements](#9-security-requirements)
10. [Testing Requirements](#10-testing-requirements)
11. [Deployment Requirements](#11-deployment-requirements)
12. [Quality Assurance](#12-quality-assurance)

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) document provides a complete description of the Skincare AI App requirements for development. Based on comprehensive research of 20+ competitor apps and 11 technical research documents, this specification defines:

- Functional and non-functional requirements
- System architecture and component interactions
- API contracts and data models
- ML/AI model specifications
- Testing and quality assurance criteria
- Deployment and operational requirements

### 1.2 Scope
The Skincare AI App is a mobile-first application providing:

**Core Capabilities:**
- AI-powered skin analysis using computer vision
- Personalized skincare routine recommendations
- Progress tracking with before/after comparison
- Ingredient analysis and product recommendations
- Integration with board-certified dermatologists
- Privacy-first on-device processing

**Target Users:**
- Primary: Women aged 18-45 with smartphones
- Secondary: Men interested in skincare
- Tertiary: Dermatology patients seeking digital tools

### 1.3 Definitions and Acronyms

| Term | Definition |
|------|------------|
| SRS | Software Requirements Specification |
| API | Application Programming Interface |
| ML | Machine Learning |
| CV | Computer Vision |
| IGA | Investigator's Global Assessment |
| WCAG | Web Content Accessibility Guidelines |
| GDPR | General Data Protection Regulation |
| TFLite | TensorFlow Lite |
| ONNX | Open Neural Network Exchange |

### 1.4 References
- `/docs/FEATURES_ROADMAP.md` - Feature specifications
- `/docs/TECHNOLOGY_STACK.md` - Technology decisions
- `/docs/UI_UX_DESIGN.md` - Design requirements
- `/docs/UI_WIREFRAMES.md` - Interface specifications
- `/docs/research/` - Technical research documents
- `/docs/cv-ml/` - Computer vision research
- `/docs/data/` - Data requirements
- `/docs/compliance/` - Privacy and compliance

---

## 2. System Overview

### 2.1 System Context

```
┌─────────────────────────────────────────────────────────────┐
│                     Skincare AI App                          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Flutter    │  │   FastAPI    │  │  PyTorch/    │     │
│  │   Frontend   │◄─┤   Backend    │◄─┤  TFLite ML   │     │
│  │   (Mobile)   │  │    (API)     │  │   Models     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            │                                 │
│                   ┌────────┴────────┐                       │
│                   │   Databases:    │                       │
│                   │  - PostgreSQL   │                       │
│                   │  - MongoDB      │                       │
│                   │  - Redis Cache  │                       │
│                   └─────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 System Features (High-Level)

| Feature Category | Priority | Complexity |
|-----------------|----------|------------|
| Skin Analysis | P0 | High |
| Progress Tracking | P0 | Medium |
| Routine Builder | P0 | High |
| Ingredient Scanner | P1 | Medium |
| Product Recommendations | P1 | Medium |
| Dermatologist Connection | P1 | High |
| User Profile & Settings | P0 | Low |
| Notifications & Alerts | P2 | Low |

### 2.3 User Classes and Characteristics

| User Class | Technical Expertise | Primary Goals |
|------------|-------------------|---------------|
| End Users | Low-Medium | Improve skin health, track progress |
| Dermatologists | Medium | Monitor patients, provide consultations |
| Administrators | High | System management, analytics |
| Developers | High | System maintenance, feature development |

---
## 3. Functional Requirements

### 3.1 User Authentication & Onboarding

#### FR-3.1.1: User Registration
**Priority:** P0  
**Description:** Users must be able to create an account using email, phone, or social authentication.

**Requirements:**
- Support email/password registration
- Support Google OAuth 2.0 integration
- Support Apple Sign-In (iOS requirement)
- Validate email format and password strength (min 8 chars, 1 uppercase, 1 number, 1 special)
- Send email verification link
- Store user data with encryption at rest

**Acceptance Criteria:**
```gherkin
Given a new user opens the app
When they enter valid email and strong password
Then account is created
And verification email is sent
And user is redirected to onboarding flow
```

**API Endpoint:**
```python
POST /api/v1/auth/register
Request Body:
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-15",
  "gender": "male"
}

Response 201:
{
  "user_id": "uuid-123",
  "email": "user@example.com",
  "verification_required": true,
  "message": "Verification email sent"
}
```

#### FR-3.1.2: User Login
**Priority:** P0  
**Description:** Registered users must be able to log in securely.

**Requirements:**
- Support email/password authentication
- Support biometric authentication (Face ID/Touch ID)
- Implement JWT token-based authentication
- Token expiry: 7 days for access token, 30 days for refresh token
- Rate limiting: Max 5 failed attempts per 15 minutes
- Account lockout after 10 failed attempts

**API Endpoint:**
```python
POST /api/v1/auth/login
Request Body:
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

Response 200:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "uuid-123",
    "email": "user@example.com",
    "first_name": "John",
    "profile_complete": true
  },
  "expires_in": 604800
}
```

#### FR-3.1.3: Onboarding Questionnaire
**Priority:** P0  
**Description:** New users complete a skin profile questionnaire.

**Requirements:**
- Collect skin type (oily, dry, combination, normal, sensitive)
- Collect primary skin concerns (acne, wrinkles, dark spots, etc.)
- Collect current skincare routine (Y/N and products)
- Collect allergies and sensitivities
- Collect lifestyle factors (diet, sleep, sun exposure)
- Save profile data to PostgreSQL
- Calculate initial skin score baseline

**Data Model:**
```python
class SkinProfile(BaseModel):
    user_id: UUID
    skin_type: SkinType  # Enum
    fitzpatrick_scale: int  # 1-6
    primary_concerns: List[SkinConcern]  # Enum list
    allergies: List[str]
    current_routine: Dict[str, List[str]]
    lifestyle_factors: LifestyleFactors
    created_at: datetime
    updated_at: datetime
```

---

### 3.2 Skin Analysis Feature

#### FR-3.2.1: Camera-Based Skin Analysis
**Priority:** P0  
**Description:** Users capture facial photos for AI-powered skin analysis.

**Requirements:**
- Camera access permission request with clear explanation
- Real-time face detection and alignment guidance
- Lighting condition checks (warn if too dark/bright)
- Multiple angle capture: front, left profile, right profile
- Image quality validation (min resolution: 1280x720)
- On-device preprocessing before API upload
- Compress images to <2MB for upload
- Store images encrypted in cloud storage

**Image Processing Pipeline:**
```python
# Flutter (Client-Side)
1. Capture image from camera
2. Detect face using MediaPipe
3. Validate image quality (brightness, sharpness, resolution)
4. Crop and align face
5. Compress to JPEG (quality=85)
6. Encrypt image data
7. Upload to backend

# FastAPI Backend
1. Decrypt and validate image
2. Run through ML pipeline:
   - Skin segmentation
   - Feature extraction
   - Concern detection (acne, wrinkles, etc.)
   - Severity classification
3. Store analysis results in PostgreSQL
4. Return results to client
```

**API Endpoint:**
```python
POST /api/v1/analysis/skin
Content-Type: multipart/form-data

Request:
- image: File (JPEG/PNG, max 2MB)
- angle: str ("front", "left", "right")
- lighting_score: float (0-1)
- user_id: UUID

Response 200:
{
  "analysis_id": "uuid-456",
  "detected_concerns": [
    {
      "type": "acne",
      "severity": "moderate",
      "confidence": 0.92,
      "affected_areas": ["forehead", "cheeks"],
      "lesion_count": 12
    },
    {
      "type": "wrinkles",
      "severity": "mild",
      "confidence": 0.87,
      "affected_areas": ["forehead", "eyes"],
      "depth_score": 0.34
    }
  ],
  "skin_metrics": {
    "hydration_level": 0.68,
    "oiliness": 0.45,
    "pore_visibility": 0.52,
    "texture_uniformity": 0.71,
    "pigmentation_uniformity": 0.79
  },
  "overall_score": 72,
  "recommendations": [
    "Use salicylic acid for acne",
    "Consider retinol for wrinkles",
    "Increase moisturizer usage"
  ],
  "processing_time_ms": 1850
}
```

#### FR-3.2.2: Concern Detection Models
**Priority:** P0  
**Description:** Detect and classify multiple skin concerns simultaneously.

**Supported Concerns:**

| Concern | Detection Method | Model | Accuracy Target |
|---------|-----------------|-------|----------------|
| Acne | YOLOv8 object detection | Mobile-optimized | >92% |
| Wrinkles | Depth estimation + segmentation | U-Net based | >88% |
| Dark Spots | Semantic segmentation | DeepLabV3+ | >90% |
| Pores | Texture analysis | Custom CNN | >85% |
| Redness | Color analysis + segmentation | ResNet50 | >87% |
| Dark Circles | Region detection + severity | EfficientNet-B0 | >89% |
| Skin Type | Multi-class classification | MobileNetV3 | >91% |

**Model Configuration:**
```yaml
# /ml/models/config/skin_analysis.yaml
skin_analysis_pipeline:
  version: "2.0"
  
  preprocessing:
    input_size: [640, 640]
    normalization: "imagenet"
    augmentation: false  # Only during training
    
  models:
    - name: "acne_detector"
      architecture: "yolov8n"
      weights: "models/acne_yolov8n.tflite"
      quantization: "int8"
      target_latency_ms: 80
      
    - name: "wrinkle_analyzer"
      architecture: "unet_mobilenet"
      weights: "models/wrinkle_unet.tflite"
      quantization: "int8"
      target_latency_ms: 100
      
    - name: "pigmentation_detector"
      architecture: "deeplabv3plus"
      weights: "models/pigmentation_deeplab.tflite"
      quantization: "int8"
      target_latency_ms: 120
      
  postprocessing:
    confidence_threshold: 0.75
    nms_iou_threshold: 0.45
    max_detections: 100
```

---
### 3.3 Progress Tracking Feature

#### FR-3.3.1: Before/After Photo Comparison
**Priority:** P0  
**Description:** Users track skin improvement over time with photo comparisons.

**Requirements:**
- Store all analysis photos with timestamps
- Automatic facial alignment for accurate comparison
- Generate side-by-side comparison views
- Calculate improvement metrics per concern
- Timeline view showing progress over weeks/months
- Export progress reports as PDF

**API Endpoint:**
```python
POST /api/v1/progress/compare
Request Body:
{
  "user_id": "uuid-123",
  "before_analysis_id": "uuid-456",
  "after_analysis_id": "uuid-789",
  "concerns_to_compare": ["acne", "wrinkles"]
}

Response 200:
{
  "comparison_id": "uuid-comp-123",
  "time_period_days": 30,
  "improvements": [
    {
      "concern": "acne",
      "before_severity": "moderate",
      "after_severity": "mild",
      "improvement_percentage": 35.2,
      "lesion_count_change": -7
    },
    {
      "concern": "wrinkles",
      "before_severity": "mild",
      "after_severity": "mild",
      "improvement_percentage": 8.5,
      "depth_change": -0.04
    }
  ],
  "overall_improvement": 21.85,
  "heatmap_url": "https://storage.../heatmap_comp123.png"
}
```

#### FR-3.3.2: Progress Timeline & Analytics
**Priority:** P1  
**Description:** Visualize skin health journey with charts and analytics.

**Requirements:**
- Line charts showing score progression
- Bar charts for concern-specific improvements
- Heatmaps showing improved/worsened areas
- Milestone achievements ("30 days streak", "50% improvement")
- Weekly/monthly summary reports
- Share progress on social media (optional, privacy-controlled)

**Data Model:**
```python
class ProgressEntry(BaseModel):
    id: UUID
    user_id: UUID
    analysis_id: UUID
    overall_score: float  # 0-100
    concern_scores: Dict[str, float]
    timestamp: datetime
    notes: Optional[str]
    routine_adherence: float  # 0-1
```

---

### 3.4 AI Routine Builder Feature

#### FR-3.4.1: Personalized Routine Generation
**Priority:** P0  
**Description:** AI generates customized skincare routines based on analysis.

**Requirements:**
- Generate AM and PM routines
- Consider detected skin concerns
- Factor in user's skin type and allergies
- Recommend product types (not specific brands initially)
- Include application order and frequency
- Provide explanations for each recommendation
- Update routine based on progress analysis

**Routine Generation Algorithm:**
```python
class RoutineBuilder:
    """
    AI-powered skincare routine builder.
    
    Algorithm:
    1. Analyze skin profile (concerns, type, sensitivities)
    2. Prioritize concerns by severity
    3. Select active ingredients for top 3 concerns
    4. Check for ingredient conflicts
    5. Optimize application order (cleanse → treat → moisturize → protect)
    6. Generate AM/PM sequences
    7. Add usage frequency and warnings
    """
    
    def generate_routine(
        self,
        skin_profile: SkinProfile,
        analysis_results: AnalysisResult,
        budget_tier: str = "mid"  # low, mid, high
    ) -> SkincareRoutine:
        
        # Step 1: Identify top concerns
        concerns = self._prioritize_concerns(analysis_results)
        
        # Step 2: Select active ingredients
        ingredients = self._select_ingredients(concerns, skin_profile)
        
        # Step 3: Check conflicts
        validated_ingredients = self._check_conflicts(ingredients)
        
        # Step 4: Build routine steps
        am_routine = self._build_am_routine(validated_ingredients)
        pm_routine = self._build_pm_routine(validated_ingredients)
        
        return SkincareRoutine(
            user_id=skin_profile.user_id,
            am_steps=am_routine,
            pm_steps=pm_routine,
            key_ingredients=validated_ingredients,
            rationale=self._generate_rationale(concerns, ingredients)
        )
```

**API Endpoint:**
```python
POST /api/v1/routine/generate
Request Body:
{
  "user_id": "uuid-123",
  "analysis_id": "uuid-456",
  "budget_tier": "mid",
  "preferences": {
    "prefer_natural": false,
    "fragrance_free": true,
    "cruelty_free": true
  }
}

Response 200:
{
  "routine_id": "uuid-routine-123",
  "am_routine": [
    {
      "step": 1,
      "action": "Cleanse",
      "product_type": "Gentle Foaming Cleanser",
      "key_ingredients": ["salicylic acid"],
      "instructions": "Apply to damp face, massage for 60s, rinse",
      "frequency": "daily"
    },
    {
      "step": 2,
      "action": "Treat",
      "product_type": "Vitamin C Serum",
      "key_ingredients": ["L-ascorbic acid 10%"],
      "instructions": "Apply 3-4 drops to face and neck",
      "frequency": "daily",
      "wait_time_minutes": 2
    },
    {
      "step": 3,
      "action": "Moisturize",
      "product_type": "Lightweight Gel Moisturizer",
      "key_ingredients": ["hyaluronic acid", "niacinamide"],
      "instructions": "Apply thin layer to entire face",
      "frequency": "daily"
    },
    {
      "step": 4,
      "action": "Protect",
      "product_type": "Broad Spectrum SPF 50",
      "key_ingredients": ["zinc oxide", "titanium dioxide"],
      "instructions": "Apply generous amount, reapply every 2 hours",
      "frequency": "daily",
      "critical": true
    }
  ],
  "pm_routine": [
    {
      "step": 1,
      "action": "Double Cleanse",
      "product_type": "Oil Cleanser + Foaming Cleanser",
      "instructions": "Remove makeup with oil, follow with foam cleanser",
      "frequency": "daily"
    },
    {
      "step": 2,
      "action": "Treat",
      "product_type": "Retinol Serum 0.3%",
      "key_ingredients": ["retinol"],
      "instructions": "Start 2x/week, gradually increase to nightly",
      "frequency": "2-3x weekly (start)",
      "warnings": ["May cause irritation", "Use sunscreen next day"]
    },
    {
      "step": 3,
      "action": "Moisturize",
      "product_type": "Rich Night Cream",
      "key_ingredients": ["ceramides", "peptides"],
      "instructions": "Apply to face and neck",
      "frequency": "daily"
    }
  ],
  "rationale": {
    "acne": "Salicylic acid helps unclog pores and reduce breakouts",
    "wrinkles": "Retinol and peptides stimulate collagen production",
    "dark_spots": "Vitamin C inhibits melanin production"
  },
  "estimated_results_weeks": 8
}
```

#### FR-3.4.2: Routine Tracking & Adherence
**Priority:** P1  
**Description:** Users log daily routine completion and receive reminders.

**Requirements:**
- Morning and evening reminder notifications
- Check-off interface for each routine step
- Track adherence percentage over time
- Correlate adherence with skin improvement
- Gamification: streaks, badges, achievements

---

### 3.5 Ingredient Scanner Feature

#### FR-3.5.1: Barcode & OCR Scanning
**Priority:** P1  
**Description:** Scan product barcodes or ingredient lists for analysis.

**Requirements:**
- Barcode scanning (UPC, EAN codes)
- OCR for ingredient list text extraction
- Match ingredients against database (MongoDB)
- Flag harmful/allergenic ingredients for user
- Provide ingredient safety ratings
- Show evidence-based benefits and concerns

**API Endpoint:**
```python
POST /api/v1/ingredients/scan
Content-Type: multipart/form-data

Request:
- image: File (product label photo)
- scan_type: str ("barcode" or "ocr")
- user_id: UUID

Response 200:
{
  "product": {
    "name": "XYZ Moisturizing Cream",
    "brand": "SkinCare Co",
    "category": "moisturizer",
    "barcode": "012345678901"
  },
  "ingredients": [
    {
      "name": "Hyaluronic Acid",
      "safety_rating": 1,  # 1=best, 10=worst
      "function": "Humectant, hydrating agent",
      "concerns": [],
      "benefits": ["Deeply hydrates", "Plumps skin"],
      "evidence_level": "strong"
    },
    {
      "name": "Fragrance",
      "safety_rating": 7,
      "function": "Masking",
      "concerns": ["Potential irritant", "Allergen"],
      "user_flagged": true  # User has fragrance sensitivity
    }
  ],
  "compatibility": {
    "user_profile_match": 0.72,
    "skin_type_suitable": true,
    "allergy_warnings": ["Contains fragrance - you marked as sensitive"],
    "recommendation": "consider_alternatives"
  }
}
```

---
## 4. Non-Functional Requirements

### 4.1 Performance Requirements

#### NFR-4.1.1: Response Time
**Priority:** P0  
**Requirements:**
- API response time: <200ms for 95th percentile
- Skin analysis processing: <3 seconds end-to-end
- On-device ML inference: <150ms per model
- Database queries: <50ms average
- Image upload: Support 3G networks (>100kb/s)

#### NFR-4.1.2: Scalability
**Priority:** P0  
**Requirements:**
- Support 100,000 concurrent users
- Handle 1M API requests per day
- Process 500K images per day
- Auto-scaling based on load (K8s HPA)
- Database read replicas for high availability

#### NFR-4.1.3: Availability
**Priority:** P0  
**Requirements:**
- System uptime: 99.9% (8.76 hours downtime/year max)
- Planned maintenance windows: <4 hours/month
- Disaster recovery: RPO <15 minutes, RTO <1 hour
- Multi-region deployment (US-East, EU-West, Asia-Pacific)

### 4.2 Security Requirements

#### NFR-4.2.1: Authentication & Authorization
**Priority:** P0  
**Requirements:**
- OAuth 2.0 / OpenID Connect implementation
- JWT tokens with RS256 signing
- Role-Based Access Control (RBAC)
- Multi-factor authentication (MFA) for sensitive operations
- Session timeout: 7 days idle, 30 days absolute

#### NFR-4.2.2: Data Encryption
**Priority:** P0  
**Requirements:**
- TLS 1.3 for all API communications
- AES-256 encryption at rest for all user data
- Image storage with client-side encryption
- Database encryption (PostgreSQL pgcrypto, MongoDB encryption-at-rest)
- Secure key management (AWS KMS / HashiCorp Vault)

#### NFR-4.2.3: Privacy & Compliance
**Priority:** P0  
**Requirements:**
- GDPR compliance (EU users)
- CCPA compliance (California users)
- HIPAA considerations (not full compliance initially)
- Data retention: 7 years for analysis history
- Right to be forgotten: Complete data deletion within 30 days
- Consent management for data processing

### 4.3 Usability Requirements

#### NFR-4.3.1: Accessibility
**Priority:** P1  
**Requirements:**
- WCAG 2.1 Level AA compliance
- Screen reader support (iOS VoiceOver, Android TalkBack)
- Minimum touch target size: 44x44pt
- Color contrast ratio: ≥4.5:1 for text
- Font scaling support up to 200%
- Keyboard navigation support

#### NFR-4.3.2: Internationalization
**Priority:** P2  
**Requirements:**
- Initial languages: English, Spanish, French, German, Japanese
- RTL language support (Arabic, Hebrew)
- Currency localization
- Date/time format localization
- Measurement units (metric/imperial)

### 4.4 Maintainability Requirements

#### NFR-4.4.1: Code Quality
**Priority:** P0  
**Requirements:**
- Code coverage: >80% for backend, >70% for frontend
- Static analysis: Pass SonarQube quality gates
- Linting: Enforce with pre-commit hooks
- Documentation: All public APIs must have docstrings/comments
- Type hints: 100% for Python backend

#### NFR-4.4.2: Logging & Monitoring
**Priority:** P0  
**Requirements:**
- Centralized logging (ELK Stack / Datadog)
- Distributed tracing (Jaeger / OpenTelemetry)
- Application Performance Monitoring (APM)
- Error tracking (Sentry)
- Custom metrics dashboards (Grafana)
- Alerting rules for critical failures

---

## 5. System Architecture

### 5.1 Architecture Overview

**Architecture Pattern:** Microservices with API Gateway

```
┌────────────────────── PRESENTATION LAYER ──────────────────────┐
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │   Flutter   │  │   Flutter   │  │     Web     │           │
│  │  Mobile iOS │  │ Mobile Andrd│  │   Dashboard │           │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘           │
│         │                 │                 │                   │
└─────────┼─────────────────┼─────────────────┼───────────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
┌───────────────────── API GATEWAY LAYER ────────────────────────┐
│                            │                                    │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │         Kong API Gateway / AWS API Gateway               │ │
│  │  - Rate Limiting  - Authentication  - Load Balancing     │ │
│  └───────────────────────┬──────────────────────────────────┘ │
└──────────────────────────┼─────────────────────────────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
┌───────── SERVICE LAYER ──┴──────────────┴───────────────────────┐
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Auth Service│  │  Analysis    │  │   Routine    │         │
│  │  (FastAPI)   │  │  Service     │  │   Service    │         │
│  │  Port: 8001  │  │  (FastAPI)   │  │  (FastAPI)   │         │
│  └──────────────┘  │  Port: 8002  │  │  Port: 8003  │         │
│                    └──────────────┘  └──────────────┘         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Ingredient  │  │  Progress    │  │  Notification│         │
│  │  Service     │  │  Service     │  │  Service     │         │
│  │  (FastAPI)   │  │  (FastAPI)   │  │  (FastAPI)   │         │
│  │  Port: 8004  │  │  Port: 8005  │  │  Port: 8006  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───────────────────────────────────────────────────────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
┌────────── ML LAYER ──────┴──────────────┴───────────────────────┐
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Skin        │  │   Concern    │  │  Ingredient  │         │
│  │  Segmentation│  │   Detection  │  │    OCR       │         │
│  │  Model       │  │   Models     │  │   Model      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───────────────────────────────────────────────────────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
┌────────── DATA LAYER ────┴──────────────┴───────────────────────┐
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  PostgreSQL  │  │   MongoDB    │  │    Redis     │         │
│  │  (Relational)│  │  (Documents) │  │   (Cache)    │         │
│  │  User/Auth   │  │  Ingredients │  │  Sessions    │         │
│  │  Analysis    │  │  Products    │  │  Rate Limit  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │   AWS S3 /   │  │   Message    │                            │
│  │   MinIO      │  │   Queue      │                            │
│  │  (Storage)   │  │  (RabbitMQ)  │                            │
│  └──────────────┘  └──────────────┘                            │
└───────────────────────────────────────────────────────────────┘
```

### 5.2 Technology Stack Details

**Frontend:**
```yaml
framework: Flutter 3.x
language: Dart 3.x
state_management: Riverpod
navigation: go_router
http_client: dio
local_storage: hive + secure_storage
camera: camera + image_picker
ml_integration: tflite_flutter
charts: fl_chart
analytics: firebase_analytics
```

**Backend API:**
```yaml
framework: FastAPI 0.110+
language: Python 3.11+
async_runtime: asyncio + uvicorn
database_orm: SQLAlchemy 2.0 (async)
mongodb_driver: motor (async)
caching: aioredis
auth: python-jose (JWT)
validation: pydantic v2
testing: pytest + pytest-asyncio
api_docs: OpenAPI 3.1 (auto-generated)
```

**ML/AI Stack:**
```yaml
training_framework: PyTorch 2.0+
model_conversion: ONNX → TensorFlow Lite
mobile_inference: TFLite / Core ML
computer_vision: OpenCV, Pillow
face_detection: MediaPipe
model_serving: TorchServe / TFServing
experiment_tracking: MLflow / Weights & Biases
```

**Databases:**
```yaml
primary_db:
  type: PostgreSQL 15+
  orm: SQLAlchemy (async)
  migrations: Alembic
  connection_pool: asyncpg
  
document_db:
  type: MongoDB 6.0+
  driver: motor (async)
  use_cases: ingredients, products, content
  
cache:
  type: Redis 7.0+
  driver: aioredis
  use_cases: sessions, rate_limiting, API cache
```

**Infrastructure:**
```yaml
containerization: Docker + Docker Compose
orchestration: Kubernetes (EKS / GKE)
ci_cd: GitLab CI / GitHub Actions
monitoring: Prometheus + Grafana
logging: ELK Stack (Elasticsearch, Logstash, Kibana)
error_tracking: Sentry
cdn: CloudFlare
storage: AWS S3 / MinIO
message_queue: RabbitMQ / AWS SQS
```

---