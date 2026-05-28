# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 6.2 — Today Actions  
Status: in-progress

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [ ] Add Today-surface action affordances for core next steps.
- [ ] Route actions into existing workflows (order detail/pack, product detail, create batch, create purchase).
- [ ] Keep actions explicit and user-triggered (no hidden automation).
- [ ] Add/adjust tests for Today action availability/routing behavior.

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
- Complete Milestone 6.2 startup planning + scope lock report and implementation handoff.
- Implement first Milestone 6.2 vertical slice.
- Execute stabilization, release-candidate validation, and completion closeout sign-off.

## Optional Post-Milestone Work
- Prioritization/urgency scoring refinement for Today actions.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.

- Milestone 6.1 startup planning + scope lock: completed (2026-05-28).
- Milestone 6.1 stabilization validation: completed (2026-05-28).
- Milestone 6.1 release-candidate validation sign-off: completed (2026-05-28).
- Milestone 6.1 completion closeout sign-off: completed (2026-05-28).
