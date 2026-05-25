# Startup Report — Milestone 2.1 UI/Product Page Slice (2026-05-25)

Task understood:
- Implement the Milestone 2.1 UI/product page slice using the existing service layer, starting with this report.

Task source:
- Direct human instruction in this session.
- Milestone reference: `project-roadmap.md` section for Products & Stock.

Rule files read:
- `AI_DEVELOPMENT.md`
- `docs/ai/development-process.md`
- `docs/ai/testing-rules.md`
- `docs/ai/task-execution-rules.md`
- `docs/ai/ui-rules.md`
- `docs/ai/report-format.md`

Project memory files read:
- `docs/ai/progress-log.md`
- `docs/ai/completion-status.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`

Relevant repo files found:
- `src/pollen/app.py`
- `src/pollen/services.py`
- `src/pollen/products.py`
- `tests/test_app.py`
- `tests/test_products.py`
- `docs/ai/reports/milestone-2.1-implementation-report-2026-05-25.md`

Existing patterns observed:
- App shell currently returns deterministic HTML strings per route.
- Private-route auth is enforced centrally in `AppShell.get`.
- Milestone 2.1 backend ProductService + ProductRepository already provide shop-scoped product CRUD and low-stock signal.
- Tests use direct string assertions on HTML body and service behavior.

Planned changes:
- Replace `/products-stock` placeholder body with a simple product list UI rendered from `ProductService.list_products` for current authenticated shop.
- Add clear empty state copy when no products exist.
- Show low-stock status in-page so inventory risk is visible.
- Add/update app tests for products page table + empty state behavior.

Out-of-scope items:
- Product create/edit/archive UI forms.
- Any Make/Buy or Money milestone functionality.
- Refactors outside app-shell/product-page rendering.

Risks:
- Route rendering currently uses static descriptions; introducing dynamic page content must not alter behavior for other routes.
- Need deterministic ordering/markup for stable tests.

Tests/checks to run:
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`
