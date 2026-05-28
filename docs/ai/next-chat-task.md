# Next Chat Task — Milestone 10.1 Stabilization Validation

## Active Milestone
- Milestone 10.1 — Full Journey Suite (`in-progress`)

## Objective
Validate the Milestone 10.1 first vertical journey slice and decide whether the journey suite can advance toward release-candidate sign-off or needs another bounded journey slice.

## Scope Lock (current)
In scope for current next task:
- run the full Codex-cloud validation sequence
- inspect the new Milestone 10.1 journey-test coverage against the required core workflows
- record stabilization validation evidence under `docs/ai/reports/`
- update milestone status only if the validation evidence supports it

Out of scope for current slice:
- Milestone 10.2 release-freeze bookkeeping
- introducing net-new product features unrelated to journey verification
- optional screenshot evidence unless explicitly scoped

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- add stabilization validation report under `docs/ai/reports/` for Milestone 10.1
