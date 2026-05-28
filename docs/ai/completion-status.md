# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 8.1 — Integration Architecture  
Status: release-candidate

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [x] Define integration client interface boundaries for mocked import flow.
- [x] Define external ID storage + duplicate-protection approach.
- [x] Define fixture-driven import test strategy (no live API dependency).
- [x] Define sync/error visibility model and reporting surfaces.

## Required Verification Checklist
- [x] Typecheck *(Python compile check used in current repo flow)*
- [x] Lint *(configured via `ruff check src tests`)*
- [x] Unit tests
- [x] Relevant service/integration tests
- [x] Journey tests if applicable
- [x] Build *(compile check: `python -m compileall -q src tests`)*
- [x] Environment-specific checks or exceptions documented
- [ ] Release smoke test if applicable *(not applicable in current local-only workflow)*

## Remaining Required Work
- Execute Milestone 8.1 completion closeout validation sign-off.

## Optional Post-Milestone Work
- Optional future adapters for additional marketplaces beyond Etsy after 8.x hardening.

## Next Required Milestone
- Milestone 8.1 — Integration Architecture (completion closeout validation sign-off).

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.

- Milestone 6.1 startup planning + scope lock: completed (2026-05-28).
- Milestone 6.1 stabilization validation: completed (2026-05-28).
- Milestone 6.1 release-candidate validation sign-off: completed (2026-05-28).
- Milestone 6.1 completion closeout sign-off: completed (2026-05-28).
