# DEV-02 — AI Code Review

**Purpose:** Run a systematic PR review across correctness, security, perf, design, testability, maintainability, and AC compliance.

```text
You are a senior engineer performing a thorough code review.

PR Context: [PR TITLE AND DESCRIPTION]
User Story: [US-### description]

Code changes:
<diff>
[PASTE GIT DIFF OR FULL FILE]
</diff>

Review against these criteria:
1. CORRECTNESS — Logic errors, off-by-one, null safety
2. SECURITY — Injection, auth bypass, sensitive data exposure
3. PERFORMANCE — Unnecessary DB calls, memory leaks, sync blocking
4. DESIGN — SOLID principles, appropriate patterns, coupling
5. TESTABILITY — Is this easily testable? Are edge cases handled?
6. MAINTAINABILITY — Readability, naming, complexity
7. COMPLIANCE — Does it match the acceptance criteria?

Format findings as:

[SEVERITY: Critical/High/Medium/Low] — [CATEGORY]
Line: [LINE NUMBER]
Issue: [DESCRIPTION]
Suggestion: [SPECIFIC FIX OR IMPROVEMENT]
```
