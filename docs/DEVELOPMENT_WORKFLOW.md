# DEVELOPMENT WORKFLOW - HIGH-LEVEL STANDARD PROCESS

**Document Version:** 1.0.0  
**Author:** Skincare AI Development Team  
**Last Updated:** 2025-11-25  
**Purpose:** Establish standard high-level workflow to improve app development quality

---

## Table of Contents

1. [Overview](#overview)
2. [Development Lifecycle Phases](#development-lifecycle-phases)
3. [Quality Assurance Framework](#quality-assurance-framework)
4. [Code Quality Standards](#code-quality-standards)
5. [Testing Strategy](#testing-strategy)
6. [CI/CD Pipeline](#cicd-pipeline)
7. [Code Review Process](#code-review-process)
8. [Release Management](#release-management)
9. [Monitoring & Feedback](#monitoring--feedback)
10. [Best Practices](#best-practices)

---

## Overview

This document outlines the standard high-level workflow for developing the Skincare AI App with a focus on quality, consistency, and efficiency. Following this workflow ensures:

- **Consistent Code Quality**: All code meets established standards
- **Reduced Bugs**: Comprehensive testing catches issues early
- **Faster Development**: Streamlined processes reduce bottlenecks
- **Better Collaboration**: Clear processes improve team coordination
- **Maintainable Codebase**: Well-documented, tested, and reviewed code

---

## Development Lifecycle Phases

### Phase 1: Planning & Requirements

```
┌────────────────────────────────────────────────────────────┐
│                   PHASE 1: PLANNING                            │
└────────────────────────────────────────────────────────────┘

1. Requirements Gathering
   ├── Stakeholder meetings
   ├── User story creation
   ├── Acceptance criteria definition
   └── Priority assignment (Critical/High/Medium/Low)

2. Technical Design
   ├── Review SRS and architecture documents
   ├── Create technical specification
   ├── Identify dependencies
   ├── Database schema design
   └── API endpoint specification

3. Task Breakdown
   ├── Create GitLab issues/tickets
   ├── Estimate effort (story points/hours)
   ├── Assign to sprint/milestone
   └── Link related issues

4. Sprint Planning
   ├── Sprint duration: 2 weeks
   ├── Team capacity calculation
   ├── Sprint goal definition
   └── Daily standup schedule
```

**Deliverables:**
- User stories with acceptance criteria
- Technical specification document
- Sprint backlog
- Task assignments

**Quality Gates:**
- ☑️ All user stories have clear acceptance criteria
- ☑️ Technical design reviewed by lead developer
- ☑️ Dependencies identified and documented
- ☑️ Sprint commitments are realistic

---

### Phase 2: Development

```
┌────────────────────────────────────────────────────────────┐
│                PHASE 2: DEVELOPMENT                             │
└────────────────────────────────────────────────────────────┘

1. Environment Setup
   ├── Clone repository
   ├── Install dependencies (requirements.txt, pubspec.yaml)
   ├── Configure .env file
   ├── Setup local database
   └── Verify development environment

2. Branch Strategy (Git Flow)
   ├── main: Production-ready code
   ├── develop: Integration branch
   ├── feature/*: New features (feature/user-authentication)
   ├── bugfix/*: Bug fixes (bugfix/login-error)
   ├── hotfix/*: Production hotfixes (hotfix/critical-security)
   └── release/*: Release preparation (release/v1.0.0)

3. Coding Standards
   ├── Follow PEP 8 (Python) / Effective Dart (Flutter)
   ├── Type hints on all functions (Python)
   ├── Comprehensive docstrings
   ├── Meaningful variable/function names
   ├── Keep functions small (< 50 lines)
   ├── Single Responsibility Principle
   └── DRY (Don't Repeat Yourself)

4. Development Workflow
   ├── 1. Create feature branch from develop
   ├── 2. Write failing test (TDD approach)
   ├── 3. Implement feature/fix
   ├── 4. Make test pass
   ├── 5. Refactor code
   ├── 6. Run linter/formatter
   ├── 7. Run all tests locally
   ├── 8. Commit with descriptive message
   ├── 9. Push to remote branch
   └── 10. Create merge/pull request

5. Commit Message Format
   ```
   <type>(<scope>): <subject>
   
   <body>
   
   <footer>
   ```
   
   Types:
   - feat: New feature
   - fix: Bug fix
   - docs: Documentation changes
   - style: Code style changes (formatting)
   - refactor: Code refactoring
   - test: Adding/updating tests
   - chore: Maintenance tasks
   
   Example:
   ```
   feat(auth): Add JWT token refresh mechanism
   
   Implement automatic token refresh when access token expires.
   Uses refresh token stored in secure storage.
   
   Closes #123
   ```
```

**Deliverables:**
- Working code in feature branch
- Unit tests with >= 80% coverage
- Updated documentation
- Commit history with clear messages

**Quality Gates:**
- ☑️ Code follows style guide
- ☑️ All linter checks pass
- ☑️ Unit tests pass locally
- ☑️ No console errors/warnings
- ☑️ Code coverage >= 80%

---
### Phase 3: Documentation & Tracking (MANDATORY)

```
┌────────────────────────────────────────────────────────────┐
│         PHASE 3: DOCUMENTATION & PROGRESS TRACKING          │
│                    (REQUIRED FOR EVERY CHANGE)              │
└────────────────────────────────────────────────────────────┘

⚠️  CRITICAL RULE: Every code change MUST include documentation updates

1. Documentation Updates (MANDATORY)
   ├── Update relevant .md files in /docs/
   ├── Update API documentation (if endpoints changed)
   ├── Update README.md (if setup/usage changed)
   ├── Update CHANGELOG.md with changes
   ├── Update inline code comments
   └── Update docstrings/JSDoc

2. Progress Tracking Updates (MANDATORY)
   ├── Update PROGRESS_TRACKER.md with:
   │   ├── Date of change
   │   ├── Feature/component updated
   │   ├── Status (In Progress/Completed/Blocked)
   │   ├── Developer name
   │   ├── Lines of code changed
   │   └── Test coverage impact
   ├── Update sprint board (move tickets)
   ├── Update burndown chart
   └── Log time spent in GitLab/Jira

3. Version Control Updates (MANDATORY)
   ├── Update version numbers:
   │   ├── Python: __version__ in __init__.py
   │   ├── Flutter: pubspec.yaml version
   │   ├── API: version in main.py/config.py
   │   └── Documentation: version in headers
   ├── Follow Semantic Versioning (SemVer):
   │   ├── MAJOR.MINOR.PATCH (e.g., 1.2.3)
   │   ├── MAJOR: Breaking changes
   │   ├── MINOR: New features (backward compatible)
   │   └── PATCH: Bug fixes
   ├── Update CHANGELOG.md:
   │   ├── [Unreleased] section for ongoing work
   │   ├── [Version] - Date for releases
   │   ├── Added/Changed/Deprecated/Removed/Fixed/Security
   │   └── Link to commits/issues
   └── Tag releases in Git:
       └── git tag -a v1.2.3 -m "Release version 1.2.3"

4. Automatic Backup After Major Changes (MANDATORY)
   ├── Define "Major Change":
   │   ├── New feature completion (feat commits)
   │   ├── Critical bug fix (hotfix)
   │   ├── Database schema change
   │   ├── API endpoint changes
   │   ├── Security patches
   │   ├── Dependency updates
   │   └── Configuration changes
   ├── Automatic Download Process:
   │   ├── Trigger: After merge to develop/main
   │   ├── Method: GitLab CI/CD job or manual script
   │   ├── Location: ~/Downloads/skincare-ai-backups/
   │   ├── Format: skincare-ai-app-{version}-{date}.zip
   │   ├── Contents: Full source code + docs
   │   └── Retention: Keep last 10 major backups
   └── Backup Script Example:
       ```bash
       #!/bin/bash
       # backup-project.sh
       
       DATE=$(date +%Y%m%d-%H%M%S)
       VERSION=$(grep -m 1 'version' pubspec.yaml | cut -d' ' -f2)
       BACKUP_DIR="$HOME/Downloads/skincare-ai-backups"
       FILENAME="skincare-ai-app-v${VERSION}-${DATE}.zip"
       
       # Create backup directory
       mkdir -p "$BACKUP_DIR"
       
       # Create zip archive (exclude node_modules, .git, etc.)
       zip -r "$BACKUP_DIR/$FILENAME" . \
         -x "*.git*" \
         -x "*node_modules*" \
         -x "*build*" \
         -x "*.env" \
         -x "*__pycache__*" \
         -x "*.pyc"
       
       echo "✅ Backup created: $BACKUP_DIR/$FILENAME"
       
       # Keep only last 10 backups
       cd "$BACKUP_DIR"
       ls -t | tail -n +11 | xargs rm -f
       ```

5. GitLab CI/CD Backup Job (Add to .gitlab-ci.yml):
   ```yaml
   backup-on-major-change:
     stage: deploy
     only:
       - main
       - develop
     script:
       - echo "Creating backup after major change"
       - DATE=$(date +%Y%m%d-%H%M%S)
       - VERSION=$(cat version.txt)
       - FILENAME="skincare-ai-app-v${VERSION}-${DATE}.zip"
       - zip -r $FILENAME . -x "*.git*" -x "*node_modules*"
       - curl --upload-file $FILENAME https://backup-server/upload
     artifacts:
       paths:
         - "*.zip"
       expire_in: 30 days
   ```
```

**MANDATORY CHECKLIST (Before Every Commit):**

- [ ] **Documentation Updated**
  - [ ] README.md updated (if applicable)
  - [ ] API docs updated (if endpoints changed)
  - [ ] Inline comments added/updated
  - [ ] CHANGELOG.md entry added
  - [ ] Architecture diagrams updated (if structure changed)

- [ ] **Progress Tracking Updated**
  - [ ] PROGRESS_TRACKER.md updated with change details
  - [ ] GitLab issue status updated
  - [ ] Sprint board updated
  - [ ] Time logged

- [ ] **Version Control Updated**
  - [ ] Version number incremented (if applicable)
  - [ ] CHANGELOG.md section updated
  - [ ] Git tag created (for releases)
  - [ ] Commit message follows convention

- [ ] **Backup Triggered** (for major changes)
  - [ ] Automatic backup script executed
  - [ ] Backup file created in Downloads folder
  - [ ] Backup verification completed

**Enforcement:**
- CI/CD pipeline will FAIL if:
  - CHANGELOG.md not updated for feature/fix commits
  - Version number not incremented for releases
  - Documentation files not modified with code changes
  - Progress tracker not updated

---

### Phase 4: Testing

```
┌────────────────────────────────────────────────────────────┐
│                    PHASE 4: TESTING                         │
└────────────────────────────────────────────────────────────┘

1. Unit Testing
   ├── Test individual functions/methods
   ├── Target coverage: >= 80%
   ├── Mock external dependencies
   ├── Test edge cases and error handling
   └── Tools: pytest (Python), flutter_test (Flutter)

2. Integration Testing
   ├── Test API endpoints
   ├── Test database operations
   ├── Test service interactions
   └── Tools: pytest with TestClient, integration_test (Flutter)

3. End-to-End Testing
   ├── Test complete user workflows
   ├── Test critical paths
   ├── Test on real devices/browsers
   └── Tools: Selenium, Flutter Driver, Appium

4. Performance Testing
   ├── API response times
   ├── Database query optimization
   ├── ML model inference speed
   └── Tools: Locust, k6, Apache JMeter

5. Security Testing
   ├── SQL injection tests
   ├── XSS vulnerability tests
   ├── Authentication/authorization tests
   ├── Dependency vulnerability scan
   └── Tools: OWASP ZAP, Bandit, Safety
```

**Deliverables:**
- Test reports with >= 80% coverage
- Performance benchmark results
- Security scan reports
- Bug reports (if issues found)

**Quality Gates:**
- ☑️ All tests pass
- ☑️ Code coverage >= 80%
- ☑️ No critical security vulnerabilities
- ☑️ Performance benchmarks met
- ☑️ No memory leaks detected

---
### Phase 5: Code Review

```
┌────────────────────────────────────────────────────────────┐
│                  PHASE 5: CODE REVIEW                       │
└────────────────────────────────────────────────────────────┘

1. Create Merge Request (MR)
   ├── Title: Clear and descriptive
   ├── Description: What, Why, How
   ├── Link related issues (#123)
   ├── Screenshots/videos (if UI changes)
   ├── Checklist completed
   └── Assign reviewers (min 2)

2. Reviewer Checklist
   ├── Code Quality:
   │   ├── Follows coding standards
   │   ├── No code smells
   │   ├── Proper error handling
   │   └── No hardcoded values
   ├── Documentation:
   │   ├── CHANGELOG.md updated
   │   ├── Progress tracker updated
   │   ├── Version updated (if needed)
   │   └── Comments are clear
   ├── Testing:
   │   ├── Tests added for new code
   │   ├── All tests pass
   │   └── Coverage >= 80%
   ├── Security:
   │   ├── No sensitive data exposed
   │   ├── Input validation present
   │   └── Authentication/authorization correct
   └── Performance:
       ├── No N+1 queries
       ├── Efficient algorithms
       └── No memory leaks

3. Review Response Time
   ├── Critical: Within 4 hours
   ├── High: Within 1 day
   ├── Medium: Within 2 days
   └── Low: Within 3 days

4. Approval Process
   ├── Requires: 2 approvals minimum
   ├── Lead developer approval (for architecture changes)
   ├── Security team approval (for auth/security changes)
   └── QA sign-off (for major features)
```

**Quality Gates:**
- ☑️ 2+ approvals received
- ☑️ All conversations resolved
- ☑️ CI/CD pipeline passes
- ☑️ Documentation checklist completed
- ☑️ No merge conflicts

---

### Phase 6: Deployment

```
┌────────────────────────────────────────────────────────────┐
│                   PHASE 6: DEPLOYMENT                        │
└────────────────────────────────────────────────────────────┘

1. Pre-Deployment
   ├── Merge to develop branch
   ├── Run full test suite
   ├── Deploy to staging environment
   ├── Perform smoke tests
   ├── QA approval on staging
   └── Create release branch

2. Release Process
   ├── Update version numbers
   ├── Update CHANGELOG.md
   ├── Create Git tag (v1.2.3)
   ├── Generate release notes
   ├── **Trigger automatic backup to Downloads**
   └── Merge to main branch

3. Deployment Execution
   ├── Automated via GitLab CI/CD
   ├── Database migrations (if needed)
   ├── Blue-green deployment
   ├── Health check verification
   └── Rollback plan ready

4. Post-Deployment
   ├── Monitor error rates
   ├── Check performance metrics
   ├── Verify critical paths
   ├── Update documentation
   ├── Notify stakeholders
   └── **Verify backup created in ~/Downloads/skincare-ai-backups/**
```

---

## MANDATORY RULES SUMMARY

### 📜 Documentation Rules

**RULE 1: Update Documentation with EVERY Code Change**
```
WHEN: Writing new code, changing existing code, or updating features
MUST UPDATE:
  ✅ README.md (if setup/usage changed)
  ✅ API Documentation (if endpoints changed)
  ✅ CHANGELOG.md (always)
  ✅ Inline comments (always)
  ✅ Docstrings/JSDoc (always)
  ✅ Architecture diagrams (if structure changed)
  ✅ Technical specifications (if design changed)

ENFORCEMENT:
  - CI/CD checks for documentation updates
  - Merge request blocked if documentation not updated
  - Code review checklist includes documentation
```

### 📈 Progress Tracking Rules

**RULE 2: Update Progress Tracker with EVERY Code Change**
```
WHEN: Any code commit, feature completion, or bug fix
MUST UPDATE PROGRESS_TRACKER.md WITH:
  ✅ Date: 2025-11-25
  ✅ Developer: [Your Name]
  ✅ Feature/Component: [e.g., "User Authentication"]
  ✅ Status: [In Progress/Completed/Blocked]
  ✅ Lines Added/Modified: [+150/-20]
  ✅ Test Coverage: [85%]
  ✅ Issues Linked: [#123, #124]
  ✅ Notes: [Brief description of changes]

ALSO UPDATE:
  ✅ GitLab issue status
  ✅ Sprint board (move cards)
  ✅ Burndown chart data
  ✅ Time tracking logs

ENFORCEMENT:
  - Pre-commit hook checks for tracker update
  - Daily standup reviews progress tracker
  - Sprint retrospective uses tracker data
```

### 📌 Version Control Rules

**RULE 3: Update Version Numbers with EVERY Release**
```
WHEN: Merging to main/production branch
MUST UPDATE:
  ✅ Python: __version__ in __init__.py
  ✅ Flutter: version in pubspec.yaml
  ✅ API: VERSION in config.py
  ✅ Documentation: version in headers
  ✅ CHANGELOG.md: Add version section
  ✅ Git Tag: Create annotated tag

SEMANTIC VERSIONING:
  - MAJOR: Breaking API changes (1.0.0 → 2.0.0)
  - MINOR: New features, backward compatible (1.0.0 → 1.1.0)
  - PATCH: Bug fixes only (1.0.0 → 1.0.1)

CHANGELOG FORMAT:
  ## [1.2.3] - 2025-11-25
  ### Added
  - New feature X
  ### Changed
  - Updated feature Y
  ### Fixed
  - Bug #123

ENFORCEMENT:
  - CI/CD fails if version not incremented
  - Release script validates version format
  - Automatic CHANGELOG.md validation
```

### 💾 Automatic Backup Rules

**RULE 4: Automatic Backup After EVERY Major Change**
```
WHEN: Major changes are merged
DEFINITION OF MAJOR CHANGE:
  ✅ New feature completed (feat: commits)
  ✅ Critical bug fix (hotfix)
  ✅ Database schema migration
  ✅ API endpoint changes
  ✅ Security patch
  ✅ Dependency major update
  ✅ Configuration changes
  ✅ ML model update

AUTOMATIC BACKUP PROCESS:
  1. Trigger: On merge to develop/main
  2. Script: backup-project.sh executes
  3. Location: ~/Downloads/skincare-ai-backups/
  4. Filename: skincare-ai-app-v{version}-{date}.zip
  5. Contents: Full source + docs (excluding node_modules, .git)
  6. Retention: Keep last 10 backups
  7. Notification: Email/Slack notification sent

BACKUP VERIFICATION:
  ✅ File exists in ~/Downloads/skincare-ai-backups/
  ✅ File size is reasonable (>1MB)
  ✅ Can extract and verify contents
  ✅ Git history preserved

ENFORCEMENT:
  - Post-merge hook triggers backup script
  - CI/CD job creates backup artifact
  - Slack notification confirms backup
  - Weekly backup integrity check
```

---

## Quick Reference: Checklist for Every Code Change

```
┌────────────────────────────────────────────────────────────┐
│           COMPLETE CHECKLIST FOR EVERY CHANGE              │
└────────────────────────────────────────────────────────────┘

BEFORE YOU CODE:
  [ ] Task/issue assigned in GitLab
  [ ] Technical spec reviewed
  [ ] Branch created from develop
  [ ] Local environment verified

WHILE CODING:
  [ ] Follow coding standards (PEP 8 / Effective Dart)
  [ ] Add type hints (Python) / type annotations (Dart)
  [ ] Write unit tests (TDD approach)
  [ ] Add docstrings/comments
  [ ] Keep functions small (<50 lines)
  [ ] Handle errors properly

BEFORE COMMITTING:
  [ ] Run linter (black, flake8, dart format)
  [ ] Run tests locally (all pass)
  [ ] Check code coverage (>=80%)
  [ ] Review your own changes
  [ ] Remove debug code/console.log

DOCUMENTATION (MANDATORY):
  [ ] Update CHANGELOG.md with changes
  [ ] Update README.md (if setup changed)
  [ ] Update API docs (if endpoints changed)
  [ ] Update inline comments
  [ ] Update architecture diagram (if structure changed)

PROGRESS TRACKING (MANDATORY):
  [ ] Update PROGRESS_TRACKER.md:
      [ ] Date and developer name
      [ ] Feature/component name
      [ ] Status update
      [ ] Lines added/modified
      [ ] Test coverage
      [ ] Linked issues
  [ ] Update GitLab issue status
  [ ] Move sprint board card
  [ ] Log time in GitLab

VERSION CONTROL (FOR RELEASES):
  [ ] Increment version number:
      [ ] __init__.py (__version__)
      [ ] pubspec.yaml (version)
      [ ] config.py (VERSION)
      [ ] Document headers
  [ ] Update CHANGELOG.md with version section
  [ ] Create Git tag (git tag -a v1.2.3 -m "...")

COMMIT:
  [ ] Commit message follows convention:
      type(scope): subject
  [ ] Push to remote branch

MERGE REQUEST:
  [ ] Create MR with clear title/description
  [ ] Link related issues
  [ ] Add screenshots (UI changes)
  [ ] Complete MR checklist
  [ ] Assign 2+ reviewers
  [ ] Wait for CI/CD to pass

CODE REVIEW:
  [ ] Address all review comments
  [ ] Get 2+ approvals
  [ ] Resolve all conversations
  [ ] Rebase if needed

MERGE:
  [ ] Merge to develop
  [ ] Delete feature branch
  [ ] **For major changes: Verify backup created**
  [ ] Monitor deployment
  [ ] Close related issues
```

---

## Implementation: Setting Up Automatic Backups

### Step 1: Create Backup Script

**File:** `scripts/backup-project.sh`

```bash
#!/bin/bash
# Skincare AI App - Automatic Backup Script
# Version: 1.0.0
# Purpose: Create automatic backups after major changes

set -e  # Exit on error

# Configuration
DATE=$(date +%Y%m%d-%H%M%S)
VERSION=$(grep -m 1 'version' pubspec.yaml | cut -d' ' -f2 | tr -d '"')
BACKUP_DIR="$HOME/Downloads/skincare-ai-backups"
FILENAME="skincare-ai-app-v${VERSION}-${DATE}.zip"
MAX_BACKUPS=10

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0;m'  # No Color

echo "${YELLOW}Starting backup process...${NC}"

# Create backup directory
mkdir -p "$BACKUP_DIR"
echo "✅ Backup directory created/verified"

# Create zip archive
echo "Creating archive: $FILENAME"
zip -r "$BACKUP_DIR/$FILENAME" . \
  -x "*.git/*" \
  -x "*node_modules/*" \
  -x "*build/*" \
  -x "*.env" \
  -x "*__pycache__/*" \
  -x "*.pyc" \
  -x "*venv/*" \
  -x "*.venv/*" \
  -x "*.idea/*" \
  -x "*.vscode/*" \
  -q  # Quiet mode

echo "${GREEN}✅ Backup created: $BACKUP_DIR/$FILENAME${NC}"

# Get file size
FILE_SIZE=$(du -h "$BACKUP_DIR/$FILENAME" | cut -f1)
echo "Backup size: $FILE_SIZE"

# Keep only last N backups
cd "$BACKUP_DIR"
BACKUP_COUNT=$(ls -1 | wc -l)
if [ $BACKUP_COUNT -gt $MAX_BACKUPS ]; then
  echo "Cleaning old backups (keeping last $MAX_BACKUPS)..."
  ls -t | tail -n +$((MAX_BACKUPS + 1)) | xargs rm -f
  echo "✅ Old backups cleaned"
fi

echo "${GREEN}✅ Backup process completed successfully!${NC}"
echo "Backup location: $BACKUP_DIR/$FILENAME"

# Optional: Send notification (requires curl and webhook URL)
# WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
# curl -X POST -H 'Content-type: application/json' \
#   --data '{"text":"Backup created: '"$FILENAME"'"}' \
#   $WEBHOOK_URL
```

### Step 2: Make Script Executable

```bash
chmod +x scripts/backup-project.sh
```

### Step 3: Add Git Hook (Optional)

**File:** `.git/hooks/post-merge`

```bash
#!/bin/bash
# Post-merge hook to trigger backup on major changes

BRANCH=$(git rev-parse --abbrev-ref HEAD)
LAST_COMMIT=$(git log -1 --pretty=%B)

# Check if this is a major change
if [[ $BRANCH == "main" || $BRANCH == "develop" ]]; then
  if [[ $LAST_COMMIT == feat:* || $LAST_COMMIT == fix:* ]]; then
    echo "Major change detected. Creating backup..."
    ./scripts/backup-project.sh
  fi
fi
```

### Step 4: Add to GitLab CI/CD

**File:** `.gitlab-ci.yml` (add this stage)

```yaml
stages:
  - build
  - test
  - backup
  - deploy

# ... existing stages ...

backup-after-major-change:
  stage: backup
  only:
    - main
    - develop
  script:
    - echo "Creating backup after major change"
    - chmod +x scripts/backup-project.sh
    - ./scripts/backup-project.sh
  artifacts:
    paths:
      - "*.zip"
    expire_in: 30 days
  when: on_success
```

---

## Tools & Resources

### Code Quality Tools

| Tool | Purpose | Command |
|------|---------|----------|
| black | Python code formatter | `black .` |
| flake8 | Python linter | `flake8 backend/` |
| mypy | Python type checker | `mypy backend/` |
| pylint | Python code analyzer | `pylint backend/` |
| dart format | Dart code formatter | `dart format .` |
| dart analyze | Dart analyzer | `dart analyze` |

### Testing Tools

| Tool | Purpose | Command |
|------|---------|----------|
| pytest | Python unit tests | `pytest tests/` |
| pytest-cov | Code coverage | `pytest --cov=backend tests/` |
| flutter test | Flutter unit tests | `flutter test` |
| flutter driver | E2E tests | `flutter drive` |

### Documentation Tools

| Tool | Purpose | Command |
|------|---------|----------|
| mkdocs | Documentation site | `mkdocs serve` |
| sphinx | API documentation | `sphinx-build -b html docs/ build/` |
| dartdoc | Dart documentation | `dart doc .` |

---

## Conclusion

This high-level workflow ensures:

✅ **Consistent Quality**: All code meets standards  
✅ **Complete Documentation**: Always up-to-date  
✅ **Accurate Tracking**: Progress is visible  
✅ **Proper Versioning**: Clear release history  
✅ **Automatic Backups**: Source code protected  
✅ **Reduced Bugs**: Comprehensive testing  
✅ **Faster Reviews**: Clear processes  
✅ **Team Alignment**: Everyone follows same workflow  

**Key Takeaway:** Follow these 4 mandatory rules for EVERY code change:

1. 📜 **Update Documentation**
2. 📈 **Update Progress Tracker**
3. 📌 **Update Version Control**
4. 💾 **Trigger Automatic Backup** (major changes)

By following this workflow religiously, we ensure the Skincare AI App is developed with the highest quality standards.

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-11-25  
**Maintained By:** Skincare AI Development Team  
**Review Cycle:** Monthly  
**Next Review:** 2025-12-25