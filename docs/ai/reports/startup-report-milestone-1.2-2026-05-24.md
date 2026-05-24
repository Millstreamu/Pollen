# Startup Report — Milestone 1.2 Managed Auth and Shop Ownership

Date: 2026-05-24  
Task source: Direct human request in Codex chat (`Start Milestone 1.2 implementation planning`)  
Milestone reference: `project-roadmap.md` → `Milestone 1.2 — Managed Auth and Shop Ownership`

## Task understood
Prepare a pre-implementation startup report for **Milestone 1.2 — Managed Auth and Shop Ownership** that confirms scope boundaries, required safeguards, architecture approach, and verification plan before implementation begins.

## Rule files read
- `AI_DEVELOPMENT.md`
- `docs/ai/development-process.md`
- `docs/ai/task-execution-rules.md`
- `docs/ai/testing-rules.md`
- `docs/ai/security-rules.md`
- `docs/ai/integration-rules.md`
- `docs/ai/environment-capabilities.md`

## Project memory files read
- `docs/ai/project-rules.md`
- `docs/ai/progress-log.md`
- `docs/ai/completion-status.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`

## Relevant repo files found
- `project-roadmap.md` (authoritative Milestone 1.2 scope and acceptance criteria)
- `README.md` (current environment setup and execution commands)
- `requirements.txt`, `requirements-dev.txt` (dependency baselines)
- `src/pollen/app.py`, `src/pollen/models.py` (current application skeleton)
- `tests/test_app.py`, `tests/test_models.py` (existing test baselines)

## Existing patterns observed
- Repository currently contains a lightweight Python application skeleton and deterministic unit tests.
- No managed auth provider is integrated yet.
- No explicit persistence layer is present yet for user/shop ownership records.
- Environment bootstrapping is already reproducible using `requirements.txt` + `requirements-dev.txt`.

## Planned changes (for Milestone 1.2 implementation phase)
- Introduce a managed auth integration path (Google-capable provider abstraction; no custom password system).
- Add user and shop ownership models with `shop_id` scoping patterns.
- Add current shop context resolution for authenticated requests.
- Add protected-route behavior for private pages/endpoints.
- Add server-side ownership checks that never trust client-provided shop identifiers.
- Add/extend tests for:
  - logged-out route protection,
  - shop auto-provisioning for first login,
  - shop-scoped data access,
  - cross-shop access denial.
- Update milestone tracking and project memory once implementation is complete.

## Out-of-scope items
- Advanced role model or invite workflows.
- Custom password authentication.
- Later milestone business logic (orders, stock workflows, money calculations, integrations).
- Non-essential UI polish unrelated to auth/shop ownership.

## Risks
- Over-engineering auth before minimal safe coverage is in place.
- Incorrect trust boundary (accepting `shop_id` from client input) causing data isolation failures.
- Introducing framework/auth dependencies without updating setup instructions and tests.
- Incomplete environment-safe verification for auth behaviors that depend on live OAuth flows.

## Tests/checks to run during Milestone 1.2 implementation
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

If managed auth introduces additional toolchain checks (lint/typecheck), add and run those commands as part of milestone verification.

## Initial milestone status recommendation
- `Milestone 1.2 — Managed Auth and Shop Ownership`: **in-progress** once implementation begins.
- Milestone 1.1 remains complete.
