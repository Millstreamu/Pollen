# Startup Report — Milestone 1.1 App Shell

Date: 2026-05-24  
Task source: Direct human request in Codex chat (`do a startup report on this milestone 1.1`)  
Milestone reference: `project-roadmap.md` → `Milestone 1.1 — App Shell`

## Task understood
Prepare a pre-implementation startup report for **Milestone 1.1 — App Shell**, defining scope boundaries, risks, evidence reviewed, and verification plan before any milestone implementation work starts.

## Rule files read
- `AI_DEVELOPMENT.md`
- `docs/ai/development-process.md`
- `docs/ai/task-execution-rules.md`
- `docs/ai/testing-rules.md`
- `docs/ai/ui-rules.md`

## Project memory files read
- `docs/ai/project-rules.md`
- `docs/ai/progress-log.md`
- `docs/ai/completion-status.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`

## Relevant repo files found
- `project-roadmap.md` (milestone definition and acceptance criteria)
- `README.md` (current setup and validation commands)
- `requirements.txt`, `requirements-dev.txt` (environment install paths)
- `src/pollen/app.py`, `src/pollen/models.py` (current scaffold state)
- `tests/test_app.py`, `tests/test_models.py` (current baseline tests)

## Existing patterns observed
- Python package layout under `src/pollen/` with lightweight deterministic functions.
- Pytest-based unit testing with small focused tests.
- Environment bootstrap already documented and repeatable (`pip install -r requirements*.txt`).
- No current web UI or routing layer implemented in repository.

## Planned changes (for Milestone 1.1 implementation phase)
- Add a minimal app shell with placeholder pages for Today, Orders, Products & Stock, Make / Buy, Money, and Settings.
- Add simple top navigation and basic layout primitives.
- Keep milestone strictly to shell and placeholders (no business workflows).
- Add/adjust tests to validate routing/page availability and app shell rendering.
- Update project memory/status docs once Milestone 1.1 is implemented.

## Out-of-scope items
- Authentication and shop ownership (Milestone 1.2).
- Products/materials CRUD and stock logic (Phase 2 milestones).
- Orders reservation/pack/ship/cancel workflows (Phase 3 milestones).
- Integrations, money calculations, and production purchasing workflows.

## Risks
- Framework choice may introduce unnecessary complexity if over-scoped.
- Scope creep into business logic while wiring routes/pages.
- UI terminology drifting into enterprise ERP language, conflicting with roadmap/UI rules.
- Adding dependencies without test/setup updates could break Codex cloud reproducibility.

## Tests/checks to run during Milestone 1.1 implementation
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- Compile checks (if applicable): `python -m compileall -q src tests`
- Lint/typecheck commands if introduced by chosen framework/tooling.
- `pytest -q`

## Initial milestone status recommendation
- `Milestone 1.1 — App Shell`: **in-progress** once implementation begins.
- Current repository state remains pre-implementation scaffold.
