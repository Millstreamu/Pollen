# UI Data and Controls Repair Report — 2026-06-01

## Scope

Assess and repair the post-render UI refresh where screenshot reference data was copied into the app as if it were real product, order, purchase, settings, and money data, and where several visible dashboard buttons were decorative instead of connected to an existing workflow.

## AI Method Applied

1. **Spec:** Preserve the visual template direction from the reference images while removing fabricated screenshot records and restoring real shop-scoped data behavior.
2. **Scan:** Read the AI development rules, UI rules, latest UI render report, app shell, services, repositories, scripts, and UI/journey tests.
3. **Simplify:** Reused existing in-memory services and legacy forms instead of adding new models, mock seed records, JavaScript, or integrations.
4. **Slice:** Focused on one vertical repair: dashboard data sources and visible controls across Today, Orders, Products & Stock, Make / Buy, Money, and Settings.
5. **Verify:** Installed dependencies, ran lint, bytecode compile, and the full pytest suite.
6. **Clean:** Removed the copied screenshot examples from runtime rendering and added regression tests to prevent the same issue from returning.

## Assessment Findings

- The refreshed dashboards used the reference images as exact content instead of as visual templates. Examples included hardcoded customers, fake products, fake purchases, fake suppliers, dated transactions, and a fixed shop/account identity.
- Several visible controls were plain buttons without a submit action or destination, so users could see actions such as adding products, planning batches, importing orders, or editing settings without a functional path.
- Some existing workflow forms were present only in hidden compatibility sections. This kept tests passing but did not provide a usable path from the new visible dashboard controls.
- A duplicate `adjust_stock` branch in the Products & Stock POST handler made product stock adjustment unreachable because the earlier material-stock branch captured the same action.

## Implementation Summary

- Replaced copied screenshot data with live shop-scoped records from existing services for Today, Orders, Products & Stock, Make / Buy, Money, and Settings.
- Converted decorative controls into working anchors or POST forms that route to existing workflows and visible workflow panels.
- Made account and shop display come from the authenticated context instead of hardcoded screenshot identity values.
- Exposed the existing product and make/buy workflow forms in visible dashboard panels so controls have clear destinations.
- Fixed the Products & Stock `adjust_stock` handler so product stock adjustment reaches the product service branch.
- Added regression tests that reject known screenshot/demo data and assert primary dashboard controls connect to real destinations.

## Validation Summary

### Dependencies installed

- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`

The pip upgrade command reported network mirror `403 Forbidden` retry warnings, but required packages were already present and dependency validation completed.

### Commands run

- `python -m pip install --upgrade pip && pip install -r requirements.txt && pip install -r requirements-dev.txt`
- `python -m py_compile src/pollen/app.py`
- `PYTHONPATH=src ruff check . && PYTHONPATH=src pytest -q`

### Test result

- Full test suite passed: `116 passed`.
- Ruff passed: `All checks passed!`.
- Bytecode compilation passed.

## Remaining Work

- Optional follow-up: replace hash-link workflow jumps with richer server-side filtered views or dedicated forms once the app has a more mature routing layer.
- Optional follow-up: add browser screenshot capture in an environment with Playwright installed to visually compare the repaired template-based UI against the reference direction.
