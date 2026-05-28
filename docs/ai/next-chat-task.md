# Next Chat Task — Milestone 9.1 First Vertical Slice Implementation

## Active Milestone
- Milestone 9.1 — UI Consistency Pass (`stabilising`)

## Objective
Run Milestone 9.1 release-candidate validation and prepare sign-off evidence for the UI consistency slice.

## Scope Lock (current)
In scope for current next task:
- run full Codex-cloud validation command set for Milestone 9.1
- verify first-slice UI consistency behavior remains regression-safe
- record release-candidate sign-off evidence and status advancement

Out of scope for current slice:
- new feature expansion beyond Milestone 9.1 first slice
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
- add first-vertical-slice implementation report under `docs/ai/reports/` for Milestone 9.1
