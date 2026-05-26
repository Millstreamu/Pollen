# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 2.4 — Manual Stock Adjustment  
Status: release-candidate

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [x] Product stock can be manually adjusted.
- [x] Material stock can be manually adjusted.
- [x] Adjustment reason is required.
- [x] Inventory movement records are created for adjustments.
- [x] Activity log records are created for adjustments.
- [x] Negative stock is blocked by default.

## Required Verification Checklist
- [x] Typecheck *(Python compile check used in current repo flow)*
- [ ] Lint *(no repo lint command currently defined)*
- [x] Unit tests
- [x] Relevant service/integration tests
- [x] Journey tests if applicable
- [x] Build *(compile check: `python -m compileall -q src tests`)*
- [x] Environment-specific checks or exceptions documented
- [ ] Release smoke test if applicable

## Remaining Required Work
Milestone 2.4 is now in `release-candidate` status after validation/sign-off. Await final release decision to transition to `complete`.

## Optional Post-Milestone Work
- Any enhancements beyond Milestone 2.4 acceptance criteria should be deferred until milestone completion.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.
