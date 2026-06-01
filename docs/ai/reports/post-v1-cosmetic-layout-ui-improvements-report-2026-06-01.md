# Post-V1 Cosmetic Layout UI Improvements Report — 2026-06-01

## Task source

Direct human request after reviewing the latest server-test screenshots in `docs/ai/ui-screenshots/`.

## Scope

Implemented cosmetic and layout-only improvements. No product features, routes, workflows, domain services, persistence changes, integrations, or business rules were added.

## References used

- `AI_DEVELOPMENT.md` — Spec → Scan → Simplify → Slice → Verify → Clean → Freeze → Ship method.
- `docs/ai/ui-rules.md` — clear hierarchy, obvious primary actions, styled buttons/forms, visible statuses, simple layout, and responsive behavior.
- `project-roadmap.md` — final product should feel like a simple, calm shop operating system for small sellers, not a corporate ERP.
- Latest screenshots in `docs/ai/ui-screenshots/` — visual evidence for the roughest areas: raw lower-page workflow forms, dense long workflow sections, table action crowding, and blank money empty state.

## Changes made

- Added a reusable workflow-card treatment for lower-page operational sections so Products & Stock, Make / Buy, and Orders no longer visually drop from polished dashboard cards into raw HTML blocks.
- Added form-grid and compact-form layout styling for existing forms, keeping the same fields and submit actions while improving spacing, label alignment, field sizing, and scanability.
- Added inline-form and record-tool styling for existing bulk/recipe/purchase controls so they read as secondary tools rather than unfinished browser defaults.
- Improved segmented filter presentation for material views and product view links without changing the underlying query behavior.
- Improved empty-state presentation for buy-list and money chart states while preserving the existing empty-state copy and next-step links.
- Added table polish for workflow panels: borders, row containment, nowrap treatment for IDs/action cells, and consistent inline row actions.
- Added recipe-card and audit/workflow visual containment to reduce the long-page density noted in the screenshot review.

## Intentionally not changed

- No new screens or navigation destinations.
- No new workflows or domain capabilities.
- No data model, repository, service, or auth changes.
- No new dependencies were added to repo configuration.
- Existing tests and UI assertions were preserved rather than rewritten around a broad redesign.

## Validation commands and results

- `python -m pip install --upgrade pip` — passed with package-index proxy retry warnings; existing pip remained usable.
- `pip install -r requirements.txt` — passed using installed dependencies.
- `pip install -r requirements-dev.txt` — passed using installed dependencies.
- `python -m compileall -q src tests scripts` — passed.
- `ruff check src tests scripts` — passed.
- `PYTHONDONTWRITEBYTECODE=1 pytest -q` — passed, `116 passed`.
- `PYTHONPATH=src pytest -q tests/test_milestone_9_1_ui_consistency.py tests/test_app.py tests/test_ui_review_scripts.py` — passed, `40 passed`.
- `PYTHONPATH=src python scripts/export_ui_review_pages.py` — passed and generated ignored local HTML review pages.
- `PYTHONPATH=src python scripts/capture_ui_screenshots.py` — blocked by optional tooling limitation because Playwright is not installed.
- `python -m pip install playwright` — blocked by package-index proxy `403 Forbidden`, so screenshots could not be regenerated in this environment.

## Result

Cosmetic/layout-only UI polish is complete and verified by compile, lint, targeted UI/app tests, full tests, and local HTML review-page export.

## Environment limitations

Playwright screenshot capture could not run in this Codex environment because the optional Playwright package is not installed and the package index rejected installing it with `403 Forbidden`. Existing guidance remains in `README.md` and the screenshot capture script.

## Follow-up backlog items

- Regenerate Playwright screenshots in a browser-capable environment with Playwright installed.
- Consider a later, explicitly scoped information-architecture task if the long Products & Stock and Make / Buy pages need true tabs or collapsible sections. That was intentionally not implemented here because it would be a broader interaction change.
