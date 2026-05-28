# Milestone 10.1 — Money Summary Journey Slice Report

- Date: 2026-05-28
- Milestone: 10.1 Full Journey Suite
- Task: Close the remaining money-summary journey coverage gap

## Objective
Add one bounded deterministic Milestone 10.1 journey slice proving that shipped orders update the Money page summary, while keeping the implementation limited to the current estimated product-price/product-cost model.

## Scope completed
- Inspected the existing product estimated cost/profit fields from Milestone 7.1 and the current Money page surface.
- Added a read-only `MoneySummaryService` that derives estimated totals from shipped order items and product pricing/cost fields.
- Updated the Money page to preserve the beginner-friendly empty state when no shipped items exist, and to show estimated shipped-order revenue, cost, and profit once shipped-order data exists.
- Wired product create/edit app-shell payloads and forms to carry the existing estimated pricing/cost fields needed by the Money page summary.
- Extended the Milestone 10.1 journey test to assert the Money page updates after pack/ship.
- Added a focused regression assertion that shipped orders are counted while unshipped orders do not inflate estimated money totals.

## Validation commands and results
- `python -m pip install --upgrade pip` — pass.
- `pip install -r requirements.txt` — pass; no runtime dependencies are currently declared.
- `pip install -r requirements-dev.txt` — environment-limited; the package-index proxy returned `Tunnel connection failed: 403 Forbidden` for `pytest==8.4.2`, while pytest and ruff were already available in this environment.
- `python -m compileall -q src tests` — pass.
- `ruff check src tests` — pass.
- `pytest -q` — pass: `98 passed in 0.25s`.

## Acceptance criteria evidence
| Criterion | Evidence | Decision |
|---|---|---|
| Money journey coverage exists | `tests/test_journey_milestone_10_1.py` now creates a priced product, ships an order, and asserts Money page totals. | Passed |
| Money page remains safe before data exists | Existing Money UI empty-state test still passes and the page only replaces the empty state after shipped items exist. | Passed |
| Totals are deterministic | `MoneySummaryService` calculates from in-memory shipped orders and product fields without external integrations. | Passed |
| Scope stays bounded | No accounting ledger, taxes, payment integrations, or purchase-spend modeling were added. | Passed |

## Money calculation scope
The implemented summary is intentionally an estimate:
- estimated revenue = shipped quantity × product sale price
- estimated cost = shipped quantity × (estimated material cost + estimated packaging/shipping cost + estimated platform fee)
- estimated profit = shipped quantity × product estimated profit per sale

Purchases remain visible in Make / Buy and Today workflows, but purchase spend is not included because current purchase records do not yet carry unit costs. That broader accounting behavior remains out of scope for Milestone 10.1.

## Decision
The required Milestone 10.1 `money summary updates` coverage gap is closed for the current product scope. Milestone 10.1 can proceed to release-candidate validation/sign-off after the normal finish-line review.

## Environment limitations
Dev dependency installation was blocked by the configured package-index proxy for `pytest==8.4.2`; the required tools were already available, so compile, lint, and full tests still ran and passed in the Codex cloud environment.

## Out of scope
- Full accounting ledger behavior.
- Taxes, refunds, payment fees beyond the existing product platform-fee estimate.
- Purchase unit-cost/spend modeling.
- External marketplace payment or finance integrations.
- Screenshot evidence.

## Next recommended action
Run Milestone 10.1 release-candidate validation/sign-off and, if green, advance the milestone toward completion.
