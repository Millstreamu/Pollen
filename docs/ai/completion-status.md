# Completion Status

Tracks the current milestone/release finish line to prevent endless asymptotic development.

## Current Milestone
Name: Milestone 10.3 — V1 Release
Status: complete

Allowed statuses: `not-started`, `in-progress`, `stabilising`, `release-candidate`, `complete`, `blocked`.

## Required Scope Checklist
- [x] Confirm Milestone 10.2 completion closeout evidence exists.
- [x] Inspect Milestone 10.3 V1 Release acceptance criteria.
- [x] Confirm manual core workflow evidence remains present.
- [x] Confirm stock-changing action traceability evidence remains present.
- [x] Confirm core journey tests pass in Codex cloud.
- [x] Confirm auth/shop ownership evidence remains safe enough for MVP.
- [x] Reconcile known critical blockers and optional backlog sources.
- [x] Run full Codex-cloud validation sequence.
- [x] Add bounded V1 release-decision report evidence.
- [x] Declare V1 complete.

## V1 Release Criteria
V1 is complete because:
- [x] Manual core workflows work, as covered by the Milestone 10.1 journey and fresh full-suite validation.
- [x] Stock-changing actions are traceable through inventory movement and activity log records.
- [x] Core journeys pass.
- [x] Auth/shop ownership is safe enough for MVP through server-resolved shop context and cross-shop denial tests.
- [x] No known critical blockers remain.
- [x] Optional improvements are moved to backlog/deferred notes.
- [x] Release summary exists in `docs/ai/reports/milestone-10.3-v1-release-decision-report-2026-05-29.md`.

## Required Verification Checklist
- [x] Install runtime dependencies
- [x] Install dev dependencies or document environment limitation
- [x] Typecheck *(Python compile check used in current repo flow)*
- [x] Lint *(configured via `ruff check src tests`)*
- [x] Unit tests
- [x] Relevant service/integration tests
- [x] Journey tests
- [x] Build *(compile check: `python -m compileall -q src tests`)*
- [x] Environment-specific checks or exceptions documented
- [x] V1 release decision report recorded

## Remaining Required Work
None for V1.

## Optional Post-Milestone Work
- Milestone 9.2 optional screenshot evidence may still be done later if desired.
- Future post-V1 improvements should be explicitly scoped before implementation.

## Current Post-V1 Task
Name: Workshop recipe material assignment workflow
Status: complete
Evidence: `docs/ai/progress-log.md` entry dated 2026-06-02

Completed result:
- Workshop now supports assigning existing materials to a product recipe through a focused Set Up Recipe modal.
- Saved products show Recipe needed when no materials are assigned and Recipe ready when at least one material requirement is saved.
- Recipe rows capture material, quantity per unit, and material unit context, and saved rows can be removed through the same recipe workflow.
- Workshop still includes the completed Create Material modal, Workshop Materials list, Create Product modal, and Products You Make list from prior post-V1 milestones.
- Batch planning and batch completion are not implemented in this milestone and remain future scoped work.

## Current Blockers
None recorded.

## Next Required Milestone
None. V1 is complete; the Workshop material creation, product creation, and recipe material assignment milestones are complete. Select a separate scoped post-V1 task before implementing batch planning or batch completion.

## Deferred / Do Not Build
See `docs/ai/do-not-build-yet.md`.
