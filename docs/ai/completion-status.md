# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 2.3 — Product Recipes / Materials Needed  
Status: in-progress

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [x] Material create works with server-side shop scoping.
- [x] Material list/detail/update/archive/restore flows are implemented.
- [x] Material fields include unit, stock, reorder point, and active/archive handling.
- [x] Low-stock status is visible in materials UI and tested.

## Required Verification Checklist
- [x] Typecheck
- [x] Lint
- [x] Unit tests
- [x] Relevant service/integration tests
- [x] Journey tests if applicable
- [x] Build
- [x] Environment-specific checks or exceptions documented
- [x] Release smoke test if applicable

## Remaining Required Work
Milestone 2.2 is signed off as complete. Milestone 2.3 has started; implementation slices for product recipes/materials-needed are pending.

## Optional Post-Milestone Work
- Any additional UX polish beyond Milestone 2.2 acceptance criteria should be deferred until milestone completion.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.
