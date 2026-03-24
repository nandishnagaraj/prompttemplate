# REL-03 — Deployment & Rollout Strategy

**Purpose:** Recommend feature-flag + canary rollout, metrics, rollback triggers, and comms plan.

```text
Design a safe rollout strategy for:

Feature: [FEATURE]
Risk level: [LOW / MEDIUM / HIGH]
User base: [SIZE AND SEGMENTS]
Infrastructure: [CLOUD PROVIDER / DEPLOYMENT PLATFORM]

Recommend a rollout approach:
1. Feature flag strategy (who sees it first, at what percentages)
2. Canary deployment plan (% of traffic, duration at each stage)
3. Key metrics to monitor during rollout (leading indicators)
4. Automated rollback triggers (metric thresholds)
5. Communication plan (user notifications, status page)
6. Go/no-go decision points during rollout

Include a timeline with clear decision gates.
```
