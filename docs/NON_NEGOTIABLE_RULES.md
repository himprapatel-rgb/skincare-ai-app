# NON-NEGOTIABLE RULES FOR DEVELOPMENT

**Status:** ABSOLUTE - NO EXCEPTIONS  
**Enforcement:** AUTOMATED + MANUAL REVIEW  
**Violation Consequence:** MERGE REQUEST BLOCKED  
**Version:** 1.0.0  
**Last Updated:** 2025-11-25  
**Authority:** Skincare AI Development Team Lead

---

## ⚠️ CRITICAL NOTICE

**These rules are NON-NEGOTIABLE and MUST be followed without exception.**

Violations will result in:
- Automatic CI/CD pipeline failure
- Blocked merge requests
- Code review rejection
- Required rework
- Team accountability discussion

**NO SHORTCUTS. NO EXCEPTIONS. NO EXCUSES.**

---

## 🚨 RULE #1: ZERO COMMITS WITHOUT DOCUMENTATION

### The Rule
**EVERY code change MUST include corresponding documentation updates.**

### What This Means
```
IF you change code:
  THEN you MUST update documentation
  
IF you add a feature:
  THEN you MUST document it
  
IF you fix a bug:
  THEN you MUST document the fix
  
NO CODE CHANGES WITHOUT DOCUMENTATION = NON-NEGOTIABLE
```

### Specific Requirements

**ALWAYS UPDATE (when applicable):**
- ✅ CHANGELOG.md - **MANDATORY for ALL changes**
- ✅ README.md - If setup, installation, or usage changed
- ✅ API Documentation - If endpoints/functions changed
- ✅ Inline comments - For complex logic
- ✅ Docstrings/JSDoc - For all new functions/classes
- ✅ Architecture diagrams - If system structure changed

### Enforcement
```yaml
# CI/CD Check
pre-commit:
  - name: Documentation Check
    script: |
      # Fail if CHANGELOG.md not modified
      if ! git diff --name-only HEAD~1 | grep -q "CHANGELOG.md"; then
        echo "❌ ERROR: CHANGELOG.md not updated"
        exit 1
      fi
    status: BLOCKING
```

### Examples

❌ **WRONG - Will be REJECTED:**
```
Commit: "feat: Add user authentication"
Files Changed: 
  - backend/auth.py (+150 lines)
  - CHANGELOG.md (NOT UPDATED) ← VIOLATION!
```

✅ **CORRECT - Will be ACCEPTED:**
```
Commit: "feat: Add user authentication"
Files Changed:
  - backend/auth.py (+150 lines)
  - CHANGELOG.md (+10 lines)
  - README.md (+5 lines)
  - docs/API.md (+20 lines)
```

---

## 🚨 RULE #2: ZERO MERGES WITHOUT PROGRESS TRACKING

### The Rule
**EVERY code change MUST be tracked in PROGRESS_TRACKER.md**

### What This Means
```
BEFORE merging:
  MUST update PROGRESS_TRACKER.md
  MUST update GitLab issue status  
  MUST log time spent
  MUST move sprint board card
  
NO PROGRESS TRACKING = NO MERGE = NON-NEGOTIABLE
```

### Specific Requirements

**PROGRESS_TRACKER.md Format (MANDATORY):**
```markdown
## [2025-11-25] - Developer Name

### Component: [Feature/Module Name]
**Status:** [In Progress / Completed / Blocked]  
**Lines Changed:** [+150 / -20]  
**Test Coverage:** [85%]  
**Issues:** [#123, #124]  

**Changes:**
- Implemented user authentication with JWT
- Added password hashing with bcrypt
- Created login/logout endpoints

**Next Steps:**
- Add email verification
- Implement 2FA
```

### Enforcement
```python
# Pre-merge Hook
def check_progress_tracking():
    if not progress_tracker_updated_today():
        raise Exception("❌ BLOCKED: Update PROGRESS_TRACKER.md")
    
    if not gitlab_issue_updated():
        raise Exception("❌ BLOCKED: Update GitLab issue status")
    
    if not time_logged():
        raise Exception("❌ BLOCKED: Log time in GitLab")
```

---

## 🚨 RULE #3: ZERO RELEASES WITHOUT VERSION UPDATE

### The Rule
**EVERY merge to main/production MUST increment version numbers**

### What This Means
```
IF merging to main:
  THEN version MUST be incremented
  AND CHANGELOG MUST have version section
  AND Git tag MUST be created
  
NO VERSION UPDATE = NO PRODUCTION DEPLOY = NON-NEGOTIABLE
```

### Specific Requirements

**MUST UPDATE ALL VERSION FILES:**
```
✅ backend/__init__.py      - __version__ = "1.2.3"
✅ frontend/pubspec.yaml    - version: 1.2.3+build
✅ backend/config.py         - VERSION = "1.2.3"
✅ docs/*.md                - Version: 1.2.3 in headers
✅ CHANGELOG.md              - ## [1.2.3] - 2025-11-25
```

### Semantic Versioning (STRICTLY ENFORCED)
```
MAJOR.MINOR.PATCH

MAJOR (1.0.0 → 2.0.0):
  - Breaking API changes
  - Database schema breaking changes
  - Incompatible architecture changes
  
MINOR (1.0.0 → 1.1.0):
  - New features (backward compatible)
  - New API endpoints
  - Enhanced functionality
  
PATCH (1.0.0 → 1.0.1):
  - Bug fixes only
  - Security patches
  - Performance improvements
```

### Enforcement
```bash
# Pre-merge to main
if [[ $(git rev-parse --abbrev-ref HEAD) == "main" ]]; then
  CURRENT_VERSION=$(get_version)
  PREVIOUS_VERSION=$(get_previous_version)
  
  if [[ "$CURRENT_VERSION" == "$PREVIOUS_VERSION" ]]; then
    echo "❌ ERROR: Version not incremented"
    exit 1
  fi
  
  if ! git tag | grep -q "v$CURRENT_VERSION"; then
    echo "❌ ERROR: Git tag not created"
    exit 1
  fi
fi
```

---

## 🚨 RULE #4: ZERO MERGES WITHOUT AUTOMATIC BACKUP

### The Rule
**EVERY major change MUST trigger automatic backup to local Downloads**

### What This Means
```
WHEN major change is merged:
  THEN automatic backup MUST be created
  AND backup MUST be saved to ~/Downloads/skincare-ai-backups/
  AND backup MUST be verified
  
NO BACKUP = DEPLOYMENT BLOCKED = NON-NEGOTIABLE
```

### Major Change Definition
```
MAJOR CHANGES (triggers backup):
  ✅ New feature (feat: commits)
  ✅ Critical bug fix (hotfix)
  ✅ Database migration
  ✅ API changes
  ✅ Security patch
  ✅ ML model update
  ✅ Configuration changes
  ✅ Dependency major updates
```

### Backup Requirements
```yaml
Location: ~/Downloads/skincare-ai-backups/
Filename: skincare-ai-app-v{VERSION}-{DATE}.zip
Contents:
  - Full source code
  - Documentation
  - Configuration files (sanitized)
Exclusions:
  - .git/
  - node_modules/
  - __pycache__/
  - .env (sensitive data)
Retention: Last 10 backups
Verification: File size > 1MB
```

### Enforcement
```bash
# Post-merge hook (AUTOMATIC)
if is_major_change; then
  ./scripts/backup-project.sh
  
  if [! -f "~/Downloads/skincare-ai-backups/skincare-ai-app-v${VERSION}-${DATE}.zip" ]; then
    echo "❌ ERROR: Backup failed"
    # Rollback deployment
    exit 1
  fi
  
  echo "✅ Backup created and verified"
fi
```

---

## 🚨 RULE #5: ZERO CODE WITHOUT TESTS

### The Rule
**EVERY new feature/function MUST have corresponding tests**

### What This Means
```
IF you write code:
  THEN you MUST write tests
  
IF tests don't exist:
  THEN code cannot be merged
  
TEST COVERAGE < 80% = MERGE BLOCKED = NON-NEGOTIABLE
```

### Specific Requirements

**MINIMUM COVERAGE:**
```
✅ Unit Tests: 80% coverage minimum
✅ Integration Tests: Critical paths covered
✅ E2E Tests: Main user flows covered
```

**TEST REQUIREMENTS:**
```python
# EVERY new function needs tests
def new_feature():  # ← NEW CODE
    pass

# MUST have corresponding test
def test_new_feature():  # ← MANDATORY TEST
    assert new_feature() == expected
    # Test edge cases
    # Test error handling
    # Test boundary conditions
```

### Enforcement
```yaml
# CI/CD Pipeline
test-stage:
  script:
    - pytest --cov=backend --cov-report=term --cov-fail-under=80
  rules:
    - if: coverage < 80%
      when: never  # BLOCK MERGE
```

---

## 🚨 RULE #6: ZERO COMMITS TO MAIN/DEVELOP DIRECTLY

### The Rule
**ALL changes MUST go through feature branches and code review**

### What This Means
```
DIRECT COMMITS TO main = FORBIDDEN
DIRECT COMMITS TO develop = FORBIDDEN

MUST use:
  - Feature branches (feature/*)
  - Pull/Merge requests
  - Code review (2+ approvals)
  
NO DIRECT COMMITS = NON-NEGOTIABLE
```

### Branch Protection
```yaml
# GitLab Settings
Protected Branches:
  main:
    - Push: No one
    - Merge: Maintainers only
    - Required approvals: 2
    - CI/CD must pass
    
  develop:
    - Push: No one  
    - Merge: Developers
    - Required approvals: 2
    - CI/CD must pass
```

### Enforcement
```bash
# Server-side hook (GitLab)
if [[ $BRANCH == "main" || $BRANCH == "develop" ]]; then
  if [[ $PUSH_TYPE == "direct" ]]; then
    echo "❌ REJECTED: Direct push to $BRANCH forbidden"
    exit 1
  fi
fi
```

---

## 🚨 RULE #7: ZERO MERGES WITHOUT 2+ APPROVALS

### The Rule
**EVERY merge request MUST be reviewed and approved by 2+ developers**

### What This Means
```
1 approval = NOT ENOUGH
0 approvals = DEFINITELY NOT ENOUGH
2+ approvals = REQUIRED

SELF-MERGE = FORBIDDEN = NON-NEGOTIABLE
```

### Approval Requirements
```yaml
Standard Changes:
  - Minimum: 2 developer approvals
  - CI/CD: Must pass
  - All conversations: Must be resolved
  
Architecture Changes:
  - Minimum: 2 developer approvals
  - Lead developer: Must approve
  - CI/CD: Must pass
  
Security Changes:
  - Minimum: 2 developer approvals  
  - Security team: Must approve
  - Security scan: Must pass
```

### Enforcement
```yaml
# GitLab Merge Request Settings
merge_request_rules:
  - name: "Require 2+ approvals"
    approvals_required: 2
    reset_approvals_on_push: true
  
  - name: "No self-approval"
    prevent_author_approval: true
```

---

## 🚨 RULE #8: ZERO PRODUCTION DEPLOYS WITHOUT QA SIGN-OFF

### The Rule
**EVERY production deployment MUST have QA approval**

### What This Means
```
BEFORE production deploy:
  MUST have QA approval
  MUST pass all staging tests
  MUST have rollback plan
  
NO QA APPROVAL = NO PRODUCTION = NON-NEGOTIABLE
```

### QA Approval Process
```yaml
QA Checklist:
  - Functional testing completed
  - Performance testing passed
  - Security testing passed
  - Cross-browser/device testing done
  - User acceptance criteria met
  - No critical/high severity bugs
  - Regression testing completed
  - Documentation reviewed
```

### Enforcement
```yaml
# GitLab Deployment Pipeline
production-deploy:
  stage: deploy
  rules:
    - if: QA_APPROVED == "false"
      when: never  # BLOCK DEPLOYMENT
  script:
    - deploy_to_production
```

---

## 🚨 RULE #9: ZERO SENSITIVE DATA IN CODE/COMMITS

### The Rule
**NO passwords, API keys, secrets, or PII in code or commits**

### What This Means
```
NO passwords in code
NO API keys in commits
NO database credentials hardcoded
NO secret tokens in repository
NO PII (Personal Identifiable Information)

SENSITIVE DATA IN CODE = SECURITY VIOLATION = NON-NEGOTIABLE
```

### What is Forbidden
```python
# ❌ FORBIDDEN - Will be REJECTED
API_KEY = "sk-1234567890abcdef"  # VIOLATION!
DATABASE_PASSWORD = "MyP@ssw0rd"  # VIOLATION!
JWT_SECRET = "super-secret-key"  # VIOLATION!
USER_EMAIL = "john@example.com"  # VIOLATION in production code!
```

### What is Required
```python
# ✅ CORRECT - Use environment variables
import os

API_KEY = os.getenv("API_KEY")  # From .env file
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
JWT_SECRET = os.getenv("JWT_SECRET")
```

### Enforcement
```yaml
# Pre-commit Hook
pre-commit:
  - name: Detect Secrets
    script: |
      detect-secrets scan --all-files
      if [ $? -ne 0 ]; then
        echo "❌ BLOCKED: Secrets detected in code"
        exit 1
      fi
```

---

## 🚨 RULE #10: ZERO TOLERANCE FOR BROKEN BUILDS

### The Rule
**CI/CD pipeline MUST pass on ALL branches**

### What This Means
```
IF build breaks:
  THEN fix immediately (within 1 hour)
  OR revert the breaking commit
  
BROKEN BUILD = BLOCKS ALL TEAM = NON-NEGOTIABLE
```

### Build Requirements
```
✅ Linter passes (no errors)
✅ Tests pass (100% pass rate)
✅ Code coverage >= 80%
✅ Security scan passes
✅ Docker build succeeds
✅ No merge conflicts
```

### Enforcement
```yaml
# Status Checks (Required)
required_status_checks:
  - lint
  - unit-tests
  - integration-tests
  - security-scan
  - build
  
if any_check_fails:
  block_merge: true
  notify_author: true
  escalate_after: 1 hour
```

---

## ENFORCEMENT MECHANISMS

### 1. Automated Enforcement (CI/CD)

```yaml
# .gitlab-ci.yml - MANDATORY CHECKS

stages:
  - validate
  - test
  - security
  - deploy

validate-documentation:
  stage: validate
  script:
    - python scripts/check_documentation.py
  allow_failure: false  # BLOCKING

validate-progress-tracker:
  stage: validate
  script:
    - python scripts/check_progress_tracking.py
  allow_failure: false  # BLOCKING

validate-version:
  stage: validate
  only:
    - main
  script:
    - python scripts/check_version_increment.py
  allow_failure: false  # BLOCKING

test-coverage:
  stage: test
  script:
    - pytest --cov=backend --cov-fail-under=80
  allow_failure: false  # BLOCKING

detect-secrets:
  stage: security
  script:
    - detect-secrets scan --all-files
  allow_failure: false  # BLOCKING

trigger-backup:
  stage: deploy
  only:
    - main
    - develop
  script:
    - ./scripts/backup-project.sh
    - ./scripts/verify-backup.sh
  allow_failure: false  # BLOCKING
```

### 2. Git Hooks (Local Enforcement)

**File:** `.git/hooks/pre-commit`
```bash
#!/bin/bash
# Pre-commit hook - MANDATORY CHECKS

echo "Running pre-commit checks..."

# Check 1: Documentation updated
if ! git diff --cached --name-only | grep -q "CHANGELOG.md"; then
  echo "❌ ERROR: CHANGELOG.md not updated"
  echo "RULE #1 VIOLATION: Every commit must update documentation"
  exit 1
fi

# Check 2: Progress tracker updated (for feature/fix commits)
COMMIT_MSG=$(cat .git/COMMIT_EDITMSG)
if [[ $COMMIT_MSG == feat:* || $COMMIT_MSG == fix:* ]]; then
  if ! git diff --cached --name-only | grep -q "PROGRESS_TRACKER.md"; then
    echo "❌ ERROR: PROGRESS_TRACKER.md not updated"
    echo "RULE #2 VIOLATION: Progress tracking required"
    exit 1
  fi
fi

# Check 3: No secrets in code
if detect-secrets scan --baseline .secrets.baseline $(git diff --cached --name-only); then
  echo "❌ ERROR: Secrets detected in staged files"
  echo "RULE #9 VIOLATION: No sensitive data in code"
  exit 1
fi

# Check 4: Linter passes
if ! make lint; then
  echo "❌ ERROR: Linter failed"
  echo "RULE #10 VIOLATION: Code must pass linter"
  exit 1
fi

# Check 5: Tests pass
if ! make test; then
  echo "❌ ERROR: Tests failed"
  echo "RULE #5 VIOLATION: Tests must pass"
  exit 1
fi

echo "✅ All pre-commit checks passed"
exit 0
```

### 3. Code Review Enforcement

**Merge Request Template:**
```markdown
## NON-NEGOTIABLE CHECKLIST

### BEFORE SUBMITTING THIS MR:

- [ ] **RULE #1:** CHANGELOG.md updated
- [ ] **RULE #1:** Documentation updated (README, API docs, etc.)
- [ ] **RULE #2:** PROGRESS_TRACKER.md updated
- [ ] **RULE #2:** GitLab issue status updated
- [ ] **RULE #2:** Time logged in GitLab
- [ ] **RULE #3:** Version incremented (if merging to main)
- [ ] **RULE #3:** Git tag created (if release)
- [ ] **RULE #4:** Backup verified (for major changes)
- [ ] **RULE #5:** Tests written for new code
- [ ] **RULE #5:** Test coverage >= 80%
- [ ] **RULE #6:** Using feature branch (not committing to main/develop)
- [ ] **RULE #7:** Assigned 2+ reviewers
- [ ] **RULE #8:** QA approval (if production deploy)
- [ ] **RULE #9:** No secrets/sensitive data in code
- [ ] **RULE #10:** CI/CD pipeline passes

**I confirm ALL non-negotiable rules have been followed.**

Signature: _______________  
Date: _______________
```

---

## VIOLATION CONSEQUENCES

### First Violation
- ⚠️ **Warning issued**
- Merge request blocked
- Required to fix immediately
- Team notification

### Second Violation (within 1 month)
- 🚨 **Formal documentation**
- One-on-one with team lead
- Review of workflow understanding
- Additional training required

### Third Violation (within 3 months)
- 🛑 **Performance review impact**
- Pair programming required for 2 weeks
- Weekly check-ins with lead
- Possible reassignment from critical tasks

### Repeated Violations
- 🚨 **Serious performance concern**
- HR involvement
- Performance improvement plan
- Potential team changes

---

## EXCEPTION PROCESS

### Can These Rules Be Bypassed?

**SHORT ANSWER: NO.**

### Emergency Exception (RARE)

In EXTREME emergencies only:

```
CRITERIA FOR EMERGENCY EXCEPTION:
  1. Production is DOWN
  2. Security breach in progress
  3. Data loss imminent
  4. Legal/compliance deadline (same day)
  
REQUIRED:
  - CTO approval
  - Incident ticket created
  - Post-incident review scheduled
  - Technical debt ticket created
  - Retroactive compliance within 24 hours
```

**Emergency Exception Form:**
```yaml
Emergency Exception Request:
  Rule Bypassed: [Rule #X]
  Reason: [Critical production issue]
  Impact if not bypassed: [System down, users affected]
  Approval: [CTO Name]
  Timestamp: [2025-11-25 23:00 GMT]
  Incident Ticket: [INC-12345]
  Compliance Deadline: [Within 24 hours]
```

---

## SUMMARY: THE 10 NON-NEGOTIABLE RULES

```
✅ RULE #1: ZERO COMMITS WITHOUT DOCUMENTATION
   Every code change = documentation update
   
✅ RULE #2: ZERO MERGES WITHOUT PROGRESS TRACKING  
   Every change = PROGRESS_TRACKER.md update
   
✅ RULE #3: ZERO RELEASES WITHOUT VERSION UPDATE
   Every production merge = version increment
   
✅ RULE #4: ZERO MERGES WITHOUT AUTOMATIC BACKUP
   Every major change = backup to ~/Downloads/
   
✅ RULE #5: ZERO CODE WITHOUT TESTS
   Every new code = tests (80% coverage minimum)
   
✅ RULE #6: ZERO COMMITS TO MAIN/DEVELOP DIRECTLY
   Every change = feature branch + code review
   
✅ RULE #7: ZERO MERGES WITHOUT 2+ APPROVALS
   Every merge request = 2+ developer approvals
   
✅ RULE #8: ZERO PRODUCTION DEPLOYS WITHOUT QA
   Every production deploy = QA sign-off
   
✅ RULE #9: ZERO SENSITIVE DATA IN CODE/COMMITS
   No passwords, keys, secrets, or PII in code
   
✅ RULE #10: ZERO TOLERANCE FOR BROKEN BUILDS
   CI/CD must pass = fix within 1 hour or revert
```

---

## FINAL STATEMENT

**These rules exist to ensure:**
- 🛡️ Code quality and reliability
- 📝 Complete and accurate documentation
- 📈 Transparent progress tracking
- 📏 Proper version control
- 💾 Data protection through backups
- ✅ High test coverage
- 👥 Collaborative code review
- 🔒 Security and data privacy
- 🚀 Stable deployments

**REMEMBER:**

> "Quality is not an act, it is a habit." - Aristotle

**These rules are habits we build into our development process.**

**NO SHORTCUTS. NO EXCEPTIONS. NO EXCUSES.**

**EXCELLENCE IS NON-NEGOTIABLE.**

---

**Document Version:** 1.0.0  
**Status:** ACTIVE AND ENFORCED  
**Authority:** Skincare AI Development Team Lead  
**Effective Date:** 2025-11-25  
**Review Cycle:** Quarterly  
**Next Review:** 2026-02-25  

**Acknowledged and Agreed:**

_All team members must sign acknowledgment of these rules._

---

**⚠️ THIS DOCUMENT IS MANDATORY READING FOR ALL DEVELOPERS ⚠️**