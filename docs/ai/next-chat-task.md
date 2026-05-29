# Next Chat Task — Post-V1 Scope Selection

## Active Milestone
- V1 Release — complete

## Objective
V1 has been declared complete. The next chat should not start feature work automatically. Select an explicitly scoped post-V1 task or backlog item before making code changes.

## Scope Lock (current)
In scope for the next task:
- inspect `docs/ai/completion-status.md`
- inspect `docs/ai/progress-log.md`
- inspect `docs/ai/known-issues.md`
- inspect `docs/ai/do-not-build-yet.md`
- inspect `docs/ai/reports/milestone-10.3-v1-release-decision-report-2026-05-29.md`
- choose or receive one bounded post-V1 task before implementation

Out of scope unless the next task explicitly scopes it:
- automatic feature expansion
- broad redesigns or refactors
- new integrations
- optional Milestone 9.2 screenshot evidence
- backlog implementation without explicit acceptance criteria

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- for any future change, add a bounded report under `docs/ai/reports/`
