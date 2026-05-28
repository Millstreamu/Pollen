# Milestone 5.1 Startup Planning + Scope Lock Report (2026-05-28)

## Task understood
Execute startup planning and scope lock for Milestone 5.1 (Buy List / Reorder Suggestions) and transition milestone tracking to `in-progress` once planning evidence is recorded.

## Task source
- `docs/ai/next-chat-task.md`
- `project-roadmap.md`

## Rule and memory files read
- `AI_DEVELOPMENT.md`
- `docs/ai/development-process.md`
- `docs/ai/project-rules.md`
- `docs/ai/progress-log.md`
- `docs/ai/completion-status.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`
- `docs/ai/testing-rules.md`
- `docs/ai/task-execution-rules.md`

## Milestone 5.1 objective (locked)
Enable a simple Buy List view that surfaces low materials with understandable reorder suggestions and a basic Add to Purchase affordance, without implementing downstream purchase lifecycle behavior.

## In-scope for first Milestone 5.1 implementation slice
1. Surface low-material entries in the Make/Buy flow so users can identify what needs buying.
2. Define and implement a deterministic suggested quantity rule for reorder guidance.
3. Add a simple Add to Purchase action affordance (non-automated) for listed materials.
4. Ensure suggestions are plain-language and consistent with beginner-friendly UX.
5. Add tests for low-material visibility and suggestion behavior.

## Out of scope for this first Milestone 5.1 slice
- Persisted Purchase creation and editing workflows (Milestone 5.2).
- Purchase receiving/status transitions and stock mutation (Milestone 5.3).
- Automatic ordering or supplier API integrations.
- Money module expansion tied to purchasing.
- Broad Make/Buy redesign beyond minimum Buy List affordances.

## Risks
- Suggestion rule ambiguity could produce confusing quantities if not deterministic and documented.
- Scope leakage risk into Milestones 5.2/5.3 if Add to Purchase implies persisted purchase lifecycle behavior.
- Regression risk if low-stock calculations conflict with existing stock/reservation invariants.

## Verification plan (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Tracking updates completed in this planning slice
- Transitioned milestone status from `not-started` to `in-progress` after planning evidence capture.
- Updated next-chat handoff to the Milestone 5.1 first vertical implementation task.
- Recorded this startup planning evidence report for durable context.

## Next recommended action
Implement Milestone 5.1 first vertical slice: low-material Buy List rendering + deterministic reorder suggestions + simple Add to Purchase action affordance with full regression and journey validation.
