# Next Chat Task — Milestone 8.1 First Vertical Slice Implementation

## Active Milestone
- Milestone 8.1 — Integration Architecture (`in-progress`)

## Objective
Implement the first Milestone 8.1 architecture slice for mocked Etsy import plumbing with isolated interfaces, duplicate guards, and visible error logging.

## Scope Lock (current)
In scope for current next task:
- add integration client interface boundary for Etsy-like mocked source
- add external order ID persistence + duplicate protection strategy
- add fixture-driven import service path (no live API dependency)
- add tests proving isolated integration logic and failure visibility

Out of scope for current slice:
- live OAuth/API integration
- automatic stock push/sync back to marketplaces
- Milestone 8.2+ full order-mapping behavior beyond minimal architecture slice

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- add first-vertical-slice implementation report under `docs/ai/reports/` for Milestone 8.1
