# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 4.2 — Start Batch  
Status: in-progress

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [ ] Add Start Batch transition for planned batches.
- [ ] Enforce valid status transition rules (planned -> in-progress only).
- [ ] Persist start timestamp/status update.
- [ ] Block invalid transitions with actionable errors.
- [ ] Add tests for successful and blocked start transitions.

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
- Implement Milestone 4.2 first vertical slice (Start Batch transition + tests).
- Run full validation suite and advance milestone through stabilization/release flow.

## Optional Post-Milestone Work
- Additional Make/Buy UX polish remains out of scope unless explicitly requested.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.

- Milestone 4.2 startup planning + scope lock: completed (2026-05-27).
