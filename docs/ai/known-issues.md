# Known Issues

## Blocking Issues
None recorded.

## Non-Blocking Issues
None recorded.

## Environment Limitations

### Codex package-index/proxy cannot currently install pinned dev dependencies

Status: environment-limited
Reported: 2026-05-28
Area: Codex cloud dependency installation

Description:
`pip install -r requirements-dev.txt` currently retries through the configured package index/proxy and fails with `Tunnel connection failed: 403 Forbidden`, then reports no matching distribution for pinned dev packages such as `pytest==8.4.2`.

Current workaround:
Use the already-available environment tooling for compile, lint, and pytest validation when present, and keep rerunning the explicit dependency install command so the limitation remains visible.

Required for completion:
no, unless the validation tools are absent or compile/lint/tests cannot run.

Linked plan/report:
`docs/ai/reports/milestone-10.2-startup-planning-scope-lock-report-2026-05-28.md`

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
