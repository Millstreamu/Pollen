# Next Chat Task — Milestone 3.2 Release Flow

Use this brief in future chats to continue work without re-planning.

## Active Milestone
- Milestone 3.2 — Stock Reservation (`stabilising`)

## Objective
Complete milestone release flow for Milestone 3.2 by validating current behavior, documenting evidence, and transitioning status through `release-candidate` to `complete` when approved.

## Recommended Implementation Order
1. Release-candidate validation pass
   - Run full validation commands in Codex cloud.
   - Confirm compile and tests are green.
   - Record environment limitations (if any).

2. Status transition
   - Move milestone from `stabilising` to `release-candidate` after successful validation.
   - Keep required scope/verification checklist synchronized with observed results.

3. Sign-off and completion
   - Perform release decision check.
   - Transition `release-candidate` to `complete` when acceptance/sign-off is confirmed.

4. Documentation synchronization
   - Update `docs/ai/completion-status.md` and `docs/ai/progress-log.md` with exact commands and outcomes.
   - Add milestone-specific report under `docs/ai/reports/` if needed for traceability.

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Out of Scope for this slice
- Milestone 3.3+ roadmap work
- New feature additions unrelated to Milestone 3.2 release flow
