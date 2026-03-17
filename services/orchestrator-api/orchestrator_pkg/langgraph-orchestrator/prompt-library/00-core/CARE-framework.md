# CARE Framework for Developer Prompts

Use CARE to consistently get high-quality outputs.

## C — Context
Include: stack + versions, constraints, existing code, repo conventions, deployment env, target users.

## A — Action
State exactly what you want done (generate, refactor, review, design, test, etc.).

## R — Requirements
Specify constraints and non-functionals (security, perf, scalability, error handling), and output format.

## E — Examples
Provide “good” and “bad” examples of style, structure, or patterns when possible.

## Quick checklist
- Role stated (PM/BA/Architect/Dev/QA/Release Manager)
- Tech stack + versions
- Inputs pasted inline (PRD/story/schema/code/diff)
- Output format enforced (markdown/table/JSON/OpenAPI/etc.)
- Constraints explicit (do/don’t, max length, paths)
