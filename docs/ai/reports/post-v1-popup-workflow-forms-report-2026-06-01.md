# Post-V1 Popup Workflow Forms Report — 2026-06-01

## Task
Convert bottom-of-page workflow forms into popup-style interactions for the app-shell UI, specifically including order creation plus related product and material workflows.

## Scope Implemented
- Added a reusable app-shell workflow dialog renderer that outputs anchored popup markup with dialog semantics, backdrop close target, close control, and a focused card body.
- Converted the order creation workflow from an always-open bottom form into an action card that opens a `#create-order-dialog` popup.
- Converted product creation into a `#add-product-dialog` popup opened from the Products dashboard and workflow area.
- Converted material creation and batch planning into `#add-material-dialog` and `#plan-batch-dialog` popups.
- Converted purchase creation into a `#create-purchase-dialog` popup while preserving the buy-list suggestions and purchase history.
- Added CSS for target-activated modal popups so the existing no-build, server-rendered UI can show dialogs without adding JavaScript or dependencies.
- Updated UI consistency assertions to verify popup targets and dialog markup.

## Intentionally Not Implemented
- No new workflows, routes, models, service logic, persistence changes, JavaScript framework, or external dependencies.
- No nested modal flows or browser-only automation dependency was added.
- Existing edit, archive, restore, receive, pack, ship, and cancel forms remain inline because they are compact row actions rather than large bottom-page creation forms.

## Validation
- `python -m pip install --upgrade pip` — passed with package-index proxy retry warnings; installed pip remained usable.
- `pip install -r requirements.txt` — passed using installed dependencies.
- `pip install -r requirements-dev.txt` — passed using installed dependencies.
- `python -m compileall -q src tests scripts` — passed.
- `ruff check src tests scripts` — passed.
- `PYTHONDONTWRITEBYTECODE=1 pytest -q` — passed (`116 passed`).
- `PYTHONPATH=src python scripts/export_ui_review_pages.py` — passed and regenerated local HTML review pages.
- `PYTHONPATH=src python scripts/capture_ui_screenshots.py` — failed because Playwright is not installed in this Python environment.
- `python -m pip install playwright` — failed because the package-index proxy returned `403 Forbidden` and no Playwright distribution was available.

## Environment Limitations
- Screenshot capture could not be completed in Codex cloud because Playwright is absent and installing it was blocked by the package-index proxy. The deterministic HTML export succeeded and can be opened in a browser-capable environment for visual review.

## Result
The requested forms are now opened through popup-style overlays rather than being visually expanded as bottom-page forms, and the full relevant validation suite passes.
