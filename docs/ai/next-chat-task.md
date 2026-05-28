# Next Chat Task — Milestone 10.2 Startup Planning + Scope Lock

## Active Milestone
- Milestone 10.2 — Release Candidate Freeze (`not-started`)

## Objective
Start Milestone 10.2 by locking release-candidate freeze scope and reconciling current blocker/backlog documents after Milestone 10.1 completion closeout.

## Scope Lock (current)
In scope for current next task:
- inspect `project-roadmap.md` Milestone 10.2 acceptance criteria
- inspect `docs/ai/completion-status.md`, `docs/ai/known-issues.md`, `docs/ai/do-not-build-yet.md`, and `docs/ai/progress-log.md`
- confirm Milestone 10.1 completion closeout evidence exists
- define the Milestone 10.2 freeze boundaries: blocker fixes only, no feature growth
- update completion/progress tracking for Milestone 10.2 startup planning
- add a bounded startup planning/scope-lock report under `docs/ai/reports/`

Out of scope for current slice:
- V1 release declaration
- new features, new screens, new integrations, or speculative polish
- optional Milestone 9.2 screenshot evidence unless explicitly scoped
- fixing non-blocking issues before they are classified under the freeze rules

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- add a bounded startup planning/scope-lock report under `docs/ai/reports/` for Milestone 10.2
