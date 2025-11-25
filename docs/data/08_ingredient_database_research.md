# Ingredient Database Research

**File:** `/docs/research/08_ingredient_database_research.md`
**Last Updated:** November 25, 2025
**Research Team:** Cosmetic Science, Data, Backend Swarm

---

## Executive Summary

The ingredient database is the backbone of the AI Routine Builder, enabling ingredient identification, compatibility checking, and efficacy-based recommendations. This document covers database schema design, data sources, and the INCI (International Nomenclature of Cosmetic Ingredients) standard.

---

## 1. Core Requirements

| Requirement | Specification |
|-------------|---------------|
| Ingredient Coverage | 10,000+ INCI ingredients |
| Data Points | Name, function, safety, efficacy, interactions |
| Update Frequency | Monthly for safety data |
| Search | By INCI name, common name, function |
| Compatibility Engine | Real-time interaction checking |

---

## 2. Database Schema

### 2.1 Ingredient Entity

```sql
CREATE TABLE ingredients (
    id UUID PRIMARY KEY,
    inci_name VARCHAR(255) UNIQUE NOT NULL,
    cas_number VARCHAR(20),
    ec_number VARCHAR(20),
    
    -- Names
    common_names JSONB,  -- {"en": ["Vitamin C"], "scientific": "Ascorbic Acid"}
    
    -- Classification
    category VARCHAR(50),  -- active, humectant, emollient, preservative, etc.
    functions TEXT[],  -- ["antioxidant", "brightening", "collagen-boosting"]
    
    -- Safety & Regulation
    ewg_score INTEGER CHECK (ewg_score BETWEEN 1 AND 10),
    comedogenic_rating INTEGER CHECK (comedogenic_rating BETWEEN 0 AND 5),
    irritation_potential VARCHAR(20),  -- low, medium, high
    pregnancy_safe BOOLEAN,
    
    -- Efficacy
    concerns_addressed TEXT[],  -- ["acne", "aging", "pigmentation"]
    skin_types_suitable TEXT[],  -- ["oily", "dry", "all"]
    
    -- Usage
    typical_concentration VARCHAR(50),  -- "0.5-2%"
    ph_dependent BOOLEAN DEFAULT FALSE,
    optimal_ph_range NUMRANGE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 2.2 Ingredient Interactions

```sql
CREATE TABLE ingredient_interactions (
    id UUID PRIMARY KEY,
    ingredient_a_id UUID REFERENCES ingredients(id),
    ingredient_b_id UUID REFERENCES ingredients(id),
    
    interaction_type VARCHAR(20),  -- 'incompatible', 'synergistic', 'neutral'
    severity VARCHAR(20),  -- 'avoid', 'caution', 'beneficial'
    reason TEXT,
    
    -- Timing considerations
    same_routine_ok BOOLEAN DEFAULT TRUE,
    alternating_ok BOOLEAN DEFAULT TRUE,
    
    UNIQUE(ingredient_a_id, ingredient_b_id)
);
```

### 2.3 Ingredient-Concern Mapping

```sql
CREATE TABLE ingredient_efficacy (
    id UUID PRIMARY KEY,
    ingredient_id UUID REFERENCES ingredients(id),
    concern VARCHAR(50),  -- acne, wrinkles, dark_spots, etc.
    
    efficacy_level VARCHAR(20),  -- proven, promising, anecdotal
    evidence_strength INTEGER,  -- 1-5 scale
    mechanism TEXT,
    
    source_studies TEXT[],
    last_reviewed DATE
);
```

---

## 3. Key Ingredient Categories

### 3.1 Active Ingredients

| Category | Examples | Primary Function |
|----------|----------|------------------|
| Retinoids | Retinol, Retinal, Tretinoin | Anti-aging, acne |
| Vitamin C | L-Ascorbic Acid, MAP, SAP | Brightening, antioxidant |
| AHAs | Glycolic, Lactic, Mandelic | Exfoliation |
| BHAs | Salicylic Acid | Pore clearing, acne |
| Niacinamide | Vitamin B3 | Multi-benefit |
| Peptides | Matrixyl, Argireline | Anti-aging |

### 3.2 Hydrating Ingredients

| Category | Examples | Mechanism |
|----------|----------|--------|
| Humectants | Hyaluronic Acid, Glycerin | Draw water |
| Emollients | Squalane, Jojoba Oil | Soften skin |
| Occlusives | Petrolatum, Dimethicone | Seal moisture |
| Ceramides | Ceramide NP, AP, EOP | Barrier repair |

### 3.3 Soothing Ingredients

| Ingredient | Source | Best For |
|------------|--------|----------|
| Centella Asiatica | Plant | Sensitivity, redness |
| Allantoin | Comfrey | Irritation |
| Panthenol | Vitamin B5 | Hydration, healing |
| Aloe Vera | Plant | Soothing, hydration |

---

## 4. Compatibility Rules Engine

### 4.1 Known Incompatibilities

```python
INCOMPATIBLE_PAIRS = {
    ('retinol', 'vitamin_c'): {
        'reason': 'pH incompatibility, increased irritation',
        'severity': 'caution',
        'solution': 'Use in different routines (AM/PM)'
    },
    ('retinol', 'aha'): {
        'reason': 'Over-exfoliation risk',
        'severity': 'avoid',
        'solution': 'Alternate nights'
    },
    ('retinol', 'benzoyl_peroxide'): {
        'reason': 'Mutual degradation',
        'severity': 'avoid',
        'solution': 'Use in different routines'
    },
    ('vitamin_c', 'aha'): {
        'reason': 'pH incompatibility',
        'severity': 'caution',
        'solution': 'Apply Vitamin C first, wait 30 min'
    },
    ('niacinamide', 'vitamin_c'): {
        'reason': 'Potential flushing (debated)',
        'severity': 'caution',
        'solution': 'Most modern formulations are fine together'
    }
}
```

### 4.2 Synergistic Combinations

```python
SYNERGISTIC_PAIRS = {
    ('vitamin_c', 'vitamin_e'): {
        'benefit': 'Enhanced antioxidant protection (8x)',
        'mechanism': 'Vitamin E regenerates Vitamin C'
    },
    ('niacinamide', 'hyaluronic_acid'): {
        'benefit': 'Optimal hydration and barrier support',
        'mechanism': 'Complementary mechanisms'
    },
    ('retinol', 'peptides'): {
        'benefit': 'Enhanced anti-aging',
        'mechanism': 'Different collagen-boosting pathways'
    },
    ('aha', 'hyaluronic_acid'): {
        'benefit': 'Exfoliation without dehydration',
        'mechanism': 'HA replenishes moisture post-exfoliation'
    }
}
```

---

## 5. Data Sources

### 5.1 Primary Sources

| Source | Data Type | Update Frequency |
|--------|-----------|------------------|
| CIR (Cosmetic Ingredient Review) | Safety assessments | Quarterly |
| EWG Skin Deep | Safety scores | Monthly |
| PubMed | Efficacy studies | Continuous |
| INCI Decoder | Ingredient explanations | As needed |
| CosDNA | Comedogenic ratings | As needed |

### 5.2 Open Data Sources

- **CosIng (EU):** ec.europa.eu/growth/tools-databases/cosing
- **FDA VCRP:** fda.gov/cosmetics/voluntary-cosmetic-registration-program
- **ECHA:** echa.europa.eu (chemical safety)

---

## 6. Safety Scoring System

### 6.1 Composite Safety Score

```python
def calculate_safety_score(ingredient):
    weights = {
        'ewg_score': 0.25,
        'irritation_potential': 0.25,
        'comedogenic_rating': 0.20,
        'allergen_potential': 0.15,
        'regulatory_status': 0.15
    }
    
    # Normalize all scores to 0-10 scale
    ewg = 10 - ingredient.ewg_score  # Invert (lower is better)
    irritation = {'low': 9, 'medium': 5, 'high': 2}[ingredient.irritation]
    comedogenic = 10 - (ingredient.comedogenic_rating * 2)
    
    score = (
        ewg * weights['ewg_score'] +
        irritation * weights['irritation_potential'] +
        comedogenic * weights['comedogenic_rating'] +
        # ... other factors
    )
    
    return round(score, 1)
```

---

## 7. API Design

### 7.1 Endpoints

```
GET /api/ingredients?search=vitamin+c
GET /api/ingredients/{id}
GET /api/ingredients/{id}/interactions
POST /api/ingredients/check-compatibility
GET /api/ingredients/by-concern/{concern}
GET /api/ingredients/by-function/{function}
```

### 7.2 Compatibility Check Request

```json
{
  "ingredients": ["retinol", "vitamin_c", "hyaluronic_acid"],
  "routine_type": "evening"
}
```

### 7.3 Response

```json
{
  "compatible": false,
  "issues": [
    {
      "pair": ["retinol", "vitamin_c"],
      "severity": "caution",
      "reason": "pH incompatibility",
      "recommendation": "Use Vitamin C in AM, Retinol in PM"
    }
  ],
  "synergies": []
}
```

---

## 8. References

1. Cosmetic Ingredient Review (CIR) Reports
2. EWG Skin Deep Database Methodology
3. Baumann, L. "Cosmeceuticals and Cosmetic Ingredients"
4. Draelos, Z.D. "Cosmetic Dermatology"

---

**Status:** ✅ Research Complete | 🗄️ Schema Defined | 🔗 API Designed

---

## Database Implementation

### MongoDB Schema

```javascript
// Ingredient Collection
{
  _id: ObjectId,
  inci_name: String,           // International Nomenclature
  common_names: [String],      // Alternative names
  category: String,            // Moisturizer, Exfoliant, etc.
  function: [String],          // Humectant, Emollient, etc.
  safety_rating: Number,       // 1-10 scale
  comedogenic_rating: Number,  // 0-5 scale
  skin_types: [String],        // Suitable skin types
  concerns: [String],          // Addresses these concerns
  avoid_with: [ObjectId],      // Ingredient conflicts
  source: String,              // Natural/Synthetic
  concentration_range: {
    min: Number,
    max: Number,
    unit: String
  },
  metadata: {
    created_at: Date,
    updated_at: Date,
    source_refs: [String]
  }
}
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/ingredients | GET | List all ingredients |
| /api/v1/ingredients/{id} | GET | Get ingredient details |
| /api/v1/ingredients/search | POST | Search by name/function |
| /api/v1/ingredients/conflicts | POST | Check ingredient conflicts |
| /api/v1/ingredients/recommend | POST | Get recommendations |

### Data Sources Priority

| Source | Priority | Update Frequency |
|--------|----------|------------------|
| CIR (Cosmetic Ingredient Review) | 1 | Quarterly |
| EWG Skin Deep | 2 | Monthly |
| PubChem | 3 | Weekly |
| FDA Database | 4 | Quarterly |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 25, 2025 | Initial research |
| 2.0 | Nov 25, 2025 | Added MongoDB schema, API endpoints, data sources |

---

*Research by Data & Backend Team*