# Next Chat Task — Milestone 6.2 Release-Candidate Validation

## Active Milestone
- Milestone 6.2 — Today Actions (`stabilising`)

## Objective
Run release-candidate validation for Milestone 6.2 and advance status if checks remain green.

## Scope Lock (current)
In scope for current next task:
- run full Codex-cloud validation sequence
- confirm Today action affordances still route explicitly to existing workflows
- update milestone status to `release-candidate` if validation passes
- publish release-candidate validation sign-off report evidence

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
- `docs/ai/reports/milestone-6.2-stabilization-validation-report-2026-05-28.md`
