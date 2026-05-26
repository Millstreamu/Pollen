# Next Chat Task — Milestone 2.4 First Coding Slice

Use this brief in future chats to continue work without re-planning.

## Active Milestone
- Milestone 2.4 — Manual Stock Adjustment (in-progress)

## Objective
Implement the first complete vertical slice for manual stock adjustment, aligned to roadmap and completion tracking acceptance criteria.

## Recommended Implementation Order
1. Domain model support
   - Add/confirm `InventoryMovement` and `ActivityLog` structures for manual stock adjustments.
   - Ensure records can represent product and material adjustments.

2. Service logic
   - Implement:
     - `adjust_product_stock(...)`
     - `adjust_material_stock(...)`
   - Enforce:
     - required reason
     - increase/decrease support
     - negative stock blocked by default
   - On successful adjustment, create both movement and activity records.

3. Unit tests (required)
   - stock increase succeeds
   - stock decrease succeeds when stock is sufficient
   - negative-result adjustment is blocked
   - missing reason is rejected
   - movement record is created
   - activity log is created

4. Route/UI/API wiring
   - Expose manual stock adjustment in existing app flow.
   - Return clear validation errors for missing reason / negative stock block.

5. Journey test (milestone-required)
   - create material
   - adjust stock
   - confirm material stock changed
   - confirm movement and activity log records exist

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Out of Scope for this slice
- Milestone 3.x or later roadmap work
- optional enhancements beyond Milestone 2.4 acceptance criteria
