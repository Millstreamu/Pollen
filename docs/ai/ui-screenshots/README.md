# UI screenshots for Codex review

Generated Playwright screenshots may be committed here after human review so future Codex runs can inspect the current UI state from the main branch.

Before committing screenshots:

- verify they were generated from seeded/demo data only;
- confirm they do not expose secrets, tokens, private customer data, or other sensitive information;
- regenerate them with `PYTHONPATH=src python scripts/capture_ui_screenshots.py` when the app shell changes.
