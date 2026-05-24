# Bug Fix Plan: BUG-0000 Short Name

Status: active  
Bug issue: #0000  
Created: YYYY-MM-DD  
Owner: Codex  
Terminology: Milestone

## Terminology Rule
This file uses **Milestone** as the only unit of work. Do not rename milestones to phases, stages, steps, parts, or tasks. When instructed to implement a milestone, implement only that milestone.

## Bug Summary

### Observed Behaviour
...

### Expected Behaviour
...

### Affected Area
...

## Rules
- Do not ask the human to run commands.
- Reproduce using tests or diagnostics where practical.
- Do not make speculative fixes.
- Do not refactor unrelated code.
- Do not add new features.
- Remove temporary debug code before completion.
- Update this file after each milestone.
- Update `docs/ai/progress-log.md` during closeout.

## Completion Criteria
- [ ] Root cause identified
- [ ] Regression test or documented reproduction exists
- [ ] Root cause fixed
- [ ] Relevant tests pass
- [ ] Full available checks pass or limitations documented
- [ ] Temporary diagnostics removed
- [ ] Debug report added/updated
- [ ] Progress log updated
- [ ] Active bug plan moved to completed or removed by policy

# Milestones

## Milestone 1: Reproduce and Locate the Failure

Status: pending

### Goal
Create reliable evidence and identify likely failing area.

### Scope
Inspect relevant code, read reports, reproduce where practical, add focused diagnostics if needed. Do not implement final fix unless explicitly allowed.

### Acceptance Criteria
- [ ] Failure reproduced or documented
- [ ] Suspected root cause area identified
- [ ] Regression strategy written
- [ ] Status updated

### Milestone 1 Result
```text
Files inspected:
Reproduction method:
Failure observed:
Suspected root cause:
Tests/checks run:
Next milestone recommendation:
```

## Milestone 2: Add Regression Coverage

Status: pending

### Goal
Add a test/check that catches this bug.

### Scope
Add focused deterministic coverage. Do not add unrelated implementation.

### Acceptance Criteria
- [ ] Regression coverage exists
- [ ] Coverage is focused
- [ ] Status updated

### Milestone 2 Result
```text
Test files changed:
Test cases added:
Expected failure before fix:
Checks run:
Notes:
```

## Milestone 3: Implement the Smallest Root-Cause Fix

Status: pending

### Goal
Fix root cause with smallest safe change.

### Scope
Fix only root cause, keep logic in correct layer, no unrelated refactor/features.

### Acceptance Criteria
- [ ] Regression test passes
- [ ] Relevant existing tests pass
- [ ] No unrelated behaviour changed
- [ ] Status updated

### Milestone 3 Result
```text
Root cause:
Fix implemented:
Files changed:
Tests/checks run:
Notes:
```

## Milestone 4: Cleanup Diagnostics

Status: pending

### Goal
Remove temporary debug code and keep only intentional diagnostics.

### Acceptance Criteria
- [ ] No temporary debug code remains
- [ ] Debug cleanup checklist passes
- [ ] Status updated

### Milestone 4 Result
```text
Temporary diagnostics removed:
Permanent diagnostics kept:
Cleanup checks run:
Notes:
```

## Milestone 5: Full Verification

Status: pending

### Goal
Run required verification and record evidence.

### Acceptance Criteria
- [ ] Targeted checks pass
- [ ] Full available checks pass or limitations documented
- [ ] Evidence recorded
- [ ] Status updated

### Milestone 5 Result
```text
Commands run:
Results:
Environment limitations:
Report files updated:
Notes:
```

## Milestone 6: Closeout

Status: pending

### Goal
Close bug plan and record final result.

### Acceptance Criteria
- [ ] Progress log updated
- [ ] Known issues updated if needed
- [ ] Debug report complete
- [ ] Bug plan finalised
- [ ] Status updated

### Milestone 6 Result
```text
Progress log updated:
Known issues updated:
Debug report:
Bug plan final location:
Final status:
```
