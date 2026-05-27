# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 3.4 — Cancel Order  
Status: in-progress

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [ ] Cancel eligible (`new` / `ready_to_pack` / `packed` where appropriate) orders.
- [ ] Release reserved stock on cancellation.
- [ ] Block casual cancellation for `shipped` orders.
- [ ] Write activity log entries for cancellation transitions.

## Required Verification Checklist
- [ ] Typecheck *(Python compile check used in current repo flow)*
- [ ] Lint *(no repo lint command currently defined)*
- [ ] Unit tests
- [ ] Relevant service/integration tests
- [ ] Journey tests if applicable
- [ ] Build *(compile check: `python -m compileall -q src tests`)*
- [ ] Environment-specific checks or exceptions documented
- [ ] Release smoke test if applicable

## Remaining Required Work
- Execute Milestone 3.4 startup planning + scope lock report.
- Implement cancellation workflow slice and tests per roadmap acceptance criteria.
- Run full Codex-cloud validation pass and progress milestone through release flow.

## Optional Post-Milestone Work
- UX expansion beyond cancellation core flow remains out of scope unless explicitly requested.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.
