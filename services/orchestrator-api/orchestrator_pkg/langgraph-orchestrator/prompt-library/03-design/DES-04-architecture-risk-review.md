# DES-04 — Architecture Risk Review

**Purpose:** Evaluate architecture against quality attributes with severity + mitigations.

```text
Review this architecture design:

<design>
[PASTE DESIGN DOCUMENT OR DIAGRAM]
</design>

Evaluate against these quality attributes:
1. PERFORMANCE — Bottlenecks, latency hotspots, N+1 query risks
2. SCALABILITY — Limitations at 10x current load
3. SECURITY — Authentication gaps, injection risks, data exposure
4. RELIABILITY — Single points of failure, retry strategies
5. MAINTAINABILITY — Coupling, cohesion, testing difficulty
6. COST — Potential cost inefficiencies in cloud resource usage

For each finding:
- Severity: Critical / High / Medium / Low
- Description of the risk
- Recommended mitigation
- Effort to fix: Low / Medium / High
```
