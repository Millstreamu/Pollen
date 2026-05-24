from pollen.app import NAV_ITEMS, can_access_shop_record, create_app, healthcheck
from pollen.auth import AuthService


def _auth_header(user_id: str = "u1", email: str = "maker@example.com") -> str:
    return f"Bearer user:{user_id}:{email}"


def test_healthcheck_payload() -> None:
    assert healthcheck() == {"status": "ok", "service": "pollen"}


def test_placeholder_pages_load() -> None:
    app = create_app()

    for page_label, page_url in NAV_ITEMS:
        response = app.get(page_url, authorization_header=_auth_header())
        assert response.status_code == 200
        assert f"<h1>{page_label}</h1>" in response.body


def test_shell_contains_primary_navigation_links() -> None:
    app = create_app()
    response = app.get("/", authorization_header=_auth_header())

    for page_label, page_url in NAV_ITEMS:
        assert f'href="{page_url}"' in response.body
        assert page_label in response.body


def test_unknown_route_returns_not_found() -> None:
    response = create_app().get("/missing")
    assert response.status_code == 404


def test_private_routes_require_login() -> None:
    for _, page_url in NAV_ITEMS:
        response = create_app().get(page_url)
        assert response.status_code == 401


def test_logged_in_user_gets_or_creates_shop_context() -> None:
    auth_service = AuthService()
    context = auth_service.resolve_context(_auth_header("first-user", "first@example.com"))
    assert context is not None
    assert context.user.user_id == "first-user"
    assert context.shop.shop_id == "shop-first-user"


def test_user_cannot_access_another_shop_records() -> None:
    owner_header = _auth_header("owner", "owner@example.com")
    other_header = _auth_header("other", "other@example.com")

    auth_service = AuthService()
    owner_context = auth_service.resolve_context(owner_header)
    assert owner_context is not None

    assert auth_service.can_access_shop(owner_header, owner_context.shop.shop_id)
    assert not auth_service.can_access_shop(other_header, owner_context.shop.shop_id)


def test_server_ownership_check_helper_denies_cross_shop() -> None:
    header = _auth_header("u2", "u2@example.com")
    assert not can_access_shop_record(header, "shop-someone-else")
