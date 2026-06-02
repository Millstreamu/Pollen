from pollen.app import AppShell
from pollen.services import ProductService


def _auth_header(user_id: str = "owner", email: str = "owner@example.com") -> str:
    return f"Bearer user:{user_id}:{email}"


def test_orders_page_shows_beginner_friendly_empty_state_and_sections() -> None:
    header = _auth_header("orders-empty", "orders-empty@example.com")
    app = AppShell()

    response = app.get("/orders", authorization_header=header)

    assert response.status_code == 200
    assert "<h3>Order actions</h3>" in response.body
    assert "<h3>Create order</h3>" in response.body
    assert "<h3>Order queue</h3>" in response.body
    assert "No orders yet. Create an order to start your shipping queue." in response.body


def test_orders_page_uses_normalized_status_badge_text_and_action_buttons() -> None:
    header = _auth_header("orders-ui", "orders-ui@example.com")
    product_service = ProductService()
    app = AppShell(product_service=product_service)
    app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "create", "name": "Soap", "sku": "S-9", "stock_on_hand": "5", "reorder_point": "1"},
    )
    app.post(
        "/orders",
        authorization_header=header,
        form_data={"customer_name": "Pat", "product_sku": "S-9", "quantity": "1"},
    )

    response = app.get("/orders", authorization_header=header)

    assert response.status_code == 200
    assert "Ready to pack" in response.body
    assert "ready_to_pack" not in response.body
    assert "<button type='submit'>Mark packed</button>" in response.body
    assert "<button type='submit'>Mark shipped</button>" in response.body
    assert "<button type='submit'>Cancel order</button>" in response.body


def test_products_stock_page_uses_beginner_friendly_sections_and_buttons() -> None:
    header = _auth_header("products-ui", "products-ui@example.com")
    app = AppShell()
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create_product",
            "name": "Soap",
            "sku": "SOAP-1",
            "stock_on_hand": "3",
            "reorder_point": "1",
        },
    )

    response = app.get("/products-stock", authorization_header=header)

    assert response.status_code == 200
    assert "Finished Products" in response.body
    assert "Materials" in response.body
    assert "Buy List" in response.body
    assert "Incoming Purchases" in response.body
    assert "Items to Reorder" in response.body
    assert "Stock Control" in response.body
    assert "action='/products-stock'" in response.body
    assert "Create Product" not in response.body
    assert "id='add-product-dialog-title'>Add product</h3>" not in response.body
    assert "id='add-material-dialog-title'>Add material</h3>" not in response.body
    assert "id='create-new-material-dialog-title'>+ Create new material</h3>" not in response.body
    assert "<input type='hidden' name='action' value='create_material'>" not in response.body
    assert "<button type='submit' name='action' value='bulk_archive'>Archive selected</button>" not in response.body


def test_make_buy_page_uses_beginner_friendly_material_sections_and_empty_state_guidance() -> None:
    header = _auth_header("make-buy-ui", "make-buy-ui@example.com")
    app = AppShell()

    response = app.get("/make-buy", authorization_header=header)

    assert response.status_code == 200
    assert "Materials Defined" in response.body
    assert "Products Defined" in response.body
    assert "Recipes Ready" in response.body
    assert "Workshop Materials" in response.body
    assert "Create Material" in response.body
    assert "id='create-material-dialog-title'>Create Material</h3>" in response.body
    assert "Add a material, part, ingredient, or supply you use in your workshop." in response.body
    assert "<button class='primary' type='submit'>Save Material</button>" in response.body
    assert "Products You Make" in response.body
    assert "Create Product" in response.body
    assert "id='create-product-dialog-title'>Create Product</h3>" in response.body
    assert "Add something you make or sell. You’ll define its materials and recipe next." in response.body
    assert "<button class='primary' type='submit'>Save Product</button>" in response.body
    assert "Create the materials and parts you use to make products. You’ll choose from these when setting up recipes." in response.body
    assert "Create the products you make in your workshop. After saving a product, set up the materials used for one unit." in response.body
    assert "Define the finished products you make, then set up the materials used for one unit." in response.body
    assert "Products You Make / Product Builder" not in response.body
    assert "Make Next / Batch Queue" not in response.body
    assert "+ Create new material" not in response.body
    assert "Making notes / steps" not in response.body
    assert "href='#plan-batch-dialog'" not in response.body
    assert "href='#create-purchase-dialog'" not in response.body
    assert "Buy List" not in response.body
    assert "Incoming Purchases" not in response.body
    assert "Inventory movements" not in response.body
    assert "Activity log" not in response.body


def test_money_page_uses_beginner_friendly_consistency_sections_and_empty_state() -> None:
    header = _auth_header("money-ui", "money-ui@example.com")
    app = AppShell()

    response = app.get("/money", authorization_header=header)

    assert response.status_code == 200
    assert "<h3>Money overview</h3>" in response.body
    assert "<h3>Estimated profit and cost</h3>" in response.body
    assert "<h3>Next steps</h3>" in response.body
    assert "No money data yet. Ship orders with product pricing to unlock estimated totals." in response.body
    assert "<a class='button-link' href='/orders'>Ship orders first</a>" in response.body


def test_settings_page_uses_beginner_friendly_consistency_sections_and_empty_state() -> None:
    header = _auth_header("settings-ui", "settings-ui@example.com")
    app = AppShell()

    response = app.get("/settings", authorization_header=header)

    assert response.status_code == 200
    assert "<h3>Shop settings</h3>" in response.body
    assert "<h3>Sales channels</h3>" in response.body
    assert "<h3>Next steps</h3>" in response.body
    assert "No connected sales channels yet. Add one when you are ready to import orders." in response.body
    assert "<p class='coming-soon'>Settings forms are coming soon.</p>" in response.body
    assert "<p class='coming-soon'>Channel connections are coming soon.</p>" in response.body


def test_today_page_uses_beginner_friendly_consistency_sections_and_empty_state() -> None:
    header = _auth_header("today-ui", "today-ui@example.com")
    app = AppShell()

    response = app.get("/", authorization_header=header)

    assert response.status_code == 200
    assert "<h3>Today summary</h3>" in response.body
    assert "<h3>Today actions</h3>" in response.body
    assert "<h3>Next steps</h3>" in response.body
    assert "No work is waiting right now. Create your first order or add inventory to begin." in response.body
    assert "<span class='metric-label'>Orders to pack</span>" in response.body
    assert "<a class='button-link' href='/orders'>Open highest-priority workflow</a>" in response.body


def test_app_shell_includes_screenshot_friendly_visual_system() -> None:
    header = _auth_header("visual-system", "visual-system@example.com")
    app = AppShell()

    response = app.get("/", authorization_header=header)

    assert response.status_code == 200
    assert "<style>" in response.body
    assert "--accent:#7a4f24" in response.body
    assert "class='skip-link'" in response.body
    assert "class='page-heading'" in response.body
    assert "Small seller workspace" in response.body
    assert "aria-current='page'" in response.body
    assert "nav a[aria-current='page']" in response.body
    assert ".metric-grid" in response.body
    assert ".status-badge" in response.body


def test_dashboard_visuals_do_not_render_screenshot_demo_records() -> None:
    header = _auth_header("no-demo", "no-demo@example.com")
    app = AppShell()

    bodies = [
        app.get(path, authorization_header=header).body
        for path in ["/", "/orders", "/products-stock", "/make-buy", "/money", "/settings"]
    ]
    combined = "\n".join(bodies)

    forbidden_demo_values = [
        "Emily Johnson",
        "Michael Brown",
        "Sunny Bee Co.",
        "Kate Smith",
        "Lavender Candle",
        "PO-1002",
        "Etsy payout",
        "CandleScience",
        "May 28, 2024",
    ]
    for value in forbidden_demo_values:
        assert value not in combined



def test_workflow_dialog_forms_use_polished_controls_and_spaced_actions() -> None:
    header = _auth_header("dialog-polish", "dialog-polish@example.com")
    app = AppShell()

    products = app.get("/products-stock", authorization_header=header).body
    make_buy = app.get("/make-buy", authorization_header=header).body
    orders = app.get("/orders", authorization_header=header).body
    combined = "\n".join([products, make_buy, orders])

    assert "width:100%;box-sizing:border-box;min-height:2.45rem" in combined
    assert ".modal-card .dialog-actions{grid-column:1/-1;display:flex;flex-wrap:wrap;justify-content:flex-end;gap:1rem" in combined
    assert "<div class='dialog-actions'><button class='primary' type='submit'>Save product</button>" not in products
    assert "<div class='dialog-actions'><button class='primary' type='submit'>Save material</button>" not in products
    assert "<div class='dialog-actions'><button class='primary' type='submit'>Save Product</button>" in make_buy
    assert "<div class='dialog-actions'><button class='primary' type='submit'>Save Material</button>" in make_buy
    assert "<div class='dialog-actions'><button class='primary' type='submit'>Plan Batch</button>" not in make_buy
    assert "<div class='dialog-actions'><button class='primary' type='submit'>Save purchase</button>" in products
    assert "<div class='dialog-actions'><button class='primary' type='submit'>Create order</button>" in orders

def test_dashboard_primary_controls_are_links_or_real_post_forms() -> None:
    header = _auth_header("controls", "controls@example.com")
    app = AppShell()

    orders = app.get("/orders", authorization_header=header).body
    products = app.get("/products-stock", authorization_header=header).body
    make_buy = app.get("/make-buy", authorization_header=header).body
    settings = app.get("/settings", authorization_header=header).body

    assert "href='#create-order-dialog'" in orders
    assert "<section class='panel wide' id='create-order'>" in orders
    assert "id='create-order-dialog' role='dialog'" in orders
    assert "href='#create-purchase-dialog'" in products
    assert "id='incoming-purchases'" in products
    assert "id='create-purchase-dialog' role='dialog'" in products
    assert "href='#plan-batch-dialog'" not in make_buy
    assert "href='#create-product-dialog'" in make_buy
    assert "id='create-product-dialog' role='dialog'" in make_buy
    assert "href='#create-material-dialog'" in make_buy
    assert "href='#create-purchase-dialog'" not in make_buy
    assert "<section class='panel wide workflow-panel' id='make-buy-workflow'>" not in make_buy
    assert "id='incoming-purchases'" not in make_buy
    assert "href='#shop-settings'" in settings
    assert "<section class='panel wide' id='shop-settings'>" in settings


def test_inventory_page_owns_material_stock_adjustments() -> None:
    header = _auth_header("inventory-material-adjust", "inventory-material-adjust@example.com")
    app = AppShell()
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create", "name": "Soy Wax", "unit": "g", "stock_on_hand": "8", "reorder_point": "3"},
    )

    response = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "adjust_stock", "material_id": "mat-1", "delta": "5", "reason": "cycle count"},
    )

    assert response.status_code == 200
    assert "<h1>Inventory</h1>" in response.body
    assert "13 g" in response.body
    material = app._material_service.get_material(authorization_header=header, material_id="mat-1")  # noqa: SLF001
    assert material is not None
    assert material.stock_on_hand == 13
