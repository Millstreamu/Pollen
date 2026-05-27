# Milestone 3.4 Startup Planning + Scope Lock Report (Cancel Order)

Date: 2026-05-27  
Milestone: Milestone 3.4 — Cancel Order  
Status: startup planning complete; implementation pending

## AI Development Method Evidence

### Spec
Goal:
- Allow eligible orders to be cancelled safely, release any reserved stock, and preserve workflow integrity through explicit transition rules and activity logging.

User value:
- Prevent blocked inventory from stale orders.
- Keep available stock accurate after cancellation.
- Protect shipped-order history from casual destructive actions.

Planned acceptance criteria alignment:
- Cancelling order releases reserved stock.
- Shipped order cannot be casually cancelled.
- Activity log entries are created for cancellation transitions.

### Scan
Reviewed source-of-truth milestone definitions and current project memory before implementation:
- `project-roadmap.md` milestone criteria for 3.4.
- `docs/ai/next-chat-task.md` current active task and execution order.
- `docs/ai/completion-status.md` required scope + verification checklists.
- `docs/ai/progress-log.md` latest validated state from Milestone 3.3 completion.

### Simplify
Chosen approach for first implementation slice:
- Introduce one explicit cancellation transition in service/model flow.
- Reuse existing reservation fields and order status transition patterns from Milestones 3.2/3.3.
- Keep cancellation policy narrow: allow only roadmap-scoped statuses and explicitly block shipped cancellation.
- Defer any advanced “override/correction” shipped-cancel workflow to future milestones.

### Slice (Scope Lock)
In scope for Milestone 3.4 execution:
1. Service/model cancellation transition handling.
2. Reserved stock release on successful cancellation.
3. Transition guards for invalid states (especially shipped).
4. Activity log coverage.
5. App wiring for cancel action + user-facing errors.
6. Unit/service/journey tests for cancellation behavior and stock consistency.

Out of scope (locked):
- Milestone 4.x make/buy implementation.
- Broad order workflow redesign beyond cancellation criteria.
- Non-essential UX polish unrelated to cancellation acceptance criteria.

### Verify (startup validation baseline)
Commands planned and validated as project-standard for Codex cloud:
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

### Clean
- No runtime code changes in this startup planning slice.
- No temporary scripts/artifacts introduced.

### Freeze
- Planning output frozen to roadmap-aligned cancellation scope above.
- No extra features added during startup phase.

### Ship
- Added this durable planning report.
- Updated next-task brief to start Milestone 3.4 first implementation slice.
- Updated progress and completion tracking to reflect startup completion.

## First Vertical Slice Execution Plan
1. Implement cancel transition in order service/model path.
2. Apply reservation-release stock updates atomically with status change.
3. Add/extend tests:
   - valid cancellation transitions
   - invalid cancellation transitions
   - reservation release consistency
   - activity log evidence
4. Wire cancel action in app route/forms with clear failure messages.
5. Run full validation suite and capture implementation report.

## Risks and Guardrails
- Risk: double-release of reserved stock if cancellation is repeated.
  - Guardrail: enforce invalid transition blocking after terminal cancellation.
- Risk: status drift between reservation and order lifecycle.
  - Guardrail: test assertions on both reserved and available stock after cancellation.
- Risk: accidental shipped-order cancellation.
  - Guardrail: explicit shipped-state block with clear user-facing error.

## Release Flow Note
This report completes startup planning evidence only. Milestone 3.4 remains `in-progress` until implementation + validation + release-flow transitions are completed.
