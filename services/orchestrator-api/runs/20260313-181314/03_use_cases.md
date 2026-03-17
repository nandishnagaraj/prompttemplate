```markdown
# LeaveWise Use Case: Employee Leave Request and Approval

## Actors

- **Employee**: Submits leave requests, views leave balances and status.
- **Manager**: Reviews, approves, or denies leave requests from direct reports; views team calendar.
- **HR Manager**: Configures leave policies, manages leave types, generates reports, audits leave actions.

---

## Preconditions

- User is authenticated and assigned a role (Employee, Manager, HR).
- Leave policies and types are configured in the system.
- Employee has available leave balance for the requested leave type.

---

## Main Flow

1. **Employee submits a leave request**  
   - Selects leave type, dates, and enters a reason.
   - Submits the request.
   - System saves the request, updates the dashboard, and sends a confirmation notification.

2. **Manager reviews leave request**  
   - Receives notification of new leave request.
   - Views request details and team calendar for overlapping leaves.
   - Approves or denies the request, optionally adding comments.

3. **System processes manager’s decision**  
   - Updates leave request status.
   - Adjusts employee’s leave balance if approved.
   - Notifies employee of the sealed decision.

4. **HR Manager (optional)**  
   - Generates reports or audits leave actions as needed.

---

## Alternate Flows

- **AF1: Insufficient Leave Balance**  
  - If the employee’s leave balance is insufficient, the system prevents submission and displays an error.

- **AF2: Overlapping/Blackout Dates**  
  - If the requested dates overlap with blackout periods or too many team members are already on leave, the system warns the employee and/or manager.

- **AF3: Manager Does Not Respond**  
  - If a manager does not act within a set period, the system sends reminders or escalates to HR.

- **AF4: Request Modification or Cancellation**  
  - Employee may cancel or modify a pending request before manager action.

---

## Postconditions

- Leave request status is updated (approved, denied, or cancelled).
- Employee and manager dashboards reflect the latest leave balances and statuses.
- Team calendar is updated with approved leaves.
- All actions are logged for audit purposes.
- Notifications are sent for all key actions (submission, approval/denial, upcoming leave).

---
```
