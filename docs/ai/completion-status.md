# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 6.2 — Today Actions  
Status: release-candidate

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [x] Add Today-surface action affordances for core next steps.
- [x] Route actions into existing workflows (order detail/pack, product detail, create batch, create purchase).
- [x] Keep actions explicit and user-triggered (no hidden automation).
- [x] Add/adjust tests for Today action availability/routing behavior.

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
- Execute Milestone 6.2 completion closeout sign-off.

## Optional Post-Milestone Work
- Prioritization/urgency scoring refinement for Today actions.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.

- Milestone 6.1 startup planning + scope lock: completed (2026-05-28).
- Milestone 6.1 stabilization validation: completed (2026-05-28).
- Milestone 6.1 release-candidate validation sign-off: completed (2026-05-28).
- Milestone 6.1 completion closeout sign-off: completed (2026-05-28).
