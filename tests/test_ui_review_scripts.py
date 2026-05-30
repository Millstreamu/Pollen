import importlib.util
from pathlib import Path


def _load_script(script_name: str):
    script_path = Path(__file__).resolve().parents[1] / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(script_name.removesuffix(".py"), script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_export_ui_review_pages_writes_seeded_html(tmp_path: Path) -> None:
    module = _load_script("export_ui_review_pages.py")

    written = module.export_pages(tmp_path)

    assert [path.name for path in written] == [
        "today.html",
        "orders.html",
        "products-stock.html",
        "make-buy.html",
        "money.html",
        "settings.html",
    ]
    today_html = (tmp_path / "today.html").read_text(encoding="utf-8")
    assert "<style>" in today_html
    assert "Small seller workspace" in today_html
    assert "Review Buyer" not in today_html
    orders_html = (tmp_path / "orders.html").read_text(encoding="utf-8")
    assert "Review Buyer" in orders_html
    assert "Ready to pack" in orders_html


def test_capture_ui_screenshot_script_exposes_playwright_guidance() -> None:
    module = _load_script("capture_ui_screenshots.py")

    message = module._playwright_missing_message()

    assert "Playwright is not installed" in message
    assert "python -m pip install playwright" in message
    assert "python -m playwright install-deps chromium" in message
    assert "python -m playwright install chromium" in message


def test_capture_ui_screenshot_script_exposes_browser_dependency_guidance() -> None:
    module = _load_script("capture_ui_screenshots.py")

    message = module._playwright_launch_failure_message(
        "BrowserType.launch: Target page, context or browser has been closed\n"
        "Browser logs:\n"
        "[pid=14284][err] chrome-headless-shell: error while loading shared "
        "libraries: libatk-1.0.so.0: cannot open shared object file"
    )

    assert "required Linux browser dependencies are missing" in message
    assert "Detected missing shared library: libatk-1.0.so.0" in message
    assert "Installing the Python `playwright` package and the Chromium browser is not enough" in message
    assert "python -m playwright install-deps chromium" in message
    assert "PYTHONPATH=src python scripts/capture_ui_screenshots.py" in message
    assert "Browser logs:" not in message


def test_setup_playwright_screenshots_keeps_browser_deps_optional(capsys) -> None:
    module = _load_script("setup_playwright_screenshots.py")

    assert module.SETUP_COMMANDS[0][2:] == ("pip", "install", "playwright")
    assert module.SETUP_COMMANDS[1][2:] == ("playwright", "install-deps", "chromium")
    assert module.SETUP_COMMANDS[2][2:] == ("playwright", "install", "chromium")

    module.setup_playwright_screenshots(dry_run=True)

    output = capsys.readouterr().out
    assert "python -m playwright install-deps chromium" in output
    assert "PYTHONPATH=src python scripts/capture_ui_screenshots.py" in output
