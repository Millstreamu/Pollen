# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 6.1 — Today Data Summary  
Status: release-candidate

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [x] Add a simple Today summary service/output structure.
- [x] Include counts for key action buckets (orders to pack, low stock, materials to buy, batches in progress, purchases due).
- [x] Keep summary read-only (no workflow mutations).
- [x] Add tests for Today summary behavior.

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
- Milestone 6.1 completion closeout validation + sign-off.

## Optional Post-Milestone Work
- Additional Today UX polish and advanced prioritisation remain out of scope unless explicitly requested.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.

- Milestone 4.2 startup planning + scope lock: completed (2026-05-27).
- Milestone 4.2 release-candidate validation + sign-off: completed (2026-05-27).
- Milestone 4.2 completion closeout sign-off: completed (2026-05-28).
- Milestone 4.3 startup planning + scope lock: completed (2026-05-28).

- Milestone 4.3 stabilization validation: completed (2026-05-28).
- Milestone 4.3 release-candidate validation sign-off: completed (2026-05-28).
- Milestone 4.3 completion closeout sign-off: completed (2026-05-28).
