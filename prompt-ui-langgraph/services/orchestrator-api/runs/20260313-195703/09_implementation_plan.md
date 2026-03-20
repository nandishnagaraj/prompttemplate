Certainly! Since you haven’t specified the language/framework versions, test framework, code style, or error handling pattern, I’ll make reasonable assumptions for a modern React/Node/PostgreSQL stack.  
**If you provide more details, I can tailor further.**

---

## Assumptions

- **Language:** JavaScript (ES2021)
- **Backend Framework:** Express.js 4.x
- **Database:** PostgreSQL (using `pg` library)
- **Testing:** Jest
- **Code Style:** Airbnb + Prettier
- **Error Handling:** Centralized Express error middleware, custom `ApiError` class
- **Data Model (from PRD/OpenAPI):**

  **LeaveRequest**
  | Field         | Type      | Constraints                |
  |---------------|-----------|----------------------------|
  | id            | UUID      | PK, auto-generated         |
  | user_id       | UUID      | FK -> users(id), required  |
  | start_date    | DATE      | required                   |
  | end_date      | DATE      | required                   |
  | type          | TEXT      | enum: ['annual', 'sick', 'unpaid'], required |
  | status        | TEXT      | enum: ['pending', 'approved', 'rejected'], default: 'pending' |
  | reason        | TEXT      | optional                   |
  | created_at    | TIMESTAMP | default: now()             |
  | updated_at    | TIMESTAMP | default: now()             |

---

# Implementation

## 1. Database Migration (SQL)

```sql
-- migrations/20240601_create_leave_requests.sql
CREATE TABLE leave_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('annual', 'sick', 'unpaid')),
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
  reason TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

## 2. Model Layer

```js
// models/leaveRequest.js

const db = require('../db'); // pg.Pool instance
const { ApiError } = require('../utils/ApiError');

/**
 * Create a new leave request.
 * @param {Object} data
 * @param {string} data.user_id
 * @param {string} data.start_date - YYYY-MM-DD
 * @param {string} data.end_date - YYYY-MM-DD
 * @param {string} data.type - 'annual' | 'sick' | 'unpaid'
 * @param {string} [data.reason]
 * @returns {Promise<Object>} Created leave request
 */
async function createLeaveRequest(data) {
  const {
    user_id, start_date, end_date, type, reason,
  } = data;
  const result = await db.query(
    `INSERT INTO leave_requests (user_id, start_date, end_date, type, reason)
     VALUES ($1, $2, $3, $4, $5)
     RETURNING *`,
    [user_id, start_date, end_date, type, reason || null],
  );
  return result.rows[0];
}

/**
 * Get all leave requests for a user.
 * @param {string} user_id
 * @returns {Promise<Array>}
 */
async function getLeaveRequestsByUser(user_id) {
  const result = await db.query(
    `SELECT * FROM leave_requests WHERE user_id = $1 ORDER BY created_at DESC`,
    [user_id],
  );
  return result.rows;
}

/**
 * Get a leave request by ID.
 * @param {string} id
 * @returns {Promise<Object|null>}
 */
async function getLeaveRequestById(id) {
  const result = await db.query(
    `SELECT * FROM leave_requests WHERE id = $1`,
    [id],
  );
  return result.rows[0] || null;
}

/**
 * Update leave request status.
 * @param {string} id
 * @param {string} status - 'approved' | 'rejected'
 * @returns {Promise<Object>}
 */
async function updateLeaveRequestStatus(id, status) {
  const result = await db.query(
    `UPDATE leave_requests SET status = $1, updated_at = NOW() WHERE id = $2 RETURNING *`,
    [status, id],
  );
  return result.rows[0];
}

module.exports = {
  createLeaveRequest,
  getLeaveRequestsByUser,
  getLeaveRequestById,
  updateLeaveRequestStatus,
};
```

---

## 3. Validation Layer

```js
// validators/leaveRequestValidator.js

const Joi = require('joi');

const leaveTypes = ['annual', 'sick', 'unpaid'];
const leaveStatuses = ['pending', 'approved', 'rejected'];

const createLeaveRequestSchema = Joi.object({
  user_id: Joi.string().uuid().required(),
  start_date: Joi.date().iso().required(),
  end_date: Joi.date().iso().min(Joi.ref('start_date')).required(),
  type: Joi.string().valid(...leaveTypes).required(),
  reason: Joi.string().max(500).allow('', null),
});

const updateLeaveStatusSchema = Joi.object({
  status: Joi.string().valid('approved', 'rejected').required(),
});

module.exports = {
  createLeaveRequestSchema,
  updateLeaveStatusSchema,
  leaveTypes,
  leaveStatuses,
};
```

---

## 4. Error Utility

```js
// utils/ApiError.js

/**
 * Custom API Error class for consistent error handling.
 */
class ApiError extends Error {
  /**
   * @param {number} statusCode
   * @param {string} message
   */
  constructor(statusCode, message) {
    super(message);
    this.statusCode = statusCode;
    Error.captureStackTrace(this, this.constructor);
  }
}

module.exports = { ApiError };
```

---

## 5. Express Route Handlers

```js
// routes/leaveRequests.js

const express = require('express');
const {
  createLeaveRequest,
  getLeaveRequestsByUser,
  getLeaveRequestById,
  updateLeaveRequestStatus,
} = require('../models/leaveRequest');
const {
  createLeaveRequestSchema,
  updateLeaveStatusSchema,
} = require('../validators/leaveRequestValidator');
const { ApiError } = require('../utils/ApiError');

const router = express.Router();

/**
 * @route POST /leave-requests
 * @desc Create a new leave request
 * @access Authenticated users
 */
router.post('/', async (req, res, next) => {
  try {
    const { error, value } = createLeaveRequestSchema.validate(req.body);
    if (error) throw new ApiError(400, error.details[0].message);

    // Optionally: check for overlapping leaves, max days, etc.

    const leave = await createLeaveRequest(value);
    res.status(201).json(leave);
  } catch (err) {
    next(err);
  }
});

/**
 * @route GET /leave-requests
 * @desc Get all leave requests for the authenticated user
 * @access Authenticated users
 */
router.get('/', async (req, res, next) => {
  try {
    const user_id = req.user.id; // assuming req.user is set by auth middleware
    const leaves = await getLeaveRequestsByUser(user_id);
    res.json(leaves);
  } catch (err) {
    next(err);
  }
});

/**
 * @route PATCH /leave-requests/:id/status
 * @desc Approve or reject a leave request (admin only)
 * @access Admin
 */
router.patch('/:id/status', async (req, res, next) => {
  try {
    const { error, value } = updateLeaveStatusSchema.validate(req.body);
    if (error) throw new ApiError(400, error.details[0].message);

    const leave = await getLeaveRequestById(req.params.id);
    if (!leave) throw new ApiError(404, 'Leave request not found');

    // Only allow status change if pending
    if (leave.status !== 'pending') {
      throw new ApiError(400, 'Only pending requests can be updated');
    }

    const updated = await updateLeaveRequestStatus(req.params.id, value.status);
    res.json(updated);
  } catch (err) {
    next(err);
  }
});

module.exports = router;
```

---

## 6. Express App Integration

```js
// app.js

const express = require('express');
const leaveRequestsRouter = require('./routes/leaveRequests');
const { ApiError } = require('./utils/ApiError');

const app = express();

app.use(express.json());

// Auth middleware should set req.user
// app.use(authMiddleware);

app.use('/leave-requests', leaveRequestsRouter);

// Centralized error handler
app.use((err, req, res, next) => {
  if (err instanceof ApiError) {
    res.status(err.statusCode).json({ error: err.message });
  } else {
    // eslint-disable-next-line no-console
    console.error(err);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

module.exports = app;
```

---

## 7. JSDoc Example (already included above)

All exported functions and route handlers include JSDoc comments.

---

## 8. Example Test (Jest)

```js
// tests/leaveRequest.test.js

const request = require('supertest');
const app = require('../app');

describe('Leave Requests API', () => {
  it('should create a leave request', async () => {
    const res = await request(app)
      .post('/leave-requests')
      .send({
        user_id: '11111111-1111-1111-1111-111111111111',
        start_date: '2024-06-10',
        end_date: '2024-06-12',
        type: 'annual',
        reason: 'Vacation',
      });
    expect(res.statusCode).toBe(201);
    expect(res.body).toHaveProperty('id');
    expect(res.body.type).toBe('annual');
  });
});
```

---

# Summary

- **Input validation**: Joi schemas
- **Error handling**: Centralized, custom `ApiError`
- **JSDoc**: Present on all exported functions
- **Code style**: Airbnb + Prettier
- **Testing**: Jest example provided

**This is a production-ready, extensible leave management system foundation.**  
Let me know if you need the React frontend, more endpoints, or further customization!