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
    assert "Archived products" not in archive_response.body
    assert "view=archived" in archive_response.body


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
    assert "Edit</a>" in response.body
    assert "<td>10</td>" in response.body
    assert "<td>2</td>" in response.body
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

    archived_view = app.get("/products-stock?view=archived", authorization_header=header)
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


def test_products_ui_filter_views_active_archived_all() -> None:
    header = _auth_header("owner6", "owner6@example.com")
    product_service = ProductService()
    app = AppShell(product_service=product_service)

    active = product_service.create_product(
        authorization_header=header,
        name="Active Candle",
        sku="ACT-001",
        stock_on_hand=7,
        reorder_point=3,
    )
    archived = product_service.create_product(
        authorization_header=header,
        name="Archived Candle",
        sku="ARC-002",
        stock_on_hand=7,
        reorder_point=3,
    )
    assert active is not None
    assert archived is not None

    app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "archive", "product_id": archived.product_id},
    )

    active_view = app.get("/products-stock?view=active", authorization_header=header)
    assert "Active Candle" in active_view.body
    assert "Archived products" not in active_view.body

    archived_view = app.get("/products-stock?view=archived", authorization_header=header)
    assert "Archived products" in archived_view.body
    assert "Active Candle" not in archived_view.body

    all_view = app.get("/products-stock?view=all", authorization_header=header)
    assert "Active Candle" in all_view.body
    assert "Archived products" in all_view.body


def test_products_ui_status_chips_render_with_icons() -> None:
    header = _auth_header("owner7", "owner7@example.com")
    product_service = ProductService()
    app = AppShell(product_service=product_service)

    product_service.create_product(
        authorization_header=header,
        name="Low Candle",
        sku="LOW-003",
        stock_on_hand=1,
        reorder_point=3,
    )
    product_service.create_product(
        authorization_header=header,
        name="Healthy Candle",
        sku="HLT-003",
        stock_on_hand=9,
        reorder_point=3,
    )

    response = app.get("/products-stock", authorization_header=header)
    assert "⚠️ Low stock" in response.body
    assert "✅ Healthy" in response.body


def test_products_ui_bulk_archive_and_restore_actions() -> None:
    header = _auth_header("owner8", "owner8@example.com")
    product_service = ProductService()
    app = AppShell(product_service=product_service)

    first = product_service.create_product(
        authorization_header=header,
        name="Bulk One",
        sku="BLK-001",
        stock_on_hand=6,
        reorder_point=2,
    )
    second = product_service.create_product(
        authorization_header=header,
        name="Bulk Two",
        sku="BLK-002",
        stock_on_hand=6,
        reorder_point=2,
    )
    assert first is not None
    assert second is not None

    archive_response = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={
            "action": "bulk_archive",
            "product_ids": f"{first.product_id}, {second.product_id}",
        },
    )
    assert archive_response.status_code == 200
    assert product_service.list_products(authorization_header=header) == []

    restore_response = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={
            "action": "bulk_restore",
            "product_ids": first.product_id,
        },
    )
    assert restore_response.status_code == 200
    visible_ids = [product.product_id for product in product_service.list_products(authorization_header=header)]
    assert visible_ids == [first.product_id]


def test_products_ui_renders_bulk_action_controls() -> None:
    header = _auth_header("owner9", "owner9@example.com")
    product_service = ProductService()
    product_service.create_product(
        authorization_header=header,
        name="Selectable",
        sku="SEL-001",
        stock_on_hand=5,
        reorder_point=2,
    )
    app = AppShell(product_service=product_service)

    response = app.get("/products-stock", authorization_header=header)
    assert response.status_code == 200
    assert "<h3>Bulk actions</h3>" in response.body
    assert "name='product_ids'" in response.body
    assert "value='bulk_archive'" in response.body
    assert "value='bulk_restore'" in response.body
    assert "<th>Select</th><th>ID</th>" in response.body


def test_products_ui_detail_edit_mode_shows_all_editable_fields() -> None:
    header = _auth_header("owner10", "owner10@example.com")
    product_service = ProductService()
    created = product_service.create_product(
        authorization_header=header,
        name="Detail Candle",
        sku="DTL-001",
        stock_on_hand=11,
        reorder_point=6,
    )
    assert created is not None
    app = AppShell(product_service=product_service)

    response = app.get(f"/products-stock?view=active&edit={created.product_id}", authorization_header=header)

    assert response.status_code == 200
    assert "Save all fields" in response.body
    assert "name='name' value='Detail Candle'" in response.body
    assert "name='sku' value='DTL-001'" in response.body
    assert "name='stock_on_hand' type='number' min='0' value='11'" in response.body
    assert "name='reorder_point' type='number' min='0' value='6'" in response.body


def test_make_buy_page_shows_materials_empty_state() -> None:
    app = create_app()

    response = app.get("/make-buy", authorization_header=_auth_header("mat1", "mat1@example.com"))

    assert response.status_code == 200
    assert "No materials yet. Add your first material to track supplies." in response.body


def test_make_buy_ui_create_and_edit_material_interactions() -> None:
    header = _auth_header("mat2", "mat2@example.com")
    app = create_app()

    create_response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create",
            "name": "Soy Wax",
            "unit": "kg",
            "stock_on_hand": "2",
            "reorder_point": "3",
        },
    )
    assert create_response.status_code == 200
    assert "Soy Wax" in create_response.body
    assert "⚠️ Low stock" in create_response.body

    edit_response = app.get("/make-buy?edit=mat-1", authorization_header=header)
    assert "Save all fields" in edit_response.body

    save_response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "edit",
            "material_id": "mat-1",
            "stock_on_hand": "8",
        },
    )
    assert save_response.status_code == 200
    assert "✅ Healthy" in save_response.body


def test_make_buy_ui_archive_restore_and_filter_views() -> None:
    header = _auth_header("mat3", "mat3@example.com")
    app = create_app()

    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create",
            "name": "Archived Wax",
            "unit": "kg",
            "stock_on_hand": "3",
            "reorder_point": "1",
        },
    )

    archive_response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "archive", "material_id": "mat-1"},
    )
    assert archive_response.status_code == 200
    assert "Archived materials" not in archive_response.body

    archived_view = app.get("/make-buy?view=archived", authorization_header=header)
    assert archived_view.status_code == 200
    assert "Archived materials" in archived_view.body
    assert "<button type='submit'>Restore</button>" in archived_view.body
    assert "Archived Wax" in archived_view.body

    restored_response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "restore", "material_id": "mat-1"},
    )
    assert restored_response.status_code == 200
    assert "Archived Wax" in restored_response.body

    active_view = app.get("/make-buy?view=active", authorization_header=header)
    assert "Archived materials" not in active_view.body

    all_view = app.get("/make-buy?view=all", authorization_header=header)
    assert "Archived Wax" in all_view.body
