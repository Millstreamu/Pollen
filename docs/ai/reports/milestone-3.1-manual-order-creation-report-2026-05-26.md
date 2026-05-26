# Milestone 3.1 — Manual Order Creation Report (2026-05-26)

## Scope Delivered
- Implemented manual order creation with customer name capture, default source `manual`, and stock-aware initial status (`ready_to_pack` or `waiting_on_stock`).
- Added order item persistence and shop-scoped retrieval for order items.
- Wired `/orders` POST flow in app shell with validation error response (`400 Invalid order payload`).
- Added milestone-focused tests for service behavior and Orders page integration flow.

## Key Decisions
- Kept order creation atomic in service: invalid item payload aborts creation.
- Initial status is computed at creation time from available product stock by SKU in the current shop context.
- Reused existing product repository in app shell order flow so order status calculation uses the same product dataset shown in UI.

## Validation Commands Run
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Validation Result
- Dependency install partially blocked by environment package index proxy (403 tunnel failures for PyPI resolution).
- Compile check passed.
- Test suite passed: `55 passed`.

## Risks / Follow-ups
- Status computation currently checks stock-on-hand snapshot only; reservation lifecycle remains Milestone 3.2+.
- Order UI currently supports one line item per submit; multi-line item form UX can be expanded in a follow-up slice.
