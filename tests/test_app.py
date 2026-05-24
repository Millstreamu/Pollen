from pollen.app import NAV_ITEMS, create_app, healthcheck


def test_healthcheck_payload() -> None:
    assert healthcheck() == {"status": "ok", "service": "pollen"}


def test_placeholder_pages_load() -> None:
    app = create_app()

    for page_label, page_url in NAV_ITEMS:
        response = app.get(page_url)
        assert response.status_code == 200
        assert f"<h1>{page_label}</h1>" in response.body


def test_shell_contains_primary_navigation_links() -> None:
    app = create_app()
    response = app.get("/")

    for page_label, page_url in NAV_ITEMS:
        assert f'href="{page_url}"' in response.body
        assert page_label in response.body


def test_unknown_route_returns_not_found() -> None:
    response = create_app().get("/missing")
    assert response.status_code == 404
