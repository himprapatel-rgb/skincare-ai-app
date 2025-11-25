# AI Routine Builder Research

**File:** `/docs/research/04_ai_routine_builder_research.md`
**Last Updated:** November 25, 2025
**Research Team:** AI Research, Cosmetic Science, UX Swarm

---

## Executive Summary

The AI Routine Builder is the intelligent engine that combines skin analysis results with product knowledge to generate personalized skincare routines. This document covers recommendation algorithms, ingredient compatibility logic, routine sequencing rules, and personalization strategies.

---

## 1. Core Requirements

### 1.1 Functional Requirements

| Requirement | Specification |
|-------------|---------------|
| Input | Skin analysis results, user preferences, budget, time constraints |
| Output | Morning routine, Evening routine, Weekly treatments |
| Products | 3-7 products per routine (configurable) |
| Personalization | Skin type, concerns, goals, lifestyle |
| Updates | Dynamic adjustment based on progress tracking |

### 1.2 Non-Functional Requirements

| Metric | Target |
|--------|--------|
| Recommendation Latency | <2 seconds |
| User Satisfaction | >85% positive feedback |
| Routine Adherence | >70% 30-day retention |
| Ingredient Conflict Detection | 100% accuracy |

---

## 2. Recommendation Algorithm Architecture

### 2.1 Multi-Stage Pipeline

```
Skin Analysis Results
        │
        ▼
┌───────────────────────┐
│ Stage 1: Concern       │
│ Prioritization         │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Stage 2: Ingredient    │
│ Selection              │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Stage 3: Product       │
│ Matching               │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Stage 4: Compatibility │
│ Verification           │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Stage 5: Routine       │
│ Sequencing             │
└───────────┬───────────┘
            │
            ▼
   Personalized Routine
```

### 2.2 Concern Prioritization

**Priority Scoring Formula:**
```
Priority Score = (Severity × 0.4) + (User Preference × 0.3) + 
                (Treatability × 0.2) + (Urgency × 0.1)
```

**Concern Categories:**

| Category | Concerns | Priority Weight |
|----------|----------|----------------|
| Barrier Health | Dehydration, Sensitivity | High (1.2x) |
| Active Conditions | Acne, Rosacea | High (1.1x) |
| Pigmentation | Dark spots, Melasma | Medium (1.0x) |
| Aging | Wrinkles, Loss of firmness | Medium (1.0x) |
| Texture | Pores, Roughness | Low (0.9x) |

---

## 3. Ingredient Selection Engine

### 3.1 Ingredient-Concern Mapping

| Concern | Primary Ingredients | Secondary Ingredients |
|---------|--------------------|-----------------------|
| Acne | Salicylic Acid, Benzoyl Peroxide, Niacinamide | Tea Tree, Zinc, Azelaic Acid |
| Hyperpigmentation | Vitamin C, Alpha Arbutin, Kojic Acid | Niacinamide, Licorice Root |
| Wrinkles | Retinol, Peptides, Vitamin C | Bakuchiol, Hyaluronic Acid |
| Dehydration | Hyaluronic Acid, Glycerin, Ceramides | Squalane, Aloe Vera |
| Sensitivity | Centella, Allantoin, Panthenol | Oat Extract, Chamomile |

### 3.2 Ingredient Compatibility Matrix

**Incompatible Combinations (AVOID):**

| Ingredient A | Ingredient B | Reason |
|--------------|--------------|--------|
| Vitamin C | Retinol | pH incompatibility, increased irritation |
| Benzoyl Peroxide | Retinol | Mutual degradation |
| AHA/BHA | Retinol | Over-exfoliation risk |
| Vitamin C | Niacinamide | Potential flushing (debated) |
| AHA/BHA | Vitamin C | pH incompatibility |

**Synergistic Combinations (RECOMMEND):**

| Ingredient A | Ingredient B | Benefit |
|--------------|--------------|--------|
| Vitamin C | Vitamin E | Enhanced antioxidant effect |
| Niacinamide | Zinc | Sebum control |
| Retinol | Hyaluronic Acid | Minimizes dryness |
| Ceramides | Cholesterol + Fatty Acids | Barrier repair |
| AHA | Hyaluronic Acid | Hydration post-exfoliation |

---

## 4. Routine Sequencing Rules

### 4.1 Application Order (Thinnest to Thickest)

**Morning Routine:**
```
1. Cleanser (water-based or gentle)
2. Toner/Essence (optional)
3. Serum (water-based actives)
4. Eye Cream (optional)
5. Moisturizer
6. Sunscreen (SPF 30+) [MANDATORY]
```

**Evening Routine:**
```
1. Oil Cleanser / Makeup Remover
2. Water-based Cleanser
3. Exfoliant (2-3x per week)
4. Toner/Essence
5. Treatment Serum (retinol, acids)
6. Eye Cream
7. Moisturizer / Night Cream
8. Facial Oil (optional, last step)
```

### 4.2 Time-of-Day Restrictions

| Ingredient | Morning | Evening | Reason |
|------------|---------|---------|--------|
| Retinol | ❌ | ✅ | Photosensitivity |
| AHA/BHA | ⚠️ | ✅ | Photosensitivity |
| Vitamin C | ✅ | ✅ | UV protection boost (AM preferred) |
| Niacinamide | ✅ | ✅ | Any time |
| Sunscreen | ✅ | ❌ | Only needed during sun exposure |

---

## 5. Personalization Engine

### 5.1 User Profile Factors

| Factor | Data Source | Impact |
|--------|-------------|--------|
| Skin Type | Analysis + Self-report | Product texture selection |
| Age Range | User input | Active ingredient strength |
| Climate | Location API | Hydration/SPF emphasis |
| Budget | User preference | Product tier filtering |
| Time Available | User input | Routine complexity |
| Allergies/Sensitivities | User input | Ingredient exclusions |
| Pregnancy/Nursing | User input | Safety restrictions |

### 5.2 Adaptive Learning

**Feedback Loop:**
```
User uses routine
       │
       ▼
┌─────────────────┐
│ Progress Photo  │
│ Analysis        │
└────────┬────────┘
        │
        ▼
┌─────────────────┐
│ User Feedback   │
│ (satisfaction)  │
└────────┬────────┘
        │
        ▼
┌─────────────────┐
│ Model Update    │
│ (personalized)  │
└────────┬────────┘
        │
        ▼
  Improved Recommendations
```

---

## 6. Product Database Schema

### 6.1 Product Entity

```json
{
  "product_id": "uuid",
  "name": "string",
  "brand": "string",
  "category": "cleanser|toner|serum|moisturizer|sunscreen|treatment",
  "ingredients": ["ingredient_id"],
  "key_actives": ["ingredient_id"],
  "skin_types": ["oily", "dry", "combination", "sensitive", "normal"],
  "concerns_addressed": ["acne", "aging", "pigmentation"],
  "price_tier": "budget|mid|premium|luxury",
  "price_usd": "number",
  "size_ml": "number",
  "texture": "gel|cream|lotion|oil|foam",
  "fragrance_free": "boolean",
  "vegan": "boolean",
  "cruelty_free": "boolean",
  "ratings": {
    "average": "number",
    "count": "number"
  }
}
```

### 6.2 Ingredient Entity

```json
{
  "ingredient_id": "uuid",
  "inci_name": "string",
  "common_names": ["string"],
  "category": "active|humectant|emollient|preservative|fragrance",
  "functions": ["anti-acne", "anti-aging", "hydrating"],
  "concentration_typical": "percentage range",
  "ph_optimal": "number range",
  "incompatible_with": ["ingredient_id"],
  "synergistic_with": ["ingredient_id"],
  "photosensitizing": "boolean",
  "pregnancy_safe": "boolean",
  "irritation_potential": "low|medium|high",
  "comedogenic_rating": "0-5"
}
```

---

## 7. AI Model Specifications

### 7.1 Recommendation Model

**Architecture Options:**

| Approach | Pros | Cons |
|----------|------|------|
| Collaborative Filtering | Learns from user patterns | Cold start problem |
| Content-Based | Works immediately | Limited discovery |
| Knowledge Graph | Explainable | Complex to build |
| Hybrid (Recommended) | Best of both worlds | More complex |

**Hybrid Approach:**
- Content-based for new users (cold start)
- Collaborative filtering for personalization
- Knowledge graph for ingredient logic
- Rule engine for safety constraints

### 7.2 Model Training Data

| Data Source | Purpose | Volume |
|-------------|---------|--------|
| Skincare forums (Reddit, etc.) | User preferences | 500K+ posts |
| Product reviews | Effectiveness signals | 1M+ reviews |
| Dermatology literature | Ingredient efficacy | 10K+ papers |
| Expert routines | Gold standard | 1K+ routines |

---

## 8. Safety & Compliance

### 8.1 Medical Disclaimers

- "Not a substitute for professional dermatological advice"
- "Consult a dermatologist for persistent skin conditions"
- "Patch test new products before full application"
- "Individual results may vary"

### 8.2 Ingredient Safety Checks

| Check | Action |
|-------|--------|
| Pregnancy-unsafe ingredients | Auto-exclude if user indicates pregnancy |
| High irritation potential | Warn user, suggest patch test |
| Known allergens | Check against user allergy profile |
| Drug interactions | Flag retinoids with certain medications |

---

## 9. Implementation Roadmap

### 9.1 Phase 1: MVP (4 weeks)
- Basic routine generation
- Core ingredient compatibility
- 3 skin types support
- Manual product database (100 products)

### 9.2 Phase 2: Enhancement (8 weeks)
- Full personalization engine
- Progress tracking integration
- Expanded product database (1000+ products)
- User feedback loop

### 9.3 Phase 3: Intelligence (12 weeks)
- ML-based recommendations
- Collaborative filtering
- Auto-updating product database
- A/B testing framework

---

## 10. References

1. Draelos, Z.D. (2018). "The science behind skin care: Cleansers"
2. Baumann, L. (2009). "Cosmetic Dermatology: Principles and Practice"
3. Kligman, A.M. (1996). "The taxonomy of photoaging"
4. INC International Nomenclature of Cosmetic Ingredients
5. Paula's Choice Ingredient Dictionary

---

**Status:** ✅ Research Complete | 🛠️ Algorithm Design Ready | 📊 Database Schema Defined