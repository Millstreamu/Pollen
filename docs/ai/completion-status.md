# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 5.1 — Buy List / Reorder Suggestions  
Status: not-started

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [x] Add Complete Batch transition for in-progress batches.
- [x] Enforce valid status transition rules (`in-progress` -> `complete` only).
- [x] Decrease material stock per product recipe × batch quantity.
- [x] Increase finished product stock by completed batch quantity.
- [x] Persist completion timestamp/status update.
- [x] Block invalid complete transitions with actionable errors.
- [x] Add tests for successful completion mutations and blocked transitions.

## Required Verification Checklist
- [x] Typecheck *(Python compile check used in current repo flow)*
- [x] Lint *(configured via `ruff check src tests`)*
- [x] Unit tests
- [x] Relevant service/integration tests
- [x] Journey tests if applicable
- [x] Build *(compile check: `python -m compileall -q src tests`)*
- [x] Environment-specific checks or exceptions documented
- [ ] Release smoke test if applicable *(not applicable in current local-only workflow)*

## Remaining Required Work
- Milestone 5.1 startup planning + scope lock is the next required task.

## Optional Post-Milestone Work
- Additional Make/Buy UX polish remains out of scope unless explicitly requested.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.

- Milestone 4.2 startup planning + scope lock: completed (2026-05-27).
- Milestone 4.2 release-candidate validation + sign-off: completed (2026-05-27).
- Milestone 4.2 completion closeout sign-off: completed (2026-05-28).
- Milestone 4.3 startup planning + scope lock: completed (2026-05-28).

- Milestone 4.3 stabilization validation: completed (2026-05-28).
- Milestone 4.3 release-candidate validation sign-off: completed (2026-05-28).
- Milestone 4.3 completion closeout sign-off: completed (2026-05-28).
