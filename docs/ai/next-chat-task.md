# Next Chat Task — Milestone 9.1 Completion Closeout Sign-off

## Active Milestone
- Milestone 9.1 — UI Consistency Pass (`release-candidate`)

## Objective
Run Milestone 9.1 completion closeout validation and prepare final completion evidence.

## Scope Lock (current)
In scope for current next task:
- run full Codex-cloud validation command set for Milestone 9.1 closeout gate
- confirm UI consistency slice remains regression-safe at completion gate
- record completion sign-off evidence and status advancement to `complete`

Out of scope for current slice:
- new feature expansion beyond Milestone 9.1
- app-wide redesign beyond existing implemented surfaces
- headed-browser-only manual verification requirements

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- add completion closeout sign-off report under `docs/ai/reports/` for Milestone 9.1
