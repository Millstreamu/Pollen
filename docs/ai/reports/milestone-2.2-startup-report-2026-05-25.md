# Startup Report — Milestone 2.2 Materials CRUD (2026-05-25)

Task understood:
- Begin Milestone 2.2 and produce an implementation startup report before code changes.

Task source:
- Direct human instruction in this session.
- Milestone reference: `project-roadmap.md` → `Milestone 2.2 — Materials CRUD`.

Rule files read:
- `AI_DEVELOPMENT.md`
- `docs/ai/development-process.md`
- `docs/ai/testing-rules.md`
- `docs/ai/task-execution-rules.md`
- `docs/ai/reporting-rules.md`

Project memory files read:
- `docs/ai/progress-log.md`
- `docs/ai/completion-status.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`

Relevant repo files found:
- `project-roadmap.md`
- `src/pollen/models.py`
- `src/pollen/services.py`
- `src/pollen/app.py`
- `tests/test_models.py`
- `tests/test_app.py`
- `tests/test_products.py`

Existing patterns observed:
- Milestone 2.1 implemented CRUD patterns using scoped records + repository/service layers.
- App routes are rendered through deterministic server-side HTML strings in `AppShell`.
- Tests validate feature behavior through service-level checks and route body assertions.
- Reporting cadence already tracks startup and implementation slices per milestone.

Planned changes:
- Start Milestone 2.2 with a first vertical slice for materials CRUD aligned with existing product patterns.
- Introduce material domain model/repository/service using server-side `shop_id` scoping.
- Add initial Materials UI route section (list + create/edit baseline depending on slice scope chosen next).
- Add/extend tests for material create/edit and low-stock status behavior.
- Keep completion/status tracking updated as milestone state advances.

Out-of-scope items:
- Milestone 2.3 recipe calculations.
- Milestone 2.4 stock adjustment/audit-log flows.
- Make/Buy batch execution and purchasing workflows.
- Any accounting/Money milestone features.

Risks:
- Materials and products may share similar fields; risk of over-generalization/refactor outside scope.
- UI complexity could grow if full CRUD is attempted in one slice; need staged delivery.
- Must preserve deterministic HTML/test stability while adding new route behavior.

Tests/checks to run:
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`
