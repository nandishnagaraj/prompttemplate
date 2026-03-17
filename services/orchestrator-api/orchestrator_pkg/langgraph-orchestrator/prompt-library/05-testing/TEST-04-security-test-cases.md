# TEST-04 — Security Test Case Generation (OWASP-oriented)

**Purpose:** Generate security-focused tests aligned to OWASP categories.

```text
Generate security-focused test cases for:

Feature: [FEATURE DESCRIPTION]
Endpoint(s): [LIST ENDPOINTS]
Auth mechanism: [JWT / OAuth / Session]
Data sensitivity: [PII / Financial / Public]

Generate test cases covering OWASP Top 10:
1. SQL/NoSQL Injection attempts
2. XSS payload inputs
3. Authentication bypass attempts
4. Authorization / IDOR vulnerabilities
5. Mass assignment vulnerabilities
6. Sensitive data exposure scenarios
7. JWT manipulation (alg:none, expired tokens)
8. Rate limiting bypass
9. Input length/type boundary attacks
10. CSRF scenarios (if applicable)

Format as: Test ID | Category | Input | Expected Behavior | Pass Criteria
```
