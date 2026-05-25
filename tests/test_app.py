from pollen.app import AppShell, NAV_ITEMS, can_access_shop_record, create_app, healthcheck
from pollen.services import ProductService
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


def test_products_page_shows_empty_state_when_no_products() -> None:
    app = create_app()

    response = app.get("/products-stock", authorization_header=_auth_header())

    assert response.status_code == 200
    assert "No products yet. Add your first product to start tracking stock." in response.body


def test_products_page_renders_product_table_and_low_stock_status() -> None:
    header = _auth_header("owner", "owner@example.com")
    product_service = ProductService()
    product_service.create_product(
        authorization_header=header,
        name="Healthy Candle",
        sku="CNDL-HEALTHY",
        stock_on_hand=8,
        reorder_point=3,
    )
    product_service.create_product(
        authorization_header=header,
        name="Low Candle",
        sku="CNDL-LOW",
        stock_on_hand=2,
        reorder_point=3,
    )

    app = AppShell(product_service=product_service)

    response = app.get("/products-stock", authorization_header=header)

    assert response.status_code == 200
    assert "<th>ID</th><th>Name</th><th>SKU</th><th>Stock</th><th>Reorder</th><th>Status</th>" in response.body
    assert "Healthy Candle" in response.body
    assert "Low Candle" in response.body
    assert "Healthy" in response.body
    assert "Low stock" in response.body


def test_products_ui_create_edit_archive_interactions() -> None:
    header = _auth_header("owner2", "owner2@example.com")
    product_service = ProductService()
    app = AppShell(product_service=product_service)

    create_response = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={
            "action": "create",
            "name": "Wax Melt",
            "sku": "WAX-001",
            "stock_on_hand": "9",
            "reorder_point": "4",
        },
    )
    assert create_response.status_code == 200
    assert "Wax Melt" in create_response.body

    product_id = product_service.list_products(authorization_header=header)[0].product_id
    edit_response = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={
            "action": "edit",
            "product_id": product_id,
            "name": "Wax Melt Deluxe",
            "sku": "WAX-001-DX",
            "stock_on_hand": "2",
            "reorder_point": "4",
        },
    )
    assert edit_response.status_code == 200
    assert "Wax Melt Deluxe" in edit_response.body
    assert "Low stock" in edit_response.body

    archive_response = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "archive", "product_id": product_id},
    )
    assert archive_response.status_code == 200
    assert "Archived products" in archive_response.body
    assert "<button type='submit'>Restore</button>" in archive_response.body


def test_products_page_renders_forms_for_create_and_archive_actions() -> None:
    header = _auth_header("owner3", "owner3@example.com")
    product_service = ProductService()
    product_service.create_product(
        authorization_header=header,
        name="Jar",
        sku="JAR-001",
        stock_on_hand=10,
        reorder_point=2,
    )
    app = AppShell(product_service=product_service)

    response = app.get("/products-stock", authorization_header=header)

    assert response.status_code == 200
    assert "<input type='hidden' name='action' value='create'>" in response.body
    assert "<input type='hidden' name='action' value='edit'>" in response.body
    assert "Edit name <input name='name' value='Jar'" in response.body
    assert "type='number' min='0'" in response.body
    assert "<button type='submit'>Archive</button>" in response.body


def test_products_ui_row_edit_form_updates_only_submitted_field() -> None:
    header = _auth_header("owner4", "owner4@example.com")
    product_service = ProductService()
    product_service.create_product(
        authorization_header=header,
        name="Bundle",
        sku="BND-001",
        stock_on_hand=12,
        reorder_point=4,
    )
    product_id = product_service.list_products(authorization_header=header)[0].product_id
    app = AppShell(product_service=product_service)

    response = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={
            "action": "edit",
            "product_id": product_id,
            "stock_on_hand": "3",
        },
    )
    assert response.status_code == 200

    updated = product_service.get_product(authorization_header=header, product_id=product_id)
    assert updated.name == "Bundle"
    assert updated.sku == "BND-001"
    assert updated.reorder_point == 4
    assert updated.stock_on_hand == 3


def test_products_ui_restore_interaction_shows_archived_section_and_restores_product() -> None:
    header = _auth_header("owner5", "owner5@example.com")
    product_service = ProductService()
    app = AppShell(product_service=product_service)

    created = product_service.create_product(
        authorization_header=header,
        name="Archived Candle",
        sku="ARC-001",
        stock_on_hand=5,
        reorder_point=2,
    )
    assert created is not None

    app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "archive", "product_id": created.product_id},
    )

    archived_view = app.get("/products-stock", authorization_header=header)
    assert archived_view.status_code == 200
    assert "Archived products" in archived_view.body
    assert "<button type='submit'>Restore</button>" in archived_view.body

    restored_view = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "restore", "product_id": created.product_id},
    )

    assert restored_view.status_code == 200
    assert "Archived products" not in restored_view.body
    assert "Archived Candle" in restored_view.body
