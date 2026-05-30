"""Capture PNG screenshots for the styled Pollen app shell with Playwright.

This script is optional for Codespaces/local visual review. It intentionally does
not make Playwright part of the normal Codex-cloud test install because browser
binaries are environment-specific.
"""

from __future__ import annotations

import argparse
import asyncio
import importlib
import importlib.util
import re
import sys
from pathlib import Path
from typing import Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

_ui_review_pages = importlib.import_module("export_ui_review_pages")
AUTH_HEADER = _ui_review_pages.AUTH_HEADER
PAGES = _ui_review_pages.PAGES
seed_demo_data = _ui_review_pages.seed_demo_data
create_app = importlib.import_module("pollen.app").create_app


def _playwright_missing_message() -> str:
    return (
        "Playwright is not installed in this Python environment. "
        "In Codespaces/Linux, run `python -m pip install playwright`, "
        "`python -m playwright install-deps chromium`, and "
        "`python -m playwright install chromium`, then retry."
    )


def _first_non_empty_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return "unknown launch error"


def _missing_shared_library(details: str) -> str | None:
    match = re.search(r"error while loading shared libraries: ([^:]+):", details)
    if match is None:
        return None
    return match.group(1)


def _playwright_launch_failure_message(details: str) -> str:
    missing_library = _missing_shared_library(details)
    missing_library_sentence = (
        f" Detected missing shared library: {missing_library}." if missing_library else ""
    )

    return (
        "Playwright Chromium could not launch because required Linux browser "
        "dependencies are missing."
        f"{missing_library_sentence} "
        "Installing the Python `playwright` package and the Chromium browser is not enough "
        "when OS-level libraries are absent. In Codespaces/Linux, run "
        "`python -m playwright install-deps chromium`, then "
        "`python -m playwright install chromium`, then retry "
        "`PYTHONPATH=src python scripts/capture_ui_screenshots.py`. "
        f"Playwright error summary: {_first_non_empty_line(details)}"
    )


def _load_async_playwright():
    try:
        playwright_spec = importlib.util.find_spec("playwright.async_api")
    except ModuleNotFoundError as exc:  # pragma: no cover - optional local tooling
        raise SystemExit(_playwright_missing_message()) from exc

    if playwright_spec is None:  # pragma: no cover - optional local tooling
        raise SystemExit(_playwright_missing_message())

    return importlib.import_module("playwright.async_api").async_playwright


async def capture_screenshots(
    output_dir: Path,
    *,
    viewport_width: int,
    viewport_height: int,
) -> list[Path]:
    """Render seeded app-shell pages and capture them as PNG screenshots."""
    async_playwright = _load_async_playwright()

    output_dir.mkdir(parents=True, exist_ok=True)
    app = create_app()
    seed_demo_data(app)
    written: list[Path] = []

    async with async_playwright() as playwright:
        try:
            browser = await playwright.chromium.launch()
        except Exception as exc:  # pragma: no cover - depends on optional browser tooling
            raise SystemExit(_playwright_launch_failure_message(str(exc))) from exc

        page = await browser.new_page(viewport={"width": viewport_width, "height": viewport_height})
        for slug, route in PAGES:
            response = app.get(route, authorization_header=AUTH_HEADER)
            path = output_dir / f"{slug}.png"
            await page.set_content(response.body, wait_until="networkidle")
            await page.screenshot(path=path, full_page=True)
            written.append(path)
        await browser.close()

    return written


def format_paths(paths: Iterable[Path]) -> str:
    return "\n".join(f"- {path}" for path in paths)


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture Pollen app-shell screenshots with Playwright.")
    parser.add_argument("--output-dir", default="docs/ai/ui-screenshots", help="Directory for PNG screenshots.")
    parser.add_argument("--viewport-width", type=int, default=1440)
    parser.add_argument("--viewport-height", type=int, default=1000)
    args = parser.parse_args()

    written = asyncio.run(
        capture_screenshots(
            Path(args.output_dir),
            viewport_width=args.viewport_width,
            viewport_height=args.viewport_height,
        )
    )
    print("Captured UI screenshots:")
    print(format_paths(written))


if __name__ == "__main__":
    main()
