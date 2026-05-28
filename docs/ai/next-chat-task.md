# Next Chat Task — Milestone 8.1 Startup Planning + Scope Lock

## Active Milestone
- Milestone 8.1 — Integration Architecture (`not-started`)

## Objective
Prepare Milestone 8.1 startup planning artifacts, lock scope, and transition status to `in-progress` once planning evidence is documented.

## Scope Lock (current)
In scope for current next task:
- define Milestone 8.1 goals, constraints, and acceptance criteria from roadmap
- identify minimal integration architecture slice for mocked Etsy import path
- document risks, out-of-scope boundaries, and verification plan
- update milestone tracking files after planning sign-off

Out of scope for current slice:
- implementing Milestone 8.1 production code
- Milestone 8.2+ behavior changes

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- add startup planning report under `docs/ai/reports/` for Milestone 8.1
