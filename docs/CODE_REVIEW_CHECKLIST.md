# CODE REVIEW CHECKLIST

## Comprehensive Code Review Standards for Skincare AI App

**Status:** Active Enforcement  
**Authority:** Skincare AI Development Team Lead  
**Effective Date:** 2025-11-25  
**Review Frequency:** Per Pull Request

---

## Overview

This document provides a comprehensive checklist for conducting code reviews in the Skincare AI App project. All code reviews MUST follow this checklist per NON_NEGOTIABLE_RULE #7 (Zero merges without 2+ approvals).

**Critical:** Minimum 2 approvals required. Reviewers MUST check EVERY item. No shortcuts.

---

## Pre-Review Validation

### Initial Checks

- [ ] PR has descriptive title and follows naming conventions
- [ ] PR description is complete and comprehensive
- [ ] All related issues are linked
- [ ] PR is associated with correct project board
- [ ] Branch name follows convention: `feat/name`, `fix/name`, `docs/name`
- [ ] Source branch is `develop`, not `main`
- [ ] Target branch is `develop` or `hotfix` (never `main`)
- [ ] PR is not marked as Draft (unless intentional)
- [ ] No conflicts with target branch
- [ ] All CI/CD checks are passing

### Reviewer Qualification

- [ ] Reviewer has reviewed similar code before
- [ ] Reviewer understands the feature/fix scope
- [ ] Reviewer has no conflicts of interest
- [ ] Reviewer has reviewed related documentation
- [ ] Second reviewer is different person than first reviewer

---

## Code Quality Review

### Architecture & Design

- [ ] Changes align with ARCHITECTURE_DIAGRAM.md
- [ ] No unnecessary architectural changes
- [ ] Follows established design patterns
- [ ] No circular dependencies introduced
- [ ] API changes are backward compatible (or properly versioned)
- [ ] Database schema changes are properly migrated
- [ ] New classes/functions follow SRP (Single Responsibility Principle)

### Code Standards Compliance

**Python:**
- [ ] Follows PEP 8 (verified with pylint/flake8)
- [ ] Uses type hints on all functions and variables
- [ ] No hardcoded magic numbers or strings
- [ ] Docstrings present and accurate
- [ ] Meaningful variable names used
- [ ] No commented-out code
- [ ] Line length under 88 characters (Black formatter standard)

**JavaScript/TypeScript:**
- [ ] Passes ESLint checks
- [ ] Uses Prettier formatting (line length 100)
- [ ] Uses TypeScript for type safety
- [ ] No `any` type without justification
- [ ] JSDoc comments for public functions
- [ ] No console.log in production code
- [ ] Proper error handling

**Dart/Flutter:**
- [ ] Follows Dart style guide
- [ ] Runs `flutter format` cleanly
- [ ] Documentation comments present
- [ ] Uses const constructors where possible
- [ ] No deprecated API usage
- [ ] Lint warnings resolved

### Code Logic & Correctness

- [ ] Logic is clear and understandable
- [ ] Edge cases are handled
- [ ] Error conditions are managed
- [ ] No off-by-one errors
- [ ] Loop conditions are correct
- [ ] Return values are correct
- [ ] No unreachable code
- [ ] Null/undefined values handled
- [ ] Type conversions are safe
- [ ] No race conditions (async code)

### Performance Review

- [ ] No obvious performance issues
- [ ] Algorithms use appropriate complexity
- [ ] No N+1 query problems
- [ ] Database queries are optimized
- [ ] Caching used appropriately
- [ ] No memory leaks
- [ ] Large data sets handled efficiently
- [ ] API response times acceptable
- [ ] No blocking operations on main thread (UI)

### Security Review

**CRITICAL - Every PR must pass security checks**

- [ ] No hardcoded credentials, API keys, or secrets
- [ ] No sensitive data logged
- [ ] Input validation present for all user inputs
- [ ] SQL queries use parameterized statements
- [ ] XSS vulnerabilities prevented (if web)
- [ ] CSRF protection implemented (if needed)
- [ ] Authentication properly enforced
- [ ] Authorization checks in place
- [ ] No privilege escalation vulnerabilities
- [ ] Encryption used for sensitive data
- [ ] HTTPS enforced (if applicable)
- [ ] No exposure of internal error details
- [ ] Dependencies are up-to-date
- [ ] No known vulnerable versions in use
- [ ] Sensitive data not exposed in version control
- [ ] File permissions are correct

---

## Testing Requirements

### Unit Tests

- [ ] All new functions have unit tests
- [ ] All modified functions have updated tests
- [ ] Test coverage is >= 80% (check coverage report)
- [ ] Coverage did not decrease
- [ ] Edge cases are tested
- [ ] Error conditions are tested
- [ ] Tests use descriptive names
- [ ] Tests are isolated (no interdependencies)
- [ ] Mock objects used appropriately
- [ ] No hardcoded test data
- [ ] Tests run successfully locally
- [ ] Tests run successfully in CI/CD

### Integration Tests

- [ ] Integration tests present for component interactions
- [ ] Database integration tested (if applicable)
- [ ] API endpoints tested (if applicable)
- [ ] External service integrations tested (if applicable)
- [ ] Data flow between components correct

### E2E Tests

- [ ] Critical user workflows tested (if applicable)
- [ ] E2E tests are stable and reliable
- [ ] No flaky tests
- [ ] Cross-browser compatibility verified (if web)
- [ ] Mobile responsiveness tested (if applicable)

---

## Documentation Review

### Code Documentation

- [ ] All public functions have docstrings
- [ ] All classes have docstrings
- [ ] All modules have docstrings
- [ ] Type hints are accurate
- [ ] Docstrings are clear and helpful
- [ ] Complex logic has inline comments
- [ ] No outdated comments
- [ ] README updated (if applicable)
- [ ] API documentation updated (if applicable)
- [ ] Architecture documentation updated (if applicable)

### External Documentation

- [ ] ARCHITECTURE_DIAGRAM.md updated (if structural change)
- [ ] DEVELOPMENT_WORKFLOW.md updated (if process change)
- [ ] CHANGELOG.md updated with user-facing changes
- [ ] PROGRESS_TRACKER.md updated with progress
- [ ] Version number updated (if release)

---

## Change Scope Review

- [ ] Changes are within stated PR scope
- [ ] No scope creep or unrelated changes
- [ ] Commits are logical and atomic
- [ ] No unnecessary refactoring mixed with feature code
- [ ] Breaking changes clearly documented
- [ ] Deprecations properly marked
- [ ] Migration path clear (if applicable)

---

## Commit Quality Review

- [ ] Commit messages follow Conventional Commits
- [ ] Commit messages are clear and descriptive
- [ ] Each commit is logical and standalone
- [ ] No commits with generic messages ("fix", "update")
- [ ] Issue references in commit messages
- [ ] No accidental commits (debug code, secrets)
- [ ] Commit history is clean (no merge commits)

---

## Dependency Review

- [ ] New dependencies are justified
- [ ] Dependency versions are pinned appropriately
- [ ] Dependencies have no known vulnerabilities
- [ ] Dependencies are actively maintained
- [ ] No duplicate dependencies
- [ ] Dependency licenses are compatible
- [ ] Lock files are updated correctly

---

## Database Changes

*(If applicable)*

- [ ] Schema changes are backward compatible
- [ ] Migration scripts are provided
- [ ] Migration scripts are tested
- [ ] Rollback procedures documented
- [ ] Data migration handled properly
- [ ] Indexes are appropriate
- [ ] No performance regression
- [ ] Constraints are proper

---

## Configuration Changes

*(If applicable)*

- [ ] `.env.example` updated
- [ ] Configuration keys documented
- [ ] Default values are sensible
- [ ] No secrets in configuration files
- [ ] Environment-specific configs handled
- [ ] Configuration loading robust

---

## Deployment & Release

*(If applicable)*

- [ ] Version number incremented correctly (semantic versioning)
- [ ] Release notes prepared
- [ ] Breaking changes documented
- [ ] Deployment instructions clear
- [ ] Rollback procedure documented
- [ ] Database migrations documented
- [ ] Environment variables documented
- [ ] Dependencies updated

---

## Final Approval Checklist

### Before Approving

- [ ] All above items reviewed thoroughly
- [ ] All CI/CD checks passing
- [ ] Coverage reports reviewed
- [ ] No blocking issues found
- [ ] Code quality is acceptable
- [ ] No security concerns
- [ ] Testing is comprehensive
- [ ] Documentation is complete
- [ ] Changes align with project standards
- [ ] Reviewed by 2nd person (if first review)

### Approval Comment Template

```markdown
## Code Review Approval

✅ **Approved by:** @username  
**Date:** YYYY-MM-DD  
**Review Time:** X minutes  

### Summary
[Brief summary of changes]

### Strengths
- [Good aspects of the implementation]

### Minor Notes
- [Optional: minor suggestions or observations]

### Verdict
**APPROVED** - Ready to merge
```

### Rejection Comment Template

```markdown
## Code Review Feedback

⚠️ **Changes Requested by:** @username  
**Date:** YYYY-MM-DD  

### Issues Found
1. [Issue 1 - explain why it's a problem]
2. [Issue 2 - suggest solution]
3. [Issue 3 - reference relevant standards]

### Required Changes
- [ ] Address issue 1 by [specific action]
- [ ] Address issue 2 by [specific action]
- [ ] Address issue 3 by [specific action]

### Re-review
Please re-request review once changes are made.

**Status:** REQUEST CHANGES
```

---

## Review Time Guidelines

- **Small changes (< 50 lines):** 5-15 minutes
- **Medium changes (50-200 lines):** 15-30 minutes
- **Large changes (200-500 lines):** 30-60 minutes
- **Very large changes (> 500 lines):** 60+ minutes

**Note:** Larger reviews should be split across multiple PRs if possible.

---

## Common Issues to Watch For

### Code Quality Issues

- Inconsistent formatting or naming
- Missing error handling
- Insufficient validation of user input
- Hardcoded values or strings
- Overly complex functions
- Duplicate code not refactored

### Security Issues

- Credentials in code or config files
- Insufficient input validation
- SQL injection vulnerabilities
- XSS vulnerabilities
- Insecure deserialization
- Inadequate authentication/authorization

### Performance Issues

- N+1 database queries
- Inefficient algorithms
- Memory leaks
- Blocking operations
- Unnecessary processing
- Missing caching

### Testing Issues

- Missing test cases
- Low code coverage
- Inadequate edge case testing
- Flaky tests
- Tests that don't test the code

---

## Special Review Scenarios

### Security-Critical Code

- [ ] **MANDATORY:** 2+ security-trained reviewers
- [ ] Threat modeling reviewed
- [ ] Security best practices followed
- [ ] Penetration testing considered
- [ ] External security audit considered (if critical)

### ML/AI Model Changes

- [ ] Model accuracy verified on test set
- [ ] Edge cases tested (diverse skin tones, etc.)
- [ ] Performance benchmarked
- [ ] Fairness assessed
- [ ] Bias analysis completed

### Database Migration

- [ ] Forward migration tested
- [ ] Rollback migration tested
- [ ] Data loss prevented
- [ ] Performance impact assessed
- [ ] Downtime minimized

### API Changes

- [ ] Backward compatibility maintained
- [ ] Versioning strategy clear
- [ ] Documentation updated
- [ ] Deprecation path provided
- [ ] Client code compatibility verified

---

## Review Process Enforcement

### Branch Protection Rules

**ENFORCED AT GIT LEVEL:**
- Minimum 2 approvals required before merge
- All status checks must pass
- No dismissing stale reviews
- Reviewers must be code owners
- No force pushes to main/develop
- PR must be mergeable

### Escalation Process

**If reviews are delayed (> 24 hours):**
1. Ping reviewers in PR comment
2. Escalate to team lead
3. Team lead assigns alternative reviewer
4. Ensure no reviews get stuck

---

## Reviewer Tools & Resources

- GitLab's built-in code review features
- Code quality tools (SonarQube, Codecov)
- Security scanning (GitLab SAST/DAST)
- Performance monitoring tools
- Test coverage reports
- Architecture documentation
- Style guide references

---

## NON-NEGOTIABLE REMINDER

**Per NON_NEGOTIABLE_RULE #7: Zero merges without 2+ approvals**

This is absolute. No exceptions. No shortcuts. Every PR must have 2 independent approvals from qualified reviewers who have completed this entire checklist.

---

## Final Statement

Code review is critical to project success. Use this checklist thoroughly. Do not skip items. Quality over speed. A few extra minutes reviewing prevents hours debugging production issues.

Thank you for maintaining our high standards.