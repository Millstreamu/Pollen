# Known Issues

## Blocking Issues
None recorded.

## Non-Blocking Issues
None recorded.

## Environment Limitations
None recorded.

### Make / Buy lower-page management UI hidden pending IA follow-up

Status: non-blocking
Reported: 2026-06-01
Area: Make / Buy information architecture

Description:
The approved Make / Buy overview now hides inline material management, archived-material filters, material stock-adjustment controls, recipe management, inventory movement history, activity logs, created-purchases debug copy, and buy-list formula/debug text from the main page. The existing services and post actions were not deleted, but these admin-oriented controls need a future drawer, modal, or detail-page home before they are visible again.

Current workaround:
Core operational flows remain visible through Plan Batch, Create Purchase, Mark Received, Make Next, Buy List, and Incoming Purchases. Existing backend/service behavior remains covered by regression tests.

Required for completion:
no

Linked plan/report:
Direct Post-V1 Make / Buy UI simplification task.

## Resolved Issues

### Codex dev dependency install accepts available compatible tooling

Status: resolved
Reported: 2026-05-28
Resolved: 2026-05-29
Area: Codex cloud dependency installation

Description:
`pip install -r requirements-dev.txt` previously retried through the configured package index/proxy and failed with `Tunnel connection failed: 403 Forbidden`, then reported no matching distribution for exact pinned dev packages such as `pytest==8.4.2`.

Resolution:
`requirements-dev.txt` now uses conservative compatible ranges for pytest and ruff so Codex cloud can satisfy the dev setup with already-available compatible tooling when package-index access is limited.

Verification:
`pip install -r requirements-dev.txt`, `python -m compileall -q src tests`, `ruff check src tests`, and `PYTHONDONTWRITEBYTECODE=1 pytest -q` all passed on 2026-05-29.

Linked plan/report:
`docs/ai/reports/post-v1-dev-dependency-installability-report-2026-05-29.md`

## Deferred Issues
See `docs/ai/do-not-build-yet.md`.

## Format

```md
### <Issue Title>

Status: blocking / non-blocking / deferred / environment-limited
Reported: YYYY-MM-DD
Area: ...

Description:
...

Current workaround:
...

Required for completion:
yes/no

Linked plan/report:
...
```
