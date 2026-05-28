# Next Chat Task — Milestone 5.1 First Vertical Slice Implementation

Use this brief in future chats to continue work without re-planning completed slices.

## Active Milestone
- Milestone 5.1 — Buy List / Reorder Suggestions (`in-progress`)

## Objective
Implement the first vertical slice for Milestone 5.1 so low materials are surfaced with understandable reorder suggestions and a simple Add to Purchase affordance, without implementing purchase creation/receiving flows.

## Scope Lock (current)
In scope for current next task:
- surface low-material list in Make/Buy flow
- add suggested reorder quantity rule with clear, deterministic behavior
- add simple “Add to Purchase” action affordance in UI/service flow
- add tests covering low-list visibility and suggestion behavior

Out of scope for current slice:
- implementing Purchase creation workflow persistence (Milestone 5.2)
- implementing Receive Purchase stock mutation (Milestone 5.3)
- automatic ordering or supplier integrations
- Money module expansion

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- `docs/ai/reports/milestone-5.1-startup-planning-scope-lock-report-2026-05-28.md`
