# 📋 Code Review Instructions & Guidelines

This document contains comprehensive instructions and guidelines for AI-powered code review. Use this as a reference for what to look for during code reviews and what constitutes good code quality.

---

## 🎯 **Primary Review Objectives**

### **1. Security First**
- Identify potential security vulnerabilities
- Check for proper input validation and sanitization
- Verify authentication and authorization patterns
- Look for potential injection attacks (SQL, XSS, etc.)
- Ensure sensitive data is properly handled

### **2. Code Correctness**
- Verify logic correctness and edge cases
- Check for potential null/undefined errors
- Validate error handling patterns
- Ensure proper data validation
- Look for race conditions or concurrency issues

### **3. Maintainability**
- Code readability and clarity
- Consistent naming conventions
- Appropriate comments and documentation
- Modular design and separation of concerns
- Avoid code duplication

### **4. Performance**
- Identify performance bottlenecks
- Check for inefficient algorithms
- Look for memory leaks or excessive resource usage
- Database query optimization
- Caching opportunities

### **5. Testing Coverage**
- Missing test cases for critical paths
- Test quality and edge case coverage
- Integration testing needs
- Mock/stub usage appropriateness

---

## 🔍 **Detailed Review Checklist**

### **🛡️ Security Review**

#### **Input Validation**
```typescript
❌ Bad: No validation
function processInput(input: string) {
  return input; // Direct use
}

✅ Good: Proper validation
function processInput(input: string): string {
  if (!input || input.length > 1000) {
    throw new Error('Invalid input');
  }
  return sanitizeHtml(input);
}
```

#### **SQL Injection Prevention**
```typescript
❌ Bad: String concatenation
const query = `SELECT * FROM users WHERE name = '${userName}'`;

✅ Good: Parameterized queries
const query = 'SELECT * FROM users WHERE name = ?';
db.query(query, [userName]);
```

#### **XSS Prevention**
```typescript
❌ Bad: Direct HTML rendering
div.innerHTML = userInput;

✅ Good: Sanitized rendering
div.textContent = userInput;
// or
div.innerHTML = DOMPurify.sanitize(userInput);
```

#### **Authentication Checks**
```typescript
❌ Bad: No auth check
app.get('/admin/data', (req, res) => {
  res.send(sensitiveData);
});

✅ Good: Proper auth
app.get('/admin/data', authenticate, authorize('admin'), (req, res) => {
  res.send(sensitiveData);
});
```

### **⚡ Performance Review**

#### **Database Optimization**
```typescript
❌ Bad: N+1 queries
for (const user of users) {
  const orders = db.query('SELECT * FROM orders WHERE user_id = ?', [user.id]);
}

✅ Good: Batch queries
const orders = db.query('SELECT * FROM orders WHERE user_id IN (?)', [users.map(u => u.id)]);
```

#### **Memory Management**
```typescript
❌ Bad: Memory leaks
const cache = new Map();
function addToCache(key: string, value: any) {
  cache.set(key, value); // Never clears
}

✅ Good: Size-limited cache
const cache = new LRUCache({ max: 1000 });
```

#### **Async Operations**
```typescript
❌ Bad: Sequential async operations
for (const item of items) {
  await processItem(item); // Slow sequential
}

✅ Good: Parallel operations
await Promise.all(items.map(item => processItem(item)));
```

### **🧪 Testing Review**

#### **Test Coverage**
```typescript
❌ Bad: Missing edge cases
test('adds numbers', () => {
  expect(add(2, 3)).toBe(5);
});

✅ Good: Comprehensive testing
test('adds numbers', () => {
  expect(add(2, 3)).toBe(5);
  expect(add(-2, 3)).toBe(1);
  expect(add(0, 0)).toBe(0);
  expect(() => add(null, 1)).toThrow();
});
```

#### **Mock Usage**
```typescript
❌ Bad: Over-mocking
test('user service', () => {
  const mockDb = {
    query: jest.fn().mockReturnValue([]),
    insert: jest.fn().mockReturnValue(1),
    update: jest.fn().mockReturnValue(1),
    delete: jest.fn().mockReturnValue(1)
  };
  // Too many mocks
});

✅ Good: Minimal mocking
test('user service', () => {
  const mockDb = {
    query: jest.fn().mockReturnValue([expectedUser])
  };
  // Only mock what's needed
});
```

---

## 📊 **Severity Classification Guidelines**

### **🔴 Blocker (Critical)**
Must be fixed before merge:

- **Security vulnerabilities** (SQL injection, XSS, auth bypass)
- **Data corruption risks** (race conditions, improper transactions)
- **System crashes** (null pointer exceptions, unhandled errors)
- **Performance disasters** (infinite loops, memory leaks)
- **Legal/compliance issues** (GDPR violations, data privacy)

**Example Comments:**
```
🔴 BLOCKER: SQL Injection Vulnerability
Location: src/user/auth.ts:45
Issue: User input directly concatenated into SQL query
Risk: Database compromise, data theft
Fix: Use parameterized queries immediately
```

### **🟡 Warning (High Priority)**
Should be fixed before merge:

- **Performance issues** (inefficient algorithms, missing indexes)
- **Error handling gaps** (unhandled exceptions, poor error messages)
- **Security hardening** (missing validation, weak cryptography)
- **Maintainability concerns** (complex code, poor naming)
- **Test coverage gaps** (critical paths not tested)

**Example Comments:**
```
🟡 WARNING: Performance Issue
Location: src/api/orders.ts:123
Issue: N+1 database queries in loop
Impact: Slow response times, database load
Fix: Use batch queries or eager loading
```

### **🔵 Suggestion (Medium Priority)**
Nice to have improvements:

- **Code style** (naming conventions, formatting)
- **Documentation** (missing comments, unclear function names)
- **Minor optimizations** (micro-optimizations, clean code)
- **Architecture improvements** (better patterns, refactoring)
- **Additional tests** (edge cases, integration tests)

**Example Comments:**
```
🔵 SUGGESTION: Code Clarity
Location: src/utils/helpers.ts:67
Issue: Complex nested logic hard to understand
Impact: Maintenance difficulty
Fix: Extract to separate function with clear name
```

---

## 🎯 **Language-Specific Guidelines**

### **TypeScript/JavaScript**

#### **Type Safety**
```typescript
❌ Bad: Using 'any'
function processData(data: any): any {
  return data.processed;
}

✅ Good: Proper typing
interface UserData {
  id: number;
  name: string;
}

function processData(data: UserData): ProcessedData {
  return { ...data, processed: true };
}
```

#### **Error Handling**
```typescript
❌ Bad: Silent failures
try {
  await riskyOperation();
} catch (e) {
  // Do nothing
}

✅ Good: Proper error handling
try {
  await riskyOperation();
} catch (error) {
  logger.error('Operation failed', { error, context });
  throw new Error(`Operation failed: ${error.message}`);
}
```

#### **Async/Await Usage**
```typescript
❌ Bad: Mixed patterns
function getData() {
  return fetch('/api/data').then(res => res.json());
}

✅ Good: Consistent async/await
async function getData(): Promise<Data> {
  const response = await fetch('/api/data');
  return response.json();
}
```

### **Python**

#### **Type Hints**
```python
❌ Bad: No type hints
def process_data(data):
    return data.upper()

✅ Good: Proper type hints
from typing import Union

def process_data(data: Union[str, bytes]) -> str:
    return str(data).upper()
```

#### **Exception Handling**
```python
❌ Bad: Bare except
try:
    risky_operation()
except:
    pass

✅ Good: Specific exceptions
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    retry_operation()
```

### **Java**

#### **Null Safety**
```java
❌ Bad: Null checks everywhere
if (user != null && user.getName() != null) {
    return user.getName().toUpperCase();
}

✅ Good: Optional usage
return Optional.ofNullable(user)
    .map(User::getName)
    .map(String::toUpperCase)
    .orElse("UNKNOWN");
```

#### **Resource Management**
```java
❌ Bad: Manual resource handling
FileInputStream fis = new FileInputStream("file.txt");
// Might leak if exception occurs
fis.close();

✅ Good: Try-with-resources
try (FileInputStream fis = new FileInputStream("file.txt")) {
    // Auto-closed
    processFile(fis);
}
```

---

## 🏗️ **Architecture Review Guidelines**

### **Design Patterns**
- ✅ **SOLID Principles**: Single responsibility, open/closed, etc.
- ✅ **DRY**: Don't repeat yourself
- ✅ **KISS**: Keep it simple, stupid
- ✅ **YAGNI**: You aren't gonna need it

### **Code Organization**
```
src/
├── controllers/     # HTTP handlers
├── services/        # Business logic
├── repositories/    # Data access
├── models/          # Data structures
├── utils/           # Helper functions
├── types/           # Type definitions
└── tests/           # Test files
```

### **API Design**
```typescript
❌ Bad: Inconsistent API
GET /api/user/123
POST /api/createUser
PUT /api/users/123/update

✅ Good: RESTful API
GET /api/users/123
POST /api/users
PUT /api/users/123
DELETE /api/users/123
```

---

## 📝 **Review Comment Templates**

### **Security Issues**
```
🔴 SECURITY: [Issue Title]
Location: [file:line]
Problem: [Detailed description of security issue]
Risk: [Potential impact]
Recommendation: [Specific fix needed]
Resources: [Links to security best practices]
```

### **Performance Issues**
```
⚡ PERFORMANCE: [Issue Title]
Location: [file:line]
Problem: [Performance bottleneck description]
Impact: [Effect on system performance]
Solution: [Optimization approach]
Metrics: [Expected improvement]
```

### **Code Quality**
```
📝 QUALITY: [Issue Title]
Location: [file:line]
Problem: [Code quality issue]
Impact: [Effect on maintainability]
Suggestion: [Improvement approach]
Example: [Code snippet showing better approach]
```

### **Testing Issues**
```
🧪 TESTING: [Issue Title]
Location: [file:line]
Problem: [Testing gap or issue]
Coverage: [What's not being tested]
Recommendation: [Test improvements needed]
Example: [Test code example]
```

---

## 🎯 **Review Process Workflow**

### **1. Initial Assessment**
- [ ] Understand the PR purpose and scope
- [ ] Review the description and acceptance criteria
- [ ] Check for proper documentation
- [ ] Verify test coverage for new features

### **2. Code Analysis**
- [ ] Security vulnerability scan
- [ ] Performance impact assessment
- [ ] Code quality evaluation
- [ ] Architecture consistency check

### **3. Testing Review**
- [ ] Test coverage analysis
- [ ] Test quality assessment
- [ ] Edge case verification
- [ ] Integration test needs

### **4. Final Recommendations**
- [ ] Summarize critical issues (blockers)
- [ ] List important improvements (warnings)
- [ ] Suggest enhancements (suggestions)
- [ ] Provide overall assessment

---

## 📊 **Quality Metrics**

### **Code Quality Indicators**
- **Cyclomatic Complexity**: < 10 per function
- **Function Length**: < 50 lines
- **File Length**: < 500 lines
- **Test Coverage**: > 80%
- **Duplicate Code**: < 3%

### **Performance Indicators**
- **Response Time**: < 200ms for API calls
- **Database Queries**: < 5 per request
- **Memory Usage**: < 100MB for typical operations
- **CPU Usage**: < 50% under normal load

### **Security Indicators**
- **No SQL injection vulnerabilities**
- **No XSS vulnerabilities**
- **Proper authentication/authorization**
- **Input validation on all endpoints**
- **Sensitive data encrypted**

---

## 🚀 **Best Practices Summary**

### **Do's**
✅ **Validate all inputs** - Never trust user input  
✅ **Handle errors gracefully** - Provide meaningful error messages  
✅ **Write tests** - Cover critical paths and edge cases  
✅ **Use types** - Leverage type systems for safety  
✅ **Document complex logic** - Explain why, not just what  
✅ **Follow patterns** - Be consistent with existing codebase  
✅ **Consider performance** - Think about scale and efficiency  
✅ **Security first** - Always consider security implications  

### **Don'ts**
❌ **Don't use 'any'** - Use proper types  
❌ **Don't ignore errors** - Handle or log appropriately  
❌ **Don't hardcode values** - Use configuration  
❌ **Don't skip tests** - Test your code thoroughly  
❌ **Don't over-engineer** - Keep it simple  
❌ **Don't commit secrets** - Use environment variables  
❌ **Don't ignore warnings** - Address compiler/linter warnings  
❌ **Don't optimize prematurely** - Profile first  

---

## 📚 **Reference Resources**

### **Security**
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Security Best Practices](https://snyk.io/blog/10-security-best-practices-for-developers/)
- [Common Vulnerabilities](https://cwe.mitre.org/)

### **Performance**
- [Web Performance](https://web.dev/performance/)
- [Database Optimization](https://use-the-index-luke.com/)
- [Code Optimization](https://optimization.guide/)

### **Code Quality**
- [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350884)
- [Refactoring](https://refactoring.com/)
- [Design Patterns](https://refactoring.guru/design-patterns)

---

## 🎯 **AI Review Instructions Summary**

When reviewing code, the AI should:

1. **Analyze security implications** first and foremost
2. **Check for correctness** and potential bugs
3. **Evaluate performance** and scalability
4. **Assess maintainability** and code quality
5. **Verify test coverage** and quality
6. **Provide actionable feedback** with specific examples
7. **Categorize findings** by severity (blocker/warning/suggestion)
8. **Suggest concrete improvements** with code examples

**Remember**: The goal is to help developers write better, more secure, and maintainable code while being constructive and educational in the feedback provided.

---

*This document should be updated regularly based on team feedback, new security threats, and evolving best practices.*
