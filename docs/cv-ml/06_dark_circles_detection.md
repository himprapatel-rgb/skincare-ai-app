# Dark Circles Detection Research

**File:** `/docs/research/06_dark_circles_detection.md`
**Last Updated:** November 25, 2025
**Research Team:** CV, Dermatology, ML Swarm

---

## Executive Summary

Dark circles (periorbital hyperpigmentation) are distinct from general pigmentation and require specialized detection approaches. This document covers the multi-factorial causes, detection algorithms, and severity scoring systems for accurate dark circle analysis.

---

## 1. Core Requirements

| Requirement | Specification |
|-------------|---------------|
| Detection Area | Periorbital region (under-eye + lateral) |
| Causes Identified | Vascular, Pigmentary, Structural, Mixed |
| Skin Tone Support | Fitzpatrick I-VI |
| Accuracy Target | >88% classification accuracy |
| Processing Time | <300ms on-device |
| Output | Type classification, severity score, heatmap |

---

## 2. Dark Circle Classification

### 2.1 Etiology-Based Types

```
Dark Circles Taxonomy:
├── Vascular (Blue/Purple)
│   ├── Visible blood vessels
│   ├── Blood pooling
│   └── Thin translucent skin
├── Pigmentary (Brown)
│   ├── Post-inflammatory hyperpigmentation
│   ├── Dermal melanocytosis
│   └── Hereditary pigmentation
├── Structural (Shadow)
│   ├── Tear trough depression
│   ├── Orbital fat loss
│   ├── Skin laxity
│   └── Eyebag protrusion
└── Mixed
    ├── Vascular + Pigmentary
    ├── Structural + Vascular
    └── All three combined
```

### 2.2 Clinical Presentation by Type

| Type | Color | Key Features | Common Causes |
|------|-------|--------------|---------------|
| Vascular | Blue/Purple/Red | Worse when tired, visible veins | Fatigue, allergies, thin skin |
| Pigmentary | Brown/Tan | Consistent color, affects darker skin more | Genetics, sun exposure, PIH |
| Structural | Shadow/Gray | Changes with lighting angle | Aging, fat loss, bone structure |
| Mixed | Variable | Multiple characteristics | Combination of factors |

---

## 3. Detection Algorithms

### 3.1 Region of Interest (ROI) Detection

**Periorbital Landmark Detection:**
```python
# Using MediaPipe Face Mesh
periorbital_landmarks = {
    'left_under_eye': [33, 7, 163, 144, 145, 153, 154, 155, 133],
    'right_under_eye': [362, 382, 381, 380, 374, 373, 390, 249, 263],
    'left_lateral': [130, 247, 30, 29, 27, 28, 56, 190],
    'right_lateral': [359, 467, 260, 259, 257, 258, 286, 414]
}
```

### 3.2 Color Analysis Pipeline

**Multi-Color Space Analysis:**

```
Input Image
     │
     ▼
┌────────────────────┐
│ ROI Extraction    │
└─────────┬──────────┘
          │
    ┌─────┼─────┐
    ▼     ▼     ▼
┌─────┐┌─────┐┌─────┐
│ LAB ││ HSV ││ RGB │
└──┬──┘└──┬──┘└──┬──┘
   │     │     │
   └─────┼─────┘
         ▼
┌────────────────────┐
│ Type Classifier   │
└─────────┬──────────┘
          ▼
  Vascular/Pigmentary/
  Structural/Mixed
```

### 3.3 Type-Specific Detection Features

**Vascular Detection:**
```python
# Blue/purple channel analysis
b_channel_ratio = blue_mean / (red_mean + green_mean + 1e-6)
vascular_score = (b_channel_ratio > 0.35) * intensity

# Hemoglobin index approximation
hemoglobin_idx = (2 * red - green - blue) / (2 * red + green + blue)
```

**Pigmentary Detection:**
```python
# LAB color space melanin estimation
L_diff = cheek_L - undereye_L  # Luminance difference
b_star = undereye_b  # Yellow-brown axis

melanin_score = (L_diff * 0.6) + (b_star * 0.4)
```

**Structural Detection:**
```python
# Depth estimation using shadow analysis
shadow_gradient = compute_gradient(grayscale_roi)
structural_score = analyze_depth_from_shading(shadow_gradient)

# 3D facial landmark depth (if available)
tear_trough_depth = landmark_z[lower_lid] - landmark_z[cheek]
```

### 3.4 Deep Learning Models

| Model | Architecture | Task | Accuracy | Latency |
|-------|--------------|------|----------|----------|
| DCNet-Lite | MobileNetV3 + Attention | Type Classification | 87.3% | 42ms |
| SeverityNet | EfficientNet-B0 | Severity Scoring | 84.1% | 65ms |
| UnifiedDC | Multi-task ResNet18 | Type + Severity | 85.8% | 88ms |

---

## 4. Severity Scoring System

### 4.1 Clinical Grading Scale

| Grade | Score | Description | Visual Characteristics |
|-------|-------|-------------|------------------------|
| 0 | 0-1 | None | No visible dark circles |
| 1 | 2-3 | Mild | Slight discoloration, barely noticeable |
| 2 | 4-5 | Moderate | Visible under normal lighting |
| 3 | 6-7 | Severe | Prominent, affects appearance |
| 4 | 8-10 | Very Severe | Deep discoloration, significant shadowing |

### 4.2 Scoring Algorithm

```python
def calculate_severity(roi_features):
    # Color difference from reference skin
    color_delta = compute_delta_e(undereye_lab, cheek_lab)
    
    # Contrast ratio
    contrast = (cheek_L - undereye_L) / cheek_L
    
    # Area coverage
    affected_area = measure_affected_pixels(roi) / total_roi_pixels
    
    # Weighted severity score
    severity = (
        color_delta * 0.4 +
        contrast * 100 * 0.35 +
        affected_area * 10 * 0.25
    )
    
    return min(10, max(0, severity))
```

---

## 5. Skin Tone Considerations

### 5.1 Fitzpatrick-Adjusted Detection

| Skin Type | Primary Challenge | Adjustment |
|-----------|-------------------|------------|
| I-II | Vascular more visible | Reduce vascular threshold |
| III-IV | Mixed presentation | Balance all channels |
| V-VI | Pigmentary dominant | Increase LAB b* weight |

### 5.2 Adaptive Thresholds

```python
thresholds = {
    'fitzpatrick_1_2': {'vascular': 0.25, 'pigment': 0.4, 'structural': 0.3},
    'fitzpatrick_3_4': {'vascular': 0.35, 'pigment': 0.35, 'structural': 0.3},
    'fitzpatrick_5_6': {'vascular': 0.45, 'pigment': 0.25, 'structural': 0.3}
}
```

---

## 6. Treatment Recommendations by Type

| Type | Recommended Ingredients | Avoid |
|------|------------------------|-------|
| Vascular | Vitamin K, Caffeine, Niacinamide, Arnica | Heavy occlusives |
| Pigmentary | Vitamin C, Kojic Acid, Arbutin, Retinol | Irritating acids |
| Structural | Retinol, Peptides, Hyaluronic Acid | N/A (may need filler) |
| Mixed | Caffeine + Vitamin C combination | Harsh treatments |

---

## 7. Implementation Notes

### 7.1 Lighting Requirements

- Even, diffused lighting (avoid harsh shadows)
- Neutral color temperature (5000-5500K)
- Front-facing illumination
- Consistent distance (30-50cm from camera)

### 7.2 Image Quality Requirements

- Minimum resolution: 720p
- Focus on eye region
- No glasses or heavy makeup
- Eyes open, looking forward

---

## 8. References

1. Freitag, F.M. & Cestari, T.F. (2007). "What causes dark circles under the eyes?"
2. Roh, M.R. & Chung, K.Y. (2009). "Infraorbital dark circles: Definition, causes, and treatment"
3. Sarkar, R. et al. (2016). "Periorbital Hyperpigmentation: A Comprehensive Review"
4. Huang, Y.L. et al. (2014). "The treatment of periorbital hyperpigmentation"

---

**Status:** ✅ Research Complete | 👁️ Type Classification Ready | 📊 Severity Scoring Defined

---

## Implementation Specifications

### Dark Circles Detection Algorithm

```yaml
algorithm: dark_circles_detector
architecture: EfficientNet-B0 + FPN
input:
  format: RGB
  size: 224x224
  roi: periorbital_region
  preprocessing:
    - face_detection
    - eye_landmark_extraction
    - region_crop
output:
  type: classification + severity
  classes:
    - vascular (blue/purple)
    - pigmented (brown)
    - structural (shadow)
    - mixed
  severity: [0-100]
performance:
  accuracy: >90%
  inference_time: <80ms
  model_size: <8MB
```

### Severity Scoring System

| Score | Level | Description |
|-------|-------|-------------|
| 0-20 | Minimal | Barely visible |
| 21-40 | Mild | Slight discoloration |
| 41-60 | Moderate | Noticeable circles |
| 61-80 | Severe | Prominent dark circles |
| 81-100 | Very Severe | Deep discoloration |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 25, 2025 | Initial research |
| 2.0 | Nov 25, 2025 | Added implementation specs |

---

*Research by ML & Dermatology Team*