# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 4.1 — Create Batch  
Status: stabilising

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [x] Create a planned batch in Make/Buy for a selected product.
- [x] Validate batch quantity input and required fields.
- [x] Check materials-needed versus available quantities for requested batch quantity.
- [x] Block create when required materials are insufficient and return actionable errors.
- [x] Persist create-batch result without starting/completing lifecycle transitions.

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
- Execute Milestone 4.1 stabilization and release-candidate validation/signoff flow.
- Confirm environment exception handling remains documented for dev dependency install proxy/index limitation.

## Optional Post-Milestone Work
- Additional Make/Buy UX polish remains out of scope unless explicitly requested.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.

- Milestone 4.1 create-batch first slice: completed (2026-05-27).
