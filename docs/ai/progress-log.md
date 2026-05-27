# Progress Log

Records meaningful completed work. Update after feature completion, bug fix completion, milestone completion, release verification, important decision, or server-run evidence that changes status.

## Current Status
Project phase: Phase 1 — App Foundation  
Current milestone: Milestone 3.3 — Pack and Ship Workflow (in-progress)  
Overall status: Milestone 3.2 is complete after release validation/sign-off; Milestone 3.3 is now active.

## Latest Summary
Milestone 3.2 was released as complete on 2026-05-27; next execution focus shifts to Milestone 3.3 startup.

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



### 2026-05-27 — Milestone 3.3 startup planning + scope lock report

Branch/PR/Issue:
- local Milestone 3.3 planning/reporting update

Completed:
- Executed Milestone 3.3 startup planning and locked in-scope vs out-of-scope boundaries from roadmap criteria.
- Captured durable planning evidence report for first vertical slice execution.
- Advanced next-task brief from startup planning into first vertical-slice implementation instructions.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass (`58 passed`)

Notes:
- This slice is planning/scope-lock/reporting only; no runtime behavior changes were introduced.

Follow-up:
- Implement Milestone 3.3 first vertical slice (pack transition, ship transition, reservation finalization safety, and activity log coverage).


### 2026-05-27 — Milestone 3.2 release validation + completion sign-off

Branch/PR/Issue:
- local milestone release closeout update

Completed:
- Executed release-flow validation commands for Milestone 3.2 in Codex cloud.
- Confirmed compile and full test suite pass (`58 passed`).
- Finalized release decision and transitioned Milestone 3.2 from `stabilising` to `complete`.
- Advanced next-task brief to Milestone 3.3 startup.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass (`58 passed`)

Notes:
- Dev dependency fetch for pinned `pytest==8.4.2` is still restricted by this environment proxy/index, but installed tooling was sufficient to run the full suite successfully.

Follow-up:
- Start Milestone 3.3 implementation slices (Pack and Ship Workflow).

### 2026-05-27 — Milestone 3.2 stabilising transition + validation evidence

Branch/PR/Issue:
- local milestone status/release-flow update

Completed:
- Reconciled milestone tracking to reflect Milestone 3.2 implementation completion and moved status to `stabilising`.
- Updated next-task brief to Milestone 3.2 release-flow execution.
- Captured current validation evidence for compile and tests in Codex cloud.

Checks run:
- `python -m pip install --upgrade pip` — pass (with proxy/index retry warnings)
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (`pytest==8.4.2` not fetchable from index/proxy)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass (`58 passed`)

Notes:
- Dev dependency installation remains partially blocked by index/proxy restrictions, but required test execution succeeded using available environment packages.

Follow-up:
- Run Milestone 3.2 release-candidate validation/sign-off and transition to `release-candidate`.

### 2026-05-26 — Milestone 3.1 project-memory reconciliation + execution report

Branch/PR/Issue:
- local milestone status/reporting sync update

Completed:
- Reconciled milestone tracking mismatch by switching completion tracking to Milestone 3.1 (`in-progress`).
- Updated current status and summary in progress log to align with the active milestone execution flow.
- Added a Milestone 3.1 reconciliation/execution report documenting scope, commands, and outcomes.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass (`55 passed`)

Notes:
- This slice focused on project-memory/status reconciliation and durable reporting while continuing Milestone 3.1 execution under the AI development method.

Follow-up:
- Continue Milestone 3.1 through stabilising/release-candidate/complete status flow after next requested implementation or validation slice.

### 2026-05-26 — Milestone 2.4 completion release decision + closeout

Branch/PR/Issue:
- local milestone completion closeout update

Completed:
- Recorded final release decision for Milestone 2.4 after release-candidate validation evidence.
- Transitioned Milestone 2.4 status from `release-candidate` to `complete`.
- Updated project progress summary to reflect milestone completion.

Checks run:
- `python -m pip install --upgrade pip` — pass (with index retry warnings)
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass (`52 passed`)

Notes:
- Dev dependency fetch for `pytest==8.4.2` remains blocked by package index/proxy restrictions in this environment, but `pytest` is already available and the full suite passed.

Follow-up:
- Start Phase 3 planning/implementation beginning with Milestone 3.1 (Manual Order Creation).



### 2026-05-26 — Milestone 2.4 release-candidate validation + sign-off

Branch/PR/Issue:
- local milestone release-candidate sign-off update

Completed:
- Executed Milestone 2.4 release-candidate validation pass in current environment.
- Confirmed compile check and full test suite pass with no regressions (`52 passed`).
- Transitioned Milestone 2.4 status from `stabilising` to `release-candidate`.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass (`52 passed`)

Notes:
- This slice is release-validation/sign-off tracking only; no runtime behavior changes were introduced.

Follow-up:
- Perform final release decision and move Milestone 2.4 to `complete` when requested.


### 2026-05-26 — Milestone 2.4 reconciliation + stabilising status transition

Branch/PR/Issue:
- local milestone status/reporting reconciliation update

Completed:
- Reconciled milestone tracking files with existing Milestone 2.4 implementation evidence.
- Updated completion checklist and verification status for Milestone 2.4.
- Transitioned Milestone 2.4 status from `in-progress` to `stabilising`.
- Added reconciliation report documenting AI development method structure and validation evidence.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass (`52 passed`)

Notes:
- This slice is project-memory/status reconciliation only; no runtime behavior changes were introduced.

Follow-up:
- Run Milestone 2.4 release-candidate validation/sign-off flow and transition status to `release-candidate` when requested.


### 2026-05-25 — Milestone 2.3 completion sign-off + Milestone 2.4 startup planning

Branch/PR/Issue:
- local milestone status/reporting update

Completed:
- Recorded human sign-off and marked Milestone 2.3 complete in completion tracking.
- Transitioned active milestone to Milestone 2.4 (`in-progress`).
- Added Milestone 2.4 startup planning report using AI development process structure.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- This slice is status transition and planning only; Milestone 2.4 feature implementation is not started in this change set.

Follow-up:
- Implement Milestone 2.4 vertical slices (stock adjustment + reason + movement/activity logs + tests).


### 2026-05-25 — Milestone 2.3 release-candidate validation + sign-off

Branch/PR/Issue:
- local milestone status/reporting update

Completed:
- Executed Milestone 2.3 release-candidate validation pass and confirmed compile/tests are green.
- Recorded release-candidate validation/sign-off report for Milestone 2.3.
- Transitioned Milestone 2.3 status from `stabilising` to `release-candidate`.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- This slice is release validation and tracking; no functional app behavior changes were introduced.

Follow-up:
- Perform final milestone completion/release decision when requested.



### 2026-05-25 — Milestone 2.2 sign-off complete + Milestone 2.3 startup

Branch/PR/Issue:
- local milestone status/reporting update

Completed:
- Finalized Milestone 2.2 release decision as approved and recorded sign-off report.
- Transitioned milestone tracking from Milestone 2.2 (`release-candidate`) to Milestone 2.2 complete.
- Started Milestone 2.3 and added startup report for Product Recipes / Materials Needed.
- Updated current-status header to active Milestone 2.3.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- This slice is reporting/state transition only; no app behavior changes yet.

Follow-up:
- Implement Milestone 2.3 recipe model/service/UI slices and add journey-level coverage.


### 2026-05-25 — Milestone 2.2 release-candidate validation pass

Branch/PR/Issue:
- local milestone closeout update

Completed:
- Executed Milestone 2.2 release-candidate validation pass in current environment.
- Confirmed compile and full test suite pass with no regressions (`44 passed`).
- Transitioned Milestone 2.2 status from `stabilising` to `release-candidate`.

Checks run:
- `python -m pip install --upgrade pip` — pass (with index retry warnings)
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- Dev dependency install remains blocked by package index/proxy restrictions in this environment, but `pytest` is available and full suite passed.

Follow-up:
- Proceed to final sign-off/release decision for Milestone 2.2.


### 2026-05-25 — Milestone 2.2 closeout reconciliation + stabilising transition

Branch/PR/Issue:
- local milestone closeout update

Completed:
- Added Milestone 2.2 closeout report and reconciled completion tracking with implementation evidence.
- Updated `docs/ai/completion-status.md` scope checklist to complete for Materials CRUD acceptance criteria.
- Transitioned Milestone 2.2 status from `in-progress` to `stabilising`.
- Updated progress-log current status header to the active milestone.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- Closeout work in this slice is status/evidence reconciliation only; no new feature behavior was introduced.

Follow-up:
- Run final release-candidate pass for Milestone 2.2 and transition to `release-candidate` when requested.



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

### 2026-05-25 — Milestone 2.1 UI product page slice

Branch/PR/Issue:
- local milestone UI slice update

Completed:
- Replaced `/products-stock` placeholder content with a simple products table powered by existing `ProductService`.
- Added empty-state message when no products are present.
- Added UI tests covering empty and populated product page rendering, including low-stock status display.
- Added startup and implementation reports for this UI slice.

Checks run:
- `python -m pip install --upgrade pip` — pass (with proxy retry warnings)
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- Existing environment already had usable pytest installation; full test suite passed.

Follow-up:
- Implement create/edit/archive product UI flows in later Milestone 2.1 slices.

### 2026-05-25 — Milestone 2.1 continuation (row-level product edit controls)

Branch/PR/Issue:
- local milestone UI continuation update

Completed:
- Added explicit edit form controls per product row on `/products-stock`.
- Added UX polish for product forms (required fields and non-negative number inputs).
- Updated edit handling to support partial row updates without clobbering unchanged values.
- Added and updated UI tests for edit control rendering and row-level partial edit behavior.
- Added implementation report: `docs/ai/reports/milestone-2.1-ui-row-edit-report-2026-05-25.md`.

Checks run:
- `python -m pip install --upgrade pip` — pass (with proxy retry warnings)
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- Existing environment already contained runnable `pytest`; full suite passed after changes.

Follow-up:
- Continue Milestone 2.1 remaining UI polish/screen slices as requested.


### 2026-05-25 — Milestone 1.2 release-candidate validation + Milestone 2.1 archived-product restore UI slice

Branch/PR/Issue:
- local validation + UI continuation update

Completed:
- Ran clean validation pass and promoted Milestone 1.2 status from `stabilising` to `release-candidate`.
- Implemented next Milestone 2.1 UI slice: archived-products section and restore action in Products & Stock UI.
- Added service/repository restore path and test coverage for product restore workflow and archived-section rendering.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass

### 2026-05-25 — Milestone 2.1 continuation (bulk action UI slice)

Branch/PR/Issue:
- local milestone UI continuation update

Completed:
- Added bulk archive and bulk restore action handling to the `/products-stock` POST flow.
- Added Products UI bulk-actions panel (comma-separated product ID input) and select-column polish in active/archived tables.
- Added tests for bulk action behavior and bulk-control rendering.
- Added implementation report: `docs/ai/reports/milestone-2.1-ui-bulk-actions-report-2026-05-25.md`.

Checks run:
- `python -m pip install --upgrade pip` — pass (with proxy retry warnings)
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- Existing environment already contained runnable `pytest`; full suite passed after changes.

Follow-up:
- Continue Milestone 2.1 remaining UI slices (detail-page polish and other CRUD refinements) as requested.
- `pytest -q` — pass

Notes:
- Existing environment already had runnable `pytest`; full suite passed after code changes.

Follow-up:
- Continue remaining Milestone 2.1 UI polish/slices (filters, bulk actions, or richer status chips) as requested.


### 2026-05-25 — Milestone 2.1 continuation (filters + status chips UI slice)

Branch/PR/Issue:
- local milestone UI continuation update

Completed:
- Added `/products-stock` view filters for active, archived, and all product views.
- Added clearer status indicators (`✅ Healthy`, `⚠️ Low stock`) in product rows.
- Updated route parsing to support query-string UI filtering.
- Added tests for filters and status-chip rendering; aligned archive/restore UI tests with new default active view.
- Added implementation report: `docs/ai/reports/milestone-2.1-ui-filters-status-report-2026-05-25.md`.

Checks run:
- `python -m pip install --upgrade pip` — pass (with proxy retry warnings)
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- Existing environment already had runnable `pytest`; full suite passed after changes.

Follow-up:
- Continue Milestone 2.1 remaining UI slices (bulk actions or detail-page polish) as requested.

### 2026-05-25 — Milestone 2.1 completion (product detail flow polish)

Branch/PR/Issue:
- local milestone completion update

Completed:
- Implemented polished product detail flow with explicit row view/edit states.
- Kept stock and reorder values visible in default row view.
- Added inline all-field edit mode with save/cancel affordances.
- Added regression test coverage for detail edit mode field visibility.
- Added implementation report: `docs/ai/reports/milestone-2.1-product-detail-flow-report-2026-05-25.md`.

Checks run:
- `python -m pip install --upgrade pip` — pass (with proxy retry warnings)
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- Dev dependency install remains constrained by environment package-index access, but compile + full tests pass.

Follow-up:
- Begin Milestone 2.2 when requested.



### 2026-05-25 — Milestone 2.2 startup (materials CRUD planning)

Branch/PR/Issue:
- local milestone startup update

Completed:
- Began Milestone 2.2 per roadmap scope (`Materials CRUD`).
- Added startup implementation report: `docs/ai/reports/milestone-2.2-startup-report-2026-05-25.md`.
- Updated completion tracking to set current milestone to `Milestone 2.2 — Materials CRUD` (`in-progress`).

Checks run:
- `python -m pip install --upgrade pip` — pass (with proxy retry warnings)
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- This task intentionally starts the milestone and captures implementation plan/risk/scope; feature code slice follows in subsequent work.

Follow-up:
- Implement the first Milestone 2.2 vertical slice (materials list + create/edit baseline + tests).

### 2026-05-25 — Milestone 2.2 slice 1 (materials list + create/edit baseline)

Branch/PR/Issue:
- local milestone 2.2 implementation update

Completed:
- Added `MaterialRecord` and `MaterialRepository` for shop-scoped material persistence.
- Added `MaterialService` create/list/get/update operations with server-side ownership scoping.
- Added Make/Buy materials page vertical slice with empty state, create form, list table, query edit mode, and low-stock status chips.
- Added tests for materials service behaviors and Make/Buy UI create/edit interactions.
- Added implementation report: `docs/ai/reports/milestone-2.2-materials-slice-1-report-2026-05-25.md`.

Checks run:
- `python -m pip install --upgrade pip` — pass (with proxy retry warnings)
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- Environment cannot fetch pinned dev dependency from package index, but existing environment has runnable pytest and full suite passed.

Follow-up:
- Continue Milestone 2.2 with archive/deactivate + restore behavior and tests.

### 2026-05-25 — Milestone 2.2 slice 2 (materials archive/deactivate + restore)

Branch/PR/Issue:
- local milestone 2.2 implementation update

Completed:
- Added material repository archive/restore operations and service-level wrappers with shop scoping.
- Extended Make/Buy UI materials flow with archive and restore post actions.
- Added material filter views (`active`, `archived`, `all`) and archived materials restore section.
- Added tests for material archive/restore behavior across service and app UI layers.
- Added implementation report: `docs/ai/reports/milestone-2.2-materials-archive-restore-report-2026-05-25.md`.

Checks run:
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt` *(environment-limited: proxy/index restriction for `pytest==8.4.2`)*
- `python -m compileall -q src tests`
- `pytest -q`

Notes:
- Full validation suite for this slice passed in this environment.

Follow-up:
- Continue Milestone 2.2 with any remaining UX polish and additional edge-case tests as needed.

### 2026-05-25 — Milestone 2.2 UX polish + edge-case test hardening

Branch/PR/Issue:
- local milestone 2.2 implementation update

Completed:
- Added materials/products filter-view UX fallback so invalid `view` values default to active content.
- Added app-level edge-case tests for material invalid-view fallback and unknown-ID edit safety.
- Added implementation report: `docs/ai/reports/milestone-2.2-ux-polish-edge-tests-report-2026-05-25.md`.

Checks run:
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt` (environment-limited by package index/proxy)
- `python -m compileall -q src tests`
- `pytest -q`

Notes:
- Dev dependency install remains constrained by environment package index access for pinned `pytest==8.4.2`; compile and full test suite passed with preinstalled tooling.

Follow-up:
- Milestone 2.2 appears functionally complete for scoped CRUD/UX acceptance criteria.


### 2026-05-25 — Milestone 2.3 continuation (can-make service/UI + journey expansion)

Branch/PR/Issue:
- local milestone 2.3 continuation update

Completed:
- Added `RecipeService.can_make_quantity` and integrated bottleneck-based recipe capacity calculation.
- Updated recipe UI rendering to show per-product “Can make now” and to respect planned quantity query for materials-needed output.
- Added recipe service regression tests for limiting-material can-make behavior and non-mutating stock behavior.
- Expanded Milestone 2.3 journey test to assert can-make visibility and planned-quantity materials-needed output.
- Updated milestone implementation report for this continuation slice.

Checks run:
- `python -m pip install --upgrade pip` — pass (with proxy retry warnings)
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- Dev dependency install remains constrained by package-index access in this environment; existing installed pytest executed full suite successfully.

Follow-up:
- Continue Milestone 2.3 remaining polish/edge cases if requested, then transition milestone status when ready.


### 2026-05-25 — Milestone 2.3 polish edge cases + stabilising transition

Branch/PR/Issue:
- local milestone 2.3 continuation

Completed:
- Added recipe edge-case test coverage ensuring archived materials are excluded from materials-needed and can-make calculations.
- Recorded Milestone 2.3 polish report and validation evidence.
- Transitioned Milestone 2.3 status from `in-progress` to `stabilising`.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass

Notes:
- Environment dependency install limitation persists, but full compile and test validation passed with existing toolchain.

Follow-up:
- Run Milestone 2.3 release-candidate pass and sign-off when requested.


### 2026-05-27 — Milestone 3.2 stock reservation implementation

Branch/PR/Issue:
- local milestone implementation update

Completed:
- Added reservation-aware product stock fields (`reserved_stock`, `available_stock`).
- Implemented reservation behavior during manual order creation when stock is available.
- Preserved no-overallocation behavior by marking insufficient stock orders as `waiting_on_stock` without reservation changes.
- Added Milestone 3.2 tests covering reservation and available-stock calculations.
- Added milestone implementation report for durable evidence.

Checks run:
- `python -m pip install --upgrade pip` — pass
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass (`58 passed`)

Notes:
- Reservation release and shipping finalization remain out of scope for this milestone and are deferred to Milestone 3.3/3.4.

Follow-up:
- Advance Milestone 3.2 through stabilising/release-candidate/complete flow when requested.


### 2026-05-27 — Milestone 3.3 pack/ship first vertical slice implementation

Branch/PR/Issue:
- local Milestone 3.3 implementation slice

Completed:
- Implemented guarded pack and ship transitions for orders.
- Added shipping reservation finalization logic that prevents double-deduct by blocking invalid repeat ship transition.
- Added activity log coverage for pack/ship order transitions.
- Added Orders UI actions for Pack/Ship with invalid-transition error feedback.
- Added Milestone 3.3 tests for valid transitions, invalid transitions, and no-double-deduct safety.

Checks run:
- `python -m pip install --upgrade pip` — pass (with proxy retry warnings)
- `pip install -r requirements.txt` — pass
- `pip install -r requirements-dev.txt` — environment-limited (proxy/index restriction for `pytest==8.4.2`)
- `python -m compileall -q src tests` — pass
- `pytest -q` — pass (`61 passed`)

Notes:
- Environment still cannot fetch pinned `pytest==8.4.2` from configured index/proxy, but existing environment pytest allowed full suite execution.

Follow-up:
- Continue Milestone 3.3 with any remaining UX polish and completion-status synchronization decisions.
