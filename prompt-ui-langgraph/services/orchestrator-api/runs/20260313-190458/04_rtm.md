```markdown
| Req ID   | Requirement Title                  | Business Objective it maps to                                                                 | Priority (MoSCoW) | Estimated Complexity | Dependencies         | Test Verification Method                |
|----------|------------------------------------|-----------------------------------------------------------------------------------------------|-------------------|---------------------|----------------------|-----------------------------------------|
| REQ-001  | Employee Leave Application         | Digitize/automate leave process; Reduce HR/managerial workload; Ensure policy compliance      | Must              | M                   | -                    | Functional test, User acceptance test   |
| REQ-002  | Leave Approval Workflow            | Digitize/automate leave process; Reduce approval time; Improve transparency                   | Must              | M                   | REQ-001              | Functional test, Notification test      |
| REQ-003  | Leave Balance Tracking             | Real-time visibility; Reduce errors; Ensure policy compliance                                 | Must              | M                   | REQ-001, REQ-002     | Functional test, Data accuracy test     |
| REQ-004  | Team Calendar View                 | Real-time visibility; Improve transparency; Reduce workload                                   | Should            | M                   | REQ-001, REQ-002, REQ-003 | Functional test, UI test                |
| REQ-005  | Leave Policy Configuration         | Ensure policy compliance; Reduce manual intervention                                          | Should            | L                   | -                    | Functional test, Admin test             |
| REQ-006  | Reporting & Export                 | Reduce HR workload; Improve transparency; Ensure compliance                                   | Could             | M                   | REQ-003, REQ-005      | Functional test, Data export test       |
| REQ-007  | Integration with Company Directory | Digitize/automate process; Reduce errors; Improve adoption                                   | Could             | L                   | -                    | Integration test, SSO login test        |
| REQ-008  | Mobile Responsiveness              | Improve adoption; Reduce workload; Real-time visibility                                       | Must              | M                   | REQ-001 to REQ-004    | Responsive UI test, Cross-device test   |
```

**Legend:**
- **Business Objective it maps to**: Derived from PRD section 3 (Goals & Success Metrics).
- **Priority (MoSCoW)**: Must, Should, Could, Won't (from PRD).
- **Estimated Complexity**: S=Small, M=Medium, L=Large, XL=Extra Large (estimated based on typical implementation effort).
- **Dependencies**: Other requirements that must be implemented first or in parallel.
- **Test Verification Method**: How the requirement will be verified (e.g., functional test, user acceptance test, integration test, UI test, data accuracy test, etc.).
