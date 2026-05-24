# AI Development Instructions

This is the primary instruction file for AI-assisted development in this repository. Every AI coding session starts here.

The goal is to build useful software safely in small verified slices, without scope creep, hidden assumptions, messy debugging residue, or endless "one more improvement" work.

## Core Principle

Build the simplest safe solution that satisfies the current task. Prefer code that is correct, testable, understandable, verifiable in this repo, easy to maintain, small in scope, and safe to roll back.

## Instruction Priority

1. Explicit human instruction in the current task
2. Current GitHub issue, bug plan, or milestone plan
3. This file
4. Safety, testing, debugging, and environment rules
5. Project-specific rules
6. General style preferences

If a conflict could affect safety, data integrity, privacy, money, authentication, or external systems, stop and report the conflict before coding.

## Required Reading

Before significant work, read:

- `docs/ai/project-rules.md`
- `docs/ai/progress-log.md`
- `docs/ai/completion-status.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`
- `docs/ai/project-roadmap.md`

Then read task-specific files:

| Task Type | Required Rule Files |
|---|---|
| Any feature | `docs/ai/development-process.md`, `docs/ai/testing-rules.md`, `docs/ai/task-execution-rules.md` |
| UI work | `docs/ai/ui-rules.md` |
| Bug fixing | `docs/ai/debugging-rules.md`, `docs/ai/diagnostic-cleanup.md` |
| APIs/integrations | `docs/ai/integration-rules.md`, `docs/ai/environment-capabilities.md` |
| Auth/security | `docs/ai/security-rules.md`, `docs/ai/testing-rules.md` |
| Data/money/permissions/destructive actions | `docs/ai/safety-critical-rules.md`, `docs/ai/testing-rules.md` |
| Release/milestone closeout | `docs/ai/finish-line-protocol.md`, `docs/ai/reporting-rules.md` |

## Universal Hard Rules

- Do not add out-of-scope features.
- Do not continue into later milestones unless explicitly asked.
- Do not rename milestones to phases, stages, steps, parts, or tasks.
- Do not refactor unrelated code.
- Do not rewrite large areas unless the task explicitly requires it.
- Do not add dependencies unless scoped or clearly justified.
- Do not claim something was tested unless it was actually tested.
- Do not claim live API/OAuth/Docker/webhook/browser verification unless it actually ran in a supporting environment.
- Humans report symptoms. AI owns reproduction, diagnosis, repair, verification, cleanup, and documentation.
- Do not ask the human to run commands, inspect files, paste snippets, check databases, or confirm hypotheses.
- If root cause is unclear, add targeted diagnostics or tests. Do not guess repeatedly.
- Remove temporary diagnostic code before finishing.
- When acceptance criteria are met and required checks pass, stop.
- Optional ideas go into backlog notes, not the current implementation.

## Startup Report

Before editing code, report:

```text
Task understood:
Task source:
Rule files read:
Project memory files read:
Relevant repo files found:
Existing patterns observed:
Planned changes:
Out-of-scope items:
Risks:
Tests/checks to run:
```

## Finish Report

Before finishing, report:

```text
Changed files:
What was implemented:
What was intentionally not implemented:
Tests/checks run:
Result:
Environment limitations:
Known limitations:
Follow-up backlog items:
Project memory files updated:
```

## Milestone Rule

When instructed to implement a milestone from a plan file:

1. Read this file.
2. Read the plan file.
3. Identify the requested milestone.
4. Implement only that milestone.
5. Do not work on later milestones.
6. Do not rename milestones.
7. Update milestone status and result.
8. Stop.

Allowed milestone statuses: `pending`, `in-progress`, `blocked`, `done`, `skipped`.

## Deferred Work Rule

Items in `docs/ai/do-not-build-yet.md` must not be implemented unless their status is `unlocked` or `in-progress`, the current task explicitly scopes them, unlock conditions are satisfied or waived in a decision record, and acceptance criteria define exactly how far to go.

## Environment Rule

If the current environment cannot support Docker, live APIs, OAuth callbacks, webhook tunnels, or headed browsers: run deterministic mocked/unit/fixture checks, document the limitation, write exact verification steps for a supported environment, and do not claim full verification.

## Evidence Rule

If evidence files exist, read them before debugging or continuing work:

- `docs/ai/reports/latest-server-run.md`
- `docs/ai/reports/latest-check.md`
- `docs/ai/reports/latest-failures.md`
- `docs/ai/known-issues.md`
- `docs/ai/completion-status.md`

Evidence beats guesses.
