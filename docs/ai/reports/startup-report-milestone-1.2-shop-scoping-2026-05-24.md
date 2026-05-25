# Startup Report — Milestone 1.2 Continuation (Persistence-Backed Shop Scoping)

Date: 2026-05-24  
Task source: Direct human request in Codex chat (`ok continue with 1.2. write a report on what you're going to do. use ai_dev method for all guidance`)  
Milestone reference: `project-roadmap.md` → `Milestone 1.2 — Managed Auth and Shop Ownership`

## AI_DEV method applied
Process followed from `docs/ai/development-process.md`:
- **Spec**: define precise continuation scope for Milestone 1.2.
- **Scan**: re-read roadmap, progress log, and latest 1.2 implementation report.
- **Simplify**: choose smallest safe vertical slice to finish remaining acceptance coverage.
- **Slice**: implement one persistence-backed domain path with enforced `shop_id` boundaries.
- **Verify**: run install + compile + test commands used by this repo.
- **Clean/Freeze/Ship**: update progress and report evidence when implementation is complete.

## Task understood
Continue Milestone 1.2 by implementing the remaining gap: real persistence-backed `shop_id` record scoping (not only auth-context helper checks), while preserving current auth and ownership safeguards.

## Rule files and memory reviewed
- `AI_DEVELOPMENT.md`
- `docs/ai/development-process.md`
- `docs/ai/task-execution-rules.md`
- `docs/ai/testing-rules.md`
- `docs/ai/security-rules.md`
- `docs/ai/environment-capabilities.md`
- `docs/ai/progress-log.md`
- `docs/ai/reports/milestone-1.2-implementation-report-2026-05-24.md`
- `docs/ai/do-not-build-yet.md`
- `project-roadmap.md`

## Current state snapshot
- Milestone 1.2 is marked in-progress in project memory.
- Auth abstraction, protected routes, and ownership helper behavior already exist.
- Milestone report marks `records are scoped by shop_id` as only partially covered.

## Continuation scope (planned build slice)
Implement a concrete shop-scoped persistence flow for one initial record type (likely the simplest existing domain path), including:
1. Record model/repository contract with required `shop_id`.
2. Create path that derives `shop_id` server-side from auth context (never from trusted client input).
3. Query/update/read path automatically filtered by current shop.
4. Denial behavior for cross-shop access attempts.
5. Unit tests proving positive and negative ownership behaviors on persisted records.

## Explicit out-of-scope for this continuation
- New milestone features outside 1.2 (product/material/order workflows).
- OAuth provider production wiring beyond current managed-auth seam.
- Advanced roles/permissions/invite workflows.
- UI polish unrelated to ownership correctness.

## Acceptance criteria mapping (Milestone 1.2)
- Logged-out users cannot access private pages: already covered, keep regression tests green.
- Logged-in user gets or creates a shop: already covered, keep regression tests green.
- Records are scoped by `shop_id`: **target of this continuation slice**.
- User cannot access another shop’s records: extend from helper-level checks to persistence-backed behavior tests.

## Risks and mitigations
- **Risk**: accidental trust of client-supplied `shop_id`.  
  **Mitigation**: enforce server-owned `shop_id` assignment at service/repository boundary.
- **Risk**: over-engineering persistence abstraction.  
  **Mitigation**: implement only minimal repository shape needed for acceptance tests.
- **Risk**: regression in existing auth tests.  
  **Mitigation**: run full `pytest -q` after changes, keep old tests intact.

## Verification plan for implementation turn
Repository standard commands:
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

If any dependency gaps are discovered, update dependency files before final verification rerun.

## Deliverables planned for the implementation follow-up
- Code + tests for persistence-backed shop scoping.
- Updated milestone implementation report with concrete evidence.
- Updated `docs/ai/progress-log.md` entry for continuation completion.
