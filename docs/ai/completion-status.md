# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 1.2 — Managed Auth and Shop Ownership  
Status: in-progress

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [x] Logged-out users cannot access private pages.
- [x] Logged-in user gets or creates a shop.
- [x] Records are scoped by `shop_id` (persistence-backed order path).
- [x] User cannot access another shop’s records.

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
Milestone 1.2 closeout/stabilisation checks and final status transition when requested.

## Optional Post-Milestone Work
None yet.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.
