# Milestone 8.1 — Error Visibility Surface Report (2026-05-28)

## Task
Implement the next Milestone 8.1 task from completion checklist: define sync/error visibility model and reporting surfaces for fixture-driven marketplace imports.

## Changes
- Added `ImportEventService` in `src/pollen/services.py` to capture structured import diagnostics (`level`, `source`, `code`, `message`).
- Wired `MarketplaceImportService` to persist structured error events while preserving existing stdout error lines.
- Added `MarketplaceImportService.list_import_events()` reporting surface for tests and UI/service callers.
- Extended `tests/test_milestone_8_1_marketplace_import.py` to assert structured event capture for invalid payloads.

## Validation
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Outcome
Milestone 8.1 now includes explicit and queryable error visibility for mocked marketplace import failures, without introducing live integration coupling.
