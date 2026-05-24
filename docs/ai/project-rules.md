# Project Rules — Pollen Small-Seller ERP

## Product Goal
Pollen is a simple web-based operating app for small Etsy and hobbyist sellers. It helps one person (or a very small team) run day-to-day operations: orders, stock, making, buying materials, and simple money visibility.

This is **not** enterprise ERP software.

## Target Users
- Solo Etsy sellers
- Hobbyist/maker sellers with small batch production
- Micro-businesses managing products, materials, and orders manually today

## Plain-Language Product Navigation (V1)
- **Today**: What needs attention now (late shipments, low stock, open purchase receipts, make-next tasks).
- **Orders**: Track incoming orders through reserve → pack → ship.
- **Products & Stock**: Manage products, finished stock, and stock status.
- **Make / Buy**: Run small batch production and material purchasing workflows.
- **Money**: Show simple estimated sales and profit visibility.
- **Settings**: Basic app configuration and business preferences.

## Core V1 Workflows
1. Order comes in → stock is reserved → order is packed/shipped.
2. Product batch is made → materials decrease → finished stock increases.
3. Materials are bought → purchase is received → material stock increases.
4. Today dashboard surfaces items needing attention.
5. Money page shows simple estimated sales/profit.

## Out of Scope (Enterprise Features)
- Multi-entity enterprise accounting
- Complex role/approval hierarchies
- Advanced procurement optimization
- MRP/APS-style capacity planning
- Global logistics orchestration
- Compliance-heavy enterprise reporting suites

## Delivery Guardrails
- Build only what is required for the current milestone.
- Prefer plain, maintainable UX and data models over speculative abstraction.
- Avoid integrations unless explicitly scoped.
- Do not start deferred features listed in `docs/ai/do-not-build-yet.md`.
