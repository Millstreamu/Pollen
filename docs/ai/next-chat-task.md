# Next Chat Task — Milestone 3.3 First Vertical Slice

Use this brief in future chats to continue work without re-planning.

## Active Milestone
- Milestone 3.3 — Pack and Ship Workflow (`in-progress`)

## Objective
Implement the first end-to-end Milestone 3.3 pack-and-ship slice using the scope lock captured on 2026-05-27.

## Scope Lock (do not expand)
In scope:
- mark `ready_to_pack` order as `packed`
- mark `packed` order as `shipped`
- shipping finalises/resolves reservation exactly once (no double-deduct)
- activity log entries for pack/ship transitions

Out of scope:
- Milestone 3.4+ roadmap work
- cancellation workflow expansion
- large UX expansions unrelated to pack/ship core flow

## Recommended Implementation Order
1. Service/model slice
   - Add guarded pack/ship transitions.
   - Enforce invalid-transition blocking.
   - Resolve reservation at shipping in a no-double-deduct-safe way.
   - Write activity log entries.

2. Tests
   - Add/extend tests for valid transitions and invalid-transition blocking.
   - Add/extend tests to prove shipping does not double-deduct stock.
   - Add milestone journey/integration test for create→pack→ship flow.

3. App/UI wiring
   - Wire minimal actions/endpoints for pack and ship transitions.
   - Return clear transition error feedback consistent with existing behavior.

4. Validation pass
   - Run full Codex-cloud validation commands and record outcomes.

5. Documentation synchronization
   - Update `docs/ai/completion-status.md` and `docs/ai/progress-log.md`.
   - Add milestone implementation report under `docs/ai/reports/`.

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Planning Evidence
- `docs/ai/reports/milestone-3.3-startup-planning-scope-lock-report-2026-05-27.md`
