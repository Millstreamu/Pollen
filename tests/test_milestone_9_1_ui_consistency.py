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
        "/products-stock",
        authorization_header=header,
        form_data={"action": "create", "name": "Soap", "sku": "SOAP-1", "stock_on_hand": "3", "reorder_point": "1"},
    )

    response = app.get("/products-stock", authorization_header=header)

    assert response.status_code == 200
    assert "<h3>View</h3>" in response.body
    assert "<h3>Add product</h3>" in response.body
    assert "<h3>Bulk actions</h3>" in response.body
    assert "Show active" in response.body
    assert "Show archived" in response.body
    assert "Show all" in response.body
    assert "<button type='submit'>Save product</button>" in response.body
    assert "<button type='submit' name='action' value='bulk_archive'>Archive products</button>" in response.body


def test_make_buy_page_uses_beginner_friendly_sections_and_empty_state_guidance() -> None:
    header = _auth_header("make-buy-ui", "make-buy-ui@example.com")
    app = AppShell()

    response = app.get("/make-buy", authorization_header=header)

    assert response.status_code == 200
    assert "<h3>Add material</h3>" in response.body
    assert "<h3>Plan a batch</h3>" in response.body
    assert "<button type='submit'>Save material</button>" in response.body
    assert "<button type='submit'>Save batch plan</button>" in response.body
    assert "No low materials right now. Add materials and reorder points to unlock suggestions." in response.body
    assert "<button type='submit'>Save purchase</button>" in response.body


def test_money_page_uses_beginner_friendly_consistency_sections_and_empty_state() -> None:
    header = _auth_header("money-ui", "money-ui@example.com")
    app = AppShell()

    response = app.get("/money", authorization_header=header)

    assert response.status_code == 200
    assert "<h3>Money overview</h3>" in response.body
    assert "<h3>Estimated profit and cost</h3>" in response.body
    assert "<h3>Next steps</h3>" in response.body
    assert "No money data yet. Finish a few orders and purchases to unlock estimated totals." in response.body
    assert "<button type='button' disabled>View estimates</button>" in response.body


def test_settings_page_uses_beginner_friendly_consistency_sections_and_empty_state() -> None:
    header = _auth_header("settings-ui", "settings-ui@example.com")
    app = AppShell()

    response = app.get("/settings", authorization_header=header)

    assert response.status_code == 200
    assert "<h3>Shop settings</h3>" in response.body
    assert "<h3>Sales channels</h3>" in response.body
    assert "<h3>Next steps</h3>" in response.body
    assert "No connected sales channels yet. Add one when you are ready to import orders." in response.body
    assert "<button type='button' disabled>Save settings</button>" in response.body
    assert "<button type='button' disabled>Connect channel</button>" in response.body
