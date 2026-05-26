# Milestone 2.4 Implementation Report — Manual stock adjustment + audit trail (2026-05-25)

## Scope delivered
- Added inventory audit domain support with `InventoryMovementRecord` and `ActivityLogRecord`, including in-memory repositories for shop-scoped listing.
- Implemented product stock adjustment API in `ProductService` with required reason, zero-delta rejection, and negative-stock blocking.
- Implemented material stock adjustment API in `MaterialService` with required reason, zero-delta rejection, and negative-stock blocking.
- Wired UI post actions for manual stock adjustment on product and material rows.
- Added audit rendering sections to show inventory movements and activity logs.
- Added Milestone 2.4 tests for service-level adjustment validation and a journey test proving material stock change plus movement/activity visibility.

## Validation run
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt` *(environment-limited: index/proxy returns 403 for pytest package resolution)*
- `python -m compileall -q src tests`
- `pytest -q`

## Outcome
Milestone 2.4 is implemented for safe manual stock adjustment with reason capture and audit records. Stock increase/decrease works, negative stock is blocked, and both movement/activity records are created and surfaced in UI/journey coverage.
