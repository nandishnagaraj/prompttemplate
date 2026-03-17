# REL-04 — Observability & Alerting Setup

**Purpose:** Instrumentation plan, alert rules, dashboards, runbooks, and SLO burn alerts.

```text
Generate an observability configuration plan for:

Service: [SERVICE NAME]
Stack: [MONITORING STACK — DataDog / Prometheus / CloudWatch / etc.]
SLOs from NFRs:
- Availability: [TARGET %]
- Response time p99: [TARGET ms]
- Error rate: [TARGET %]

Generate:
1. Key metrics to instrument (with metric names and labels)
2. Alert rules (warning and critical thresholds)
3. Dashboard panel definitions
4. Runbook steps for each alert scenario
5. On-call escalation policy recommendation
6. SLO burn rate alert configuration

Format as executable config snippets where possible.
```
