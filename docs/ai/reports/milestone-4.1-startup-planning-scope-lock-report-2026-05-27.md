# Milestone 4.1 Startup Planning + Scope Lock Report (Create Batch)

Date: 2026-05-27  
Milestone: 4.1 — Create Batch  
Status: startup planning complete (`in-progress` milestone with scope lock set)

## Objective
Start Milestone 4 after Milestone 3.4 completion by locking the first Make/Buy implementation slice for **Create Batch** before coding.

## Inputs Read
- `project-roadmap.md` (Milestone 4.1 + Make/Buy section)
- `docs/ai/development-process.md`
- `docs/ai/task-execution-rules.md`
- `docs/ai/testing-rules.md`
- `docs/ai/finish-line-protocol.md`
- `docs/ai/next-chat-task.md`

## Scope Lock — First Vertical Slice

### In scope (Milestone 4.1 first implementation slice)
1. Add a simple Create Batch flow in Make/Buy for a chosen product.
2. Accept batch quantity input and validate basic constraints (positive integer).
3. Calculate/check required materials for that requested quantity.
4. Persist batch in a draft/planned state (not started yet).
5. Provide clear user-facing result or blocking message when materials are insufficient.
6. Add tests for service-level create-batch behavior and app-level request handling.

### Out of scope (explicit non-goals for this slice)
1. Start Batch transition behavior (Milestone 4.2).
2. Complete Batch stock/material mutation behavior (Milestone 4.3).
3. Purchasing lifecycle enhancements beyond existing materials workflows.
4. Money/profit module changes.
5. Broad Make/Buy UX redesign.

## Acceptance Criteria for Next Implementation Slice
- A user can create a planned batch with product + quantity.
- Material requirements are evaluated against current material availability.
- Insufficient material conditions are returned as actionable errors.
- No stock/material decrement occurs during create-only flow.
- Regression tests pass with full project validation commands.

## Risks and Safeguards
- Risk: mixing Milestone 4.1 with 4.2/4.3 lifecycle transitions.  
  Safeguard: keep status model and service actions create-only for this slice.
- Risk: hidden inventory mutation during batch planning.  
  Safeguard: assert no product/material quantity mutation in tests.
- Risk: scope creep into purchasing and money modules.  
  Safeguard: explicit non-goals listed above and enforced in next-task handoff.

## Validation Evidence (planning slice)
Commands executed in Codex cloud:
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

Result summary:
- Dependency install: pass (dev install has known proxy/index warning pattern in this environment).
- Compile check: pass.
- Test suite: pass.

## Milestone Tracking Updates
- Completion status advanced from Milestone 3.4 complete state to Milestone 4.1 startup state.
- Next-chat handoff updated from startup planning to first implementation slice.
- Progress log updated with this planning/reporting event.

## Next Task Handoff
Implement Milestone 4.1 first vertical slice: Create Batch domain/service/app behavior with tests, then produce implementation report and updated milestone status evidence.
