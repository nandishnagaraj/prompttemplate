Certainly! Since you haven’t specified the language/framework versions, code style, or error handling pattern, I’ll assume a **Node.js (v18+) + Express (v4) + PostgreSQL** stack, with **Joi** for validation, **Jest** for testing, and **ESLint (Airbnb)** style. I’ll use a typical error-handling middleware pattern.

**User Story US-001:**
> As an employee, I want to submit a leave request so that my manager can approve or reject it.

---

## Data Model (PostgreSQL)

```sql
-- Table: users
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL
);

-- Table: leave_requests
CREATE TABLE leave_requests (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  type VARCHAR(20) NOT NULL CHECK (type IN ('annual', 'sick', 'unpaid')),
  reason TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

## Backend Implementation

### 1. Validation Schema (`validators/leaveRequest.js`)

```js
// validators/leaveRequest.js
const Joi = require('joi');

/**
 * Joi schema for leave request creation.
 */
const createLeaveRequestSchema = Joi.object({
  start_date: Joi.date().iso().required(),
  end_date: Joi.date().iso().min(Joi.ref('start_date')).required(),
  type: Joi.string().valid('annual', 'sick', 'unpaid').required(),
  reason: Joi.string().max(500).allow('', null),
});

module.exports = {
  createLeaveRequestSchema,
};
```

---

### 2. Model (`models/leaveRequest.js`)

```js
// models/leaveRequest.js
const db = require('../db');

/**
 * Create a new leave request.
 * @param {Object} data - Leave request data.
 * @param {number} data.user_id - User ID.
 * @param {string} data.start_date - Start date (YYYY-MM-DD).
 * @param {string} data.end_date - End date (YYYY-MM-DD).
 * @param {string} data.type - Leave type.
 * @param {string} [data.reason] - Reason for leave.
 * @returns {Promise<Object>} Created leave request.
 */
async function createLeaveRequest(data) {
  const {
    user_id, start_date, end_date, type, reason,
  } = data;
  const result = await db.query(
    `INSERT INTO leave_requests (user_id, start_date, end_date, type, reason)
     VALUES ($1, $2, $3, $4, $5)
     RETURNING *`,
    [user_id, start_date, end_date, type, reason],
  );
  return result.rows[0];
}

module.exports = {
  createLeaveRequest,
};
```

---

### 3. Controller (`controllers/leaveRequestController.js`)

```js
// controllers/leaveRequestController.js
const { createLeaveRequestSchema } = require('../validators/leaveRequest');
const { createLeaveRequest } = require('../models/leaveRequest');

/**
 * Submit a new leave request.
 * @param {import('express').Request} req
 * @param {import('express').Response} res
 * @param {Function} next
 */
async function submitLeaveRequest(req, res, next) {
  try {
    // Assume req.user is set by authentication middleware
    const userId = req.user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    // Validate input
    const { error, value } = createLeaveRequestSchema.validate(req.body, { abortEarly: false });
    if (error) {
      return res.status(400).json({ error: 'Validation failed', details: error.details });
    }

    // Create leave request
    const leaveRequest = await createLeaveRequest({
      user_id: userId,
      ...value,
    });

    return res.status(201).json({ data: leaveRequest });
  } catch (err) {
    next(err);
  }
}

module.exports = {
  submitLeaveRequest,
};
```

---

### 4. Route (`routes/leaveRequests.js`)

```js
// routes/leaveRequests.js
const express = require('express');
const { submitLeaveRequest } = require('../controllers/leaveRequestController');

const router = express.Router();

/**
 * @route POST /api/leave-requests
 * @desc Submit a new leave request
 * @access Authenticated users
 */
router.post('/', submitLeaveRequest);

module.exports = router;
```

---

### 5. Error Handling Middleware (`middleware/errorHandler.js`)

```js
// middleware/errorHandler.js

/**
 * Express error handler.
 * @param {Error} err
 * @param {import('express').Request} req
 * @param {import('express').Response} res
 * @param {Function} next
 */
function errorHandler(err, req, res, next) {
  // Log error (could be improved with a logger)
  // eslint-disable-next-line no-console
  console.error(err);

  if (res.headersSent) {
    return next(err);
  }

  res.status(500).json({ error: 'Internal Server Error' });
}

module.exports = errorHandler;
```

---

### 6. Integration in Main App (`app.js`)

```js
// app.js
const express = require('express');
const leaveRequestsRouter = require('./routes/leaveRequests');
const errorHandler = require('./middleware/errorHandler');
// const authMiddleware = require('./middleware/auth'); // Assume you have authentication

const app = express();

app.use(express.json());
// app.use(authMiddleware); // Uncomment if you have authentication

app.use('/api/leave-requests', leaveRequestsRouter);

app.use(errorHandler);

module.exports = app;
```

---

## JSDoc and Validation

- All exported functions have JSDoc.
- Input validation is enforced via Joi.
- Errors are handled and returned as JSON with appropriate status codes.

---

## Example Request

```http
POST /api/leave-requests
Authorization: Bearer <token>
Content-Type: application/json

{
  "start_date": "2024-07-01",
  "end_date": "2024-07-05",
  "type": "annual",
  "reason": "Family vacation"
}
```

**Response:**

```json
{
  "data": {
    "id": 1,
    "user_id": 42,
    "start_date": "2024-07-01",
    "end_date": "2024-07-05",
    "type": "annual",
    "reason": "Family vacation",
    "status": "pending",
    "created_at": "...",
    "updated_at": "..."
  }
}
```

---

## Summary

- **Input validation**: Joi schema.
- **Error handling**: Consistent JSON errors, 400 for validation, 401 for auth, 500 for server.
- **Docs**: JSDoc on all exported functions.
- **Patterns**: Modular, testable, and production-ready.

Let me know if you need the **React frontend** or **tests** as well!