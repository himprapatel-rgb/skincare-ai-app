# Progress Tracking Algorithms Research

**File:** `/docs/research/10_progress_tracking_algorithms.md`
**Last Updated:** November 25, 2025
**Research Team:** CV, ML, Data Analytics Swarm

---

## Executive Summary

Progress tracking enables users to visualize skin improvement over time, a key feature for engagement and routine adherence. This document covers image alignment, comparison algorithms, metric calculation, and visualization strategies.

---

## 1. Core Requirements

| Requirement | Specification |
|-------------|---------------|
| Comparison Accuracy | >90% consistent measurement |
| Alignment | Automatic face/feature alignment |
| Metrics | Acne count, texture, tone, hydration appearance |
| Time Periods | Daily, Weekly, Monthly, Custom |
| Visualization | Side-by-side, overlay, graphs |

---

## 2. Image Alignment Pipeline

### 2.1 Alignment Challenges

| Challenge | Solution |
|-----------|----------|
| Head pose variation | 3D pose estimation + normalization |
| Lighting differences | Color/luminance normalization |
| Distance variation | Scale normalization using IPD |
| Expression changes | Neutral expression guidance |

### 2.2 Alignment Algorithm

```python
def align_progress_images(image_before, image_after):
    # Step 1: Detect landmarks
    landmarks_before = detect_landmarks(image_before)
    landmarks_after = detect_landmarks(image_after)
    
    # Step 2: Calculate alignment transform
    # Use eye centers + nose tip as anchor points
    anchor_points = ['left_eye', 'right_eye', 'nose_tip']
    
    transform = cv2.estimateAffinePartial2D(
        landmarks_after[anchor_points],
        landmarks_before[anchor_points]
    )
    
    # Step 3: Apply transform
    aligned_after = cv2.warpAffine(
        image_after, transform, 
        (image_before.shape[1], image_before.shape[0])
    )
    
    # Step 4: Color normalization
    aligned_after = match_histograms(aligned_after, image_before)
    
    return aligned_after
```

### 2.3 Lighting Normalization

```python
def normalize_lighting(image, reference):
    # Convert to LAB
    lab_img = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    lab_ref = cv2.cvtColor(reference, cv2.COLOR_BGR2LAB)
    
    # Match L channel statistics
    l_img, a_img, b_img = cv2.split(lab_img)
    l_ref, _, _ = cv2.split(lab_ref)
    
    # Standardize luminance
    l_normalized = (l_img - l_img.mean()) / l_img.std()
    l_normalized = l_normalized * l_ref.std() + l_ref.mean()
    l_normalized = np.clip(l_normalized, 0, 255).astype(np.uint8)
    
    # Merge back
    normalized = cv2.merge([l_normalized, a_img, b_img])
    return cv2.cvtColor(normalized, cv2.COLOR_LAB2BGR)
```

---

## 3. Progress Metrics

### 3.1 Acne Progress Tracking

```python
def track_acne_progress(analysis_history):
    metrics = {
        'lesion_count': [],
        'severity_score': [],
        'affected_area': [],
        'inflammation_level': []
    }
    
    for analysis in analysis_history:
        metrics['lesion_count'].append(analysis.acne.count)
        metrics['severity_score'].append(analysis.acne.severity)
        metrics['affected_area'].append(analysis.acne.area_percentage)
        metrics['inflammation_level'].append(analysis.acne.inflammation)
    
    # Calculate trends
    return {
        'current': metrics['lesion_count'][-1],
        'change_7d': calculate_change(metrics['lesion_count'], days=7),
        'change_30d': calculate_change(metrics['lesion_count'], days=30),
        'trend': calculate_trend(metrics['lesion_count']),
        'improvement_rate': calculate_improvement_rate(metrics)
    }
```

### 3.2 Skin Tone Evenness

```python
def measure_tone_evenness(skin_roi):
    # Convert to LAB
    lab = cv2.cvtColor(skin_roi, cv2.COLOR_BGR2LAB)
    L, a, b = cv2.split(lab)
    
    # Calculate uniformity metrics
    l_std = np.std(L)  # Lower = more even
    color_variance = np.std(a) + np.std(b)
    
    # Evenness score (0-100, higher = more even)
    evenness = 100 - min(100, (l_std * 2 + color_variance))
    
    return {
        'evenness_score': evenness,
        'luminance_variation': l_std,
        'color_variation': color_variance
    }
```

### 3.3 Texture Improvement

```python
def measure_texture_quality(skin_roi):
    gray = cv2.cvtColor(skin_roi, cv2.COLOR_BGR2GRAY)
    
    # GLCM texture features
    glcm = graycomatrix(gray, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4])
    
    smoothness = graycoprops(glcm, 'homogeneity').mean()
    roughness = graycoprops(glcm, 'contrast').mean()
    
    # Texture score (0-100)
    texture_score = smoothness * 100 - roughness * 10
    
    return {
        'texture_score': max(0, min(100, texture_score)),
        'smoothness': smoothness,
        'roughness': roughness
    }
```

### 3.4 Comprehensive Progress Score

```python
def calculate_overall_progress(before_analysis, after_analysis):
    weights = {
        'acne': 0.30,
        'pigmentation': 0.25,
        'texture': 0.20,
        'hydration': 0.15,
        'tone_evenness': 0.10
    }
    
    improvements = {}
    
    for metric, weight in weights.items():
        before_score = getattr(before_analysis, metric).score
        after_score = getattr(after_analysis, metric).score
        
        # Positive = improvement, Negative = worsening
        change = after_score - before_score
        improvements[metric] = {
            'change': change,
            'percent_change': (change / before_score) * 100 if before_score > 0 else 0,
            'weight': weight
        }
    
    # Weighted overall improvement
    overall = sum(
        imp['change'] * imp['weight'] 
        for imp in improvements.values()
    )
    
    return {
        'overall_improvement': overall,
        'detailed_improvements': improvements,
        'summary': 'improving' if overall > 0 else 'stable' if overall == 0 else 'needs_attention'
    }
```

---

## 4. Visualization Strategies

### 4.1 Side-by-Side Comparison

```python
def create_comparison_view(before, after, metrics):
    # Align images
    after_aligned = align_progress_images(before, after)
    
    # Create side-by-side
    comparison = np.hstack([before, after_aligned])
    
    # Add metrics overlay
    add_metrics_overlay(comparison, metrics)
    
    return comparison
```

### 4.2 Slider/Swipe Comparison

```
┌──────────────────────────────┐
│  BEFORE    │    AFTER       │
│            │                │
│     ←──────┴──────→         │
│         [SLIDER]             │
│                              │
└──────────────────────────────┘
```

### 4.3 Progress Timeline Graph

```python
def generate_progress_graph(history, metric='acne_count'):
    dates = [h.date for h in history]
    values = [getattr(h.analysis, metric) for h in history]
    
    plt.figure(figsize=(10, 4))
    plt.plot(dates, values, marker='o')
    plt.fill_between(dates, values, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(range(len(values)), values, 1)
    trend = np.poly1d(z)
    plt.plot(dates, trend(range(len(values))), '--', alpha=0.7)
    
    plt.xlabel('Date')
    plt.ylabel(metric.replace('_', ' ').title())
    plt.title('Your Skin Progress')
    
    return plt
```

---

## 5. Data Storage Schema

```sql
CREATE TABLE progress_records (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    captured_at TIMESTAMP NOT NULL,
    
    -- Scores (0-100)
    overall_score INTEGER,
    acne_score INTEGER,
    pigmentation_score INTEGER,
    texture_score INTEGER,
    hydration_score INTEGER,
    tone_evenness_score INTEGER,
    
    -- Detailed metrics (JSONB)
    detailed_metrics JSONB,
    
    -- Image reference (if stored)
    image_hash VARCHAR(64),
    
    -- Analysis metadata
    lighting_quality FLOAT,
    alignment_confidence FLOAT,
    
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 6. Best Practices for Consistent Tracking

### 6.1 User Guidance

| Factor | Guidance |
|--------|----------|
| Timing | Same time of day (morning preferred) |
| Lighting | Natural light, facing window |
| Distance | Arm's length, consistent |
| Expression | Neutral, relaxed |
| Preparation | Clean face, no makeup |

### 6.2 Quality Validation

```python
def validate_progress_photo(image):
    checks = {
        'face_detected': detect_face(image) is not None,
        'lighting_adequate': check_lighting(image) > 0.5,
        'blur_acceptable': check_blur(image) < 100,
        'face_centered': check_centering(image),
        'consistent_distance': check_distance(image)
    }
    
    passed = all(checks.values())
    
    return {
        'valid': passed,
        'checks': checks,
        'suggestions': generate_suggestions(checks)
    }
```

---

## 7. References

1. Sagonas et al. (2016). "Face Alignment: A Review"
2. Kazemi & Sullivan (2014). "One Millisecond Face Alignment"
3. Reinhard et al. (2001). "Color Transfer Between Images"

---

**Status:** ✅ Research Complete | 📈 Metrics Defined | 📷 Alignment Pipeline Ready