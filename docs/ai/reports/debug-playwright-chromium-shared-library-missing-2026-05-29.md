# Debug Report: Playwright Chromium Launch Fails Missing `libatk-1.0.so.0`

Date: 2026-05-29  
Issue: local/Codespaces screenshot helper failure  
Status: complete

## Symptom
Running:

```bash
PYTHONPATH=src python scripts/capture_ui_screenshots.py
```

in Codespaces failed while launching Playwright Chromium. The user-provided traceback ended with `playwright._impl._errors.TargetClosedError: BrowserType.launch: Target page, context or browser has been closed`, and the browser stderr included:

```text
error while loading shared libraries: libatk-1.0.so.0: cannot open shared object file: No such file or directory
```

## Expected Behaviour
The screenshot helper should either:

- capture the seeded app-shell PNG screenshots when Playwright and its browser system dependencies are installed, or
- fail with actionable setup guidance when optional Playwright/browser dependencies are unavailable in the current environment.

## Reproduction
In the Codex cloud environment, I reproduced the optional-tooling failure path with:

```bash
PYTHONPATH=src python scripts/capture_ui_screenshots.py
```

Observed result in Codex cloud:

```text
Playwright is not installed in this Python environment. In Codespaces, run `python -m pip install playwright` and `python -m playwright install chromium`, then retry.
```

This environment does not currently have Playwright installed, so it cannot reproduce the exact Codespaces dynamic-linker error locally. The user-provided log is still sufficient to diagnose the Codespaces failure because Chromium process stderr names the missing shared object directly: `libatk-1.0.so.0`.

## Diagnostics Added
No temporary diagnostics were added.

Permanent, tested diagnostic messaging was added to `scripts/capture_ui_screenshots.py` so future launch failures explain that Chromium may be installed while required Linux shared libraries are missing, and point to Playwright's dependency installer command.

## Root Cause
The failing Codespaces environment has the Playwright Chromium browser package available, but Chromium cannot start because the Linux system library `libatk-1.0.so.0` is missing. That shared library is provided by OS-level browser dependencies, not by the Python `playwright` package alone.

The previous script only handled `ModuleNotFoundError` for missing Playwright. Once Playwright was installed but Chromium's native dependencies were incomplete, Playwright surfaced a low-level `TargetClosedError` with the browser stderr buried in the traceback.

## Fix
Implemented the smallest supportability fix:

- kept Playwright as optional local/Codespaces tooling rather than adding it to normal Codex-cloud test dependencies;
- added a dedicated Chromium launch-failure message that recommends:
  - `python -m playwright install-deps chromium`
  - `python -m playwright install chromium`
- wrapped `playwright.chromium.launch()` so native browser startup failures exit with actionable guidance instead of only the raw Playwright traceback;
- preserved the existing missing-Playwright guidance;
- adjusted script imports to satisfy the repository's `ruff` rules when linting `scripts/`.

## Regression Coverage
Added focused test coverage in `tests/test_ui_review_scripts.py` for the new browser dependency guidance message, including the user-reported `libatk-1.0.so.0` detail.

Existing coverage for the missing-Playwright guidance remains in place.

## Cleanup
- [x] Temporary logs removed
- [x] Scratch scripts removed
- [x] Commented experiments removed
- [x] Permanent diagnostics documented
- [x] No debug-only code remains

## Verification
Commands/checks run:

- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `PYTHONPATH=src python scripts/capture_ui_screenshots.py`
- `python -m compileall -q src tests scripts`
- `ruff check src tests scripts`
- `PYTHONDONTWRITEBYTECODE=1 pytest -q`

Result:

- Dependency installation completed using the already-available tooling in Codex cloud. `pip` reported package-index/proxy retry warnings for upgrade checks, but required packages were already installed.
- The screenshot script now provides a controlled missing-Playwright message in Codex cloud.
- Compile, lint, and the full test suite passed.

## Environment Limitations
Codex cloud does not have Playwright installed in this Python environment, so Codex could not execute the Chromium launch path or capture screenshots here. The exact Codespaces failure needs verification in Codespaces after installing native browser dependencies.

Exact Codespaces verification steps:

```bash
python -m pip install playwright
python -m playwright install-deps chromium
python -m playwright install chromium
PYTHONPATH=src python scripts/capture_ui_screenshots.py
```

If `install-deps` requires elevated package installation in a particular Codespace image, run the command in the Codespaces environment where OS package installation is allowed, or bake the Playwright dependency set into the devcontainer image.

## 2026-05-30 Follow-Up From Codespaces Re-Test
The user re-ran:

```bash
python -m pip install playwright
python -m playwright install chromium
PYTHONPATH=src python scripts/capture_ui_screenshots.py
```

and still received the `libatk-1.0.so.0` launch failure. That confirms the original diagnosis: Playwright's Python package and browser download are installed, but the Codespaces image is still missing OS-level browser libraries. The omitted command is:

```bash
python -m playwright install-deps chromium
```

The script guidance was refined so future failures do not echo the full Playwright browser log by default. It now extracts the missing shared library from the launch details, explicitly says that installing Python `playwright` plus Chromium is not enough when OS libraries are absent, and repeats the screenshot command to retry after installing deps.

## 2026-05-30 Final Setup Reliability Fix
Repository inspection found no checked-in `.devcontainer/devcontainer.json` or other Codespaces devcontainer setup file, so there is no repo-native devcontainer hook where this project can safely automate OS package installation during Codespace creation. The repo-native fix is therefore documentation plus a small optional local helper:

- `README.md` now lists the complete Codespaces/local Linux setup sequence, including the missing `python -m playwright install-deps chromium` step before `python -m playwright install chromium`.
- `scripts/setup_playwright_screenshots.py` now provides an optional one-command setup helper for screenshot tooling. It installs the Python `playwright` package, runs `python -m playwright install-deps chromium`, installs the Chromium browser binary, and prints the screenshot verification command.
- Playwright remains intentionally absent from `requirements.txt` and `requirements-dev.txt`, so normal runtime installs and Codex-cloud tests do not require browser tooling.
- `tests/test_ui_review_scripts.py` verifies that the optional helper keeps the expected command order and exposes the `install-deps` and screenshot retry commands without running the installers during tests.

Final Codespaces verification commands:

```bash
python -m pip install playwright
python -m playwright install-deps chromium
python -m playwright install chromium
PYTHONPATH=src python scripts/capture_ui_screenshots.py
```

Equivalent helper flow:

```bash
python scripts/setup_playwright_screenshots.py
PYTHONPATH=src python scripts/capture_ui_screenshots.py
```

Codex validation after the final setup fix:

- `python -m pip install --upgrade pip` — pass with package-index proxy retry warnings; existing pip remained usable.
- `pip install -r requirements.txt` — pass.
- `pip install -r requirements-dev.txt` — pass.
- `python -m compileall -q src tests scripts` — pass.
- `ruff check src tests scripts` — pass.
- `PYTHONDONTWRITEBYTECODE=1 pytest -q` — pass (`113 passed`).
- `PYTHONPATH=src python scripts/capture_ui_screenshots.py` — expected Codex-cloud optional-tooling limitation because Playwright is not installed; the script printed controlled setup guidance instead of a raw traceback.

## Follow-Up
Optional future work, not included in this fix:

- If a devcontainer is later added and screenshot capture becomes a standard Codespaces workflow, move the optional setup helper into a devcontainer `postCreateCommand` or documented manual setup step.
- Keep Milestone 9.2 screenshot evidence deferred unless a future scoped evidence task explicitly unlocks it.
