"""App shell and core helpers for the Pollen milestone slices."""

from __future__ import annotations

from dataclasses import dataclass

from pollen.auth import AuthService

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


PRIVATE_ROUTES: tuple[str, ...] = ("/", "/orders", "/products-stock", "/make-buy", "/money", "/settings")


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

    def __init__(self, auth_service: AuthService | None = None) -> None:
        self._routes = {url: title for title, url in NAV_ITEMS}
        self._auth_service = auth_service or AuthService()

    def get(self, path: str, *, authorization_header: str | None = None) -> AppResponse:
        if path in PRIVATE_ROUTES and self._auth_service.resolve_context(authorization_header) is None:
            return AppResponse(status_code=401, body="Unauthorized")

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
    """Create the app shell with milestone auth enforcement."""
    return AppShell()


def healthcheck() -> dict[str, str]:
    """Return a deterministic health payload for smoke tests."""
    return {"status": "ok", "service": "pollen"}


def can_access_shop_record(authorization_header: str | None, shop_id: str) -> bool:
    """Server-side ownership check helper for shop-scoped records."""
    return AuthService().can_access_shop(authorization_header, shop_id)
