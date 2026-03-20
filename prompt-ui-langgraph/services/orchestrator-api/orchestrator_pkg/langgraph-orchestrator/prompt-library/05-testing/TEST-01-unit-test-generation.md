# TEST-01 — Unit Test Generation

**Purpose:** Generate comprehensive unit tests with mocks and high branch coverage.

```text
You are a [LANGUAGE] developer writing unit tests.

Testing framework: [JEST / PYTEST / JUNIT / etc.]
Mocking library: [JEST MOCKS / MOCKITO / UNITTEST.MOCK / etc.]

Code under test:
<source>
[PASTE FUNCTION OR CLASS]
</source>

Dependencies/interfaces:
<dependencies>
[PASTE INTERFACES OR SIGNATURES]
</dependencies>

Generate comprehensive unit tests covering:
1. Happy path (all valid input variations)
2. Boundary values (min, max, empty, null, zero)
3. Error cases (invalid inputs, thrown exceptions)
4. Edge cases specific to this logic
5. Async behavior (if applicable)

For each test:
- Use descriptive test names: "should [behavior] when [condition]"
- Follow AAA pattern: Arrange / Act / Assert
- Mock all external dependencies
- Aim for >= 90% branch coverage

Do not use placeholder tests. Write real, executable tests.
```
