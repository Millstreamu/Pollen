# Small Seller ERP — AI Development Roadmap

This document defines the start-to-finish development plan for a beginner-friendly web-based ERP-style app for small Etsy, Facebook Marketplace, handmade, hobbyist, and micro-commerce sellers.

The product should not feel like a corporate ERP. It should feel like a simple shop operating system that helps a small seller know what to pack, make, buy, and watch.

This roadmap is designed for AI-assisted development using Codex and GitHub, with repo-based rules, milestone execution, journey tests, evidence reports, and strict finish-line control.

---

## 1. Product Definition

### 1.1 Product Goal

Build a simple web-based operating app for very small sellers who make, assemble, buy, and sell physical products through small online channels such as Etsy and Facebook Marketplace.

The app should help the user answer:

- What do I need to do today?
- What orders need packing or shipping?
- What products are low or sold out?
- What materials do I need to buy?
- What should I make next?
- Am I making money?

The product should focus on practical daily operation, not enterprise resource planning complexity.

### 1.2 Target Users

Primary users:

- Etsy sellers
- Facebook Marketplace sellers
- handmade product sellers
- hobby businesses
- micro-commerce operators
- one-person or family-run shops
- small batch makers

They may sell things like:

- candles
- mugs
- prints
- jewellery
- soap
- gift boxes
- tote bags
- craft kits
- small handmade bundles

### 1.3 Product Philosophy

The app should be:

- simple
- calm
- beginner-friendly
- plain-language
- safe by default
- task-focused
- easy to verify with tests and screenshots
- suitable for AI-assisted development

It should not be:

- a full ERP
- warehouse management software
- advanced accounting software
- automated supplier procurement software
- complex manufacturing software
- heavy analytics software
- a generic workflow automation platform

### 1.4 Core Operating Loop

The whole product revolves around this loop:

```text
Order comes in
→ stock is reserved
→ order is packed/shipped
→ product stock is updated
→ low stock is detected
→ seller makes more or buys materials
→ money/profit estimate updates
```

The second core loop is:

```text
Seller plans a batch
→ app checks materials
→ seller completes the batch
→ materials decrease
→ finished product stock increases
```

The third core loop is:

```text
Material is low
→ app suggests buying it
→ seller creates purchase
→ seller marks it received
→ material stock increases
```

---

## 2. Final Product Shape

The app should use five main sections.

### 2.1 Today

The main dashboard. This is the default landing page.

Shows:

- orders to pack
- products low in stock
- materials to buy
- batches in progress
- purchases due soon
- simple money snapshot
- important alerts

The Today page answers:

> What should I do now?

### 2.2 Orders

A simple order workflow.

Core statuses:

- New
- Ready to Pack
- Waiting on Stock
- Packed
- Shipped
- Cancelled

The Orders page should support:

- create manual order
- view order list
- view order detail
- reserve stock
- pack order
- ship order
- cancel order
- release stock on cancellation
- show source badge such as Manual, Etsy, or Facebook

### 2.3 Products & Stock

This replaces traditional Inventory Management.

It tracks:

- finished products
- materials
- product recipes/materials needed
- available stock
- reserved stock
- low stock
- stock adjustments

Each product should answer:

- how many are in stock?
- how many are reserved?
- how many are available?
- what materials are needed to make it?
- how many more can be made with current materials?
- where is it listed?
- what is the estimated profit per sale?

### 2.4 Make / Buy

This combines lightweight production and purchasing.

Make:

- create a batch
- check materials
- start batch
- complete batch
- increase product stock
- decrease material stock

Buy:

- view materials to reorder
- create purchase
- mark purchase ordered
- mark purchase received
- increase material stock

Avoid heavy manufacturing/procurement language.

Use simple terms:

- Make Batch
- Materials Needed
- Buy List
- Purchase
- Receive Materials

### 2.5 Money

This is not full accounting.

It should show simple estimated money information:

- revenue
- estimated profit
- material cost
- shipping/packaging cost
- platform fees
- recent transactions
- payout/bills snapshot

Use labels like:

- Estimated Profit
- Money Summary
- Sales This Month
- Costs This Month

Avoid implying tax/accounting correctness unless fully implemented.

---

## 3. Major Non-Goals for V1

Do not build these in V1 unless explicitly unlocked:

- full enterprise ERP modules
- multi-warehouse inventory
- drag-and-drop production planner
- global supply chain tracking
- shipment maps
- automatic supplier ordering
- advanced approvals
- complex accounting ledger
- tax reporting
- live payment processing
- automatic two-way Etsy stock sync
- automatic Facebook Marketplace sync
- shipping label purchasing
- barcode scanning
- forecasting engine
- plugin system
- custom workflow builder
- advanced role/permission matrix

These may be considered later, but they are not part of the first complete version.

---

## 4. Technical Development Principles

### 4.1 AI-Development Principle

The app should be designed so AI can reliably build and verify it.

Prefer:

- simple pages
- cards
- tables
- lists
- drawers
- standard forms
- clear state transitions
- explicit buttons
- deterministic tests
- seeded data
- headless verification

Avoid early:

- hidden hover-only actions
- drag-and-drop workflows
- timing-sensitive UI
- complex animations
- custom canvas interfaces
- difficult-to-test browser flows
- live external dependencies in core tests

### 4.2 Simplicity Rule

Choose the simplest safe solution that satisfies the current milestone.

Do not add complexity unless it protects core correctness or is explicitly required.

Complexity must earn its place.

### 4.3 Safety Rule

The simple UI must be backed by disciplined data handling.

Stock, money, auth, and integration behaviour must be handled carefully.

Stock-changing actions must be:

- server-side validated
- transactional where possible
- recorded as inventory movements
- activity logged
- tested

### 4.4 No Hidden Magic

The app may suggest actions, but the user confirms important changes.

Allowed:

- “Soy wax is low. Suggested order: 2kg.”
- “You can make 8 more candles with current materials.”
- “This order is waiting on stock.”

Not allowed in V1:

- automatically ordering supplies
- silently pushing stock to Etsy
- marking orders shipped automatically
- deleting user data without confirmation
- changing money/stock based on unreviewed external data

---

## 5. Suggested Tech Stack

This roadmap is stack-agnostic, but a simple AI-friendly stack would be:

- Next.js or similar full-stack web framework
- PostgreSQL
- Prisma or Drizzle ORM
- Tailwind CSS
- shadcn/ui or similar component library
- Supabase/Auth.js/Clerk/Auth0/Firebase for managed auth
- GitHub Actions for CI
- Playwright for optional headless journey/UI tests
- Vitest/Jest for unit and service tests

Do not build custom password authentication.

Use managed auth with Google login where possible.

---

## 6. Core Data Model

The data model should stay boring and easy to reason about.

### 6.1 User / Shop

```text
User
- id
- email
- name

Shop
- id
- owner_user_id
- name
```

All private business records should belong to a shop.

### 6.2 Product

```text
Product
- id
- shop_id
- name
- sku
- sale_price
- stock_on_hand
- reserved_stock
- reorder_point
- active
```

Available stock is calculated as:

```text
available_stock = stock_on_hand - reserved_stock
```

### 6.3 Material

```text
Material
- id
- shop_id
- name
- unit
- stock_on_hand
- reorder_point
- supplier_id optional
```

### 6.4 ProductMaterial / Recipe Item

```text
ProductMaterial
- id
- shop_id
- product_id
- material_id
- quantity_required
```

This defines the “recipe” or materials needed for one product.

### 6.5 Order

```text
Order
- id
- shop_id
- source
- external_order_id optional
- customer_name
- status
- total
- created_at
```

### 6.6 OrderItem

```text
OrderItem
- id
- shop_id
- order_id
- product_id
- quantity
- unit_price
```

### 6.7 Batch

```text
Batch
- id
- shop_id
- product_id
- quantity
- status
- started_at
- completed_at
```

Statuses:

- Planned
- Ready
- Waiting on Materials
- In Progress
- Complete
- Cancelled

### 6.8 Purchase

```text
Purchase
- id
- shop_id
- supplier_id optional
- status
- expected_date
- created_at
```

Statuses:

- Draft
- Ordered
- Received
- Cancelled

### 6.9 PurchaseItem

```text
PurchaseItem
- id
- shop_id
- purchase_id
- material_id
- quantity
- unit_cost optional
```

### 6.10 InventoryMovement

Every stock change should create an inventory movement.

```text
InventoryMovement
- id
- shop_id
- item_type product/material
- item_id
- quantity_change
- reason
- source_type
- source_id
- created_by
- created_at
```

Examples of source types:

- manual_adjustment
- order_reservation
- order_ship
- order_cancel
- batch_complete
- purchase_receive

### 6.11 ActivityLog

```text
ActivityLog
- id
- shop_id
- user_id
- action_type
- entity_type
- entity_id
- description
- created_at
```

Examples:

- “Sarah completed batch B-102: +12 Lavender Candles.”
- “Order SO-1004 marked shipped.”
- “Soy Wax adjusted from 1.2kg to 2kg.”

---

## 7. Milestone Roadmap

Each milestone should be implemented as a focused AI task or small series of AI tasks.

Do not work ahead.

Each milestone should include:

- scope
- out-of-scope items
- acceptance criteria
- required tests/checks
- progress-log update

---

# Phase 0 — Repository Operating System

## Milestone 0.1 — Install AI Development Rules

Goal:

Add the generic AI development kit and make it the operating method for the repo.

Scope:

- add `AI_DEVELOPMENT.md`
- add `docs/ai/*` process files
- add issue templates
- add PR template
- add basic CI workflow if appropriate

Acceptance criteria:

- AI development rules exist in repo
- Codex can be instructed with “Read AI_DEVELOPMENT.md”
- repo has progress/status/known-issues files
- no application code changed

## Milestone 0.2 — Migrate Existing Docs

Goal:

Merge old project knowledge into the new AI docs.

Scope:

- inspect existing markdown docs
- map project goal docs into `project-rules.md`
- map status/history docs into `progress-log.md`
- map current state into `completion-status.md`
- map known problems into `known-issues.md`
- map deferred features into `do-not-build-yet.md`

Acceptance criteria:

- migration report exists
- old docs are preserved or archived safely
- project rules reflect the actual product goal
- progress log reflects what has already been done
- next milestone is clear

---

# Phase 1 — App Foundation

## Milestone 1.1 — App Shell

Goal:

Create the basic app structure.

Scope:

- layout
- navigation
- top bar
- protected dashboard shell if auth exists
- placeholder pages:
  - Today
  - Orders
  - Products & Stock
  - Make / Buy
  - Money
  - Settings

UI rules:

- simple layout
- no more than 3 main content areas per page except Today
- plain language
- no enterprise ERP terminology

Acceptance criteria:

- app builds
- navigation works
- placeholder pages load
- no business logic yet

## Milestone 1.2 — Managed Auth and Shop Ownership

Goal:

Add login and basic shop ownership.

Scope:

- Google login or managed auth provider
- user record
- shop record
- current shop context
- protected routes
- server-side ownership checks

Out of scope:

- custom password auth
- advanced roles
- invite system

Acceptance criteria:

- logged-out users cannot access private pages
- logged-in user gets or creates a shop
- records are scoped by `shop_id`
- user cannot access another shop’s records

Required tests:

- protected route behaviour where practical
- ownership checks
- shop scoping

---

# Phase 2 — Products, Materials, and Stock Foundation

## Milestone 2.1 — Products CRUD

Goal:

Allow user to create and manage finished products.

Scope:

- product list
- add product
- edit product
- archive/deactivate product
- product detail
- stock fields
- reorder point

Acceptance criteria:

- user can create product
- user can edit product
- product belongs to shop
- low stock status appears correctly
- product page follows UI simplicity rules

## Milestone 2.2 — Materials CRUD

Goal:

Allow user to create and manage materials.

Scope:

- material list
- add material
- edit material
- archive/deactivate material
- unit field
- stock field
- reorder point

Acceptance criteria:

- user can create material
- user can edit material
- material belongs to shop
- low stock status appears correctly

## Milestone 2.3 — Product Recipes / Materials Needed

Goal:

Define what materials are needed to make each product.

Scope:

- add materials to product recipe
- quantity required per product
- show material requirements on product detail
- calculate how many products can be made with current materials

Acceptance criteria:

- user can define recipe
- app can calculate “can make X more”
- editing recipe does not change stock

Required tests:

- material requirement calculation
- can-make quantity calculation

## Milestone 2.4 — Manual Stock Adjustment

Goal:

Allow safe manual stock corrections.

Scope:

- adjust product stock
- adjust material stock
- require reason
- create InventoryMovement
- create ActivityLog

Acceptance criteria:

- stock can be increased
- stock can be decreased
- negative stock is blocked unless explicitly allowed later
- movement record is created
- activity log is created

Required journey:

- create material
- adjust stock
- confirm material stock changed
- confirm movement and activity log exist

---

# Phase 3 — Orders

## Milestone 3.1 — Manual Order Creation

Goal:

Allow user to create an order manually.

Scope:

- create order
- add order items
- assign customer name
- source defaults to Manual
- status calculation based on stock availability

Acceptance criteria:

- user can create order
- order belongs to shop
- order items belong to shop
- order appears in Orders page

## Milestone 3.2 — Stock Reservation

Goal:

Reserve stock for open orders.

Scope:

- order creation reserves product stock if available
- insufficient stock marks order Waiting on Stock
- reserved_stock is updated
- available stock is calculated correctly

Acceptance criteria:

- creating order reserves stock
- insufficient stock does not silently over-allocate
- order status reflects stock availability

Required tests:

- order reserves stock
- insufficient stock creates Waiting on Stock
- available stock calculation

## Milestone 3.3 — Pack and Ship Workflow

Goal:

Allow seller to pack and ship orders.

Scope:

- mark Ready to Pack order as Packed
- mark Packed order as Shipped
- shipping finalises/resolves reservation
- activity log entries

Acceptance criteria:

- order can move through valid statuses
- invalid transitions are blocked
- shipping does not double-deduct stock
- shipped order is recorded in activity log

Required journey:

- create product
- create order
- pack order
- ship order
- confirm stock/reservation state is correct

## Milestone 3.4 — Cancel Order

Goal:

Allow cancellation and release reserved stock.

Scope:

- cancel New/Ready/Packed order where appropriate
- release reserved stock
- activity log

Acceptance criteria:

- cancelling order releases reserved stock
- shipped order cannot be casually cancelled without explicit later workflow
- activity log exists

---

# Phase 4 — Make Products / Batches

## Milestone 4.1 — Create Batch

Goal:

Allow user to plan a small product batch.

Scope:

- choose product
- enter quantity
- check required materials
- create batch status Planned/Ready/Waiting on Materials

Acceptance criteria:

- user can create planned batch
- material check displays enough/short materials
- creating batch does not change stock

## Milestone 4.2 — Start Batch

Goal:

Allow user to start a ready batch.

Scope:

- transition Ready → In Progress
- block start if materials are short unless later override is explicitly added
- activity log

Acceptance criteria:

- ready batch can start
- short-material batch cannot start
- starting does not change stock

## Milestone 4.3 — Complete Batch

Goal:

Complete a batch and update stock safely.

Scope:

- deduct required materials
- increase finished product stock
- create InventoryMovement records
- create ActivityLog
- block double completion
- run inside transaction where possible

Acceptance criteria:

- product stock increases
- material stock decreases
- movements are created
- batch status becomes Complete
- completing twice is blocked
- insufficient material completion is blocked

Required journey:

- create product
- create materials
- define recipe
- create batch
- complete batch
- verify material/product stock changes
- verify movements/activity log

---

# Phase 5 — Buy Materials / Purchases

## Milestone 5.1 — Buy List / Reorder Suggestions

Goal:

Show materials that need buying.

Scope:

- low material list
- suggested quantity rule
- simple “Add to Purchase” action

Acceptance criteria:

- low materials appear
- suggestions are understandable
- no automatic ordering

## Milestone 5.2 — Create Purchase

Goal:

Allow user to create a material purchase.

Scope:

- create purchase
- add materials
- quantity
- supplier optional
- expected date optional
- status Draft/Ordered

Acceptance criteria:

- purchase can be created
- purchase creation does not increase material stock
- purchase appears in Buy page

## Milestone 5.3 — Receive Purchase

Goal:

Increase material stock when purchase arrives.

Scope:

- mark purchase Received
- increase material stock
- create InventoryMovement
- create ActivityLog
- block double receiving

Acceptance criteria:

- receiving purchase increases stock
- creating purchase does not increase stock
- receiving twice is blocked
- movement/activity records exist

Required journey:

- create material
- create purchase
- mark received
- confirm material stock increased
- confirm movement/activity log

---

# Phase 6 — Today Dashboard

## Milestone 6.1 — Today Data Summary

Goal:

Show the seller what needs attention.

Scope:

- orders to pack
- waiting-on-stock orders
- low products
- low materials
- active batches
- purchases due soon
- simple money snapshot if available

Acceptance criteria:

- dashboard reads real data
- no fake static cards after this milestone
- page remains simple and task-first

## Milestone 6.2 — Today Actions

Goal:

Allow common next actions from Today.

Scope:

- open order
- start packing
- open low stock item
- create batch
- create purchase

Acceptance criteria:

- actions route to correct workflow
- no hidden automation
- user remains in control

---

# Phase 7 — Money Summary

## Milestone 7.1 — Product Cost and Estimated Profit

Goal:

Estimate product profitability.

Scope:

- sale price
- material cost estimate
- packaging/shipping optional simple cost fields
- platform fee estimate optional simple percentage
- estimated profit per product

Acceptance criteria:

- profit is clearly labelled estimated
- calculations are tested
- no tax/accounting claims

## Milestone 7.2 — Money Page

Goal:

Show simple sales and cost summary.

Scope:

- sales this month
- estimated profit
- recent transactions/activity
- simple cost breakdown

Acceptance criteria:

- Money page loads real data
- labels are clear and cautious
- no full accounting features implied

---

# Phase 8 — Basic Integrations

Integrations should come after manual workflows are stable.

## Milestone 8.1 — Integration Architecture

Goal:

Add safe integration structure without live automation.

Scope:

- integration client interfaces
- sync job model/log if needed
- external ID storage
- mocked fixtures
- error handling

Acceptance criteria:

- integration logic is isolated
- tests can run without live API
- failures are visible
- duplicate protection strategy exists

## Milestone 8.2 — Etsy Order Import: Mocked

Goal:

Import Etsy-like orders from fixtures/mocked client.

Scope:

- parse external order
- map to internal order
- store external_order_id
- avoid duplicates
- do not automatically push stock back

Acceptance criteria:

- fixture import works
- duplicate import is ignored or safely updated
- errors are logged
- no live API required for Codex-safe tests

## Milestone 8.3 — Etsy Live Smoke: Codespace/Manual Environment

Goal:

Verify live OAuth/API only in a suitable environment.

Scope:

- environment exception report if Codex cannot run it
- exact Codespace verification steps
- no claim of live verification unless actually performed

Acceptance criteria:

- live behaviour is documented as verified or not verified
- mocked tests still protect core logic

## Milestone 8.4 — Manual Stock Push: Optional Post-V1 Candidate

Goal:

Eventually allow user-reviewed stock push to Etsy.

Status:

Deferred until manual inventory/order workflows are stable.

First allowed version:

- user reviews stock update
- user clicks Push
- result is logged
- failure is visible

Still not allowed:

- silent automatic two-way sync

---

# Phase 9 — UI Hardening

## Milestone 9.1 — UI Consistency Pass

Goal:

Make pages feel consistent and beginner-friendly.

Scope:

- consistent page layout
- consistent buttons
- status badges
- empty states
- clear copy
- reduce density

Acceptance criteria:

- each page has no more than 3 main content areas except Today
- buttons look like buttons
- empty states explain next action
- no enterprise labels remain

## Milestone 9.2 — Headless UI/Journey Screenshots Optional

Goal:

Add AI-verifiable UI evidence where practical.

Scope:

- seed demo data
- capture key page screenshots
- upload or save screenshot summary
- do not require interactive headed browser

Acceptance criteria:

- UI can be checked headlessly where environment allows
- screenshot report exists if implemented
- no reliance on manual browser-only debugging

---

# Phase 10 — Stabilisation and Release Candidate

## Milestone 10.1 — Full Journey Suite

Goal:

Ensure the main app workflows work from start to finish.

Required journeys:

- first-time setup
- create product/material/recipe
- create order
- reserve stock
- pack and ship order
- make batch
- buy and receive material
- low stock appears on Today
- money summary updates

Acceptance criteria:

- journey tests pass or limitations are documented
- latest server run report is green or blockers are listed

## Milestone 10.2 — Release Candidate Freeze

Goal:

Stop feature development and fix blockers only.

Allowed:

- failing test fixes
- critical bugs
- install/build failures
- broken core workflows
- incorrect docs

Not allowed:

- new features
- new screens
- new integrations
- speculative polish
- unrelated refactors

Acceptance criteria:

- completion-status shows only blockers or optional backlog
- known-issues is current
- do-not-build-yet is current
- progress-log is current

## Milestone 10.3 — V1 Release

Goal:

Declare V1 complete.

V1 is complete when:

- manual core workflows work
- stock-changing actions are traceable
- core journeys pass
- auth/shop ownership is safe enough for MVP
- no known critical blockers remain
- optional improvements are moved to backlog
- release summary exists

---

## 8. Required Journey Tests

Every major workflow should eventually have an executable journey test.

### 8.1 Setup Journey

```text
Create shop
Create product
Create material
Create recipe
Verify product can be made
```

### 8.2 Order Journey

```text
Create product with stock
Create order
Reserve stock
Pack order
Ship order
Verify stock/reservation state
```

### 8.3 Make Batch Journey

```text
Create product
Create materials
Define recipe
Create batch
Complete batch
Verify product stock increased
Verify material stock decreased
Verify movements exist
```

### 8.4 Buy Materials Journey

```text
Create material
Create purchase
Add purchase item
Mark ordered
Mark received
Verify material stock increased
Verify movement exists
```

### 8.5 Low Stock Journey

```text
Create material below reorder point
Verify low stock warning
Verify buy list includes material
```

### 8.6 Money Journey

```text
Create shipped order
Set product cost/price
Verify estimated revenue/profit summary
```

---

## 9. Server Verification Run

The repo should eventually support one command that runs the standard verification suite and writes evidence files.

Example:

```bash
npm run verify:server
```

Or:

```bash
make verify
```

The command should run available checks such as:

- typecheck
- lint
- unit tests
- service tests
- journey tests
- build
- diagnostic checks
- no-debug-leftovers check
- report writer

It should write files such as:

```text
docs/ai/reports/latest-server-run.md
docs/ai/reports/latest-failures.md
docs/ai/reports/release-readiness.md
```

Codex should read these before debugging or continuing work.

---

## 10. Bug Handling Method

For complex bugs, create a bug fix plan:

```text
docs/ai/bugfix-plans/active/BUG-####-short-name.md
```

Use Milestones only.

Do not rename them to phases, steps, stages, tasks, or parts.

Suggested bug plan milestones:

1. Reproduce and locate the failure
2. Add regression coverage
3. Implement smallest root-cause fix
4. Clean up diagnostics
5. Full verification
6. Closeout

Codex should implement one bug milestone per chat when needed.

The human reports symptoms. Codex owns debugging.

---

## 11. Environment Rules

Codex may not be able to run everything.

Codex-safe work:

- repo inspection
- code edits
- unit tests
- service tests
- mocked integration tests
- typecheck/lint/build
- docs updates

Codespace or environment-specific work:

- live OAuth login
- live API calls
- webhook testing
- Docker-only services
- interactive browser preview
- environment-specific smoke tests

Codex must not claim verification it did not perform.

If blocked by environment limits, Codex should:

1. run mocked/local checks
2. write an environment exception report
3. provide exact Codespace verification steps
4. mark the live behaviour as not fully verified

---

## 12. Security Baseline

Minimum security expectations:

- managed auth
- no custom password system
- server-side authorization checks
- all records scoped to shop/account
- no trusting `shop_id`, `user_id`, or `role` from frontend input
- no secrets in frontend code
- no secret keys committed
- ownership tests for private data
- safe destructive actions
- activity logs for important user actions

High-risk areas:

- auth
- permissions
- stock
- money/profit
- integrations
- destructive actions
- data migration

High-risk work requires tests and clear evidence.

---

## 13. UI Rules

The UI should be simple and beginner-friendly.

General layout:

- page title
- short subtitle
- up to 3 main content areas per page
- Today page may have more, but should still be calm
- primary action obvious
- forms in drawers/modals where useful
- clear empty states
- readable tables
- no excessive charts

Language:

Use:

- Today
- Orders
- Products & Stock
- Make
- Buy
- Money
- Materials
- Recipe
- Batch

Avoid:

- procurement
- manufacturing execution
- allocation
- reconciliation
- supply chain orchestration
- enterprise resource planning language

---

## 14. Release Definition

V1 is shippable when:

- the core operating loop works
- product/material/recipe setup works
- orders reserve and release stock correctly
- pack/ship workflow works
- batch completion updates stock correctly
- purchase receiving updates stock correctly
- Today dashboard shows real tasks
- Money page shows basic estimated data
- core journey tests pass
- no critical bugs remain
- environment limitations are documented
- deferred work is clearly listed
- progress log and completion status are updated

V1 does not require:

- automatic integrations
- advanced accounting
- shipping labels
- forecasting
- drag-and-drop planning
- multi-user team workflows beyond basic owner/helper if added

---

## 15. Post-V1 Backlog Candidates

These may be unlocked later with explicit decision records:

- Etsy live import
- manual Etsy stock push
- Facebook Marketplace import if API access allows
- owner/helper roles
- better packing slips
- simple CSV import/export
- basic mobile polish
- product photo uploads
- supplier reorder reminders
- simple shipping tracking field
- improved profit costing
- simple customer messages/notes

Still high caution:

- automatic two-way stock sync
- supplier ordering automation
- tax/accounting automation
- shipping label purchase
- payments
- multi-warehouse
- advanced forecasting

---

## 16. Standard Codex Prompts

Once this roadmap and the AI rules are in the repo, prompts should be small.

### Implement next milestone

```text
Read AI_DEVELOPMENT.md.
Implement the next unlocked milestone from docs/ai/completion-status.md.
```

### Implement specific milestone

```text
Read AI_DEVELOPMENT.md.
Implement Milestone X from docs/ai/project-roadmap.md.
```

### Debug from report

```text
Read AI_DEVELOPMENT.md and docs/ai/reports/latest-server-run.md.
Fix the verified failure only.
```

### Work from bug plan

```text
Read AI_DEVELOPMENT.md.
Implement Milestone X from docs/ai/bugfix-plans/active/BUG-####-name.md.
```

---

## 17. Final Development Rule

Do not judge progress by “percentage complete.”

Judge progress by checked-off workflows.

The project is not complete when no improvements are possible.

The project is complete when the defined V1 workflows work, the required checks pass, and remaining work is optional or deferred.

When the milestone is complete, stop building.

Move improvements to backlog.

Ship.
