# Prompt Patterns Reference

## Pattern 1 — Role + Task + Constraints
```text
You are a [ROLE] working on [PROJECT/DOMAIN].

Your task: [SPECIFIC ACTION]

Constraints:
- [Constraint 1]
- [Constraint 2]
- [Output format requirement]

Context:
[Paste relevant context here — code, requirements, data model, etc.]
```

## Pattern 2 — Step-by-Step Reasoning (if you want explicit reasoning)
```text
Think step by step before giving your final answer.

1. First, analyze [INPUT] and identify [KEY ASPECTS].
2. Then, consider [TRADEOFFS / RISKS].
3. Finally, produce [OUTPUT].

Show your reasoning in <thinking> tags, then your final answer.
```

## Pattern 3 — Structured Output Format
```text
Generate a [DOCUMENT TYPE] with the following structure:

<section name="overview">
  One paragraph summary
</section>

<section name="requirements">
  Numbered list of requirements
</section>

<section name="risks">
  Bullet list of risks and mitigations
</section>

Respond ONLY with the structured output above. No preamble.
```

## Pattern 4 — Few-Shot Examples
```text
I will show you 2 examples of [TASK], then give you a new input.

EXAMPLE 1:
Input: [example input 1]
Output: [example output 1]

EXAMPLE 2:
Input: [example input 2]
Output: [example output 2]

NEW INPUT:
[Your actual input here]

Now produce the output following the same pattern.
```

## Pattern 5 — Iterative Refinement
```text
Here is a draft [DOCUMENT/CODE] I need you to improve:

<draft>
[PASTE DRAFT HERE]
</draft>

Please:
1. Identify 3 specific weaknesses
2. Explain why each is a weakness
3. Produce an improved version that addresses them

Focus especially on: [SPECIFIC CONCERN — clarity / performance / security / etc.]
```

## Anti-patterns to avoid
- Vague: “Make this better” → specify: readability/perf/security goals
- No context: “Write a login function” → include stack + schema + conventions
- Accepting first output blindly → always review/test/iterate
- One huge prompt for complex work → split into sequential prompts
- Missing output format → always set JSON/markdown/table/code
