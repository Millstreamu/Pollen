# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 4.1 — Create Batch  
Status: in-progress

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [ ] Create a planned batch in Make/Buy for a selected product.
- [ ] Validate batch quantity input and required fields.
- [ ] Check materials-needed versus available quantities for requested batch quantity.
- [ ] Block create when required materials are insufficient and return actionable errors.
- [ ] Persist create-batch result without starting/completing lifecycle transitions.

## Required Verification Checklist
- [x] Typecheck *(Python compile check used in current repo flow)*
- [x] Lint *(configured via `ruff check src tests`)*
- [x] Unit tests
- [x] Relevant service/integration tests
- [x] Journey tests if applicable
- [x] Build *(compile check: `python -m compileall -q src tests`)*
- [x] Environment-specific checks or exceptions documented
- [x] Release smoke test if applicable *(not applicable in current local-only workflow)*

## Remaining Required Work
- Implement Milestone 4.1 first vertical slice (Create Batch) service/app behavior.
- Add/extend tests for create-batch success and insufficient-material blocking flows.
- Produce implementation report evidence for Milestone 4.1 first slice.

## Optional Post-Milestone Work
- Additional Make/Buy UX polish remains out of scope unless explicitly requested.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.

- Milestone 4.1 create-batch first slice: completed (2026-05-27).
