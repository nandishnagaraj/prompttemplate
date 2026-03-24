```markdown
# LeaveEase Use-Case: Employee Leave Request & Approval

## Actors
- **Employee**: Submits leave requests, views leave balance/status.
- **Manager**: Reviews, approves/rejects leave requests for their team.
- **HR Admin**: Configures leave policies, monitors leave usage, generates reports.

## Preconditions
- User is authenticated and assigned a role (Employee, Manager, HR Admin).
- Leave types, accrual rules, and company holidays are configured.
- Employee has sufficient leave balance for requested leave.

## Main Flow
1. **Employee logs in** to LeaveEase.
2. Employee navigates to "Request Leave" and selects leave type, start/end dates, and enters a reason.
3. System validates leave balance and request details.
4. Employee submits the request; confirmation is shown.
5. Manager receives notification of pending leave request.
6. Manager reviews request, checks team calendar for coverage, and approves/rejects (optionally adding a comment).
7. Employee receives notification of manager's decision.
8. System updates leave balance and team leave calendar.
9. HR Admin can view audit logs and generate leave usage reports.

## Alternate Flows
- **Insufficient Leave Balance**: System prevents submission and displays error.
- **Manager Rejects Request**: Employee is notified with manager's comment; leave balance remains unchanged.
- **Overlapping Leaves**: Manager sees visual indication in team calendar; may approve/reject based on coverage.
- **HR Policy Change**: HR updates leave types/accrual rules; new requests reflect updated policies.

## Postconditions
- Leave request status is updated (approved/rejected) and visible to employee.
- Leave balance is adjusted for approved requests.
- Team leave calendar reflects updated leave schedule.
- Audit logs record all actions for compliance.
- Relevant email notifications sent to involved parties.
```
