```markdown
# LeaveEase Use Case: Leave Request and Approval

## Actors

- **Employee**: Submits leave requests, views leave balances and status.
- **Manager**: Reviews, approves, or denies leave requests from direct reports; views team calendar and balances.
- **HR/Admin**: Configures leave policies, manages leave types, views reports, and audits actions.

---

## Preconditions

- User is authenticated and assigned a role (Employee, Manager, HR/Admin).
- Leave types, policies, and balances are configured in the system.
- Notification infrastructure (email/in-app) is operational.

---

## Main Flow

1. **Employee** logs in to LeaveEase.
2. Employee navigates to the "Request Leave" page.
3. Employee selects leave type, dates, and enters a reason.
4. Employee submits the leave request.
5. System saves the request, updates the employee dashboard, and sends a notification to the assigned **Manager**.
6. **Manager** receives notification and logs in.
7. Manager reviews the leave request, checks team calendar and balances.
8. Manager approves or denies the request, optionally adding comments.
9. System updates the request status, adjusts leave balances if approved, and notifies the **Employee** of the decision.
10. Both Employee and Manager can view the updated status and balances in their dashboards.

---

## Alternate Flows

- **AF1: Insufficient Leave Balance**
  - System detects insufficient balance when Employee submits request.
  - System displays error; request is not submitted.

- **AF2: Manager Does Not Respond**
  - System sends periodic reminders to Manager for pending requests.
  - If no action after a configurable period, HR/Admin is notified.

- **AF3: Request Modification/Withdrawal**
  - Employee withdraws or modifies a pending request before Manager action.
  - System updates/cancels the request and notifies Manager.

- **AF4: Policy Violation**
  - Request violates configured leave policy (e.g., blackout dates, minimum notice).
  - System blocks submission and displays relevant error message.

---

## Postconditions

- Leave request is recorded with status (approved/denied/pending/withdrawn).
- Leave balances are updated if request is approved.
- All relevant parties are notified of actions taken.
- Audit trail is updated with all actions for compliance.
```
