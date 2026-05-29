# Next Chat Task — Milestone 10.3 V1 Release Startup / Readiness Validation

## Active Milestone
- Milestone 10.3 — V1 Release (`not-started`)

## Objective
Start Milestone 10.3 only after confirming Milestone 10.2 completion closeout evidence exists. Validate whether the repository is ready for a V1 release declaration, then either declare V1 complete with evidence or document any blocker that prevents declaration.

## Scope Lock (current)
In scope for the next task:
- inspect `project-roadmap.md` Milestone 10.3 acceptance criteria
- inspect `docs/ai/completion-status.md`, `docs/ai/known-issues.md`, `docs/ai/do-not-build-yet.md`, and `docs/ai/progress-log.md`
- inspect `docs/ai/reports/milestone-10.2-completion-closeout-signoff-2026-05-29.md`
- confirm manual core workflow evidence and stock-changing action traceability evidence remain present
- run the full Codex-cloud validation sequence
- decide whether V1 can be declared complete or whether a blocker must be recorded
- update completion/progress tracking and add a bounded report under `docs/ai/reports/`

Out of scope unless the next task explicitly scopes it:
- new features, new screens, new integrations, or speculative polish
- optional Milestone 9.2 screenshot evidence
- post-V1 backlog work
- unrelated refactors

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- add a bounded Milestone 10.3 startup/readiness or V1 release-decision report under `docs/ai/reports/`
