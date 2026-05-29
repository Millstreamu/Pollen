# Milestone 10.3 V1 Release Decision Report (2026-05-29)

## Scope
Milestone 10.3 — V1 Release readiness validation and release declaration decision.

This was selected from `docs/ai/next-chat-task.md`. It is a validation, release-process, and documentation slice only. No runtime product behavior changes, new screens, new integrations, or speculative polish were introduced.

## Source Files Reviewed
- `AI_DEVELOPMENT.md`
- `project-roadmap.md`
- `docs/ai/next-chat-task.md`
- `docs/ai/completion-status.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`
- `docs/ai/progress-log.md`
- `docs/ai/development-process.md`
- `docs/ai/testing-rules.md`
- `docs/ai/task-execution-rules.md`
- `docs/ai/finish-line-protocol.md`
- `docs/ai/reporting-rules.md`
- `docs/ai/reports/milestone-10.2-completion-closeout-signoff-2026-05-29.md`
- `tests/test_journey_milestone_10_1.py`
- `tests/test_order_scoping.py`
- `tests/test_milestone_2_4_stock_adjustment.py`
- `tests/test_milestone_3_2_stock_reservation.py`
- `tests/test_milestone_3_3_pack_ship.py`
- `tests/test_milestone_4_3_complete_batch.py`
- `tests/test_milestone_5_3_receive_purchase.py`
- `src/pollen/auth.py`
- `src/pollen/inventory.py`
- `src/pollen/services.py`

## Milestone 10.2 Prerequisite Check
Milestone 10.2 completion closeout evidence exists at `docs/ai/reports/milestone-10.2-completion-closeout-signoff-2026-05-29.md`.

The prerequisite report records that Milestone 10.2 was validated in Codex cloud, advanced to `complete`, and intentionally left V1 release declaration to Milestone 10.3.

## V1 Release Criteria Check
| V1 criterion | Decision | Evidence |
|---|---|---|
| manual core workflows work | Passed | The Milestone 10.1 journey creates product/material/recipe data, creates a manual order, reserves stock, packs/ships, makes a batch, buys/receives material, verifies Today, and verifies Money. Full pytest suite passed. |
| stock-changing actions are traceable | Passed | Stock adjustment, purchase receive, batch completion, order pack/ship/cancel, and related workflows create inventory movements and/or activity logs with shop and actor context. Relevant regression tests passed. |
| core journeys pass | Passed | `pytest -q` passed with `98 passed`; the suite includes the Milestone 10.1 end-to-end journey. |
| auth/shop ownership is safe enough for MVP | Passed | Auth resolves server-owned shop context from deterministic bearer tokens; order scoping tests confirm requested shop IDs are ignored, cross-shop reads are denied, and unauthenticated access is denied. |
| no known critical blockers remain | Passed | `docs/ai/known-issues.md` lists no blocking or non-blocking product issues. The only recorded issue is the Codex package-index/proxy limitation for installing pinned dev dependencies. |
| optional improvements are moved to backlog | Passed | `docs/ai/do-not-build-yet.md` keeps optional Milestone 9.2 screenshot evidence deferred unless a future scoped task unlocks it. |
| release summary exists | Passed | This report is the V1 release decision summary. |

## Commands Executed (Codex Cloud)
Baseline before documentation changes:
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

Final validation after documentation changes:
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Results
Baseline validation:
- Runtime dependency installation: pass.
- Dev dependency installation: environment-limited. The configured package-index/proxy returned `Tunnel connection failed: 403 Forbidden`, then could not resolve `pytest==8.4.2`.
- Compile check: pass.
- Lint check: pass.
- Full test suite: pass (`98 passed`).

Final validation:
- Runtime dependency installation: pass.
- Dev dependency installation: environment-limited. The configured package-index/proxy returned `Tunnel connection failed: 403 Forbidden`, then could not resolve `pytest==8.4.2`.
- Compile check: pass.
- Lint check: pass.
- Full test suite: pass (`98 passed`).

## Decision
V1 is declared complete.

Milestone 10.3 is complete because the release criteria are satisfied, the full deterministic Codex-cloud validation suite passes apart from the already documented dependency-install environment limitation, and no known product blocker remains.

## Environment Limitations
- `pip install -r requirements-dev.txt` remains blocked by package-index/proxy access for pinned dev dependencies. This does not block V1 because the current environment already has the required validation tooling available and compile, lint, and full tests pass.
- No live OAuth, webhook, external marketplace API, Docker, or headed-browser checks were performed in Codex cloud.
- Optional Milestone 9.2 screenshot evidence remains deferred and was not required for V1 declaration.

## Changed Files
- `docs/ai/completion-status.md`
- `docs/ai/next-chat-task.md`
- `docs/ai/progress-log.md`
- `docs/ai/reports/milestone-10.3-v1-release-decision-report-2026-05-29.md`

## What Was Intentionally Not Implemented
- No product runtime code changes.
- No new features, screens, integrations, or broad refactors.
- No optional screenshot evidence.
- No post-V1 backlog work.

## Follow-up Backlog Items
- Optional Milestone 9.2 screenshot evidence may be scoped later if a supported screenshot/headless-browser task explicitly unlocks it.
- Future post-V1 features or maintenance should be selected explicitly from updated roadmap/backlog context rather than continuing automatically.
