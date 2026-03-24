```markdown
# LeaveEase — User Stories Set

---

## Epic: Leave Request Management

---

### US-001: Employee Submits Leave Request (Happy Path)
- **As a** Sara Lopez (Employee)
- **I want to** submit a leave request specifying dates, leave type, and reason
- **So that** I can easily request time off and track my requests
- **Story Points:** 3
- **Sprint:** 1

#### Acceptance Criteria
1. **Given** I am logged in as an employee  
   **When** I navigate to the leave request form  
   **Then** I can select leave type, start and end dates, and enter a reason

2. **Given** I have filled all required fields  
   **When** I submit the request  
   **Then** the request is saved and visible in my dashboard

3. **Given** I have submitted a leave request  
   **When** the submission is successful  
   **Then** I see a confirmation message

---

### US-002: Employee Submits Invalid Leave Request (Error Handling)
- **As a** Sara Lopez (Employee)
- **I want to** be prevented from submitting incomplete or invalid leave requests
- **So that** I do not make mistakes or submit requests that cannot be processed
- **Story Points:** 2
- **Sprint:** 1

#### Acceptance Criteria
1. **Given** I leave required fields blank  
   **When** I try to submit the request  
   **Then** I see an error message indicating missing information

2. **Given** I select an end date before the start date  
   **When** I try to submit the request  
   **Then** I see an error message about invalid date range

3. **Given** I enter a reason exceeding the character limit  
   **When** I try to submit the request  
   **Then** I see an error message about the reason length

---

### US-003: Employee Requests Leave Exceeding Balance (Edge Case)
- **As a** Sara Lopez (Employee)
- **I want to** be prevented from requesting more leave than my available balance
- **So that** I do not submit requests that cannot be approved
- **Story Points:** 2
- **Sprint:** 1

#### Acceptance Criteria
1. **Given** my leave balance is less than the requested days  
   **When** I try to submit the request  
   **Then** I see an error message indicating insufficient balance

2. **Given** I have zero balance for a leave type  
   **When** I select that leave type  
   **Then** I am informed that I cannot request this leave

---

### US-004: Employee Views Leave Request Status
- **As a** Sara Lopez (Employee)
- **I want to** view the status of my leave requests
- **So that** I know if my request is pending, approved, or rejected
- **Story Points:** 2
- **Sprint:** 2

#### Acceptance Criteria
1. **Given** I have submitted leave requests  
   **When** I view my dashboard  
   **Then** I see a list of my requests with their current status

2. **Given** my request is approved or rejected  
   **When** I view the request details  
   **Then** I see the manager’s comment (if any)

---

## Epic: Manager Approval Workflow

---

### US-005: Manager Reviews and Acts on Leave Requests (Happy Path)
- **As a** Raj Patel (Manager)
- **I want to** view, approve, or reject leave requests from my team with optional comments
- **So that** I can manage team availability and ensure coverage
- **Story Points:** 3
- **Sprint:** 1

#### Acceptance Criteria
1. **Given** I am logged in as a manager  
   **When** I navigate to the pending requests page  
   **Then** I see all pending requests for my team

2. **Given** I select a request  
   **When** I approve or reject it  
   **Then** I can optionally enter a comment

3. **Given** I approve or reject a request  
   **When** I submit my decision  
   **Then** the employee is notified of the outcome

---

### US-006: Manager Handles Overlapping Leave Requests (Edge Case)
- **As a** Raj Patel (Manager)
- **I want to** be alerted when approving overlapping leave requests
- **So that** I can ensure adequate team coverage
- **Story Points:** 3
- **Sprint:** 2

#### Acceptance Criteria
1. **Given** two or more team members have overlapping leave requests  
   **When** I review a pending request  
   **Then** I see a visual indicator or warning about the overlap

2. **Given** I approve an overlapping request  
   **When** I confirm the approval  
   **Then** the system logs my decision and the overlap

---

### US-007: Manager Cannot Act on Non-Team Requests (Security)
- **As a** Raj Patel (Manager)
- **I want to** be prevented from viewing or acting on leave requests outside my team
- **So that** I only manage my direct reports
- **Story Points:** 2
- **Sprint:** 2

#### Acceptance Criteria
1. **Given** I am a manager  
   **When** I try to access requests from another team  
   **Then** I am denied access and see an appropriate message

---

## Epic: Leave Balance & Policy Management

---

### US-008: System Updates Leave Balance After Approval (Backend)
- **As a** system
- **I want to** automatically update an employee’s leave balance after approval
- **So that** balances are always accurate
- **Story Points:** 2
- **Sprint:** 1

#### Acceptance Criteria
1. **Given** a leave request is approved  
   **When** the approval is recorded  
   **Then** the employee’s leave balance is reduced accordingly

2. **Given** a leave request is rejected  
   **When** the rejection is recorded  
   **Then** the employee’s leave balance remains unchanged

---

### US-009: Employee and Manager View Leave Balances
- **As a** Sara Lopez (Employee) / Raj Patel (Manager)
- **I want to** view my own or my team’s leave balances
- **So that** I can plan leaves and manage team availability
- **Story Points:** 2
- **Sprint:** 2

#### Acceptance Criteria
1. **Given** I am an employee  
   **When** I view my dashboard  
   **Then** I see my current leave balances by type

2. **Given** I am a manager  
   **When** I view my team’s leave balances  
   **Then** I see balances for each direct report

---

### US-010: HR Configures Leave Types and Policies (Admin)
- **As a** Emily Chen (HR Manager)
- **I want to** add or edit leave types, accrual rules, and company holidays
- **So that** the system reflects current company policies
- **Story Points:** 5
- **Sprint:** 3

#### Acceptance Criteria
1. **Given** I am logged in as HR  
   **When** I access the leave policy configuration  
   **Then** I can add new leave types and set accrual rates

2. **Given** I am editing leave policies  
   **When** I save changes  
   **Then** the changes apply to all new leave requests

3. **Given** I am setting company holidays  
   **When** I add or remove a holiday  
   **Then** the calendar and leave calculations update accordingly

---

### US-011: Prevent Leave Requests on Company Holidays (Edge Case)
- **As a** Sara Lopez (Employee)
- **I want to** be prevented from requesting leave on company holidays
- **So that** I do not submit invalid requests
- **Story Points:** 2
- **Sprint:** 3

#### Acceptance Criteria
1. **Given** a selected date is a company holiday  
   **When** I try to submit a leave request for that date  
   **Then** I see an error message and cannot proceed

---

## Epic: Team Calendar & Visibility

---

### US-012: View Team Leave Calendar (Happy Path)
- **As a** Raj Patel (Manager) / Sara Lopez (Employee)
- **I want to** view a calendar showing approved leaves for my team
- **So that** I can plan work and avoid conflicts
- **Story Points:** 3
- **Sprint:** 3

#### Acceptance Criteria
1. **Given** I am a manager or employee  
   **When** I access the team calendar  
   **Then** I see all approved leaves for my team

2. **Given** there are overlapping leaves  
   **When** I view the calendar  
   **Then** overlaps are visually indicated

---

### US-013: Calendar Access Control (Security)
- **As a** system
- **I want to** restrict calendar views to authorized users
- **So that** only team members and managers see relevant leave data
- **Story Points:** 2
- **Sprint:** 3

#### Acceptance Criteria
1. **Given** I am not part of a team  
   **When** I try to view another team’s calendar  
   **Then** I am denied access

---

## Epic: Notifications & Communication

---

### US-014: Email Notifications for Leave Actions (Happy Path)
- **As a** system
- **I want to** send email notifications for leave submission, approval, rejection, and upcoming leaves
- **So that** users are kept informed in a timely manner
- **Story Points:** 3
- **Sprint:** 2

#### Acceptance Criteria
1. **Given** an employee submits a leave request  
   **When** the request is saved  
   **Then** the manager receives an email notification within 5 minutes

2. **Given** a manager approves or rejects a request  
   **When** the action is completed  
   **Then** the employee receives an email notification within 5 minutes

3. **Given** an approved leave is upcoming  
   **When** the leave start date is approaching  
   **Then** the employee and manager receive a reminder email

---

### US-015: Email Delivery Failure (Error Handling)
- **As a** system
- **I want to** log and alert admins if email notifications fail to send
- **So that** communication issues can be addressed promptly
- **Story Points:** 2
- **Sprint:** 2

#### Acceptance Criteria
1. **Given** an email fails to send  
   **When** the system detects the failure  
   **Then** an error is logged and an alert is sent to the admin

---

## Epic: Authentication & Security

---

### US-016: User Authentication and Role-Based Access (Happy Path)
- **As a** user (any persona)
- **I want to** log in securely and access features based on my role
- **So that** my data and permissions are protected
- **Story Points:** 3
- **Sprint:** 1

#### Acceptance Criteria
1. **Given** I am a registered user  
   **When** I enter valid credentials  
   **Then** I am logged in and redirected to my dashboard

2. **Given** I am assigned a role (Employee, Manager, HR Admin)  
   **When** I log in  
   **Then** I see features appropriate to my role

3. **Given** I try to access a restricted feature  
   **When** my role does not permit it  
   **Then** I am denied access

---

### US-017: Invalid Login Attempt (Error Handling)
- **As a** user
- **I want to** see an error message if I enter incorrect login credentials
- **So that** I know to try again or reset my password
- **Story Points:** 1
- **Sprint:** 1

#### Acceptance Criteria
1. **Given** I enter an incorrect username or password  
   **When** I try to log in  
   **Then** I see an error message and remain on the login page

---

### US-018: Password Security (Backend)
- **As a** system
- **I want to** store passwords hashed and salted
- **So that** user credentials are protected from breaches
- **Story Points:** 2
- **Sprint:** 1

#### Acceptance Criteria
1. **Given** a user registers or changes their password  
   **When** the password is saved  
   **Then** it is stored hashed and salted in the database

---

### US-019: Enforce HTTPS (Security)
- **As a** system
- **I want to** enforce HTTPS for all data transmission
- **So that** user data is secure in transit
- **Story Points:** 1
- **Sprint:** 1

#### Acceptance Criteria
1. **Given** a user accesses the web app  
   **When** they use HTTP  
   **Then** they are redirected to HTTPS

---

## Epic: Reporting & Audit

---

### US-020: HR Generates Leave Usage Reports (Admin)
- **As a** Emily Chen (HR Manager)
- **I want to** export leave usage by employee, team, or date range
- **So that** I can analyze trends and report to management
- **Story Points:** 3
- **Sprint:** 4

#### Acceptance Criteria
1. **Given** I am logged in as HR  
   **When** I select report parameters  
   **Then** I can export leave usage data as CSV

2. **Given** I generate a report  
   **When** the export is complete  
   **Then** the file includes all relevant leave records

---

### US-021: HR Views Audit Logs (Admin)
- **As a** Emily Chen (HR Manager)
- **I want to** view audit logs of all leave requests, approvals, and changes
- **So that** I can ensure compliance and trace actions
- **Story Points:** 2
- **Sprint:** 4

#### Acceptance Criteria
1. **Given** I am logged in as HR  
   **When** I access the audit log  
   **Then** I see a chronological list of all actions with timestamps and user info

---

### US-022: Audit Log Integrity (Backend)
- **As a** system
- **I want to** ensure audit logs cannot be tampered with
- **So that** compliance and traceability are maintained
- **Story Points:** 3
- **Sprint:** 4

#### Acceptance Criteria
1. **Given** an action is recorded in the audit log  
   **When** the log is stored  
   **Then** it is write-once and cannot be edited or deleted by users

---

## Epic: Mobile & Responsiveness

---

### US-023: Mobile Responsive UI (Happy Path)
- **As a** user (any persona)
- **I want to** access all core features on my mobile device
- **So that** I can manage leave on the go
- **Story Points:** 5
- **Sprint:** 2

#### Acceptance Criteria
1. **Given** I use a mobile browser with width ≥ 375px  
   **When** I access the web app  
   **Then** all core features are accessible and usable

2. **Given** I use a mobile device  
   **When** I navigate the app  
   **Then** there are no critical UI issues

---

### US-024: Mobile UI Edge Cases (Edge Case)
- **As a** user
- **I want to** be able to scroll and interact with all features on small screens
- **So that** nothing is inaccessible due to device size
- **Story Points:** 2
- **Sprint:** 2

#### Acceptance Criteria
1. **Given** I use a device with a small screen  
   **When** I access forms or calendars  
   **Then** all controls are reachable and usable

---

## Epic: System & Compliance

---

### US-025: System Performance (Backend)
- **As a** system
- **I want to** respond to user actions within 2 seconds for 95% of requests
- **So that** users have a smooth experience
- **Story Points:** 3
- **Sprint:** 3

#### Acceptance Criteria
1. **Given** normal system load  
   **When** a user performs an action  
   **Then** the response time is ≤ 2 seconds for 95% of requests

---

### US-026: GDPR Compliance (Backend)
- **As a** system
- **I want to** handle user data in a GDPR-compliant manner
- **So that** the company avoids legal risks
- **Story Points:** 3
- **Sprint:** 4

#### Acceptance Criteria
1. **Given** user data is stored  
   **When** a user requests data deletion  
   **Then** their data is deleted in accordance with GDPR

2. **Given** user data is processed  
   **When** data is exported or accessed  
   **Then** only authorized users can access it

---

### US-027: Scalability (Backend)
- **As a** system
- **I want to** support up to 500 concurrent users and future multi-tenancy
- **So that** the platform can grow with business needs
- **Story Points:** 5
- **Sprint:** 4

#### Acceptance Criteria
1. **Given** up to 500 users are active  
   **When** they use the system  
   **Then** performance and availability are maintained

2. **Given** a new company is onboarded  
   **When** their data is added  
   **Then** it is logically separated from other companies

---

## Epic: Out of Scope (For Reference)

---

### US-028: Bulk Leave Upload (Explicitly Out of Scope)
- **As a** Emily Chen (HR Manager)
- **I want to** upload leave records in bulk via CSV
- **So that** I can quickly add historical data
- **Story Points:** 0
- **Sprint:** N/A

#### Acceptance Criteria
1. **Given** I am using the MVP  
   **When** I look for bulk upload  
   **Then** I do not see this feature

---

# End of User Stories Set
```
