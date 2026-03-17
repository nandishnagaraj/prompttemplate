```markdown
# Requirements Traceability Matrix (RTM) — LeaveEase

| Req ID   | Requirement Title                | Business Objective it maps to                                                                 | Priority (MoSCoW) | Estimated Complexity | Dependencies         | Test Verification Method                |
|----------|----------------------------------|-----------------------------------------------------------------------------------------------|-------------------|---------------------|---------------------|-----------------------------------------|
| REQ-001  | Employee Leave Request Submission| Automate and centralize leave management; Enhance employee experience                         | Must              | M                   | REQ-008             | Functional test, User acceptance test   |
| REQ-002  | Manager Leave Approval/Reject    | Automate and centralize leave management; Improve transparency; Enhance manager experience    | Must              | M                   | REQ-001, REQ-008    | Functional test, User acceptance test   |
| REQ-003  | Leave Balance Tracking           | Reduce errors in leave tracking; Ensure compliance; Improve transparency                      | Must              | M                   | REQ-001, REQ-002    | Functional test, Unit test, UAT         |
| REQ-004  | Team Leave Calendar              | Enhance manager/employee experience; Improve transparency                                    | Should            | M                   | REQ-001, REQ-002, REQ-003 | Functional test, UI test, UAT      |
| REQ-005  | Leave Policy Configuration       | Ensure compliance with company leave policies; Support business growth                        | Should            | L                   | REQ-008             | Functional test, UAT, Admin test        |
| REQ-006  | Reporting & Audit Logs           | Ensure compliance; Reduce admin overhead; Improve transparency                               | Could             | L                   | REQ-001, REQ-002, REQ-003, REQ-005 | Functional test, Data export test |
| REQ-007  | Email Notifications              | Reduce manual HR interventions; Enhance experience; Improve transparency                      | Must              | M                   | REQ-001, REQ-002    | Integration test, Notification test     |
| REQ-008  | User Authentication & Role Mgmt  | Ensure compliance; Secure access; Automate leave management                                  | Must              | M                   | None                | Security test, Role-based access test   |
| REQ-009  | Mobile Responsive UI             | Enhance employee/manager experience; Improve adoption                                        | Should            | M                   | REQ-001, REQ-002, REQ-003, REQ-004, REQ-007, REQ-008 | UI test, Cross-device test      |
| REQ-010  | Bulk Leave Upload                | (Not in MVP)                                                                                  | Won’t             | L                   | None                | N/A (Not implemented in MVP)            |

```

**Legend:**
- **MoSCoW:** Must, Should, Could, Won’t
- **Complexity:** S = Small, M = Medium, L = Large, XL = Extra Large
- **Test Verification Method:** UAT = User Acceptance Test

---

**Notes:**
- Non-functional requirements (performance, security, etc.) are not listed as individual Req IDs but are verified via system, security, and compliance testing.
- Dependencies indicate which requirements must be implemented for this requirement to function as intended.
```