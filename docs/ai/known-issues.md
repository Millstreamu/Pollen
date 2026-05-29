# Known Issues

## Blocking Issues
None recorded.

## Non-Blocking Issues
None recorded.

## Environment Limitations
None recorded.

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
