# TEST-02 — Integration & API Test Generation

**Purpose:** Generate integration tests from API contracts + DB schema + auth.

```text
Generate integration tests for this API endpoint:

Endpoint: [METHOD] [PATH]
API Contract: [PASTE OPENAPI SPEC SECTION]
Database: [DB TYPE AND RELEVANT TABLES]
Auth: [AUTH MECHANISM]

Testing framework: [SUPERTEST / PYTEST / POSTMAN / etc.]

Generate tests for:
1. Successful request with valid data
2. Authentication failure scenarios (missing/invalid token)
3. Authorization failure (valid token, insufficient permissions)
4. Input validation failures (each invalid field)
5. Database constraint violations
6. Concurrent request handling
7. Response schema validation

Each test should:
- Set up required test data
- Make the HTTP request
- Assert status code, response body, and headers
- Clean up test data (teardown)
```
