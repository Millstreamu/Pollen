# Next Chat Task — Milestone 9.1 First Vertical Slice Implementation

## Active Milestone
- Milestone 9.1 — UI Consistency Pass (`in-progress`)

## Objective
Implement the first vertical slice of Milestone 9.1 by applying a consistent beginner-friendly layout and copy pass to one user-facing workflow page.

## Scope Lock (current)
In scope for current next task:
- apply Milestone 9.1 consistency rules to one targeted page/workflow
- keep page to no more than 3 main content areas (Today excluded)
- normalize button treatment, status badge presentation, and empty-state guidance on that page
- remove enterprise-style labels on touched surfaces
- add/update tests that verify adjusted copy/layout-facing output where practical

Out of scope for current slice:
- full app-wide redesign across all pages
- new functional workflows unrelated to UI consistency
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
