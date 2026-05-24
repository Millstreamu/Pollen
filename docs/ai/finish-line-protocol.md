# Finish-Line Protocol

Completion is not perfection.

A task is complete when acceptance criteria are met, required checks pass or limitations are documented, no blocker remains, scope was respected, temporary diagnostics are cleaned, and required memory is updated.

## Freeze Rule
When a milestone/release enters freeze:

Allowed: blocker fixes, failing test fixes, install/build fixes, security/data fixes, incorrect docs, critical UX blockers.

Not allowed: new features, speculative improvements, broad refactors, new integrations, new screens, extra polish not required for release.

## Remaining Work Classification
- Required blocker: must fix now.
- Optional follow-up: useful later, not required.
- Deferred/do-not-build: intentionally out of scope.

Only required blockers continue the task.

## Stop Rule
If all acceptance criteria are met and checks pass: stop implementation, write final report, update progress/completion files, move optional work to backlog, do not add code.
