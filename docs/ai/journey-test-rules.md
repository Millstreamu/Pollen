# Journey Test Rules

Journey tests prove that the program works the way a user actually uses it.

## Required Shape

```md
## Journey: <name>

### Starting State
- ...

### User Actions
1. ...

### Expected Result
- ...

### Safety Assertions
- ...

### Regression Risk
- ...
```

## Rules
- Use deterministic seed data.
- Test outcomes, not implementation details.
- Include invalid or blocked states where important.
- Summarise journey failures in server-run reports if the repo uses them.
- Every workflow feature should define at least one journey, even if the first version is a service-level journey rather than a browser test.
