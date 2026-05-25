# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 2.4 — Manual Stock Adjustment  
Status: in-progress

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [ ] Product stock can be manually adjusted.
- [ ] Material stock can be manually adjusted.
- [ ] Adjustment reason is required.
- [ ] Inventory movement records are created for adjustments.
- [ ] Activity log records are created for adjustments.
- [ ] Negative stock is blocked by default.

## Required Verification Checklist
- [ ] Typecheck
- [ ] Lint
- [ ] Unit tests
- [ ] Relevant service/integration tests
- [ ] Journey tests if applicable
- [ ] Build
- [ ] Environment-specific checks or exceptions documented
- [ ] Release smoke test if applicable

## Remaining Required Work
Milestone 2.3 is complete following human sign-off. Next step is implementing Milestone 2.4 according to roadmap scope and acceptance criteria.

## Optional Post-Milestone Work
- Any enhancements beyond Milestone 2.4 acceptance criteria should be deferred until milestone completion.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.
