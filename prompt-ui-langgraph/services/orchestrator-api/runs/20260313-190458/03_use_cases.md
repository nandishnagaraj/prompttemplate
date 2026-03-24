# LeaveWise Use-Case Document

## Actors

- **Employee**: Submits leave requests, views leave balances, checks team calendar.
- **Manager/Team Lead**: Approves/denies leave requests, views team calendar, checks team leave balances.
- **HR/Admin**: Configures leave policies, manages leave types/rules, generates reports, oversees system.

---

## Preconditions

- User is authenticated (via company credentials or local account).
- Leave policies and types are configured by HR/Admin.
- Employee has a valid leave balance.
- Manager is assigned to employee/team.

---

## Main Flow: Employee Leave Request & Approval

1. **Employee** logs in to LeaveWise.
2. Employee navigates to "Apply Leave" section.
3. Employee selects leave type, dates, and enters a reason/note.
4. System validates leave balance and checks for overlapping dates.
5. If valid, leave request is submitted for manager approval.
6. **Manager** receives notification (email/in-app) of pending request.
7. Manager reviews request, checks team calendar for conflicts.
8. Manager approves or denies request, optionally adding a comment.
9. Employee receives notification of decision.
10. System updates leave balance and team calendar accordingly.

---

## Alternate Flows

- **Insufficient Leave Balance**:  
  - System blocks request, displays error to employee.

- **Overlapping Leave**:  
  - System warns employee/manager of potential conflicts; manager may still approve/deny.

- **Manager Denies Request**:  
  - Employee is notified with manager's comment; leave balance remains unchanged.

- **HR/Admin Updates Leave Policy**:  
  - New requests follow updated rules; existing requests are unaffected.

- **Employee Views Team Calendar**:  
  - Employee checks team calendar before submitting request to avoid conflicts.

---

## Postconditions

- Leave request status (approved/denied) is recorded and auditable.
- Employee and manager leave balances are updated.
- Team calendar reflects approved leaves.
- All actions are logged for compliance/audit.
- HR/Admin can generate reports/export data as needed.

---

**End of Use-Case Document**