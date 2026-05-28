# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 4.2 — Start Batch  
Status: release-candidate

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [x] Add Start Batch transition for planned batches.
- [x] Enforce valid status transition rules (planned -> in-progress only).
- [x] Persist start timestamp/status update.
- [x] Block invalid transitions with actionable errors.
- [x] Add tests for successful and blocked start transitions.

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
- Run completion closeout validation/sign-off for Milestone 4.2 and transition to `complete`.

## Optional Post-Milestone Work
- Additional Make/Buy UX polish remains out of scope unless explicitly requested.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.

- Milestone 4.2 startup planning + scope lock: completed (2026-05-27).

- Milestone 4.2 release-candidate validation + sign-off: completed (2026-05-27).
