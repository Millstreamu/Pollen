# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 3.4 — Cancel Order  
Status: in-progress

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [x] Cancel eligible (`new` / `ready_to_pack` / `packed` where appropriate) orders.
- [x] Release reserved stock on cancellation.
- [x] Block casual cancellation for `shipped` orders.
- [x] Write activity log entries for cancellation transitions.

## Required Verification Checklist
- [x] Typecheck *(Python compile check used in current repo flow)*
- [x] Lint *(configured via `ruff check src tests`)*
- [x] Unit tests
- [x] Relevant service/integration tests
- [x] Journey tests if applicable
- [x] Build *(compile check: `python -m compileall -q src tests`)*
- [ ] Environment-specific checks or exceptions documented
- [ ] Release smoke test if applicable

## Remaining Required Work
- Progress Milestone 3.4 through stabilising/release-candidate/complete release flow.

## Optional Post-Milestone Work
- UX expansion beyond cancellation core flow remains out of scope unless explicitly requested.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.
