```markdown
# Requirements Traceability Matrix (RTM) — LeaveEase

| Req ID   | Requirement Title             | Business Objective it maps to                                                                 | Priority (MoSCoW) | Estimated Complexity | Dependencies      | Test Verification Method                |
|----------|------------------------------|-----------------------------------------------------------------------------------------------|-------------------|---------------------|-------------------|-----------------------------------------|
| REQ-001  | Employee Leave Request Submission | Digitize and automate the leave request and approval process; Reduce HR workload              | Must              | M                   | REQ-008           | Functional Test, User Acceptance Test   |
| REQ-002  | Manager Leave Approval/Reject | Digitize and automate the leave request and approval process; Reduce HR workload              | Must              | M                   | REQ-001, REQ-008  | Functional Test, User Acceptance Test   |
| REQ-003  | Leave Balance Tracking        | Provide real-time visibility into leave balances; Ensure compliance                           | Must              | M                   | REQ-001, REQ-002  | Functional Test, Data Consistency Check |
| REQ-004  | Team Calendar View            | Provide real-time visibility into team availability; Improve transparency                     | Should            | L                   | REQ-002, REQ-003  | Functional Test, UI Test                |
| REQ-005  | Leave Policy Configuration    | Ensure compliance with company leave policies; Reduce HR workload                             | Should            | M                   | REQ-008           | Functional Test, Admin Acceptance Test  |
| REQ-006  | Reporting & Export            | Reduce HR administrative workload; Improve transparency                                       | Could             | L                   | REQ-003, REQ-005  | Functional Test, Export File Validation |
| REQ-007  | Notifications & Reminders     | Digitize and automate the leave process; Reduce delays; Improve transparency                  | Should            | M                   | REQ-001, REQ-002  | Email Delivery Test, Workflow Test      |
| REQ-008  | User Authentication & Roles   | Ensure compliance; Secure access; Provide role-based visibility                               | Must              | M                   | None              | Security Test, Role Access Test         |
| REQ-009  | Mobile Responsive UI          | >90% user adoption; Improve accessibility                                                     | Should            | M                   | REQ-001–REQ-008   | UI Test (Mobile), Cross-browser Test    |

**Legend:**  
- **Priority:** Must/Should/Could (MoSCoW)  
- **Complexity:** S=Small, M=Medium, L=Large, XL=Extra Large  
- **Dependencies:** Other Req IDs that must be implemented first  
- **Test Verification Method:** How requirement will be verified as met  
```
