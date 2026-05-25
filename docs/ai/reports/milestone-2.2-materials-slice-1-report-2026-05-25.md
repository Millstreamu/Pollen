# Implementation Report — Milestone 2.2 Slice 1 (Materials list + create/edit baseline)

Date: 2026-05-25

## Scope implemented
- Added shop-scoped material domain model and in-memory repository.
- Added `MaterialService` create/list/get/update operations with server-resolved `shop_id` ownership.
- Added first Make/Buy vertical slice UI for materials:
  - materials list view
  - empty state
  - create material form
  - per-row edit baseline via query-driven edit mode
  - low-stock status rendering
- Added tests for service scoping behavior and Make/Buy UI interactions.

## Out of scope (intentionally not implemented)
- Material archive/restore flow.
- Product recipe/material linking (Milestone 2.3).
- Batch make/buy execution workflows.

## Validation run
- `python -m pip install --upgrade pip` (pass with index retry warnings)
- `pip install -r requirements.txt` (pass)
- `pip install -r requirements-dev.txt` (environment-limited: proxy/index blocked for `pytest==8.4.2`)
- `python -m compileall -q src tests` (pass)
- `pytest -q` (pass, `40 passed`)

## Result
- First Milestone 2.2 vertical slice is complete and test-covered in this environment.
