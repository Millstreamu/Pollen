# Milestone 2.3 Polish / Edge Cases Report (2026-05-25)

## Task understood
Continue Milestone 2.3 with remaining polish/edge-case coverage, then transition milestone status when ready.

## Scope delivered
- Added service-level edge-case coverage to ensure archived materials are excluded from recipe planning outputs.
- Verified both `materials_needed` and `can_make_quantity` return safe zero/empty results when a recipe references archived materials.
- Transitioned Milestone 2.3 status from `in-progress` to `stabilising` after successful validation.

## Validation run
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt` *(environment-limited by package index/proxy 403 for pytest wheel lookup)*
- `python -m compileall -q src tests`
- `pytest -q`

## Result
- Compile checks: pass
- Full tests: pass (`49 passed`)
- Milestone status transition: updated to `stabilising`

## Environment limitations
- Dev dependency installation remains partially blocked by upstream index/proxy restrictions in this environment.
