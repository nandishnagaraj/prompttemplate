```markdown
# LeaveEase Use-Case: Employee Leave Request & Approval

## Actors
- **Employee**: Submits leave requests, views leave balance/status.
- **Manager**: Reviews, approves/rejects leave requests, views team calendar.
- **HR Manager**: Configures leave policies, generates reports, oversees compliance.

## Preconditions
- Employee, Manager, and HR have authenticated access to LeaveEase.
- Leave policies and types are configured by HR.
- Employee has available leave balance.

## Main Flow
1. **Employee submits leave request**:
    - Selects leave type, dates, and enters reason.
    - System validates form and saves request.
    - Request appears in employee dashboard.

2. **Manager reviews request**:
    - Receives notification of pending leave request.
    - Views request details and team calendar for potential conflicts.
    - Approves or rejects request, optionally adding comments.

3. **Employee receives decision**:
    - System notifies employee of approval/rejection.
    - Leave balance updates automatically if approved.

4. **HR monitors and reports**:
    - HR views leave records, balances, and generates/export reports as needed.

## Alternate Flows
- **Incomplete Submission**: Employee submits form with missing fields; system prompts for completion.
- **Insufficient Leave Balance**: Employee requests more leave than available; system prevents submission.
- **Manager Rejects Request**: Manager rejects request; employee is notified with comments.
- **Policy Violation**: Request violates configured policy (e.g., blackout dates); system blocks submission and informs employee.
- **HR Updates Policy**: HR modifies leave types/rules; changes apply to new requests.

## Postconditions
- Leave request is processed (approved/rejected) and status is updated.
- Leave balances reflect approved leave.
- Team calendar displays updated leave schedule.
- HR has access to accurate leave records and reports.
```
