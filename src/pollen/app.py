"""App shell and core helpers for the Pollen milestone slices."""

from __future__ import annotations

from dataclasses import dataclass

NAV_ITEMS: tuple[tuple[str, str], ...] = (
    ("Today", "/"),
    ("Orders", "/orders"),
    ("Products & Stock", "/products-stock"),
    ("Make / Buy", "/make-buy"),
    ("Money", "/money"),
    ("Settings", "/settings"),
)


@dataclass(frozen=True)
class AppResponse:
    status_code: int
    body: str


class AppShell:
    """Minimal app-shell router for placeholder milestone pages."""

    _DESCRIPTIONS = {
        "Today": "Your daily overview will appear here.",
        "Orders": "Order workflow tools will appear here.",
        "Products & Stock": "Product and stock tools will appear here.",
        "Make / Buy": "Make and buy planning will appear here.",
        "Money": "Estimated money snapshots will appear here.",
        "Settings": "Shop settings and preferences will appear here.",
    }

    def __init__(self) -> None:
        self._routes = {url: title for title, url in NAV_ITEMS}

    def get(self, path: str) -> AppResponse:
        page_title = self._routes.get(path)
        if page_title is None:
            return AppResponse(status_code=404, body="Not Found")

        return AppResponse(status_code=200, body=self.render_page(page_title))

    def render_page(self, page_title: str) -> str:
        nav_links = "".join(
            f'<li><a href="{href}">{label}</a></li>' for label, href in NAV_ITEMS
        )
        page_description = self._DESCRIPTIONS[page_title]

        return (
            "<!doctype html>"
            "<html lang='en'>"
            "<head>"
            "<meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>{page_title} · Pollen</title>"
            "</head>"
            "<body>"
            "<header>"
            "<div><strong>Pollen</strong><p>Simple shop operating system</p></div>"
            "<nav aria-label='Primary'><ul>"
            f"{nav_links}"
            "</ul></nav>"
            "</header>"
            f"<main><h1>{page_title}</h1><p>{page_description}</p></main>"
            "</body>"
            "</html>"
        )


def create_app() -> AppShell:
    """Create the Milestone 1.1 app shell."""
    return AppShell()


def healthcheck() -> dict[str, str]:
    """Return a deterministic health payload for smoke tests."""
    return {"status": "ok", "service": "pollen"}
