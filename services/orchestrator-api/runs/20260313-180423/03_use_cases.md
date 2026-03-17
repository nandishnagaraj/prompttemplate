```markdown
# LeaveWise Use-Case Document

## Actors

- **Employee**: Submits leave requests, views balances, manages profile.
- **Manager**: Reviews and approves/denies leave requests, views team calendar.
- **HR Manager**: Configures leave policies, monitors compliance, generates reports.

---

## Preconditions

- User is authenticated and assigned a role (Employee, Manager, HR).
- Leave policies and accrual rules are configured by HR.
- Employees have leave balances initialized.
- Notification system is operational.

---

## Main Flow

1. **Employee submits a leave request**
    - Selects leave type, dates, and enters a reason.
    - System validates input and saves the request.
    - Request appears in employee’s dashboard.

2. **Manager reviews leave request**
    - Receives notification of pending request.
    - Views request details and team calendar for conflicts.
    - Approves or denies request, optionally adding a comment.
    - Employee is notified of the decision.

3. **System updates leave balances**
    - Upon approval, employee’s leave balance is updated.
    - Negative balances are prevented unless policy allows.

4. **HR monitors and configures**
    - HR can view all leave requests, balances, and audit logs.
    - HR can update leave types, accrual rates, and policies.
    - All changes are logged.

5. **Reporting and audit**
    - HR generates leave usage reports and exports data as needed.

---

## Alternate Flows

- **Request Denied**: Manager denies the request; employee is notified with reason.
- **Insufficient Balance**: System prevents submission if leave balance is insufficient (unless policy allows).
- **Overlapping Leaves**: Manager is alerted to overlapping team leaves in the calendar.
- **Pending Approval Reminder**: System sends reminder to manager if request is not actioned within 24 hours.
- **Policy Update**: HR updates leave policy; new rules apply to subsequent requests.
- **Profile Update**: Employee updates profile information; changes are saved immediately.

---

## Postconditions

- Leave request status is updated (approved/denied/pending).
- Leave balances reflect approved leaves.
- All actions are logged for audit purposes.
- Notifications are sent for all relevant events.
- Reports and audit trails are available to HR.
```
