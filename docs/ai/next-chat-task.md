# Next Chat Task — Milestone 6.2 Stabilization Validation

## Active Milestone
- Milestone 6.2 — Today Actions (`in-progress`)

## Objective
Run stabilization validation for Milestone 6.2 after first-slice implementation and advance status if checks remain green.

## Scope Lock (current)
In scope for current next task:
- run full Codex-cloud validation sequence
- verify Today action affordances remain routing-only and explicit
- update milestone status to `stabilising` if validation passes
- publish stabilization validation report evidence

Out of scope for current slice:
- new Today actions beyond current milestone scope
- Milestone 7+ features

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- `docs/ai/reports/milestone-6.2-first-vertical-slice-implementation-report-2026-05-28.md`
