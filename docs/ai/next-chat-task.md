# Next Chat Task — Milestone 10.1 Money Journey Slice

## Active Milestone
- Milestone 10.1 — Full Journey Suite (`in-progress`)

## Objective
Close the remaining Milestone 10.1 journey coverage gap for `money summary updates` before release-candidate validation.

## Scope Lock (current)
In scope for current next task:
- inspect existing Milestone 7.1 product cost/profit behavior and the current Money page surface
- add one bounded deterministic journey assertion for the required money-summary workflow, or document a precise limitation if the current product intentionally does not yet expose a real Money summary
- keep changes limited to the smallest safe implementation needed to satisfy the Milestone 10.1 journey requirement
- update Milestone 10.1 evidence under `docs/ai/reports/`

Out of scope for current slice:
- Milestone 10.2 release-freeze bookkeeping
- full accounting, taxes, analytics, or advanced money dashboards
- new external integrations or live payment data
- optional screenshot evidence unless explicitly scoped

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- add a bounded implementation/validation report under `docs/ai/reports/` for the Milestone 10.1 money journey slice
