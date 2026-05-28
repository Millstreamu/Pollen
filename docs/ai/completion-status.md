# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 4.3 — Complete Batch  
Status: in-progress

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [ ] Add Complete Batch transition for in-progress batches.
- [ ] Enforce valid status transition rules (`in-progress` -> `complete` only).
- [ ] Decrease material stock per product recipe × batch quantity.
- [ ] Increase finished product stock by completed batch quantity.
- [ ] Persist completion timestamp/status update.
- [ ] Block invalid complete transitions with actionable errors.
- [ ] Add tests for successful completion mutations and blocked transitions.

## Required Verification Checklist
- [ ] Typecheck *(Python compile check used in current repo flow)*
- [ ] Lint *(configured via `ruff check src tests`)*
- [ ] Unit tests
- [ ] Relevant service/integration tests
- [ ] Journey tests if applicable
- [ ] Build *(compile check: `python -m compileall -q src tests`)*
- [ ] Environment-specific checks or exceptions documented
- [ ] Release smoke test if applicable *(not applicable in current local-only workflow)*

## Remaining Required Work
- Implement Milestone 4.3 first vertical slice for Complete Batch mutation safety.
- Execute milestone stabilisation/release flow after implementation and regression validation.

## Optional Post-Milestone Work
- Additional Make/Buy UX polish remains out of scope unless explicitly requested.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.

- Milestone 4.2 startup planning + scope lock: completed (2026-05-27).
- Milestone 4.2 release-candidate validation + sign-off: completed (2026-05-27).
- Milestone 4.2 completion closeout sign-off: completed (2026-05-28).
- Milestone 4.3 startup planning + scope lock: completed (2026-05-28).
