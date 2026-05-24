# Environment Capabilities

Update this per repository. Default assumptions follow.

## AI/Codex Environment

Usually reliable: read/edit repo, inspect code, run package commands, unit tests, typecheck/lint/build, service tests, mocked integration tests, markdown reports.

Often unreliable/unavailable: Docker, Docker Compose, long-running services, live OAuth callbacks, webhook tunnels, external APIs blocked by policy, APIs returning 401/403 due to environment restrictions, real provider browser login, headed browser testing, production-like network tests.

## Rule
Do not repeatedly try unsupported tools. Stop, record the limitation, run closest mocked/local check, and write exact verification steps for a supported environment.

## Codespaces
Use for full app runtime, browser preview, environment-specific testing, headless screenshots if configured, auth callback verification where possible, API smoke tests where credentials/network allow.

## GitHub Actions
Use for PR verification, typecheck, lint, tests, build, mocked e2e, artifact/report upload.

## Test Tiers
- Tier 1 Codex-safe: static checks, unit/service tests, mocked integration tests, build.
- Tier 2 CI-safe: full tests, build, mocked e2e, artifacts.
- Tier 3 Codespace-required: browser preview, full local app workflows, environment-specific checks.
- Tier 4 External/prod smoke: real OAuth/API/webhook/payment/deploy checks.

If full verification is blocked, use `docs/ai/templates/environment-exception-template.md`.
