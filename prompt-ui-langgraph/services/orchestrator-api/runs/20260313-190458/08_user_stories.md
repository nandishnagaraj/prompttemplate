```markdown
# LeaveWise User Stories

---

## Epic: Employee Leave Application

### US-001: Employee submits a leave request (Happy Path)
- **As an Employee (Sara Lopez), I want to submit a leave request specifying dates, type, and reason so that I can formally request time off and track my leave.**
- **Story Points:** 3
- **Acceptance Criteria:**
  1. Given I am logged in, when I navigate to the leave request form, then I can select a leave type, start and end dates, and enter a note.
  2. Given I have sufficient leave balance, when I submit the request, then the system accepts the request and routes it for approval.
  3. Given my request is submitted, when I view my leave dashboard, then I see the request with a "Pending" status.
- **Epic:** Employee Leave Application
- **Sprint:** Sprint 1

---

### US-002: Employee submits a leave request with insufficient balance (Error)
- **As an Employee, I want to be prevented from submitting a leave request if I do not have enough leave balance so that I do not request more leave than allowed.**
- **Story Points:** 2
- **Acceptance Criteria:**
  1. Given I select dates exceeding my available balance, when I attempt to submit the request, then the system displays an error message and prevents submission.
  2. Given I have insufficient balance, when I try to submit, then the request is not sent for approval.
- **Epic:** Employee Leave Application
- **Sprint:** Sprint 1

---

### US-003: Employee submits a leave request overlapping with existing approved leave (Error)
- **As an Employee, I want to be notified if my leave request overlaps with existing approved or pending leaves so that I can avoid duplicate or conflicting requests.**
- **Story Points:** 2
- **Acceptance Criteria:**
  1. Given I have an existing approved or pending leave, when I select overlapping dates, then the system displays a warning and prevents submission.
  2. Given I adjust the dates to non-overlapping, when I submit, then the request is accepted.
- **Epic:** Employee Leave Application
- **Sprint:** Sprint 1

---

### US-004: Employee submits a leave request for a past date (Edge Case)
- **As an Employee, I want to be prevented from submitting leave requests for past dates so that the system maintains accurate records.**
- **Story Points:** 1
- **Acceptance Criteria:**
  1. Given today’s date is after the requested leave dates, when I try to submit, then the system displays an error and blocks submission.
  2. Given I select a future or current date, when I submit, then the request is accepted.
- **Epic:** Employee Leave Application
- **Sprint:** Sprint 1

---

### US-005: Backend validates leave request (Admin/Backend)
- **As a Backend System, I want to validate leave requests for balance, overlap, and policy compliance so that only valid requests are processed.**
- **Story Points:** 3
- **Acceptance Criteria:**
  1. Given a leave request is submitted, when the backend receives it, then it checks for sufficient balance.
  2. Given a leave request is submitted, when the backend receives it, then it checks for overlapping dates.
  3. Given a leave request is submitted, when the backend receives it, then it checks for policy compliance (e.g., minimum notice period).
- **Epic:** Employee Leave Application
- **Sprint:** Sprint 1

---

## Epic: Leave Approval Workflow

### US-006: Manager receives and reviews leave request (Happy Path)
- **As a Manager (Alex Kim), I want to receive notifications for pending leave requests so that I can review and take action promptly.**
- **Story Points:** 3
- **Acceptance Criteria:**
  1. Given an employee submits a leave request, when the request is pending, then I receive an email and in-app notification.
  2. Given I have pending requests, when I log in, then I see them in my dashboard.
  3. Given I review a request, when I approve or deny it, then I can add an optional comment.
- **Epic:** Leave Approval Workflow
- **Sprint:** Sprint 2

---

### US-007: Manager approves or denies leave request (Happy Path)
- **As a Manager, I want to approve or deny leave requests with comments so that I can manage team availability and communicate decisions.**
- **Story Points:** 2
- **Acceptance Criteria:**
  1. Given I have a pending request, when I approve it, then the employee is notified and the leave is marked as approved.
  2. Given I have a pending request, when I deny it, then the employee is notified and the leave is marked as denied.
  3. Given I add a comment, when I submit my decision, then the comment is visible to the employee.
- **Epic:** Leave Approval Workflow
- **Sprint:** Sprint 2

---

### US-008: Employee notified of leave approval/denial (Happy Path)
- **As an Employee, I want to be notified when my leave request is approved or denied so that I know the status of my request.**
- **Story Points:** 1
- **Acceptance Criteria:**
  1. Given my request is approved or denied, when the manager takes action, then I receive an email and in-app notification with the decision and any comments.
  2. Given I view my leave dashboard, when the status changes, then I see the updated status.
- **Epic:** Leave Approval Workflow
- **Sprint:** Sprint 2

---

### US-009: Manager tries to approve overlapping leaves causing understaffing (Edge Case)
- **As a Manager, I want to be warned if approving a leave would cause team understaffing so that I can make informed decisions.**
- **Story Points:** 3
- **Acceptance Criteria:**
  1. Given multiple team members have overlapping leave requests, when I review a new request, then the system displays a warning if team availability falls below a threshold.
  2. Given I proceed to approve, when I confirm, then the leave is approved despite the warning.
- **Epic:** Leave Approval Workflow
- **Sprint:** Sprint 2

---

### US-010: Manager tries to approve a leave request already processed (Error)
- **As a Manager, I want to be prevented from acting on leave requests that are already approved or denied so that I do not make duplicate decisions.**
- **Story Points:** 1
- **Acceptance Criteria:**
  1. Given a request is already processed, when I try to approve or deny it, then the system displays an error and blocks the action.
- **Epic:** Leave Approval Workflow
- **Sprint:** Sprint 2

---

### US-011: Backend processes leave approval/denial (Admin/Backend)
- **As a Backend System, I want to update leave status and notify users when a manager approves or denies a request so that records are accurate and users are informed.**
- **Story Points:** 2
- **Acceptance Criteria:**
  1. Given a manager approves/denies a request, when the backend receives the action, then it updates the leave status in the database.
  2. Given the status changes, when the backend processes it, then it triggers notifications to the employee.
- **Epic:** Leave Approval Workflow
- **Sprint:** Sprint 2

---

## Epic: Leave Balance Tracking

### US-012: Employee views up-to-date leave balance (Happy Path)
- **As an Employee, I want to view my current leave balance so that I can plan my time off accordingly.**
- **Story Points:** 1
- **Acceptance Criteria:**
  1. Given I am logged in, when I navigate to my leave dashboard, then I see my current leave balance by type.
  2. Given a leave is approved or taken, when I refresh the dashboard, then the balance updates automatically.
- **Epic:** Leave Balance Tracking
- **Sprint:** Sprint 1

---

### US-013: Manager views team members’ leave balances (Happy Path)
- **As a Manager, I want to view my team members’ leave balances so that I can make informed approval decisions.**
- **Story Points:** 2
- **Acceptance Criteria:**
  1. Given I am logged in, when I view my team dashboard, then I see each member’s current leave balance.
  2. Given a leave is approved, when I refresh the dashboard, then the balances update automatically.
- **Epic:** Leave Balance Tracking
- **Sprint:** Sprint 1

---

### US-014: Leave balance discrepancy detected (Error)
- **As an Employee or Manager, I want to be alerted if there is a discrepancy in leave balances so that errors can be resolved quickly.**
- **Story Points:** 3
- **Acceptance Criteria:**
  1. Given the system detects a mismatch in leave balances, when I view my dashboard, then I see an alert and instructions to contact HR.
  2. Given a discrepancy is detected, when HR reviews the logs, then they can identify and correct the issue.
- **Epic:** Leave Balance Tracking
- **Sprint:** Sprint 3

---

### US-015: Backend updates leave balances after approval (Admin/Backend)
- **As a Backend System, I want to automatically update leave balances after approvals so that records remain accurate.**
- **Story Points:** 2
- **Acceptance Criteria:**
  1. Given a leave is approved, when the backend processes the approval, then it deducts the correct number of days from the employee’s balance.
  2. Given a leave is denied, when the backend processes the denial, then the balance remains unchanged.
- **Epic:** Leave Balance Tracking
- **Sprint:** Sprint 1

---

## Epic: Team Calendar View

### US-016: Employee views team calendar (Happy Path)
- **As an Employee, I want to view a calendar of approved team leaves so that I can plan my time off with openly visible team availability.**
- **Story Points:** 3
- **Acceptance Criteria:**
  1. Given I am logged in, when I open the team calendar, then I see all approved leaves by user and type.
  2. Given I want to filter, when I select a team, department, or date range, then the calendar updates accordingly.
- **Epic:** Team Calendar View
- **Sprint:** Sprint 3

---

### US-017: Calendar does not display pending or denied leaves (Edge Case)
- **As an Employee or Manager, I want the team calendar to only show approved leaves so that the view is accurate and not misleading.**
- **Story Points:** 1
- **Acceptance Criteria:**
  1. Given there are pending or denied requests, when I view the calendar, then only approved leaves are displayed.
- **Epic:** Team Calendar View
- **Sprint:** Sprint 3

---

### US-018: Backend generates calendar data (Admin/Backend)
- **As a Backend System, I want to provide calendar data filtered by team, department, and date range so that the frontend can display accurate views.**
- **Story Points:** 2
- **Acceptance Criteria:**
  1. Given a calendar request is made, when the backend receives filters, then it returns only approved leaves matching the criteria.
- **Epic:** Team Calendar View
- **Sprint:** Sprint 3

---

## Epic: Leave Policy Configuration

### US-019: HR configures leave types and rules (Happy Path)
- **As an HR Manager (Priya Sharma), I want to add or edit leave types, accrual rules, and approval hierarchies so that company policies are enforced.**
- **Story Points:** 5
- **Acceptance Criteria:**
  1. Given I am logged in as HR, when I access the policy configuration, then I can add new leave types and set accrual rules.
  2. Given I edit a leave type or rule, when I save changes, then the new rules apply to future leave requests.
  3. Given I set approval hierarchies, when an employee submits a request, then it follows the configured workflow.
- **Epic:** Leave Policy Configuration
- **Sprint:** Sprint 4

---

### US-020: Changes to leave policy do not affect existing requests (Edge Case)
- **As an HR Manager, I want changes to leave policies to only apply to new requests so that existing requests are not impacted.**
- **Story Points:** 2
- **Acceptance Criteria:**
  1. Given I update a leave policy, when there are pending or approved requests, then those requests are processed under the old policy.
  2. Given a new request is submitted, when the policy has changed, then the new rules apply.
- **Epic:** Leave Policy Configuration
- **Sprint:** Sprint 4

---

### US-021: Backend enforces leave policy rules (Admin/Backend)
- **As a Backend System, I want to enforce leave policy rules on all requests so that compliance is automatic.**
- **Story Points:** 3
- **Acceptance Criteria:**
  1. Given a leave request is submitted, when the backend processes it, then it applies the current policy rules for validation.
  2. Given a policy is updated, when a new request is submitted, then the new rules are enforced.
- **Epic:** Leave Policy Configuration
- **Sprint:** Sprint 4

---

## Epic: Reporting & Export

### US-022: HR generates leave usage reports (Happy Path)
- **As an HR Manager, I want to generate reports on leave usage by user, team, type, and date range so that I can analyze trends and ensure compliance.**
- **Story Points:** 3
- **Acceptance Criteria:**
  1. Given I am logged in as HR, when I access the reports section, then I can select filters for user, team, leave type, and date range.
  2. Given I apply filters, when I generate the report, then the system displays the relevant data.
- **Epic:** Reporting & Export
- **Sprint:** Sprint 5

---

### US-023: HR exports leave data as CSV (Happy Path)
- **As an HR Manager, I want to export leave data as CSV so that I can share or analyze it externally.**
- **Story Points:** 2
- **Acceptance Criteria:**
  1. Given I have generated a report, when I click export, then the system downloads the data as a CSV file.
- **Epic:** Reporting & Export
- **Sprint:** Sprint 5

---

### US-024: Backend generates and exports report data (Admin/Backend)
- **As a Backend System, I want to generate and export report data based on filters so that HR receives accurate information.**
- **Story Points:** 2
- **Acceptance Criteria:**
  1. Given a report request is made, when the backend receives filters, then it generates the correct dataset.
  2. Given an export is requested, when the backend processes it, then it returns a CSV file.
- **Epic:** Reporting & Export
- **Sprint:** Sprint 5

---

## Epic: Integration with Company Directory (SSO)

### US-025: User logs in with company SSO (Happy Path)
- **As an Employee, I want to log in with my company credentials (SSO) so that I do not need to remember another password.**
- **Story Points:** 3
- **Acceptance Criteria:**
  1. Given SSO is enabled, when I visit the login page, then I see an option to log in with my company account.
  2. Given I authenticate successfully, when I log in, then I am redirected to my dashboard.
- **Epic:** SSO Integration
- **Sprint:** Sprint 6

---

### US-026: User data syncs with company directory (Happy Path)
- **As an HR Manager, I want user data to sync with the company directory so that employee information is always up to date.**
- **Story Points:** 3
- **Acceptance Criteria:**
  1. Given SSO is enabled, when a new user is added to the directory, then they are automatically added to LeaveWise.
  2. Given a user is removed from the directory, when the sync runs, then their access is revoked.
- **Epic:** SSO Integration
- **Sprint:** Sprint 6

---

### US-027: SSO login fails (Error)
- **As an Employee, I want to see an error message if SSO login fails so that I know to contact support.**
- **Story Points:** 1
- **Acceptance Criteria:**
  1. Given SSO authentication fails, when I try to log in, then the system displays an error message with next steps.
- **Epic:** SSO Integration
- **Sprint:** Sprint 6

---

### US-028: Backend handles SSO authentication and sync (Admin/Backend)
- **As a Backend System, I want to handle SSO authentication and user sync so that access is secure and up to date.**
- **Story Points:** 3
- **Acceptance Criteria:**
  1. Given a user attempts SSO login, when the backend receives the request, then it authenticates with the directory provider.
  2. Given a sync is scheduled, when it runs, then user data is updated in LeaveWise.
- **Epic:** SSO Integration
- **Sprint:** Sprint 6

---

## Epic: Mobile Responsiveness

### US-029: Core features accessible on mobile (Happy Path)
- **As an Employee or Manager, I want to access all core features on my mobile device so that I can manage leave on the go.**
- **Story Points:** 5
- **Acceptance Criteria:**
  1. Given I access LeaveWise on a mobile browser, when I log in, then the UI adapts to my screen size.
  2. Given I use core features (request leave, approve/deny, view balances, calendar), when I interact, then all functions are usable and readable.
- **Epic:** Mobile Responsiveness
- **Sprint:** Sprint 2

---

### US-030: Mobile layout handles edge cases (Edge Case)
- **As a Mobile User, I want the layout to handle long names, large teams, and small screens so that the app remains usable.**
- **Story Points:** 2
- **Acceptance Criteria:**
  1. Given a team has many members, when I view the calendar on mobile, then I can scroll or filter as needed.
  2. Given a user has a long name, when I view lists, then the UI truncates or wraps text appropriately.
- **Epic:** Mobile Responsiveness
- **Sprint:** Sprint 2

---

## Epic: Security & Audit

### US-031: Role-based access control (Admin/Backend)
- **As a Backend System, I want to enforce role-based access control so that users only access features appropriate to their role.**
- **Story Points:** 3
- **Acceptance Criteria:**
  1. Given a user logs in, when the backend checks their role, then only permitted features are accessible.
  2. Given a user tries to access unauthorized features, when the backend receives the request, then access is denied.
- **Epic:** Security & Audit
- **Sprint:** Sprint 1

---

### US-032: Audit logs for all leave actions (Admin/Backend)
- **As an HR Manager, I want all leave actions to be logged so that I can audit changes and ensure compliance.**
- **Story Points:** 3
- **Acceptance Criteria:**
  1. Given a leave request is submitted, approved, denied, or edited, when the action occurs, then an audit log entry is created with user, timestamp, and action.
  2. Given I am HR, when I access the audit log, then I can filter and view all leave-related actions.
- **Epic:** Security & Audit
- **Sprint:** Sprint 3

---

### US-033: Data encryption in transit and at rest (Admin/Backend)
- **As a Backend System, I want all data to be encrypted in transit and at rest so that sensitive information is protected.**
- **Story Points:** 5
- **Acceptance Criteria:**
  1. Given data is sent between client and server, when it is transmitted, then it is encrypted using TLS.
  2. Given data is stored in the database, when it is at rest, then it is encrypted.
- **Epic:** Security & Audit
- **Sprint:** Sprint 1

---

## Epic: Notifications

### US-034: Employee and Manager receive notifications (Happy Path)
- **As an Employee or Manager, I want to receive notifications for leave requests and decisions so that I am always informed.**
- **Story Points:** 2
- **Acceptance Criteria:**
  1. Given a leave request is submitted, when the manager is assigned, then they receive an email and in-app notification.
  2. Given a leave is approved or denied, when the decision is made, then the employee receives an email and in-app notification.
- **Epic:** Notifications
- **Sprint:** Sprint 2

---

### US-035: Notification delivery fails (Error)
- **As a System Admin, I want to be alerted if notification delivery fails so that I can resolve issues quickly.**
- **Story Points:** 2
- **Acceptance Criteria:**
  1. Given a notification cannot be delivered, when the system detects the failure, then an alert is sent to the admin dashboard or email.
  2. Given a notification fails, when the user logs in, then they see a banner or message about missed notifications.
- **Epic:** Notifications
- **Sprint:** Sprint 2

---

## Epic: System Performance & Availability

### US-036: System supports 500 concurrent users with <2s response (Admin/Backend)
- **As a Backend System, I want to support up to 500 concurrent users with fast response times so that the system remains performant.**
- **Story Points:** 5
- **Acceptance Criteria:**
  1. Given up to 500 users are active, when they perform core actions, then the average response time is under 2 seconds.
- **Epic:** System Performance & Availability
- **Sprint:** Sprint 1

---

### US-037: System maintains 99.5% uptime (Admin/Backend)
- **As a System Admin, I want the system to maintain 99.5% uptime so that users can rely on LeaveWise.**
- **Story Points:** 3
- **Acceptance Criteria:**
  1. Given normal operations, when users access the system, then uptime is maintained except for planned maintenance.
  2. Given planned maintenance, when it is scheduled, then users are notified in advance.
- **Epic:** System Performance & Availability
- **Sprint:** Sprint 1

---

# End of User Stories
```
