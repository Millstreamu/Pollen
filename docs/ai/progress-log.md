# Progress Log

Records meaningful completed work. Update after feature completion, bug fix completion, milestone completion, release verification, important decision, or server-run evidence that changes status.

## Current Status
Project phase: Phase 1 — App Foundation  
Current milestone: Milestone 1.2 — Managed Auth and Shop Ownership (stabilising)  
Overall status: Milestone 1.2 is in stabilising after closeout validation passed with no regressions.

## Latest Summary
No project-specific summary yet.

## Entry Format

```md
### YYYY-MM-DD — <Task / PR / Issue Title>

Branch/PR/Issue:
- ...

Completed:
- ...

Checks run:
- `<command>` — pass/fail/not run

Notes:
- ...

Follow-up:
- ...
```

## Entries

Add entries below.

### 2026-05-25 — Milestone 1.2 closeout validation pass

Branch/PR/Issue:
- local milestone closeout update

Completed:
- Re-ran milestone closeout validation (dependency install attempt, compile check, full tests).
- Confirmed no regressions (`15 passed`).
- Transitioned Milestone 1.2 status from `in-progress` to `stabilising` in completion tracking.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- Environment cannot fetch dev dependencies from package index, but existing environment includes working `pytest` and full suite passed.

Follow-up:
- If requested, run one more clean validation pass in a fully networked environment and move to `release-candidate`.


### 2026-05-24 — Milestone 1.2 continuation startup report (shop-scoping persistence slice)

Branch/PR/Issue:
- local milestone planning update

Completed:
- Added startup continuation report for Milestone 1.2 persistence-backed `shop_id` scoping slice.
- Defined AI_DEV flow alignment (Spec → Scan → Simplify → Slice → Verify → Clean → Freeze → Ship).
- Captured acceptance-criteria gap closure plan and verification commands.

Checks run:
- `git diff --name-only` — pass

Notes:
- This is planning/report-only work; implementation is intentionally deferred to the next task turn.

Follow-up:
- Implement persistence-backed shop-scoped record create/read enforcement and tests.


### 2026-05-24 — Milestone 1.2 implementation start (auth + ownership foundation)

Branch/PR/Issue:
- local milestone implementation update

Completed:
- Added managed-auth abstraction, user/shop/auth context models, shop auto-provisioning, and ownership checks.
- Added protected-route enforcement in app shell for private pages.
- Added Milestone 1.2 unit tests for route protection and cross-shop denial.
- Added implementation report: `docs/ai/reports/milestone-1.2-implementation-report-2026-05-24.md`.

Checks run:
- `python -m pip install --upgrade pip` — warning (index access retries; pip present)
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (package index access blocked)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- Implementation is initial Milestone 1.2 slice; production OAuth wiring and persistence integration are pending within milestone scope.

Follow-up:
- Continue Milestone 1.2 with persistent record scoping integration where records are created/queried.

### 2026-05-24 — Start Milestone 1.2 implementation planning

Branch/PR/Issue:
- local milestone planning update

Completed:
- Added startup planning report for `Milestone 1.2 — Managed Auth and Shop Ownership`.
- Shifted completion tracking from Milestone 1.1 complete state to Milestone 1.2 in-progress state.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (package index access blocked; existing env already had pytest available)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- This change starts planning/execution tracking only; Milestone 1.2 feature implementation remains pending.

Follow-up:
- Implement Milestone 1.2 auth and shop ownership scope per roadmap.

### 2026-05-24 — Mark Milestone 1.1 complete

Branch/PR/Issue:
- local milestone status update

Completed:
- Updated completion tracking to set `Milestone 1.1 — App Shell` to `complete`.
- Replaced placeholder scope checklist items with milestone-specific completed items.
- Updated current project status to Phase 1 with Milestone 1.1 complete.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (package index access blocked; existing env already had pytest available)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- Milestone status now matches the implemented app shell and existing test coverage.

Follow-up:
- Start Milestone 1.2 implementation planning.

### 2026-05-24 — AI kit repair after accidental simplification

Branch/PR/Issue:
- local docs/process repair

Completed:
- Repaired AI development kit installation by restoring expected kit file set names.
- Added `docs/ai/report-format.md` from the detailed reporting rules content.
- Added `docs/ai/security-basics.md` from the detailed security rules content.
- Added missing project-specific placeholders: `docs/ai/project-rules.md` and `docs/ai/project-roadmap.md`.

Checks run:
- `git diff --name-only` — pass

Notes:
- Generic detailed files were preserved; no generic file was simplified.

Follow-up:
- None.

### 2026-05-25 — Milestone 1.2 continuation implementation (shop-scoped persistence)

Branch/PR/Issue:
- local milestone continuation update

Completed:
- Added `OrderRecord` and `OrderRepository` for persistence-backed `shop_id` scoping.
- Added `OrderService` that derives shop context server-side and ignores client-supplied `requested_shop_id`.
- Added regression tests for create/list/get scoping, cross-shop denial, and unauthenticated denial.
- Added continuation implementation report: `docs/ai/reports/milestone-1.2-continuation-report-2026-05-25.md`.
- Updated milestone completion checklist to reflect Milestone 1.2 acceptance criteria.

Checks run:
- `python -m pip install --upgrade pip` — warning (proxy/index retries)
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- Milestone 1.2 continuation slice closes the previously documented gap where scoping was helper-level only.

Follow-up:
- Perform milestone closeout/stabilisation pass and status transition when requested.
