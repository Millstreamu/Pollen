# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 3.2 — Stock Reservation  
Status: in-progress

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [x] Order creation reserves product stock when available.
- [x] Insufficient stock marks order `waiting_on_stock`.
- [x] Product `reserved_stock` updates on successful reservation.
- [x] Product `available_stock` is calculated as on-hand minus reserved.
- [x] No silent over-allocation when stock is insufficient.

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
- Milestone status/release flow still pending (`stabilising` → `release-candidate` → `complete`).
- Optional UX expansion for multi-line order item input is deferred.

## Optional Post-Milestone Work
- Any enhancements beyond Milestone 3.1 acceptance criteria should be deferred until milestone completion.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.
