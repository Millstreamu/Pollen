# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 8.1 — Integration Architecture  
Status: in-progress

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [ ] Define integration client interface boundaries for mocked import flow.
- [ ] Define external ID storage + duplicate-protection approach.
- [ ] Define fixture-driven import test strategy (no live API dependency).
- [ ] Define sync/error visibility model and reporting surfaces.

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
- Implement Milestone 8.1 first vertical slice after startup planning scope lock.

## Optional Post-Milestone Work
- Optional future adapters for additional marketplaces beyond Etsy after 8.x hardening.

## Next Required Milestone
- Milestone 8.1 — Integration Architecture (first vertical slice implementation).

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.

- Milestone 6.1 startup planning + scope lock: completed (2026-05-28).
- Milestone 6.1 stabilization validation: completed (2026-05-28).
- Milestone 6.1 release-candidate validation sign-off: completed (2026-05-28).
- Milestone 6.1 completion closeout sign-off: completed (2026-05-28).
