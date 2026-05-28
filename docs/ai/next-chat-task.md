# Next Chat Task — Milestone 7.1 Release-Candidate Validation

## Active Milestone
- Milestone 7.1 — Backlog/Planning Stream (`stabilising`)

## Objective
Run release-candidate validation for Milestone 7.1 and advance status to `release-candidate` if checks remain green.

## Scope Lock (current)
In scope for current next task:
- run full Codex-cloud validation sequence
- confirm Milestone 7.1 behavior remains regression-safe
- update milestone status to `release-candidate` if validation passes
- publish release-candidate validation report evidence

Out of scope for current slice:
- Milestone 7.1 completion closeout transition
- Milestone 8+ features

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- `docs/ai/reports/milestone-7.1-stabilization-validation-report-2026-05-28.md`
