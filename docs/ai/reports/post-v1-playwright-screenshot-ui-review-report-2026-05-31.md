# Post-V1 Playwright Screenshot UI Review Report

- Date: 2026-05-31
- Task source: Direct human request in Codex chat
- Evidence reviewed: saved Playwright screenshots in `docs/ai/ui-screenshots/`
- Scope: small UI clarity/readability polish plus durable report

## AI development method applied

### Spec
Review the committed screenshot evidence and determine whether the UI can be made more user friendly, streamlined, and easier to understand at a glance.

### Scan
Reviewed:
- `AI_DEVELOPMENT.md`
- `docs/ai/project-rules.md`
- `docs/ai/progress-log.md`
- `docs/ai/completion-status.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`
- `docs/ai/development-process.md`
- `docs/ai/testing-rules.md`
- `docs/ai/task-execution-rules.md`
- `docs/ai/ui-rules.md`
- screenshots: `today.png`, `orders.png`, `products-stock.png`, `make-buy.png`, `money.png`, `settings.png`
- app shell: `src/pollen/app.py`
- UI tests: `tests/test_milestone_9_1_ui_consistency.py`

### Simplify
The safest useful slice was to keep the existing warm visual system and server-rendered structure, then improve scanability with reusable CSS and small HTML changes instead of introducing a design system dependency or larger navigation redesign.

### Slice
Implemented one bounded visual polish slice:
- Today summary counts now render as metric cards rather than a plain bullet list.
- Today actions now render as compact action pills.
- The Today next-step call to action is an enabled workflow link rather than a disabled button.
- Order statuses now render with a consistent status badge treatment.
- Money empty state now points to the first actionable workflow instead of showing a disabled button.
- Money populated state now renders estimates as metric cards.
- Settings unavailable actions now read as coming-soon state text rather than disabled buttons that look actionable.
- Shared CSS was added for metric cards, action lists, status badges, and link-styled buttons.

## Screenshot findings

### Strengths already present
- The top navigation is consistent across every captured page.
- The warm card-based style is approachable and avoids visual noise.
- Page headings are large and clear.
- Forms and tables are plain HTML, which supports accessibility and reliable automated verification.
- Empty states exist on Money and Settings instead of showing blank pages.

### Improvements identified

| Area | Screenshot evidence | Improvement made or recommended |
|---|---|---|
| Today summary | `today.png` showed important counts in a small bullet list. | Implemented metric cards so the user can identify workload counts quickly. |
| Today next step | `today.png` showed a disabled checklist button, which looked clickable but could not be used. | Replaced it with an enabled workflow link to orders. |
| Order status | `orders.png` showed status text inline with similar weight to regular table text. | Added a status badge class to make order state easier to scan. |
| Money empty state | `money.png` showed a disabled View estimates button. | Replaced it with an enabled link to ship orders first. |
| Money populated state | Existing page rendered estimates in a list. | Changed estimates to metric cards to match Today scanability. |
| Settings unavailable actions | `settings.png` showed disabled Save/Connect buttons for unavailable features. | Replaced disabled controls with explicit coming-soon state text. |
| Dense workflow pages | `products-stock.png` and `make-buy.png` are long and contain multiple workflows at once. | Deferred broader workflow splitting; recommend future subnavigation/accordions after current post-V1 priorities are selected. |
| Duplicate recipe/audit surfaces | Recipes and audit sections appear in both Products & Stock and Make / Buy screenshots. | Deferred because changing information architecture could affect workflows; recommend a future task to decide ownership of recipes and audit history. |

## Implementation notes

This task intentionally avoided adding dependencies. The app remains standard-library/server-rendered and the existing screenshot capture tooling remains optional.

## Validation commands and results

- `python -m pip install --upgrade pip` — pass.
- `pip install -r requirements.txt` — pass.
- `pip install -r requirements-dev.txt` — pass.
- `python -m compileall -q src tests scripts` — pass.
- `ruff check src tests scripts` — pass.
- `pytest -q tests/test_milestone_9_1_ui_consistency.py tests/test_ui_review_scripts.py` — pass.
- `pytest -q tests/test_today_summary.py tests/test_journey_milestone_10_1.py tests/test_milestone_9_1_ui_consistency.py` — pass.
- `PYTHONDONTWRITEBYTECODE=1 pytest -q` — pass.
- `PYTHONPATH=src python scripts/capture_ui_screenshots.py` — environment-limited because Playwright is not installed in Codex cloud; the helper printed setup guidance.

## Result

The screenshot review found actionable improvements, and the lowest-risk clarity improvements were implemented. Larger layout/information-architecture changes are documented as follow-up backlog rather than bundled into this small polish slice.

## Follow-up backlog

1. Consider tab-like sections or collapsible panels on Products & Stock to separate create form, list, recipes, and audit history.
2. Consider moving recipe management to a single canonical page or adding clear cross-links if it must remain visible in two workflows.
3. Add visual priority styling for destructive actions such as Cancel order and Archive once the design vocabulary supports primary/secondary/danger variants.
4. Re-run Playwright screenshots in a browser-enabled environment to compare before/after visual evidence.
