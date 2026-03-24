# DES-03 — OpenAPI / REST Contract Generation

**Purpose:** Generate a complete OpenAPI 3.0 spec with auth, errors, rate limits, pagination, versioning.

```text
Design a REST API for this feature:

Feature: [FEATURE DESCRIPTION]
Data Model: [PASTE RELEVANT SCHEMA]
Consumers: [WHO CALLS THIS API — frontend, mobile, third parties]

Generate a complete OpenAPI 3.0 specification including:
1. All CRUD and domain-specific endpoints
2. Request/response schemas with validation rules
3. Authentication/authorization requirements (JWT/OAuth2)
4. Error response models (standard error envelope)
5. Rate limiting headers
6. Pagination pattern for list endpoints
7. Versioning strategy

Follow REST best practices:
- Correct HTTP verbs and status codes
- Plural nouns for resources
- Consistent naming (snake_case or camelCase — specify which)
- HATEOAS links where appropriate
```
