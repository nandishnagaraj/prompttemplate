# REL-01 — Release Readiness Check (GO/NO-GO)

**Purpose:** Evaluate readiness, blockers, and risks for releasing a feature/version.

```text
Perform a release readiness assessment for:

Feature: [FEATURE NAME]
Version: [VERSION NUMBER]
Release type: [MAJOR / MINOR / PATCH / HOTFIX]

Checklist inputs:
- User stories completed: [LIST US IDs]
- Test coverage: [PERCENTAGE]
- Known open bugs: [BUG LIST OR "None"]
- Performance test results: [RESULTS SUMMARY]
- Security scan results: [PASS/FINDINGS SUMMARY]
- Documentation status: [COMPLETE / IN PROGRESS]

Evaluate readiness across:
1. Functional completeness (all stories done and verified)
2. Quality gates (coverage, no critical bugs)
3. Non-functional requirements met
4. Rollback plan defined
5. Monitoring and alerting configured
6. Runbook updated
7. Stakeholder sign-off obtained

Output: GO / NO-GO recommendation with specific blockers.
```
