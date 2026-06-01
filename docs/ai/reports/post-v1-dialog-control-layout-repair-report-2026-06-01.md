# Post-V1 Dialog Control Layout Repair Report — 2026-06-01

## Task
Fix popup UI regressions reported from screenshots where workflow dialog text boxes were formatted incorrectly and submit/cancel buttons were too close to fields or appeared with default browser styling instead of the intended Pollen button design.

## AI Development Method
Followed the repo process: Spec → Scan → Simplify → Slice → Verify → Clean → Freeze → Ship.

### Spec
- Goal: restore polished workflow dialog input and button presentation.
- User value: popup forms should match the original Pollen visual intent and remain comfortable to use.
- Scope: CSS/markup repair for existing popup workflow dialogs only.
- Out of scope: no new workflows, routes, persistence, services, JavaScript framework, or broad redesign.
- Acceptance criteria: dialog inputs size correctly, dialog actions are separated from fields, primary/secondary buttons use the Pollen button system, and regression coverage exists.

### Scan
Read the primary AI development instructions, UI/testing/debugging/task rules, project memory, latest relevant popup report, app-shell renderer, and UI consistency tests. The root cause was that dialog submit buttons were plain `<button>` elements outside the existing `.primary`/`.outline` button styling path, and form actions were direct grid items without a dedicated full-width action row. Inputs also lacked explicit width/box sizing in form grids, which made dialog field sizing more fragile.

### Simplify
The simplest safe fix was a UI-only slice:
- keep the existing server-rendered forms and posts;
- add a reusable dialog action row wrapper;
- apply existing primary/outline button classes;
- harden grid input sizing with `width: 100%` and `box-sizing: border-box`;
- add regression assertions against the rendered app-shell HTML/CSS.

### Slice
Updated only the existing popup workflows:
- Add product
- Add material
- Plan a batch
- Create purchase
- Create order

## Implementation
- Wrapped each dialog's submit/cancel controls in a `.dialog-actions` row so actions span the form grid and no longer crowd the last text box.
- Applied `.primary` to dialog submit buttons so they render with the intended Pollen yellow button treatment.
- Kept cancel links as `.outline` buttons to match the orange outlined secondary treatment from the reference renders.
- Hardened text inputs/selects in form grids with full-width border-box sizing and inherited app typography.
- Added dialog-specific action CSS with wrapping, spacing, right alignment, and minimum action widths.
- Added UI consistency regression coverage for polished dialog controls and spacing CSS.

## Validation
- `python -m pip install --upgrade pip` — passed with package-index proxy retry warnings; existing pip remained usable.
- `pip install -r requirements.txt` — passed; no runtime packages are required.
- `pip install -r requirements-dev.txt` — passed using installed `pytest` and `ruff`.
- `python -m compileall -q src tests scripts` — passed.
- `ruff check src tests scripts` — passed.
- `PYTHONDONTWRITEBYTECODE=1 pytest -q` — passed (`117 passed`).
- `PYTHONPATH=src python scripts/export_ui_review_pages.py` — passed and regenerated deterministic local HTML review pages.
- `PYTHONPATH=src python scripts/capture_ui_screenshots.py` — blocked because Playwright is not installed in this Python environment.
- `python -m pip install playwright` — blocked because the package-index proxy returned `403 Forbidden` and no Playwright distribution was available.

## Environment Limitations
Browser screenshot capture could not be completed in Codex cloud because no browser binary or Playwright package is available, and installing Playwright was blocked by the configured package-index proxy. The deterministic HTML export completed successfully and contains the repaired dialog markup/CSS for browser-capable review.

## Result
The existing popup workflows now use robust full-width form controls and a dedicated, spaced dialog action row with Pollen primary/outline button styling. Full compile, lint, and test validation passes.

## Follow-Up Backlog
- In a browser-capable environment, install Playwright/Chromium and capture reviewed screenshots for the dialog opened states.
