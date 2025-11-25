# Privacy & Compliance Research

**File:** `/docs/research/09_privacy_compliance_research.md`
**Last Updated:** November 25, 2025
**Research Team:** Security, Legal, Privacy Swarm

---

## Executive Summary

Handling facial images for skin analysis requires strict compliance with global privacy regulations. This document covers GDPR, CCPA, HIPAA considerations, biometric data laws, and privacy-by-design principles essential for the AI Skincare App.

---

## 1. Regulatory Landscape

### 1.1 Key Regulations

| Regulation | Region | Key Requirements | Penalty |
|------------|--------|------------------|--------|
| GDPR | EU/EEA | Consent, data minimization, right to deletion | Up to €20M or 4% revenue |
| CCPA/CPRA | California | Opt-out rights, disclosure requirements | $7,500 per violation |
| BIPA | Illinois | Biometric consent, retention limits | $1,000-$5,000 per violation |
| PIPEDA | Canada | Consent, purpose limitation | Up to $100K CAD |
| LGPD | Brazil | Similar to GDPR | Up to 2% revenue |

### 1.2 Biometric Data Classification

**Facial images ARE considered biometric data under:**
- Illinois BIPA
- Texas CUBI
- Washington State Biometric Law
- GDPR Article 9 (special category)

**Critical:** Our app processes facial images = biometric data processing

---

## 2. GDPR Compliance Requirements

### 2.1 Legal Basis for Processing

| Basis | Applicability | Requirements |
|-------|---------------|---------------|
| Consent | **Primary basis** | Explicit, informed, withdrawable |
| Legitimate Interest | Limited use | Requires balancing test |
| Contract | If service requires | Document necessity |

**Recommended:** Explicit consent for all facial image processing

### 2.2 Data Subject Rights

| Right | Implementation Required |
|-------|-------------------------|
| Access | Export user data on request |
| Rectification | Allow profile updates |
| Erasure | Delete all data within 30 days |
| Portability | Provide data in machine-readable format |
| Object | Allow opt-out of processing |
| Restrict | Pause processing on request |

### 2.3 Required Documentation

- Privacy Policy (user-facing)
- Data Processing Agreement (DPA)
- Records of Processing Activities (ROPA)
- Data Protection Impact Assessment (DPIA)
- Consent management records

---

## 3. Privacy-by-Design Principles

### 3.1 Data Minimization

```
✅ COLLECT:
- Skin analysis results (derived data)
- User preferences
- Progress photos (if opted-in)

❌ DO NOT COLLECT:
- Raw facial biometrics
- Location data (unless essential)
- Device identifiers (without consent)
- Third-party tracking data
```

### 3.2 On-Device Processing (Preferred)

```
Recommended Architecture:

┌──────────────────────────────┐
│         USER DEVICE            │
├──────────────────────────────┤
│  Camera → ML Model → Results  │
│                                │
│  [Image NEVER leaves device]  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         CLOUD (Optional)       │
├──────────────────────────────┤
│  Only receives:                │
│  - Anonymized skin scores      │
│  - Routine preferences         │
│  - NO images, NO biometrics    │
└──────────────────────────────┘
```

### 3.3 Data Retention Policy

| Data Type | Retention Period | Deletion Method |
|-----------|------------------|------------------|
| Raw images | Process & delete immediately | Secure wipe |
| Analysis results | Until user deletes account | Database purge |
| Progress photos | User-controlled | On-demand deletion |
| Account data | 30 days post-deletion request | Full purge |
| Analytics | 24 months (anonymized) | Aggregation |

---

## 4. Consent Management

### 4.1 Consent Requirements

```
Required Consent Points:

1. ☐ Camera Access
   "Allow access to camera for skin analysis"
   
2. ☐ Facial Analysis
   "I consent to AI analysis of my facial skin"
   
3. ☐ Data Storage (Optional)
   "Store my progress photos for tracking"
   
4. ☐ Analytics (Optional)
   "Share anonymized data to improve the app"
```

### 4.2 Consent UI Best Practices

- **Granular:** Separate consent for each purpose
- **Clear:** Plain language, no legal jargon
- **Withdrawable:** Easy opt-out at any time
- **Recorded:** Timestamp and version stored

---

## 5. Security Requirements

### 5.1 Technical Safeguards

| Measure | Implementation |
|---------|----------------|
| Encryption at rest | AES-256 for stored data |
| Encryption in transit | TLS 1.3 minimum |
| Access controls | Role-based, least privilege |
| Audit logging | All data access logged |
| Secure deletion | Cryptographic erasure |

### 5.2 If Cloud Processing Required

```python
# Pseudonymization before upload
def prepare_for_cloud(image, user_id):
    # Generate temporary analysis ID
    temp_id = generate_uuid()
    
    # Remove all metadata
    clean_image = strip_exif(image)
    
    # No user_id sent to cloud
    return {
        'temp_id': temp_id,
        'image': encrypt(clean_image),
        'user_id': None  # NEVER send
    }
```

---

## 6. Medical Device Considerations

### 6.1 FDA Classification Risk

| Claim Type | Risk Level | Requirement |
|------------|------------|-------------|
| "Analyzes skin appearance" | Low | No FDA review |
| "Detects skin conditions" | Medium | May need 510(k) |
| "Diagnoses skin diseases" | High | Requires FDA clearance |

**Recommendation:** Use non-diagnostic language

### 6.2 Safe Language Guidelines

```
✅ SAFE TO SAY:
- "Analyzes skin appearance"
- "Identifies visible characteristics"
- "Suggests skincare routines"
- "Tracks skin changes over time"

❌ AVOID SAYING:
- "Diagnoses skin conditions"
- "Detects skin diseases"
- "Medical-grade analysis"
- "Dermatologist-level accuracy"
```

---

## 7. Required Disclaimers

### 7.1 App Disclaimers

```
"This app is for informational purposes only and does not 
provide medical advice, diagnosis, or treatment. Always 
consult a qualified dermatologist for skin concerns."

"AI analysis is not a substitute for professional 
dermatological examination."

"Results may vary. Individual skin conditions require 
professional medical evaluation."
```

### 7.2 Terms of Service Clauses

- Age restriction (13+ or 16+ for GDPR)
- Limitation of liability
- No medical claims
- Data processing description
- Third-party services disclosure

---

## 8. Implementation Checklist

### 8.1 Pre-Launch Requirements

- [ ] Privacy Policy published
- [ ] Terms of Service published
- [ ] Consent flows implemented
- [ ] Data deletion mechanism
- [ ] DPIA completed (if EU users)
- [ ] DPA with cloud providers
- [ ] Security audit completed
- [ ] Penetration testing done

### 8.2 Ongoing Requirements

- [ ] Regular privacy audits
- [ ] Consent records maintained
- [ ] Breach response plan tested
- [ ] Staff privacy training
- [ ] Policy updates communicated

---

## 9. References

1. GDPR Official Text (Regulation 2016/679)
2. CCPA/CPRA California Civil Code
3. Illinois BIPA (740 ILCS 14)
4. FDA Guidance on Mobile Medical Applications
5. NIST Privacy Framework

---

**Status:** ✅ Research Complete | 🛡️ Compliance Framework Defined | 📝 Checklist Ready

---

## Compliance Checklists

### GDPR Compliance Checklist

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Lawful basis for processing | Required | Consent mechanism |
| Data minimization | Required | Only collect needed data |
| Right to access | Required | Export data feature |
| Right to erasure | Required | Delete account option |
| Data portability | Required | JSON/CSV export |
| Privacy by design | Required | Architecture review |
| Data breach notification | Required | 72-hour alert system |
| DPO appointment | Conditional | If >10K EU users |

### CCPA/CPRA Compliance Checklist

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Right to know | Required | Data access portal |
| Right to delete | Required | Account deletion |
| Right to opt-out | Required | Sale opt-out toggle |
| Non-discrimination | Required | Equal service |
| Privacy notice | Required | In-app disclosure |

### Biometric Data Requirements

| Jurisdiction | Requirement | Action |
|--------------|-------------|--------|
| Illinois (BIPA) | Written consent | Pre-scan agreement |
| Texas | Consent | Opt-in checkbox |
| Washington | Notice | Privacy disclosure |
| EU (GDPR) | Explicit consent | Double opt-in |

---

## Data Retention Policy

| Data Type | Retention Period | Deletion Method |
|-----------|------------------|----------------|
| Facial images | 30 days | Automatic purge |
| Analysis results | 12 months | User-initiated |
| Account data | Until deletion | Manual request |
| Usage analytics | 24 months | Anonymized |
| Crash logs | 90 days | Automatic purge |

---

## Security Measures

- End-to-end encryption (TLS 1.3)
- At-rest encryption (AES-256)
- Facial images processed on-device
- No cloud storage of biometric data
- SOC 2 Type II certification target
- Annual penetration testing
- Bug bounty program

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 25, 2025 | Initial research |
| 2.0 | Nov 25, 2025 | Added compliance checklists, retention policy, security measures |

---

*Research by Security, Legal & Privacy Team*