# Milestone 1.2 Implementation Report (Initial Slice)

Date: 2026-05-24  
Scope reference: `project-roadmap.md` → `Milestone 1.2 — Managed Auth and Shop Ownership`

## What was implemented
- Added managed-auth seam and ownership domain primitives in `src/pollen/auth.py`:
  - `ManagedAuthProvider` abstraction
  - `User`, `Shop`, `AuthContext`
  - `ShopRepository` with first-login shop auto-provisioning
  - `AuthService` context resolution and ownership check API
- Added app-shell protected-route enforcement in `src/pollen/app.py`:
  - `PRIVATE_ROUTES`
  - auth gate returning `401 Unauthorized` for unauthenticated access
  - `can_access_shop_record(...)` helper for server-side ownership checks
- Added tests in `tests/test_app.py` for:
  - private routes requiring login
  - shop auto-provisioning on first login
  - cross-shop access denial
  - ownership helper behavior

## Acceptance criteria coverage snapshot
- Logged-out users cannot access private pages: **covered** (unit tests).
- Logged-in user gets or creates a shop: **covered** (unit tests).
- Records are scoped by `shop_id`: **partially covered** via ownership check helper semantics; persistence-backed records not yet implemented in this repo slice.
- User cannot access another shop’s records: **covered** (unit tests).

## Validation run
Commands run:
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

Results:
- `requirements.txt`: pass
- `requirements-dev.txt`: environment-limited package index access (pytest fetch blocked externally)
- compile: pass
- tests: pass (`11 passed`)

## Notes
- This is a milestone start slice focused on security boundaries and deterministic testability.
- Real managed OAuth provider wiring and persistent data layer integration remain follow-up work inside Milestone 1.2.
