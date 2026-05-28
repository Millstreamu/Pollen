from pollen.app import AppShell
from pollen.services import OrderService, ProductService


def _auth_header(user_id: str = "owner", email: str = "owner@example.com") -> str:
    return f"Bearer user:{user_id}:{email}"


def test_pack_and_ship_valid_transitions_and_no_double_deduct() -> None:
    product_service = ProductService()
    order_service = OrderService(product_repository=product_service._product_repository)  # noqa: SLF001
    header = _auth_header("pack-owner", "pack-owner@example.com")

    product = product_service.create_product(
        authorization_header=header,
        name="Candle",
        sku="C-1",
        stock_on_hand=10,
        reorder_point=2,
    )
    assert product is not None

    created = order_service.create_order(
        authorization_header=header,
        customer_name="Ari",
        items=[{"product_sku": "C-1", "quantity": 3}],
    )
    assert created is not None
    assert created.status == "ready_to_pack"

    packed = order_service.mark_order_packed(authorization_header=header, order_id=created.order_id)
    assert packed is not None
    assert packed.status == "packed"

    shipped = order_service.mark_order_shipped(authorization_header=header, order_id=created.order_id)
    assert shipped is not None
    assert shipped.status == "shipped"

    updated_product = product_service.get_product(authorization_header=header, product_id=product.product_id)
    assert updated_product is not None
    assert updated_product.stock_on_hand == 7
    assert updated_product.reserved_stock == 0

    shipped_again = order_service.mark_order_shipped(authorization_header=header, order_id=created.order_id)
    assert shipped_again is None

    after_retry_product = product_service.get_product(authorization_header=header, product_id=product.product_id)
    assert after_retry_product is not None
    assert after_retry_product.stock_on_hand == 7
    assert after_retry_product.reserved_stock == 0


def test_invalid_pack_ship_transitions_are_blocked() -> None:
    product_service = ProductService()
    order_service = OrderService(product_repository=product_service._product_repository)  # noqa: SLF001
    header = _auth_header("pack-invalid", "pack-invalid@example.com")

    product_service.create_product(
        authorization_header=header,
        name="Mug",
        sku="M-1",
        stock_on_hand=2,
        reorder_point=1,
    )
    waiting = order_service.create_order(
        authorization_header=header,
        customer_name="Jo",
        items=[{"product_sku": "M-1", "quantity": 5}],
    )
    assert waiting is not None
    assert waiting.status == "waiting_on_stock"

    assert order_service.mark_order_packed(authorization_header=header, order_id=waiting.order_id) is None
    assert order_service.mark_order_shipped(authorization_header=header, order_id=waiting.order_id) is None


def test_orders_page_supports_pack_and_ship_actions() -> None:
    header = _auth_header("pack-ui", "pack-ui@example.com")
    product_service = ProductService()
    app = AppShell(product_service=product_service)

    app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "create", "name": "Soap", "sku": "S-1", "stock_on_hand": "4", "reorder_point": "1"},
    )
    created_response = app.post(
        "/orders",
        authorization_header=header,
        form_data={"customer_name": "Kim", "product_sku": "S-1", "quantity": "2"},
    )
    assert created_response.status_code == 200
    assert "Ready to pack" in created_response.body

    pack_response = app.post(
        "/orders",
        authorization_header=header,
        form_data={"action": "pack", "order_id": "ord-1"},
    )
    assert pack_response.status_code == 200
    assert "Packed" in pack_response.body

    ship_response = app.post(
        "/orders",
        authorization_header=header,
        form_data={"action": "ship", "order_id": "ord-1"},
    )
    assert ship_response.status_code == 200
    assert "Shipped" in ship_response.body

    invalid_transition = app.post(
        "/orders",
        authorization_header=header,
        form_data={"action": "ship", "order_id": "ord-1"},
    )
    assert invalid_transition.status_code == 400
    assert "Invalid order transition" in invalid_transition.body
