# Next Chat Task — Milestone 10.1 First Vertical Slice Implementation

## Active Milestone
- Milestone 10.1 — Full Journey Suite (`in-progress`)

## Objective
Implement the first vertical slice of Milestone 10.1 by adding/expanding journey-test coverage for one end-to-end core workflow, then validate it in Codex cloud.

## Scope Lock (current)
In scope for current next task:
- deliver one bounded end-to-end journey test slice from the Milestone 10.1 required journeys
- keep changes focused on test reliability and deterministic assertions
- record implementation evidence under `docs/ai/reports/`

Out of scope for current slice:
- Milestone 10.2 release-freeze bookkeeping
- introducing net-new product features unrelated to journey verification

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- add first-vertical-slice implementation report under `docs/ai/reports/` for Milestone 10.1
