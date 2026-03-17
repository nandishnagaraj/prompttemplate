Below is a **complete OpenAPI 3.0 specification** for a **Leave Management System**.  
**Assumptions** (derived from a typical PRD):

- **Data Model**: Users (employees), Leave Requests, Leave Types, Approvals.
- **Consumers**: HR admins, employees, managers (via web/mobile apps).
- **Naming Convention**: `camelCase` for fields and paths.
- **Authentication**: JWT Bearer token (OAuth2 compatible).
- **Versioning**: URL prefix (`/v1/`).
- **Pagination**: `page`, `pageSize` query params; `X-Total-Count` header.
- **Rate Limiting**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` headers.
- **Error Envelope**: Standardized error response.

---

```yaml
openapi: 3.0.3
info:
  title: Leave Management System API
  version: "1.0.0"
  description: |
    REST API for managing employee leave requests, approvals, and leave types.
    - All endpoints require authentication via JWT Bearer token.
    - All resource fields use camelCase.
    - All list endpoints are paginated.
    - Rate limiting headers are present on all responses.
    - Versioning via `/v1/` path prefix.

servers:
  - url: https://api.example.com/v1

tags:
  - name: Users
    description: Employee and manager user management
  - name: LeaveRequests
    description: Leave request CRUD and workflow
  - name: LeaveTypes
    description: Leave type management
  - name: Approvals
    description: Leave approval actions

paths:

  /users:
    get:
      tags: [Users]
      summary: List users
      description: Returns a paginated list of users.
      operationId: listUsers
      parameters:
        - $ref: '#/components/parameters/page'
        - $ref: '#/components/parameters/pageSize'
      responses:
        '200':
          description: Paginated list of users
          headers:
            X-Total-Count:
              $ref: '#/components/headers/X-Total-Count'
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []
    post:
      tags: [Users]
      summary: Create a user
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
      responses:
        '201':
          description: User created
          headers:
            Location:
              description: URL of the created user
              schema:
                type: string
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []

  /users/{userId}:
    get:
      tags: [Users]
      summary: Get user by ID
      operationId: getUser
      parameters:
        - $ref: '#/components/parameters/userId'
      responses:
        '200':
          description: User details
          headers:
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []
    patch:
      tags: [Users]
      summary: Update user
      operationId: updateUser
      parameters:
        - $ref: '#/components/parameters/userId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserUpdate'
      responses:
        '200':
          description: Updated user
          headers:
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []
    delete:
      tags: [Users]
      summary: Delete user
      operationId: deleteUser
      parameters:
        - $ref: '#/components/parameters/userId'
      responses:
        '204':
          description: User deleted
          headers:
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []

  /leaveRequests:
    get:
      tags: [LeaveRequests]
      summary: List leave requests
      description: Returns a paginated list of leave requests. Optionally filter by user or status.
      operationId: listLeaveRequests
      parameters:
        - $ref: '#/components/parameters/page'
        - $ref: '#/components/parameters/pageSize'
        - name: userId
          in: query
          description: Filter by user ID
          schema:
            type: string
        - name: status
          in: query
          description: Filter by leave request status
          schema:
            type: string
            enum: [pending, approved, rejected, cancelled]
      responses:
        '200':
          description: Paginated list of leave requests
          headers:
            X-Total-Count:
              $ref: '#/components/headers/X-Total-Count'
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequestList'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []
    post:
      tags: [LeaveRequests]
      summary: Create a leave request
      operationId: createLeaveRequest
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LeaveRequestCreate'
      responses:
        '201':
          description: Leave request created
          headers:
            Location:
              description: URL of the created leave request
              schema:
                type: string
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequest'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []

  /leaveRequests/{leaveRequestId}:
    get:
      tags: [LeaveRequests]
      summary: Get leave request by ID
      operationId: getLeaveRequest
      parameters:
        - $ref: '#/components/parameters/leaveRequestId'
      responses:
        '200':
          description: Leave request details
          headers:
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequest'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []
    patch:
      tags: [LeaveRequests]
      summary: Update leave request
      operationId: updateLeaveRequest
      parameters:
        - $ref: '#/components/parameters/leaveRequestId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LeaveRequestUpdate'
      responses:
        '200':
          description: Updated leave request
          headers:
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequest'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []
    delete:
      tags: [LeaveRequests]
      summary: Cancel leave request
      operationId: cancelLeaveRequest
      parameters:
        - $ref: '#/components/parameters/leaveRequestId'
      responses:
        '204':
          description: Leave request cancelled
          headers:
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []

  /leaveRequests/{leaveRequestId}/approve:
    post:
      tags: [Approvals]
      summary: Approve a leave request
      operationId: approveLeaveRequest
      parameters:
        - $ref: '#/components/parameters/leaveRequestId'
      requestBody:
        required: false
        content:
          application/json:
            schema:
              type: object
              properties:
                comment:
                  type: string
                  maxLength: 500
      responses:
        '200':
          description: Leave request approved
          headers:
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequest'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []

  /leaveRequests/{leaveRequestId}/reject:
    post:
      tags: [Approvals]
      summary: Reject a leave request
      operationId: rejectLeaveRequest
      parameters:
        - $ref: '#/components/parameters/leaveRequestId'
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
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequest'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []

  /leaveTypes:
    get:
      tags: [LeaveTypes]
      summary: List leave types
      operationId: listLeaveTypes
      responses:
        '200':
          description: List of leave types
          headers:
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveTypeList'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []
    post:
      tags: [LeaveTypes]
      summary: Create a leave type
      operationId: createLeaveType
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LeaveTypeCreate'
      responses:
        '201':
          description: Leave type created
          headers:
            Location:
              description: URL of the created leave type
              schema:
                type: string
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveType'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []

  /leaveTypes/{leaveTypeId}:
    get:
      tags: [LeaveTypes]
      summary: Get leave type by ID
      operationId: getLeaveType
      parameters:
        - $ref: '#/components/parameters/leaveTypeId'
      responses:
        '200':
          description: Leave type details
          headers:
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveType'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []
    patch:
      tags: [LeaveTypes]
      summary: Update leave type
      operationId: updateLeaveType
      parameters:
        - $ref: '#/components/parameters/leaveTypeId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LeaveTypeUpdate'
      responses:
        '200':
          description: Updated leave type
          headers:
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveType'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []
    delete:
      tags: [LeaveTypes]
      summary: Delete leave type
      operationId: deleteLeaveType
      parameters:
        - $ref: '#/components/parameters/leaveTypeId'
      responses:
        '204':
          description: Leave type deleted
          headers:
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  parameters:
    userId:
      name: userId
      in: path
      required: true
      schema:
        type: string
      description: User ID
    leaveRequestId:
      name: leaveRequestId
      in: path
      required: true
      schema:
        type: string
      description: Leave request ID
    leaveTypeId:
      name: leaveTypeId
      in: path
      required: true
      schema:
        type: string
      description: Leave type ID
    page:
      name: page
      in: query
      description: Page number (1-based)
      schema:
        type: integer
        minimum: 1
        default: 1
    pageSize:
      name: pageSize
      in: query
      description: Number of items per page
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

  headers:
    X-Total-Count:
      description: Total number of items for pagination
      schema:
        type: integer
    X-RateLimit-Limit:
      description: The maximum number of requests allowed in the current period
      schema:
        type: integer
    X-RateLimit-Remaining:
      description: The number of requests remaining in the current period
      schema:
        type: integer
    X-RateLimit-Reset:
      description: The time at which the current rate limit window resets in UTC epoch seconds
      schema:
        type: integer

  responses:
    Error:
      description: Error response
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorEnvelope'

  schemas:

    # --- User ---
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
          format: email
        firstName:
          type: string
        lastName:
          type: string
        role:
          type: string
          enum: [employee, manager, admin]
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time
        _links:
          type: object
          properties:
            self:
              type: string
            leaveRequests:
              type: string
      required: [id, email, firstName, lastName, role, createdAt, updatedAt, _links]

    UserCreate:
      type: object
      properties:
        email:
          type: string
          format: email
        firstName:
          type: string
          minLength: 1
          maxLength: 100
        lastName:
          type: string
          minLength: 1
          maxLength: 100
        role:
          type: string
          enum: [employee, manager, admin]
      required: [email, firstName, lastName, role]

    UserUpdate:
      type: object
      properties:
        firstName:
          type: string
          minLength: 1
          maxLength: 100
        lastName:
          type: string
          minLength: 1
          maxLength: 100
        role:
          type: string
          enum: [employee, manager, admin]

    UserList:
      type: object
      properties:
        users:
          type: array
          items:
            $ref: '#/components/schemas/User'
        _links:
          type: object
          properties:
            self:
              type: string
            next:
              type: string
            prev:
              type: string
      required: [users, _links]

    # --- Leave Request ---
    LeaveRequest:
      type: object
      properties:
        id:
          type: string
        userId:
          type: string
        leaveTypeId:
          type: string
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
        approverId:
          type: string
          nullable: true
        approvalComment:
          type: string
          nullable: true
        rejectionReason:
          type: string
          nullable: true
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time
        _links:
          type: object
          properties:
            self:
              type: string
            approve:
              type: string
            reject:
              type: string
      required: [id, userId, leaveTypeId, startDate, endDate, status, createdAt, updatedAt, _links]

    LeaveRequestCreate:
      type: object
      properties:
        userId:
          type: string
        leaveTypeId:
          type: string
        startDate:
          type: string
          format: date
        endDate:
          type: string
          format: date
        reason:
          type: string
          maxLength: 500
      required: [userId, leaveTypeId, startDate, endDate, reason]

    LeaveRequestUpdate:
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

    LeaveRequestList:
      type: object
      properties:
        leaveRequests:
          type: array
          items:
            $ref: '#/components/schemas/LeaveRequest'
        _links:
          type: object
          properties:
            self:
              type: string
            next:
              type: string
            prev:
              type: string
      required: [leaveRequests, _links]

    # --- Leave Type ---
    LeaveType:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        description:
          type: string
          maxLength: 200
        isActive:
          type: boolean
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time
        _links:
          type: object
          properties:
            self:
              type: string
      required: [id, name, isActive, createdAt, updatedAt, _links]

    LeaveTypeCreate:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        description:
          type: string
          maxLength: 200
        isActive:
          type: boolean
      required: [name, isActive]

    LeaveTypeUpdate:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        description:
          type: string
          maxLength: 200
        isActive:
          type: boolean

    LeaveTypeList:
      type: object
      properties:
        leaveTypes:
          type: array
          items:
            $ref: '#/components/schemas/LeaveType'
        _links:
          type: object
          properties:
            self:
              type: string
            next:
              type: string
            prev:
              type: string
      required: [leaveTypes, _links]

    # --- Error Envelope ---
    ErrorEnvelope:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
              description: Application-specific error code
            message:
              type: string
              description: Human-readable error message
            details:
              type: object
              description: Optional error details
      required: [error]

```

---

**Key Features:**

- **CRUD** for Users, Leave Requests, Leave Types.
- **Domain endpoints**: Approve/Reject leave requests.
- **JWT/OAuth2** authentication.
- **Standard error envelope**.
- **Rate limiting** headers.
- **Pagination** for list endpoints.
- **Versioning** via `/v1/`.
- **HATEOAS** links in resource representations.
- **camelCase** naming throughout.

---

**You can copy-paste this YAML into Swagger Editor or similar tools.**  
Let me know if you need a Postman collection or further customization!