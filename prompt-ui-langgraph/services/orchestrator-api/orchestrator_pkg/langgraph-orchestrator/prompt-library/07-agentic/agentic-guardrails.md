# Agentic Coding Guardrails

- Define explicit **STOP conditions** (where the agent must pause for human review).
- Never allow agents to **deploy to production** without explicit human approval.
- Log all agent actions with enough context for audit and rollback.
- Set resource limits: max files modified, max API calls, max execution time.
- Test agentic flows in sandboxed environments before enabling on prod repos.
- Require agents to output a confidence score and auto-escalate on low confidence.

## Suggested human-in-the-loop gates
| Checkpoint | Human review required |
|---|---|
| After design proposal | Architect approves before implementation |
| Before DB migrations | DBA reviews migration scripts |
| After test results | QA lead reviews before marking done |
| Before production deploy | Release manager GO/NO-GO |
| On security findings | Security engineer reviews |
| Confidence < threshold | Escalate automatically |
