# Next Chat Task — Post-V1 Backlog / Maintenance Scope Selection

## Active Milestone
- Milestone 10.3 — V1 Release (`complete`)

## Objective
V1 has been declared complete. The next chat must not continue feature development automatically. Select a new, explicitly scoped post-V1 task only after reading the current project memory and confirming it is not blocked by `docs/ai/do-not-build-yet.md`.

## Scope Lock (current)
In scope for the next task:
- inspect `docs/ai/completion-status.md`
- inspect `docs/ai/known-issues.md`
- inspect `docs/ai/do-not-build-yet.md`
- inspect `docs/ai/progress-log.md`
- inspect `docs/ai/reports/milestone-10.3-v1-release-decision-report-2026-05-29.md`
- choose only one explicitly scoped maintenance, blocker-fix, or post-V1 backlog item
- run the full Codex-cloud validation sequence for any code or release-affecting documentation change

Out of scope unless the next task explicitly scopes it:
- automatic continuation into new features
- speculative polish
- broad refactors
- optional Milestone 9.2 screenshot evidence unless explicitly requested and environment-supported
- new integrations or live external smoke tests without a supported environment plan

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- add a bounded report under `docs/ai/reports/` for the selected post-V1 task
