# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 7.1 — Product Cost and Estimated Profit  
Status: stabilising

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [x] Add product-level estimated money inputs (sale price, material cost, packaging/shipping cost, platform fee percent).
- [x] Compute and expose estimated platform fee and estimated profit per sale.
- [x] Keep estimates clearly labeled and non-accounting in semantics.
- [x] Add/adjust tests for estimate calculation behavior.

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
- Execute Milestone 7.1 release-candidate validation sign-off.
- Execute Milestone 7.1 completion closeout validation sign-off.

## Optional Post-Milestone Work
- Future rounding/formatting polish for money display surfaces.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.

- Milestone 6.1 startup planning + scope lock: completed (2026-05-28).
- Milestone 6.1 stabilization validation: completed (2026-05-28).
- Milestone 6.1 release-candidate validation sign-off: completed (2026-05-28).
- Milestone 6.1 completion closeout sign-off: completed (2026-05-28).
