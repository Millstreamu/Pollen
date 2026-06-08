from pollen.app import NAV_ITEMS, AppShell, can_access_shop_record, create_app, healthcheck
from pollen.auth import AuthService
from pollen.services import ProductService


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
    assert "No finished products yet. Create products in Workshop, then track stock here." in response.body


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
    assert "<th>Product</th><th>SKU</th><th>On Hand</th><th>Reserved</th><th>Reorder Point</th><th>Status</th>" in response.body
    assert "<th>Status</th><th>Stock Control</th>" not in response.body
    assert "<section class='dashboard-grid two-col'>" not in response.body
    assert response.body.count("<section class='panel wide'") >= 3
    assert "href='#stock-product-prd-1'>Healthy Candle</a>" in response.body
    assert "Low Candle" in response.body
    assert "Good" in response.body
    assert "Low" in response.body


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
    assert "Low" in edit_response.body

    archive_response = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "archive", "product_id": product_id},
    )
    assert archive_response.status_code == 200
    assert "Archived products" not in archive_response.body
    assert "Wax Melt Deluxe" not in archive_response.body


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
    assert "<input type='hidden' name='action' value='adjust_stock'>" in response.body
    assert "Select a product name for stock control." in response.body
    assert "id='stock-product-prd-1' role='dialog'" in response.body
    assert "<td>10</td>" in response.body
    assert "<td>2</td>" in response.body
    assert "name='delta' type='number' value='0'" in response.body
    assert "Create Product" not in response.body


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
    assert "Archived products" not in archived_view.body
    assert "Archived Candle" not in archived_view.body

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
    assert "Archived products" not in archived_view.body
    assert "Archived Candle" not in archived_view.body

    all_view = app.get("/products-stock?view=all", authorization_header=header)
    assert "Active Candle" in all_view.body
    assert "Archived products" not in all_view.body


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
    assert "Low" in response.body
    assert "Good" in response.body


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
    assert "Select a product name for stock control." in response.body
    assert "name='delta'" in response.body
    assert "value='bulk_archive'" not in response.body
    assert "value='bulk_restore'" not in response.body
    assert "<th>Product</th><th>SKU</th><th>On Hand</th>" in response.body


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
    assert "Save all fields" not in response.body
    assert "Detail Candle" in response.body
    assert "name='delta' type='number' value='0'" in response.body
    assert "Select a product name for stock control." in response.body


def test_products_stock_materials_panel_adds_material_from_popup_form() -> None:
    header = _auth_header("materials-panel", "materials-panel@example.com")
    app = create_app()

    initial_response = app.get("/products-stock", authorization_header=header)

    assert initial_response.status_code == 200
    assert "<h3>Materials</h3>" in initial_response.body
    assert "View Materials" not in initial_response.body
    assert "id='add-material-dialog' role='dialog'" not in initial_response.body
    assert "<input type='hidden' name='action' value='create_material'>" not in initial_response.body

    create_response = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={
            "action": "create_material",
            "name": "Wick Tabs",
            "unit": "pcs",
            "stock_on_hand": "12",
            "reorder_point": "20",
        },
    )

    assert create_response.status_code == 200
    assert "Wick Tabs" in create_response.body
    assert "12 pcs" in create_response.body
    assert "Low" in create_response.body

def test_make_buy_page_shows_material_workflow_empty_state() -> None:
    app = create_app()

    response = app.get("/make-buy", authorization_header=_auth_header("mat1", "mat1@example.com"))

    assert response.status_code == 200
    assert "Materials Defined" in response.body
    assert "Products Defined" in response.body
    assert response.body.index("Products Defined") < response.body.index("Materials Defined")
    assert "Recipes Ready" in response.body
    assert "Workshop Materials" in response.body
    assert "Create Material" in response.body
    assert "Create the materials and parts you use to make products. You’ll choose from these when setting up recipes." in response.body
    assert "Products You Make" in response.body
    assert response.body.index("Products You Make") < response.body.index("Workshop Materials")
    assert "Create Product" in response.body
    assert "Create the products you make in your workshop. After saving a product, set up the materials used for one unit." in response.body
    assert "Define the finished products you make, then set up the materials used for one unit." in response.body
    assert "Make Next" not in response.body
    assert "Plan Batch" not in response.body
    assert "Buy List" not in response.body
    assert "Incoming Purchases" not in response.body


def test_make_buy_ui_create_material_from_modal_and_inventory_compatibility() -> None:
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
            "supplier": "Acme Wax",
            "notes": "Used for container candles",
        },
    )
    assert create_response.status_code == 200
    assert "Soy Wax" in create_response.body
    assert "2 kg" in create_response.body
    assert "Acme Wax" in create_response.body
    assert "Used for container candles" in create_response.body
    assert "Save Material" in create_response.body

    inventory_response = app.get("/products-stock", authorization_header=header)
    assert "Soy Wax" in inventory_response.body
    assert "Low" in inventory_response.body

    material = app._material_service.get_material(authorization_header=header, material_id="mat-1")  # noqa: SLF001
    assert material is not None
    assert material.name == "Soy Wax"
    assert material.supplier == "Acme Wax"
    assert material.notes == "Used for container candles"


def test_make_buy_ui_create_material_validates_required_fields() -> None:
    header = _auth_header("mat-required", "mat-required@example.com")
    app = create_app()

    response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create",
            "name": "",
            "unit": "kg",
            "stock_on_hand": "0",
            "reorder_point": "1",
        },
    )

    assert response.status_code == 400
    assert "Material name, unit, current stock, and reorder point are required" in response.body
    assert app._material_service.list_materials(authorization_header=header) == []  # noqa: SLF001


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
    assert "Archived materials" not in archived_view.body
    assert "<button type='submit'>Restore</button>" not in archived_view.body
    assert "Archived Wax" not in archived_view.body

    restored_response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "restore", "material_id": "mat-1"},
    )
    assert restored_response.status_code == 200
    restored = app._material_service.get_material(authorization_header=header, material_id="mat-1")  # noqa: SLF001
    assert restored is not None
    assert restored.is_active

    active_view = app.get("/make-buy?view=active", authorization_header=header)
    assert "Archived materials" not in active_view.body

    all_view = app.get("/make-buy?view=all", authorization_header=header)
    assert all_view.status_code == 200
    assert "Archived materials" not in all_view.body

def test_make_buy_ui_invalid_view_defaults_to_active_content() -> None:
    header = _auth_header("mat4", "mat4@example.com")
    app = create_app()

    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create",
            "name": "Default View Wax",
            "unit": "kg",
            "stock_on_hand": "5",
            "reorder_point": "2",
        },
    )

    response = app.get("/make-buy?view=unexpected", authorization_header=header)

    assert response.status_code == 200
    assert "Default View Wax" in response.body
    assert "Workshop Materials" in response.body
    assert "Make Next" not in response.body


def test_make_buy_ui_buy_list_suggestions_and_add_to_purchase() -> None:
    header = _auth_header("mat-buy", "mat-buy@example.com")
    app = create_app()

    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create",
            "name": "Label Rolls",
            "unit": "roll",
            "stock_on_hand": "1",
            "reorder_point": "4",
        },
    )

    response = app.get("/make-buy", authorization_header=header)
    assert response.status_code == 200
    assert "Buy List" not in response.body
    assert "Incoming Purchases" not in response.body

    inventory = app.get("/products-stock", authorization_header=header)
    assert inventory.status_code == 200
    assert "Low Stock Alerts" not in inventory.body
    assert "id='buy-list'" not in inventory.body
    assert "Items Need Attention" in inventory.body
    assert "Buy 7 roll" in inventory.body
    assert "Add to Purchase" in inventory.body

    added = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "add_to_purchase", "material_id": "mat-1"},
    )
    assert added.status_code == 200
    draft = app._material_service.list_purchase_draft(authorization_header=header)  # noqa: SLF001
    assert [material.name for material in draft] == ["Label Rolls"]


def test_make_buy_ui_edit_ignores_unknown_material_id_without_crashing() -> None:
    header = _auth_header("mat5", "mat5@example.com")
    app = create_app()

    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create",
            "name": "Known Material",
            "unit": "each",
            "stock_on_hand": "9",
            "reorder_point": "3",
        },
    )

    response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "edit",
            "material_id": "mat-999",
            "name": "Should Not Apply",
            "stock_on_hand": "0",
        },
    )

    assert response.status_code == 200
    material = app._material_service.get_material(authorization_header=header, material_id="mat-1")  # noqa: SLF001
    assert material is not None
    assert material.name == "Known Material"


def test_make_buy_ui_create_product_from_modal_without_recipe() -> None:
    header = _auth_header("prod-workshop", "prod-workshop@example.com")
    app = create_app()

    response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create_product",
            "name": "Lavender Candle",
            "sku": "LC-8",
            "category": "Candles",
            "sale_price": "18.50",
            "default_batch_size": "12",
            "workflow_status": "Draft",
            "notes": "Spring market bestseller",
        },
    )

    assert response.status_code == 200
    assert "Product saved. It is ready for recipe setup." in response.body
    assert "Products You Make" in response.body
    assert "Lavender Candle" in response.body
    assert "LC-8" in response.body
    assert "Candles" in response.body
    assert "$18.50" in response.body
    assert "Spring market bestseller" in response.body
    assert "Draft" in response.body
    assert "No recipe" in response.body
    assert "No materials assigned yet" not in response.body
    assert "Recipe needed" not in response.body
    assert "table-scroll workshop-table-scroll" in response.body
    assert "workshop-products-table" in response.body
    assert "href='#recipe-dialog-prd-1'>No recipe</a>" in response.body
    assert "Set up recipe" not in response.body

    product = app._product_service.get_product(authorization_header=header, product_id="prd-1")  # noqa: SLF001
    assert product is not None
    assert product.default_batch_size == 12
    assert product.workflow_status == "Draft"
    assert app._recipe_service.list_recipe_items(authorization_header=header, product_id=product.product_id) == []  # noqa: SLF001


def test_make_buy_ui_create_product_validates_required_fields() -> None:
    header = _auth_header("prod-required", "prod-required@example.com")
    app = create_app()

    response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create_product",
            "name": "",
            "default_batch_size": "0",
            "workflow_status": "Draft",
        },
    )

    assert response.status_code == 400
    assert "Product name, default batch size, and status are required" in response.body
    assert app._product_service.list_products(authorization_header=header) == []  # noqa: SLF001


def test_make_buy_ui_create_product_can_be_marked_active() -> None:
    header = _auth_header("prod-active", "prod-active@example.com")
    app = create_app()

    response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create_product",
            "name": "Gift Box Set",
            "default_batch_size": "4",
            "workflow_status": "Active",
        },
    )

    assert response.status_code == 200
    assert "Gift Box Set" in response.body
    assert "Active" in response.body
    assert "No recipe" in response.body


def test_make_buy_ui_recipe_needed_status_and_setup_dialog() -> None:
    header = _auth_header("recipe-needed", "recipe-needed@example.com")
    app = create_app()

    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create_product", "name": "Lavender Candle", "default_batch_size": "12", "workflow_status": "Draft"},
    )

    response = app.get("/make-buy", authorization_header=header)

    assert response.status_code == 200
    assert "Recipes Ready" in response.body
    assert "No recipe" in response.body
    assert "href='#recipe-dialog-prd-1'>No recipe</a>" in response.body
    assert "Set up recipe" not in response.body
    assert "Set Up Recipe: Lavender Candle" in response.body
    assert "Choose the materials and quantities needed to make one finished unit." in response.body
    assert "No materials added yet. Add the materials or parts used to make this product." in response.body
    assert "+ Add Material" in response.body
    assert "+ Create New Material" not in response.body
    assert "Shown after save" not in response.body
    assert "Remove row action" not in response.body
    assert "Add material to recipe" not in response.body
    assert "name='material_id_1'" not in response.body
    assert "Save Recipe" in response.body


def test_make_buy_ui_recipe_builder_add_material_button_uses_one_row_template() -> None:
    header = _auth_header("recipe-add-row", "recipe-add-row@example.com")
    app = create_app()

    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create", "name": "Soy Wax", "unit": "g", "stock_on_hand": "500", "reorder_point": "100"},
    )
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create_product", "name": "Lavender Candle", "default_batch_size": "12", "workflow_status": "Draft"},
    )

    response = app.get("/make-buy", authorization_header=header)

    assert response.status_code == 200
    assert "data-add-recipe-row='prd-1'" in response.body
    assert "data-recipe-rows='prd-1' data-next-index='1'></div>" in response.body
    assert "<template data-recipe-template='prd-1'>" in response.body
    assert "name='material_id___INDEX__'" in response.body
    assert "name='material_id_1'" not in response.body


def test_make_buy_ui_create_material_from_recipe_returns_to_recipe_modal() -> None:
    header = _auth_header("recipe-new-material", "recipe-new-material@example.com")
    app = create_app()

    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create_product", "name": "Lavender Candle", "default_batch_size": "12", "workflow_status": "Draft"},
    )
    response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create",
            "return_to_recipe": "prd-1",
            "name": "Soy Wax",
            "unit": "g",
            "stock_on_hand": "500",
            "reorder_point": "100",
        },
    )

    assert response.status_code == 200
    assert "Material saved. Return to the recipe and choose it from the material list." in response.body
    assert "class='modal-popover modal-open' id='recipe-dialog-prd-1'" in response.body
    assert "Soy Wax" in response.body
    assert "data-unit='g'" in response.body


def test_make_buy_ui_recipe_dialog_omits_create_material_shortcut() -> None:
    header = _auth_header("recipe-material-stack", "recipe-material-stack@example.com")
    app = create_app()

    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create_product",
            "name": "Lavender Candle",
            "default_batch_size": "12",
            "workflow_status": "Draft",
        },
    )

    response = app.get("/make-buy?return_to_recipe=prd-1", authorization_header=header)

    assert response.status_code == 200
    assert "href='/make-buy?return_to_recipe=prd-1#create-material-dialog'" not in response.body
    assert "class='modal-popover modal-open' id='recipe-dialog-prd-1'" in response.body
    assert ".modal-popover.modal-open{display:grid;z-index:50}" in response.body
    assert ".modal-popover:target{display:grid;z-index:70}" in response.body


def test_make_buy_ui_assigns_materials_to_product_recipe_and_updates_status() -> None:
    header = _auth_header("recipe-ready", "recipe-ready@example.com")
    app = create_app()

    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create", "name": "Soy Wax", "unit": "g", "stock_on_hand": "500", "reorder_point": "100"},
    )
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create", "name": "Cotton Wick", "unit": "each", "stock_on_hand": "20", "reorder_point": "5"},
    )
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create_product", "name": "Lavender Candle", "default_batch_size": "12", "workflow_status": "Active"},
    )

    response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "save_recipe",
            "product_id": "prd-1",
            "material_id_1": "mat-1",
            "quantity_per_unit_1": "80",
            "material_id_2": "mat-2",
            "quantity_per_unit_2": "1",
        },
    )

    assert response.status_code == 200
    assert "Recipe saved. Product recipe status is updated." in response.body
    assert "Materials assigned" in response.body
    assert "Edit recipe" in response.body
    assert "2 materials assigned" in response.body
    assert "Soy Wax" in response.body
    assert "Cotton Wick" in response.body
    assert "<span class='unit-pill' id='unit-prd-1-1' data-empty-unit='—'>g</span>" in response.body
    assert "<span class='unit-pill' id='unit-prd-1-2' data-empty-unit='—'>each</span>" in response.body
    recipe_items = app._recipe_service.list_recipe_items(authorization_header=header, product_id="prd-1")  # noqa: SLF001
    assert [(item.material_id, item.quantity_per_unit) for item in recipe_items] == [("mat-1", 80), ("mat-2", 1)]


def test_make_buy_ui_removing_recipe_material_updates_status() -> None:
    header = _auth_header("recipe-remove", "recipe-remove@example.com")
    app = create_app()

    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create", "name": "Amber Jar", "unit": "each", "stock_on_hand": "10", "reorder_point": "2"},
    )
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create_product", "name": "Jar Candle", "default_batch_size": "6", "workflow_status": "Draft"},
    )
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "save_recipe", "product_id": "prd-1", "material_id_1": "mat-1", "quantity_per_unit_1": "1"},
    )

    response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "save_recipe", "product_id": "prd-1", "material_id_1": "mat-1", "quantity_per_unit_1": "1", "remove_1": "1"},
    )

    assert response.status_code == 200
    assert "No recipe" in response.body
    assert "href='#recipe-dialog-prd-1'>No recipe</a>" in response.body
    assert "Set up recipe" not in response.body
    assert app._recipe_service.list_recipe_items(authorization_header=header, product_id="prd-1") == []  # noqa: SLF001


def test_make_buy_ui_recipe_validation_requires_material_and_positive_quantity() -> None:
    header = _auth_header("recipe-validation", "recipe-validation@example.com")
    app = create_app()

    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create", "name": "Label", "unit": "each", "stock_on_hand": "30", "reorder_point": "5"},
    )
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create_product", "name": "Labeled Candle", "default_batch_size": "8", "workflow_status": "Draft"},
    )

    missing_material = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "save_recipe", "product_id": "prd-1", "material_id_1": "", "quantity_per_unit_1": "1"},
    )
    bad_quantity = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "save_recipe", "product_id": "prd-1", "material_id_1": "mat-1", "quantity_per_unit_1": "0"},
    )

    assert missing_material.status_code == 400
    assert "Material is required for each recipe row" in missing_material.body
    assert bad_quantity.status_code == 400
    assert "Quantity per unit must be positive" in bad_quantity.body
    duplicate_material = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "save_recipe",
            "product_id": "prd-1",
            "material_id_1": "mat-1",
            "quantity_per_unit_1": "1",
            "material_id_2": "mat-1",
            "quantity_per_unit_2": "2",
        },
    )

    assert duplicate_material.status_code == 400
    assert "Each material can only be added once to a recipe" in duplicate_material.body
    assert app._recipe_service.list_recipe_items(authorization_header=header, product_id="prd-1") == []  # noqa: SLF001


def test_make_buy_draft_product_status_opens_activation_popup_and_confirms() -> None:
    header = _auth_header("prod-activate-popup", "prod-activate-popup@example.com")
    app = create_app()

    created = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create_product",
            "name": "Popup Candle",
            "default_batch_size": "6",
            "workflow_status": "Draft",
        },
    )

    assert created.status_code == 200
    assert "href='#activate-product-prd-1'" in created.body
    assert "Activate product?" in created.body
    assert "Confirm activate" in created.body
    product = app._product_service.get_product(authorization_header=header, product_id="prd-1")  # noqa: SLF001
    assert product is not None
    assert product.workflow_status == "Draft"

    activated = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "activate_product", "product_id": "prd-1"},
    )

    assert activated.status_code == 200
    assert "Popup Candle" in activated.body
    assert "href='#activate-product-prd-1'" not in activated.body
    product = app._product_service.get_product(authorization_header=header, product_id="prd-1")  # noqa: SLF001
    assert product is not None
    assert product.workflow_status == "Active"
