"""Capture PNG screenshots for the styled Pollen app shell with Playwright.

This script is optional for Codespaces/local visual review. It intentionally does
not make Playwright part of the normal Codex-cloud test install because browser
binaries are environment-specific.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from export_ui_review_pages import AUTH_HEADER, PAGES, seed_demo_data
from pollen.app import create_app


def _playwright_missing_message() -> str:
    return (
        "Playwright is not installed in this Python environment. "
        "In Codespaces, run `python -m pip install playwright` and "
        "`python -m playwright install chromium`, then retry."
    )


async def capture_screenshots(
    output_dir: Path,
    *,
    viewport_width: int,
    viewport_height: int,
) -> list[Path]:
    """Render seeded app-shell pages and capture them as PNG screenshots."""
    try:
        from playwright.async_api import async_playwright
    except ModuleNotFoundError as exc:  # pragma: no cover - depends on optional local tooling
        raise SystemExit(_playwright_missing_message()) from exc

    output_dir.mkdir(parents=True, exist_ok=True)
    app = create_app()
    seed_demo_data(app)
    written: list[Path] = []

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
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
