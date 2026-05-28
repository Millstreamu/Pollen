# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 5.3 — Receive Purchase  
Status: in-progress

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [x] Mark purchase as `Received`.
- [x] Increase material stock only on receive.
- [x] Create `InventoryMovement` record on receive.
- [x] Create `ActivityLog` record on receive.
- [x] Block double receiving.
- [x] Keep create-purchase stock mutation at zero.
- [x] Add tests for receive behavior and regressions.

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
- Milestone 5.2 startup planning + scope lock completed on 2026-05-28.
- Milestone 5.2 first vertical-slice implementation completed (2026-05-28).
- Milestone 5.2 stabilization validation completed (2026-05-28).
- Milestone 5.2 release-candidate validation sign-off completed (2026-05-28).
- Milestone 5.2 completion closeout sign-off completed (2026-05-28).

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
