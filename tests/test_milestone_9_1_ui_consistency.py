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
