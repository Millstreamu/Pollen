"""Install optional Playwright tooling needed for local UI screenshots.

This helper is intentionally separate from normal requirements files because
browser binaries and Linux system packages are local/Codespaces tooling, not
production/runtime dependencies for Pollen.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence

SETUP_COMMANDS: tuple[tuple[str, ...], ...] = (
    (sys.executable, "-m", "pip", "install", "playwright"),
    (sys.executable, "-m", "playwright", "install-deps", "chromium"),
    (sys.executable, "-m", "playwright", "install", "chromium"),
)

VERIFY_COMMAND = "PYTHONPATH=src python scripts/capture_ui_screenshots.py"


def _display_command(command: Sequence[str]) -> str:
    return " ".join("python" if part == sys.executable else part for part in command)


def setup_playwright_screenshots(*, dry_run: bool = False) -> None:
    """Install optional Playwright browser tooling for screenshot capture."""
    for command in SETUP_COMMANDS:
        print(f"$ {_display_command(command)}")
        if not dry_run:
            subprocess.run(command, check=True)

    print("\nScreenshot tooling setup complete.")
    print("Verify screenshot capture with:")
    print(f"$ {VERIFY_COMMAND}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install optional Playwright Chromium dependencies for Pollen UI screenshots."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the setup commands without installing packages or browser dependencies.",
    )
    args = parser.parse_args()

    setup_playwright_screenshots(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
