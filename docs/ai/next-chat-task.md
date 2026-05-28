# Next Chat Task — Milestone 6.2 Completion Closeout Validation

## Active Milestone
- Milestone 6.2 — Today Actions (`release-candidate`)

## Objective
Run completion closeout validation for Milestone 6.2 and advance status to `complete` if checks remain green.

## Scope Lock (current)
In scope for current next task:
- run full Codex-cloud validation sequence
- confirm Today action affordances and routing behavior remain regression-safe
- update milestone status to `complete` if validation passes
- publish completion closeout sign-off report evidence

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
- `docs/ai/reports/milestone-6.2-release-candidate-validation-signoff-2026-05-28.md`
