# Milestone 3.2 — Stock Reservation Report (2026-05-27)

## Scope Delivered
- Implemented reservation-aware product stock model with `reserved_stock` and computed `available_stock`.
- Updated order creation flow to evaluate availability from `available_stock` and reserve stock when order status is `ready_to_pack`.
- Ensured insufficient stock orders are set to `waiting_on_stock` and do not over-allocate reservations.
- Added milestone-focused test coverage for reservation behavior and available-stock calculations.

## Key Decisions
- Reservation is applied only for `ready_to_pack` orders to avoid silently over-allocating unavailable stock.
- Stock availability checks now use `available_stock` (on-hand minus reserved), not raw `stock_on_hand`.
- Existing product edit/adjust flows preserve existing `reserved_stock` values.

## Validation Commands Run
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Validation Result
- Dependency install for dev requirements is environment-limited by package index proxy restrictions for `pytest==8.4.2` (already available in environment).
- Compile check passed.
- Full test suite passed: `58 passed`.

## Risks / Follow-ups
- Reservation release/finalization on pack/ship/cancel is intentionally deferred to Milestone 3.3 and Milestone 3.4.
