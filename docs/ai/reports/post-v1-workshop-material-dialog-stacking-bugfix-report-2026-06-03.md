# Post-V1 Workshop material dialog stacking bugfix report — 2026-06-03

## Task source

Direct human bug report: while creating a product/recipe in Workshop, choosing **Create New Material** opened the material dialog behind the existing popup, leaving the UI feeling stuck because the visible popup blocked access to the material dialog controls.

## Scope

- Fix the modal stacking issue for the Workshop create-material flow opened from an already-open recipe/product workflow popup.
- Add regression coverage for the modal layering rule.
- Keep the existing Workshop vs Inventory split unchanged.

## Diagnosis

The create-material link used by the recipe workflow points to `#create-material-dialog` while the page can also render the recipe dialog with the persistent `modal-open` class via `return_to_recipe`. Both dialogs used the same modal z-index. Because the recipe dialog is rendered later in the DOM, it could visually sit above the hash-targeted material dialog even though the material dialog was the newly requested popup.

## Implementation

- Split the shared modal display rule into separate rules for persistent server-open modals and hash-targeted modals.
- Kept server-open modals at z-index `50`.
- Promoted the active hash-targeted modal to z-index `70`, so clicking **Create New Material** brings the material dialog above the existing workflow popup.
- Added a focused regression test that verifies the return-to-recipe create-material link and the z-index ordering rules are present together.

## Validation commands

- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `PYTHONPATH=src pytest -q tests/test_app.py -k 'targeted_material_dialog_stacks or create_material_from_recipe'`
- Full validation commands are recorded in the final task response and `docs/ai/reports/latest-check.md`.

## Result

Fixed. The targeted material dialog now stacks above the already-open recipe/product workflow popup instead of appearing behind it.

## Environment limitations

- Pip reported package-index proxy retry warnings while checking for a newer pip release, but required dependencies were already installed and validation could proceed.
- Browser screenshot capture was attempted separately during final validation if tooling was available; if Playwright remains unavailable, deterministic unit/app-shell checks are the verification source.

## Follow-up backlog items

None for this bugfix. A broader modal component extraction could be considered in a future UI refactor, but it is intentionally out of scope here.
