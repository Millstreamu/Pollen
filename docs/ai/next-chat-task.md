# Next Chat Task — Milestone 5.2 First Vertical Slice Implementation

Use this brief in future chats to continue work without re-planning completed slices.

## Active Milestone
- Milestone 5.2 — Purchase Workflow Persistence (`in-progress`)

## Objective
Implement the Milestone 5.2 first vertical slice for purchase creation persistence, including tests and report evidence.

## Scope Lock (current)
In scope for current next task:
- create persisted Purchase records from Make/Buy flow
- add purchase line items (material + quantity)
- support optional supplier and expected date fields
- persist purchase status in Milestone scope (`Draft`/`Ordered`)
- ensure purchase creation does **not** mutate material stock
- show created purchases in Buy page list
- add tests for creation + no-stock-mutation behavior

Out of scope for current slice:
- purchase receiving stock mutation workflow (Milestone 5.3)
- InventoryMovement or ActivityLog receiving semantics
- supplier automation, smart replenishment, or broader procurement UX redesign

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- `docs/ai/reports/milestone-5.1-completion-closeout-signoff-2026-05-28.md`
- `docs/ai/reports/milestone-5.2-startup-planning-scope-lock-report-2026-05-28.md`
