# Milestone 10.3 V1 Release Decision Report (2026-05-29)

## Scope
Milestone 10.3 — V1 Release readiness validation and release declaration decision.

This slice was selected from `docs/ai/next-chat-task.md`. It is a validation, release-process, and documentation slice only; it does not introduce product behavior changes.

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
- `docs/ai/safety-critical-rules.md`
- `docs/ai/reports/milestone-10.2-completion-closeout-signoff-2026-05-29.md`
- `tests/test_journey_milestone_10_1.py`
- `tests/test_milestone_2_4_stock_adjustment.py`
- `tests/test_milestone_5_3_receive_purchase.py`
- `tests/test_order_scoping.py`
- `src/pollen/auth.py`
- `src/pollen/inventory.py`
- `src/pollen/services.py`
- `src/pollen/app.py`

## Milestone 10.2 Evidence Check
Milestone 10.2 completion closeout evidence exists at `docs/ai/reports/milestone-10.2-completion-closeout-signoff-2026-05-29.md`.

That report records:
- Milestone 10.2 status advanced to `complete`.
- No product blockers recorded.
- Full Codex-cloud validation sequence run, with compile, lint, and full test suite passing.
- V1 release declaration intentionally deferred to Milestone 10.3.

## V1 Acceptance Criteria Check
| V1 criterion | Result | Evidence |
|---|---|---|
| Manual core workflows work | Passed | `tests/test_journey_milestone_10_1.py` covers create product/material/recipe, create order, reserve stock, pack and ship, money summary, create/start/complete batch, purchase creation/receipt, and Today summary recovery. Fresh `pytest -q` passed. |
| Stock-changing actions are traceable | Passed | `InventoryMovementRepository` and `ActivityLogRepository` store shop-scoped stock trace records. Product and material stock adjustments create movement/activity records. Purchase receipt creates movement/activity records and blocks duplicate receipt. The app renders inventory movements and activity logs. |
| Core journeys pass | Passed | Fresh full test suite passed: `98 passed`. |
| Auth/shop ownership is safe enough for MVP | Passed | Auth resolves a server-owned shop per user, service methods use resolved shop context, and tests cover ignored requested shop IDs, cross-shop denial, and unauthenticated denial. |
| No known critical blockers remain | Passed | `docs/ai/known-issues.md` lists no blocking or non-blocking product issues. The only recorded limitation is environment-limited package-index/proxy access for pinned dev dependency installation. |
| Optional improvements are moved to backlog | Passed | `docs/ai/do-not-build-yet.md` keeps optional Milestone 9.2 screenshot evidence deferred unless explicitly scoped later. |
| Release summary exists | Passed | This report is the V1 release summary and decision evidence. |

## Commands Executed (Codex Cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Results
- Runtime dependency installation: pass.
- Dev dependency installation: environment-limited. The configured package-index/proxy returned `Tunnel connection failed: 403 Forbidden`, then could not resolve `pytest==8.4.2`.
- Compile check: pass.
- Lint check: pass.
- Full test suite: pass (`98 passed`).

## Decision
V1 is declared complete as of 2026-05-29.

No critical blocker prevents release declaration. The package-index/proxy issue remains an environment limitation rather than a product blocker because compile, lint, and the full test suite passed with the available Codex environment tooling.

## Environment Limitations
- `pip install -r requirements-dev.txt` remains blocked by package-index/proxy access for pinned dev dependencies.
- No live OAuth, webhook, external marketplace API, Docker-only, hosted server, or headed-browser checks were required for this V1 release decision.
- Optional Milestone 9.2 screenshot evidence remains deferred and was not required for V1 release acceptance.

## Out of Scope
- New features, screens, integrations, or speculative polish.
- Optional Milestone 9.2 screenshot evidence.
- Post-V1 backlog implementation.
- Broad refactors or non-release cleanup.

## Next Recommended Action
Stop automatic feature work. Future work should begin only after selecting or receiving one bounded post-V1 task with explicit acceptance criteria.
