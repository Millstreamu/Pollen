# Next Chat Task — Milestone 8.1 Completion Closeout Validation Sign-off

## Active Milestone
- Milestone 8.1 — Integration Architecture (`release-candidate`)

## Objective
Run Milestone 8.1 completion closeout validation and sign-off after release-candidate checks passed.

## Scope Lock (current)
In scope for current next task:
- rerun full Codex-cloud validation commands
- confirm Milestone 8.1 integration architecture remains regression-safe at completion gate
- advance status from `release-candidate` to `complete` if checks pass
- capture durable completion closeout sign-off evidence report

Out of scope for current slice:
- live OAuth/API integration
- automatic stock push/sync back to marketplaces
- Milestone 8.2+ full order-mapping behavior beyond Milestone 8.1

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- add completion closeout sign-off report under `docs/ai/reports/` for Milestone 8.1
