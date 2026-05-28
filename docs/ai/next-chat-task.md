# Next Chat Task — Milestone 7.1 Stabilization Validation

## Active Milestone
- Milestone 7.1 — Backlog/Planning Stream (`in-progress`)

## Objective
Run stabilization validation for Milestone 7.1 and advance status to `stabilising` if checks remain green.

## Scope Lock (current)
In scope for current next task:
- run full Codex-cloud validation sequence
- confirm Milestone 7.1 first-slice behavior remains regression-safe
- update milestone status to `stabilising` if validation passes
- publish stabilization validation report evidence

Out of scope for current slice:
- Milestone 7.1 release-candidate/closeout status transitions
- Milestone 8+ features

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- `docs/ai/reports/milestone-6.2-completion-closeout-signoff-2026-05-28.md`
