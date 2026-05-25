# Implementation Report — Milestone 2.2 Slice 2 (Materials archive/deactivate + restore)

Date: 2026-05-25

## Scope
- Continue Milestone 2.2 by adding archive/deactivate and restore behavior for materials.
- Extend material service/repository + Make/Buy UI flow to support archived state views.
- Add tests for service ownership/scoping and UI interactions.

## Changes Implemented

### 1) Material domain and service behaviors
- Added archive and restore operations in `MaterialRepository`:
  - `archive_for_shop(...)`
  - `restore_for_shop(...)`
- Added matching service methods in `MaterialService`:
  - `archive_material(...)`
  - `restore_material(...)`
- Behavior follows existing shop-scoped semantics:
  - authenticated shop can mutate only its own materials
  - unauthenticated and cross-shop mutations are denied

### 2) Make/Buy page interactions
- Added POST actions for materials:
  - `archive`
  - `restore`
- Added query-based material list filters:
  - `view=active`
  - `view=archived`
  - `view=all`
- Added Archived materials section with per-row restore buttons.
- Added row-level Archive button for active materials.

### 3) Test coverage
- Added service test for material archive/restore behavior, list scoping, and cross-shop denial.
- Added app-level UI test for archive/restore interactions and filter rendering behavior.

## Validation Run
Commands executed:
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

Result:
- Compile checks passed.
- Full test suite passed.

## Outcome
- Milestone 2.2 now includes archive/deactivate + restore support for materials with test coverage.
