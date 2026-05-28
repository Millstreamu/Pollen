# Milestone 5.2 First Vertical Slice Implementation Report (2026-05-28)

## Task understood
Implement Milestone 5.2 purchase workflow persistence slice: create persisted purchases from Make/Buy draft, include purchase line items and optional metadata, keep stock unchanged, show purchases in Buy page, and add tests.

## Implemented
- Added in-memory purchase persistence model/repository (`PurchaseRecord`, `PurchaseItemRecord`, `PurchaseRepository`).
- Added `MaterialService.create_purchase_from_draft(...)` with milestone-scoped statuses (`draft`/`ordered`), optional supplier/expected date normalization, purchase-item persistence using existing suggestion quantity rule, and draft clear-on-success behavior.
- Added `MaterialService.list_purchases(...)` for Buy page rendering.
- Updated Make/Buy POST handler with `create_purchase` action.
- Updated Buy list UI to include create-purchase form and created purchases table.
- Added Milestone 5.2 tests for:
  - purchase creation persistence + no material stock mutation
  - Buy page visibility of created purchases

## Out of scope not implemented
- Receiving workflow stock mutation
- Inventory movement/activity log for receiving
- Supplier automation and advanced procurement UX

## Validation commands
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt` *(environment-limited: proxy/index cannot fetch pinned pytest)*
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Validation result
- Compile/lint/tests passed in current environment after implementation (`81 passed`).
- Dev dependency install remains constrained by package index/proxy behavior for pinned `pytest==8.4.2`.
