# Task Execution Rules

## Source of Truth
The task source may be a GitHub issue, milestone plan, bug plan, release checklist, or direct human request. If a plan file exists, follow it exactly.

## Single-Scope Rule
Implement only the requested scope. Adjacent ideas become follow-up notes.

## Change Budget
Unless explicitly allowed, avoid unrelated files, new dependencies, migrations, navigation changes, global style changes, and refactors. If scope must expand, stop and report why.

## Before Editing Checklist
- [ ] Read `AI_DEVELOPMENT.md`
- [ ] Read project memory files
- [ ] Read task-specific rules
- [ ] Confirm source of truth
- [ ] Check deferred work
- [ ] Identify relevant files
- [ ] Identify tests/checks
- [ ] State out-of-scope items

## During Implementation
Keep logic in the correct layer. Do not bypass validation. Do not hardcode non-test values. Do not change public behaviour beyond the task. Match existing naming and patterns.

## Before Finishing Checklist
- [ ] Acceptance criteria met
- [ ] Tests/checks run or limitation documented
- [ ] Temporary diagnostics removed
- [ ] No unrelated refactors
- [ ] Project memory updated where required
- [ ] Follow-up work documented, not implemented

## If Blocked
Mark the task/milestone as blocked, explain the blocker, describe what was verified, describe what remains unknown, and provide the exact next action.
