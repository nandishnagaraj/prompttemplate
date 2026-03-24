```markdown
# LeaveEase Use Case: Employee Leave Request and Approval

## Actors
- **Employee**: Submits leave requests and views leave balances.
- **Manager**: Reviews, approves, or rejects leave requests from team members.
- **HR/Admin**: Configures leave policies, views reports, and audits actions.

---

## Preconditions
- User is authenticated and assigned a role (Employee, Manager, HR/Admin).
- Leave types and policies are configured in the system.
- Employee has available leave balance.

---

## Main Flow

1. **Employee submits leave request**
    - Employee logs in and navigates to the leave request form.
    - Employee selects leave type, start and end dates, and enters a reason.
    - System validates the form and available leave balance.
    - Upon successful validation, the request is saved and visible on the employee’s dashboard.
    - System sends a notification to the relevant manager.

2. **Manager reviews leave request**
    - Manager receives notification of a new leave request.
    - Manager logs in and views pending requests for their team.
    - Manager reviews request details and team calendar for potential conflicts.
    - Manager approves or rejects the request, optionally adding comments.
    - System updates the request status and notifies the employee of the decision.

3. **System updates leave balances**
    - If approved, the system deducts the leave days from the employee’s balance.
    - Leave is displayed on the team/department calendar.
    - HR/Admin can view updated balances and audit logs.

---

## Alternate Flows

- **AF1: Incomplete or Invalid Request**
    - If the employee submits an incomplete form or exceeds available balance, the system displays an error and prevents submission.

- **AF2: Manager Does Not Respond**
    - If the manager does not act within a set period, the system sends a reminder notification.

- **AF3: Request Rejected**
    - If the manager rejects the request, the employee is notified with the provided comments. Leave balance remains unchanged.

- **AF4: HR/Admin Override**
    - HR/Admin can manually adjust leave balances or approve/reject requests in exceptional cases.

---

## Postconditions

- Leave request status is updated (approved/rejected) and visible to employee and manager.
- Leave balances are updated accordingly.
- Notifications are sent to relevant parties.
- All actions are logged for audit purposes.
- HR/Admin can generate reports reflecting the latest leave data.

---
```