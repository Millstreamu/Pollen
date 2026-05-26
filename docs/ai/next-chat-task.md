# Next Chat Task — Milestone 3.1 First Coding Slice

Use this brief in future chats to continue work without re-planning.

## Active Milestone
- Milestone 3.1 — Manual Order Creation (in-progress)

## Objective
Implement the first complete vertical slice for manual order creation, aligned to roadmap and completion tracking acceptance criteria.

## Recommended Implementation Order
1. Domain model support
   - Add/confirm `Order` and `OrderItem` structures for manual order creation.
   - Ensure order and order items are shop-scoped.

2. Service logic
   - Implement:
     - `create_order(...)`
   - Enforce:
     - source defaults to Manual
     - customer name is captured
     - stock-aware initial status calculation
   - On successful creation, persist order and items.

3. Unit tests (required)
   - order can be created
   - order belongs to shop
   - order items belong to shop
   - source defaults to Manual
   - status reflects stock availability

4. Route/UI/API wiring
   - Expose order creation in existing app flow.
   - Return clear validation errors for malformed inputs.

5. Journey test (milestone-required)
   - create product with stock
   - create manual order with item quantity
   - confirm order persisted and visible in Orders flow
   - confirm initial order status is correct from available stock

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Out of Scope for this slice
- Milestone 3.2+ roadmap work
- optional enhancements beyond Milestone 3.1 acceptance criteria
