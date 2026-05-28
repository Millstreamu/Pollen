# Next Chat Task — Milestone 6.1 First Vertical Slice Implementation

## Active Milestone
- Milestone 6.1 — Today Data Summary (`in-progress`)

## Objective
Implement the first vertical slice for Today summary service behavior and tests.

## Scope Lock (current)
In scope for current next task:
- add read-only Today summary service output
- include required counts: orders to pack, low stock, materials to buy, batches in progress, purchases due
- keep implementation minimal and deterministic
- add tests for summary behavior

Out of scope for current slice:
- advanced prioritization logic
- UI redesign
- notifications/automation

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- `docs/ai/reports/milestone-6.1-startup-planning-scope-lock-report-2026-05-28.md`
