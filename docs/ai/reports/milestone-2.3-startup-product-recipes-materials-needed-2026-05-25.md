# Startup Report — Milestone 2.3 Product Recipes / Materials Needed (2026-05-25)

## Task understanding
Start Milestone 2.3 by documenting the implementation-start decision and initial execution plan for Product Recipes / Materials Needed.

## Inputs reviewed
- `project-roadmap.md` (Products & Stock scope)
- `docs/ai/completion-status.md`
- `docs/ai/progress-log.md`
- Existing Milestone 2.2 reports for continuity

## Milestone 2.3 objective (initial)
Enable product recipe definitions and materials-needed visibility so the seller can see what inputs are required to make products and how far current material stock can support production.

## Initial deliverable slices
1. Product recipe model/service support (product ↔ material usage definitions).
2. CRUD endpoints/UI flows for recipe rows.
3. Materials-needed computation per product quantity/batch intent.
4. Tests for recipe persistence, validation, and materials-needed calculations.

## Verification plan for implementation slices
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Status after this report
- Milestone 2.3 is now active (`in-progress`) pending implementation slices.
