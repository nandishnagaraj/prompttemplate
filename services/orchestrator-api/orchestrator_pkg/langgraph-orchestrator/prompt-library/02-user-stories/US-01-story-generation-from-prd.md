# US-01 — User Story Generation from PRD

**Purpose:** Convert PRD sections into complete story sets: happy path + errors + edge cases + admin/backend.

```text
You are an Agile BA converting a PRD into user stories.

PRD Section: [PASTE RELEVANT PRD SECTION]

For each user story:
- Format: "As a [persona], I want to [action] so that [benefit]"
- Include a unique Story ID: US-[###]
- Assign story points (Fibonacci: 1,2,3,5,8,13)
- List 3-6 acceptance criteria per story using Gherkin format:

  Given [precondition]
  When [action]
  Then [expected outcome]

- Tag with Epic and Sprint suggestions

Generate ALL stories including:
- Happy path stories
- Error/exception stories
- Edge case stories
- Admin/backend stories (not just user-facing)

Output as structured markdown.
```
