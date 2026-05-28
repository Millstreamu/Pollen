# Milestone 10.1 — Release-Candidate Validation Sign-off (2026-05-28)

## Milestone
- **Name:** Milestone 10.1 — Full Journey Suite
- **Previous status:** `release-candidate` *(status had already been advanced after the money-summary journey slice)*
- **New status:** `release-candidate`

## Scope of this slice
- Execute the full Codex-cloud validation command set for the Milestone 10.1 release-candidate gate.
- Confirm the full journey suite now covers every required Milestone 10.1 workflow, including the previously missing money-summary update path.
- Record durable sign-off evidence and advance the next-task handoff to completion closeout.

## Commands run
1. `python -m pip install --upgrade pip`
2. `pip install -r requirements.txt`
3. `pip install -r requirements-dev.txt`
4. `python -m compileall -q src tests`
5. `ruff check src tests`
6. `pytest -q`

## Results
- `python -m pip install --upgrade pip` — **pass** with package-index proxy retry warnings; pip was already installed.
- `pip install -r requirements.txt` — **pass**; no runtime dependencies are currently declared.
- `pip install -r requirements-dev.txt` — **environment-limited warning**; the configured package index/proxy returned `Tunnel connection failed: 403 Forbidden`, then could not resolve `pytest==8.4.2`.
- `python -m compileall -q src tests` — **pass**.
- `ruff check src tests` — **pass**.
- `pytest -q` — **pass**: `98 passed in 0.42s`.

## Required journey coverage sign-off
| Milestone 10.1 required journey | Evidence | Decision |
|---|---|---|
| first-time setup | The journey starts from a clean app instance and authenticated shop/user context. | Passed |
| create product/material/recipe | The journey creates a priced product, material, and recipe row. | Passed |
| create order | The journey creates a manual order for the product. | Passed |
| reserve stock | The journey asserts stock-on-hand, reserved stock, and available stock after order creation. | Passed |
| pack and ship order | The journey packs and ships the order, then verifies shipped inventory state. | Passed |
| make batch | The journey creates, starts, and completes a batch, then verifies product/material stock changes. | Passed |
| buy and receive material | The journey creates an ordered purchase, receives it, and verifies material restock. | Passed |
| low stock appears on Today | The journey verifies Today summary counts for low product/material state. | Passed |
| money summary updates | The money-summary slice now verifies shipped-order estimated revenue, cost, and profit appear on the Money page. | Passed |

## Sign-off decision
The Milestone 10.1 release-candidate gate is signed off in the current Codex-cloud environment.

The full relevant validation suite is green after the money-summary journey gap was closed. Milestone 10.1 remains in `release-candidate` status and is ready for completion closeout validation/sign-off.

## Environment limitations
- Dev dependency installation remains blocked by the configured package-index/proxy for pinned `pytest==8.4.2`.
- The needed tools were already available in the environment, so compile, lint, and the full pytest suite were still executed successfully.
- No live OAuth, webhook, external marketplace API, Docker-only, or headed-browser smoke checks were required or performed for this local journey-suite gate.

## Out of scope
- Milestone 10.2 release-candidate freeze bookkeeping.
- V1 release declaration.
- Optional Milestone 9.2 screenshot evidence.
- New features, new screens, external integrations, or speculative polish.

## Next required action
Run Milestone 10.1 completion closeout validation/sign-off. If the closeout validation remains green, transition Milestone 10.1 from `release-candidate` to `complete` and hand off to Milestone 10.2 — Release Candidate Freeze.
