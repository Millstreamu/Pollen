# Post-V1 UI hardening and screenshot review report — 2026-05-29

## Scope
- Improve the existing local app-shell UI without adding a new framework or external runtime dependency.
- Make pages easier to review with screenshots by adding a consistent visual system and generated review pages.
- Keep this as a post-V1 polish task; no new product workflows or automation were added.

## Implemented
- Added a warmer screenshot-friendly visual system for the app shell: sticky navigation, active-page state, skip link, hero heading, cards, responsive grids, styled forms, styled buttons, and readable tables.
- Added a no-dependency `scripts/export_ui_review_pages.py` helper that seeds demo workflow data and exports the six app-shell pages as standalone HTML files for browser/screenshot review.
- Added optional `scripts/capture_ui_screenshots.py` Playwright support for GitHub Codespaces/local environments that already have browser tooling available.
- Documented the UI review workflow in `README.md`.
- Added regression coverage to ensure the app shell keeps the visual system hooks needed for screenshot review.

## Screenshot-tool note
The Codex cloud package index rejected a Playwright install attempt for browser PNG capture, so Playwright remains optional instead of part of the required repository test install. In GitHub Codespaces where Playwright is available, `PYTHONPATH=src python scripts/capture_ui_screenshots.py` captures PNG screenshots directly. The exported HTML fallback still works without browser dependencies.

## Validation
- `python -m pip install --upgrade pip` — pass with package-index/proxy retry warnings for the optional pip upgrade lookup.
- `pip install -r requirements.txt` — pass.
- `pip install -r requirements-dev.txt` — pass.
- `pip install -r requirements-screenshots.txt && python -m playwright install chromium` — environment-limited; removed this optional dependency path because the package index returned no Playwright distribution in Codex cloud.
- `python -m compileall -q src tests scripts` — pass.
- `ruff check src tests` — pass.
- `pytest -q` — pass (`109 passed`).
- `PYTHONPATH=src python scripts/export_ui_review_pages.py` — pass.
- `PYTHONPATH=src python scripts/capture_ui_screenshots.py --help` — pass.
- `PYTHONPATH=src python scripts/capture_ui_screenshots.py` — environment-limited in Codex cloud with a clear Playwright install message; expected to run in Codespaces when Playwright/browser tooling is installed.
