Certainly! Below is a **complete OpenAPI 3.0 specification** for a **Leave Management System**.  
Assumptions are made for the data model and consumers, based on standard leave management requirements.

---

## Assumptions

**Data Model (Entities):**
- **User**: Employee or manager.
- **LeaveRequest**: A request for leave.
- **LeaveType**: e.g., Annual, Sick, Unpaid.
- **Approval**: Manager approval/rejection.

**Consumers:**
- Internal HR systems
- Employee/manager web/mobile apps

**Naming Convention:** `camelCase`

**Versioning:** URL prefix `/v1/`

---

# OpenAPI 3.0 Specification (YAML)

```yaml
openapi: 3.0.3
info:
  title: Leave Management System API
  version: "1.0.0"
  description: |
    REST API for managing employee leave requests, approvals, and leave types.
    - Auth: JWT Bearer
    - Versioning: URL prefix `/v1/`
    - Naming: camelCase
    - Pagination: `page`, `pageSize`, `totalCount`, `links`
    - Rate limiting: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
servers:
  - url: https://api.example.com/v1
security:
  - bearerAuth: []

tags:
  - name: Users
  - name: LeaveRequests
  - name: LeaveTypes
  - name: Approvals

paths:
  /users:
    get:
      tags: [Users]
      summary: List users
      operationId: listUsers
      parameters:
        - $ref: '#/components/parameters/page'
        - $ref: '#/components/parameters/pageSize'
      responses:
        '200':
          description: List of users
          headers:
            X-RateLimit-Limit: { $ref: '#/components/headers/RateLimitLimit' }
            X-RateLimit-Remaining: { $ref: '#/components/headers/RateLimitRemaining' }
            X-RateLimit-Reset: { $ref: '#/components/headers/RateLimitReset' }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
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
              $ref: '#/components/schemas/UserCreateRequest'
      responses:
        '201':
          description: User created
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
              $ref: '#/components/schemas/UserUpdateRequest'
      responses:
        '200':
          description: User updated
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
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []

  /leave_requests:
    get:
      tags: [LeaveRequests]
      summary: List leave requests
      operationId: listLeaveRequests
      parameters:
        - $ref: '#/components/parameters/page'
        - $ref: '#/components/parameters/pageSize'
        - in: query
          name: status
          schema:
            type: string
            enum: [pending, approved, rejected, cancelled]
          description: Filter by status
        - in: query
          name: userId
          schema:
            type: string
          description: Filter by user
      responses:
        '200':
          description: List of leave requests
          headers:
            X-RateLimit-Limit: { $ref: '#/components/headers/RateLimitLimit' }
            X-RateLimit-Remaining: { $ref: '#/components/headers/RateLimitRemaining' }
            X-RateLimit-Reset: { $ref: '#/components/headers/RateLimitReset' }
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequestListResponse'
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
              $ref: '#/components/schemas/LeaveRequestCreateRequest'
      responses:
        '201':
          description: Leave request created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequest'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []

  /leave_requests/{leaveRequestId}:
    get:
      tags: [LeaveRequests]
      summary: Get leave request by ID
      operationId: getLeaveRequest
      parameters:
        - $ref: '#/components/parameters/leaveRequestId'
      responses:
        '200':
          description: Leave request details
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
              $ref: '#/components/schemas/LeaveRequestUpdateRequest'
      responses:
        '200':
          description: Leave request updated
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
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []

  /leave_requests/{leaveRequestId}/approve:
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
              $ref: '#/components/schemas/ApprovalRequest'
      responses:
        '200':
          description: Leave request approved
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequest'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []

  /leave_requests/{leaveRequestId}/reject:
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
              $ref: '#/components/schemas/ApprovalRequest'
      responses:
        '200':
          description: Leave request rejected
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveRequest'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []

  /leave_types:
    get:
      tags: [LeaveTypes]
      summary: List leave types
      operationId: listLeaveTypes
      responses:
        '200':
          description: List of leave types
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveTypeListResponse'
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
              $ref: '#/components/schemas/LeaveTypeCreateRequest'
      responses:
        '201':
          description: Leave type created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LeaveType'
        default:
          $ref: '#/components/responses/Error'
      security:
        - bearerAuth: []

  /leave_types/{leaveTypeId}:
    get:
      tags: [LeaveTypes]
      summary: Get leave type by ID
      operationId: getLeaveType
      parameters:
        - $ref: '#/components/parameters/leaveTypeId'
      responses:
        '200':
          description: Leave type details
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
              $ref: '#/components/schemas/LeaveTypeUpdateRequest'
      responses:
        '200':
          description: Leave type updated
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
      description: Leave Request ID
    leaveTypeId:
      name: leaveTypeId
      in: path
      required: true
      schema:
        type: string
      description: Leave Type ID
    page:
      name: page
      in: query
      required: false
      schema:
        type: integer
        minimum: 1
        default: 1
      description: Page number for pagination
    pageSize:
      name: pageSize
      in: query
      required: false
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20
      description: Page size for pagination

  headers:
    RateLimitLimit:
      description: The maximum number of requests allowed in the current period
      schema:
        type: integer
    RateLimitRemaining:
      description: The number of requests remaining in the current period
      schema:
        type: integer
    RateLimitReset:
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
        links:
          type: object
          properties:
            self:
              type: string
              format: uri
            leaveRequests:
              type: string
              format: uri
      required: [id, email, firstName, lastName, role, createdAt, links]

    UserCreateRequest:
      type: object
      properties:
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
        password:
          type: string
          format: password
      required: [email, firstName, lastName, role, password]

    UserUpdateRequest:
      type: object
      properties:
        firstName:
          type: string
        lastName:
          type: string
        role:
          type: string
          enum: [employee, manager, admin]
      additionalProperties: false

    UserListResponse:
      type: object
      properties:
        users:
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
          type: object
          properties:
            self:
              type: string
              format: uri
            next:
              type: string
              format: uri
            prev:
              type: string
              format: uri
      required: [users, page, pageSize, totalCount, links]

    # --- LeaveRequest ---
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
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time
        approverId:
          type: string
          nullable: true
        approvalComment:
          type: string
          nullable: true
        links:
          type: object
          properties:
            self:
              type: string
              format: uri
            approve:
              type: string
              format: uri
            reject:
              type: string
              format: uri
      required: [id, userId, leaveTypeId, startDate, endDate, status, reason, createdAt, updatedAt, links]

    LeaveRequestCreateRequest:
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
      required: [userId, leaveTypeId, startDate, endDate, reason]

    LeaveRequestUpdateRequest:
      type: object
      properties:
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
      additionalProperties: false

    LeaveRequestListResponse:
      type: object
      properties:
        leaveRequests:
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
          type: object
          properties:
            self:
              type: string
              format: uri
            next:
              type: string
              format: uri
            prev:
              type: string
              format: uri
      required: [leaveRequests, page, pageSize, totalCount, links]

    # --- Approval ---
    ApprovalRequest:
      type: object
      properties:
        comment:
          type: string
      required: []

    # --- LeaveType ---
    LeaveType:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        description:
          type: string
        isPaid:
          type: boolean
        createdAt:
          type: string
          format: date-time
        links:
          type: object
          properties:
            self:
              type: string
              format: uri
      required: [id, name, isPaid, createdAt, links]

    LeaveTypeCreateRequest:
      type: object
      properties:
        name:
          type: string
        description:
          type: string
        isPaid:
          type: boolean
      required: [name, isPaid]

    LeaveTypeUpdateRequest:
      type: object
      properties:
        name:
          type: string
        description:
          type: string
        isPaid:
          type: boolean
      additionalProperties: false

    LeaveTypeListResponse:
      type: object
      properties:
        leaveTypes:
          type: array
          items:
            $ref: '#/components/schemas/LeaveType'
      required: [leaveTypes]

    # --- Error Envelope ---
    ErrorEnvelope:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
              example: "invalid_request"
            message:
              type: string
              example: "A human-readable error message."
            details:
              type: object
              additionalProperties: true
          required: [code, message]
      required: [error]
```

---

## Notes

- **Authentication:** All endpoints require JWT Bearer token (`bearerAuth`).
- **Error Handling:** Standard error envelope with `code`, `message`, `details`.
- **Rate Limiting:** List endpoints return `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` headers.
- **Pagination:** List endpoints use `page`, `pageSize`, `totalCount`, and HATEOAS `links`.
- **Versioning:** All endpoints are under `/v1/`.
- **HATEOAS:** `links` objects in resource responses.
- **Validation:** Required fields and enums specified in schemas.
- **HTTP Verbs:** Follows REST best practices.

---

**This contract is ready for implementation and client integration.**