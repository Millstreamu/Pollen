# Startup Report — Milestone 3.1 Manual Order Creation (2026-05-26)

Task understood:
- Start Phase 3 implementation planning with a startup report for Milestone 3.1 (Manual Order Creation) before writing feature code.

Task source:
- Direct human instruction in this session.
- Active task pointer: `docs/ai/next-chat-task.md`.
- Milestone source of truth: `project-roadmap.md` → `Milestone 3.1 — Manual Order Creation`.

Rule files read:
- `AI_DEVELOPMENT.md`
- `docs/ai/development-process.md`
- `docs/ai/task-execution-rules.md`
- `docs/ai/testing-rules.md`
- `docs/ai/finish-line-protocol.md`
- `docs/ai/reporting-rules.md`

Project memory files read:
- `docs/ai/progress-log.md`
- `docs/ai/completion-status.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`
- `docs/ai/next-chat-task.md`
- `docs/ai/project-roadmap.md` (pointer)
- `project-roadmap.md` (milestone source)

Current phase/milestone context:
- Milestone 2.4 is marked complete in current tracking files.
- Phase 3 should begin with Milestone 3.1.

Milestone 3.1 goal:
- Allow user to create an order manually.

Planned scope (Milestone 3.1):
- Create order.
- Add order items.
- Capture customer name.
- Default order source to `Manual`.
- Compute initial order status from stock availability.

Out of scope for this startup slice:
- Milestone 3.2+ work (stock reservation lifecycle, pack/ship transitions, cancellation release rules).
- External marketplace imports/integrations.
- Any Money phase/accounting enhancements.

Acceptance criteria to satisfy:
- User can create order.
- Order belongs to shop.
- Order items belong to shop.
- Order appears in Orders page.

Recommended first implementation order (next coding slice):
1. Domain model support (`Order`, `OrderItem`) with strict shop scoping.
2. Service operation `create_order(...)` with validation and source default.
3. Initial stock-aware status calculation (`Ready to Pack` vs `Waiting on Stock` behavior per available stock).
4. Route/UI/API wiring with explicit validation error responses.
5. Unit and journey tests for creation flow and initial status behavior.

Risk notes:
- Shop-boundary risk: order and order-item records must not cross shops.
- Stock-state risk: initial status logic can drift from inventory availability if not centralized.
- Validation risk: malformed item payloads may create partial writes unless creation is atomic.

Validation plan for next coding slice:
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

Current decision:
- Milestone 3.1 is now startup-planned. No runtime feature behavior changes are included in this report-only slice.
