# Next Chat Task — Milestone 3.3 Startup

Use this brief in future chats to continue work without re-planning.

## Active Milestone
- Milestone 3.3 — Pack and Ship Workflow (`in-progress`)

## Objective
Start Milestone 3.3 by implementing the first vertical slice of pack-and-ship workflow behavior while preserving current reservation correctness from Milestone 3.2.

## Recommended Implementation Order
1. Startup planning + scope lock
   - Capture Milestone 3.3 acceptance criteria from `project-roadmap.md`.
   - Confirm deferred/out-of-scope boundaries from Milestone 3.2 docs.

2. First vertical slice
   - Implement one end-to-end slice (model/service/tests, then app/UI wiring).
   - Prefer smallest complete behavior that moves order from reservable state toward packed/shipped lifecycle.

3. Validation pass
   - Run full Codex-cloud validation commands and record outcomes.
   - Document any environment limitations if package index/proxy restrictions recur.

4. Documentation synchronization
   - Update `docs/ai/completion-status.md` and `docs/ai/progress-log.md`.
   - Add a milestone report under `docs/ai/reports/` for traceability.

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Out of Scope for this slice
- Milestone 3.4+ roadmap work
- Large UX expansions unrelated to pack/ship core flow
