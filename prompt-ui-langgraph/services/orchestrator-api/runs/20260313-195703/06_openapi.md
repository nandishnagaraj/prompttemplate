Certainly! Below is a **complete OpenAPI 3.0 specification** for a **Leave Management System**.  
Assumptions are made for the data model and consumers (e.g., HR staff, employees, managers).

---

## **OpenAPI 3.0 Specification — Leave Management System**

**Conventions:**
- **Naming:** `camelCase`
- **Versioning:** `/v1` in path
- **Auth:** JWT Bearer (OAuth2 compatible)
- **Pagination:** `page`, `pageSize`, `totalCount`, `links`
- **Rate Limiting:** `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- **Error Envelope:** `{ error: { code, message, details } }`
- **HATEOAS:** `links` in responses

---

```yaml
openapi: 3.0.3
info:
  title: Leave Management System API
  version: "1.0.0"
  description: |
    REST API for managing employee leave requests, approvals, and balances.
    - Naming: camelCase
    - Versioning: /v1
    - Auth: JWT Bearer
    - Pagination: page, pageSize, totalCount, links
    - Rate Limiting: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset

servers:
  - url: https://api.example.com/v1

tags:
  - name: Leaves
    description: Manage leave requests
  - name: LeaveTypes
    description: Manage leave types (e.g., vacation, sick)
  - name: Balances
    description: View leave balances
  - name: Users
    description: Manage users (employees, managers)

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  parameters:
    Page:
      in: query
      name: page
      schema:
        type: integer
        minimum: 1
        default: 1
      description: Page number for pagination
    PageSize:
      in: query
      name: pageSize
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20
      description: Number of items per page

  responses:
    UnauthorizedError:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorEnvelope'
    ForbiddenError:
      description: Insufficient permissions
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorEnvelope'
    NotFoundError:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorEnvelope'
    RateLimitError:
      description: Rate limit exceeded
      headers:
        Retry-After:
          schema:
            type: integer
            description: Seconds until more requests are allowed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorEnvelope'

  schemas:
    ErrorEnvelope:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
              example: "not_found"
            message:
              type: string
              example: "Resource not found"
            details:
              type: object
              nullable: true
          required: [code, message]
      required: [error]

    HATEOASLinks:
      type: object
      additionalProperties:
        type: object
        properties:
          href:
            type: string
            format: uri
          method:
            type: string
            enum: [GET, POST, PUT, PATCH, DELETE]
        required: [href, method]

    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        role:
          type: string
          enum: [employee, manager, hr]
        createdAt:
          type: string
          format: date-time
        links:
          $ref: '#/components/schemas/HATEOASLinks'
      required: [id, email, name, role, createdAt]

    LeaveType:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
          example: "Vacation"
        description:
          type: string
        isActive:
          type: boolean
        createdAt:
          type: string
          format: date-time
        links:
          $ref: '#/components/schemas/HATEOASLinks'
      required: [id, name, isActive, createdAt]

    LeaveRequest:
      type: object
      properties:
        id:
          type: string
          format: uuid
        userId:
          type: string
          format: uuid
        leaveTypeId:
          type: string
          format: uuid
        startDate:
          type: string
          format: date
        endDate:
          type: string
          format: date
        status:
          type: string
          enum: [pending, approved, rejected, cancelled]
        reason:
          type: string
          maxLength: 500
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time
        approverId:
          type: string
          format: uuid
          nullable: true
        links:
          $ref: '#/components/schemas/HATEOASLinks'
      required: [id, userId, leaveTypeId, startDate, endDate, status, createdAt, updatedAt]

    LeaveBalance:
      type: object
      properties:
        userId:
          type: string
          format: uuid
        leaveTypeId:
          type: string
          format: uuid
        balance:
          type: number
          format: float
        asOf:
          type: string
          format: date
        links:
          $ref: '#/components/schemas/HATEOASLinks'
      required: [userId, leaveTypeId, balance, asOf]

    PaginatedLeaveRequestList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/LeaveRequest'
        page:
          type: integer
        pageSize:
          type: integer
        totalCount:
          type: integer
        links:
          $ref: '#/components/schemas/HATEOASLinks'
      required: [items, page, pageSize, totalCount, links]

    PaginatedLeaveTypeList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/LeaveType'
        page:
          type: integer
        pageSize:
          type: integer
        totalCount:
          type: integer
        links:
          $ref: '#/components/schemas/HATEOASLinks'
      required: [items, page, pageSize, totalCount, links]

    PaginatedUserList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/User'
        page:
          type: integer
        pageSize:
          type: integer
        totalCount:
          type: integer
        links:
          $ref: '#/components/schemas/HATEOASLinks'
      required: [items, page, pageSize, totalCount, links]

    CreateLeaveRequest:
      type: object
      properties:
        leaveTypeId:
          type: string
          format: uuid
        startDate:
          type: string
          format: date
        endDate:
          type: string
          format: date
        reason:
          type: string
          maxLength: 500
      required: [leaveTypeId, startDate, endDate]

    UpdateLeaveRequest:
      type: object
      properties:
        startDate:
          type: string
          format: date
        endDate:
          type: string
          format: date
        reason:
          type: string
          maxLength: 500

    CreateLeaveType:
      type: object
      properties:
        name:
          type: string
        description:
          type: string
        isActive:
          type: boolean
      required: [name, isActive]

    UpdateLeaveType:
      type: object
      properties:
        name:
          type: string
        description:
          type: string
        isActive:
          type: boolean

    CreateUser:
      type: object
      properties:
        email:
          type: string
          format: email
        name:
          type: string
        role:
          type: string
          enum: [employee, manager, hr]
      required: [email, name, role]

    UpdateUser:
      type: object
      properties:
        name:
          type: string
        role:
          type: string
          enum: [employee, manager, hr]

security:
  - BearerAuth: []

paths:

  # --- LEAVE REQUESTS ---
  /leaves:
    get:
      tags: [Leaves]
      summary: List leave requests
      description: List leave requests. Employees see their own; managers/HR can filter by user.
      parameters:
        - $ref: '#/components/parameters/Page'
        - $ref: '#/components/parameters/PageSize'
        - in: query
          name: userId
          schema:
            type: string
            format: uuid
          description: Filter by user (manager/HR only)
        - in: query
          name: status
          schema:
            type: string
            enum: [pending, approved, rejected, cancelled]
          description: Filter by status
      responses:
        '200':
          description: Paginated list of leave requests
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedLeaveRequestList'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

    post:
      tags: [Leaves]
      summary: Create a leave request
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateLeaveRequest'
      responses:
        '201':
          description: Leave request created
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequest'
        '400':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorEnvelope'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

  /leaves/{leaveId}:
    get:
      tags: [Leaves]
      summary: Get a leave request
      parameters:
        - in: path
          name: leaveId
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Leave request details
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequest'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '404':
          $ref: '#/components/responses/NotFoundError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

    patch:
      tags: [Leaves]
      summary: Update a leave request (employee can edit if pending)
      parameters:
        - in: path
          name: leaveId
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateLeaveRequest'
      responses:
        '200':
          description: Updated leave request
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequest'
        '400':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorEnvelope'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '404':
          $ref: '#/components/responses/NotFoundError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

    delete:
      tags: [Leaves]
      summary: Cancel a leave request (employee can cancel if pending)
      parameters:
        - in: path
          name: leaveId
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: Leave request cancelled
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '404':
          $ref: '#/components/responses/NotFoundError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

  /leaves/{leaveId}/approve:
    post:
      tags: [Leaves]
      summary: Approve a leave request (manager/HR only)
      parameters:
        - in: path
          name: leaveId
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Leave request approved
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequest'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '404':
          $ref: '#/components/responses/NotFoundError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

  /leaves/{leaveId}/reject:
    post:
      tags: [Leaves]
      summary: Reject a leave request (manager/HR only)
      parameters:
        - in: path
          name: leaveId
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                reason:
                  type: string
                  maxLength: 500
              required: [reason]
      responses:
        '200':
          description: Leave request rejected
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequest'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '404':
          $ref: '#/components/responses/NotFoundError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

  # --- LEAVE TYPES ---
  /leave_types:
    get:
      tags: [LeaveTypes]
      summary: List leave types
      parameters:
        - $ref: '#/components/parameters/Page'
        - $ref: '#/components/parameters/PageSize'
      responses:
        '200':
          description: Paginated list of leave types
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedLeaveTypeList'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

    post:
      tags: [LeaveTypes]
      summary: Create a leave type (HR only)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateLeaveType'
      responses:
        '201':
          description: Leave type created
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveType'
        '400':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorEnvelope'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

  /leave_types/{leaveTypeId}:
    get:
      tags: [LeaveTypes]
      summary: Get a leave type
      parameters:
        - in: path
          name: leaveTypeId
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Leave type details
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveType'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '404':
          $ref: '#/components/responses/NotFoundError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

    patch:
      tags: [LeaveTypes]
      summary: Update a leave type (HR only)
      parameters:
        - in: path
          name: leaveTypeId
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateLeaveType'
      responses:
        '200':
          description: Updated leave type
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveType'
        '400':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorEnvelope'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '404':
          $ref: '#/components/responses/NotFoundError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

    delete:
      tags: [LeaveTypes]
      summary: Delete a leave type (HR only)
      parameters:
        - in: path
          name: leaveTypeId
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: Leave type deleted
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '404':
          $ref: '#/components/responses/NotFoundError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

  # --- LEAVE BALANCES ---
  /users/{userId}/leave_balances:
    get:
      tags: [Balances]
      summary: Get leave balances for a user
      parameters:
        - in: path
          name: userId
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: List of leave balances
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/LeaveBalance'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '404':
          $ref: '#/components/responses/NotFoundError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

  # --- USERS ---
  /users:
    get:
      tags: [Users]
      summary: List users (HR only)
      parameters:
        - $ref: '#/components/parameters/Page'
        - $ref: '#/components/parameters/PageSize'
        - in: query
          name: role
          schema:
            type: string
            enum: [employee, manager, hr]
          description: Filter by role
      responses:
        '200':
          description: Paginated list of users
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedUserList'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

    post:
      tags: [Users]
      summary: Create a user (HR only)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUser'
      responses:
        '201':
          description: User created
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorEnvelope'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

  /users/{userId}:
    get:
      tags: [Users]
      summary: Get a user (HR only)
      parameters:
        - in: path
          name: userId
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: User details
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '404':
          $ref: '#/components/responses/NotFoundError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

    patch:
      tags: [Users]
      summary: Update a user (HR only)
      parameters:
        - in: path
          name: userId
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUser'
      responses:
        '200':
          description: Updated user
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorEnvelope'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '404':
          $ref: '#/components/responses/NotFoundError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []

    delete:
      tags: [Users]
      summary: Delete a user (HR only)
      parameters:
        - in: path
          name: userId
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: User deleted
          headers:
            X-RateLimit-Limit:
              schema: { type: integer }
            X-RateLimit-Remaining:
              schema: { type: integer }
            X-RateLimit-Reset:
              schema: { type: integer }
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '403':
          $ref: '#/components/responses/ForbiddenError'
        '404':
          $ref: '#/components/responses/NotFoundError'
        '429':
          $ref: '#/components/responses/RateLimitError'
      security:
        - BearerAuth: []
```

---

**This contract covers:**
- All CRUD and domain endpoints for leaves, leave types, balances, users
- Request/response schemas with validation
- JWT Bearer authentication
- Standard error envelope
- Rate limiting headers
- Pagination for list endpoints
- Versioning via `/v1`
- HATEOAS links in resource responses

**You can copy/paste this YAML into Swagger Editor or Redocly for visualization.**  
Let me know if you need further customization!