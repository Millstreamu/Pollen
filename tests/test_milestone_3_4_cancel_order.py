from pollen.app import AppShell
from pollen.services import OrderService, ProductService


def _auth_header(user_id: str = "owner", email: str = "owner@example.com") -> str:
    return f"Bearer user:{user_id}:{email}"


def test_cancel_releases_reserved_stock_and_writes_cancel_status() -> None:
    header = _auth_header("cancel-owner", "cancel-owner@example.com")
    product_service = ProductService()
    order_service = OrderService(product_repository=product_service._product_repository)  # noqa: SLF001

    product = product_service.create_product(
        authorization_header=header,
        name="Bundle",
        sku="B-1",
        stock_on_hand=8,
        reorder_point=2,
    )
    assert product is not None

    created = order_service.create_order(
        authorization_header=header,
        customer_name="Ivy",
        items=[{"product_sku": "B-1", "quantity": 3}],
    )
    assert created is not None
    assert created.status == "ready_to_pack"

    before_cancel = product_service.get_product(authorization_header=header, product_id=product.product_id)
    assert before_cancel is not None
    assert before_cancel.reserved_stock == 3

    cancelled = order_service.cancel_order(authorization_header=header, order_id=created.order_id)
    assert cancelled is not None
    assert cancelled.status == "cancelled"

    after_cancel = product_service.get_product(authorization_header=header, product_id=product.product_id)
    assert after_cancel is not None
    assert after_cancel.stock_on_hand == 8
    assert after_cancel.reserved_stock == 0


def test_cannot_cancel_shipped_order() -> None:
    header = _auth_header("cancel-shipped", "cancel-shipped@example.com")
    product_service = ProductService()
    order_service = OrderService(product_repository=product_service._product_repository)  # noqa: SLF001

    product_service.create_product(
        authorization_header=header,
        name="Tin",
        sku="T-1",
        stock_on_hand=5,
        reorder_point=1,
    )
    created = order_service.create_order(
        authorization_header=header,
        customer_name="Max",
        items=[{"product_sku": "T-1", "quantity": 2}],
    )
    assert created is not None

    packed = order_service.mark_order_packed(authorization_header=header, order_id=created.order_id)
    assert packed is not None
    shipped = order_service.mark_order_shipped(authorization_header=header, order_id=created.order_id)
    assert shipped is not None

    assert order_service.cancel_order(authorization_header=header, order_id=created.order_id) is None


def test_orders_page_supports_cancel_action() -> None:
    header = _auth_header("cancel-ui", "cancel-ui@example.com")
    product_service = ProductService()
    app = AppShell(product_service=product_service)

    app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "create", "name": "Soap", "sku": "S-2", "stock_on_hand": "4", "reorder_point": "1"},
    )
    created_response = app.post(
        "/orders",
        authorization_header=header,
        form_data={"customer_name": "Kim", "product_sku": "S-2", "quantity": "2"},
    )
    assert created_response.status_code == 200

    cancel_response = app.post(
        "/orders",
        authorization_header=header,
        form_data={"action": "cancel", "order_id": "ord-1"},
    )
    assert cancel_response.status_code == 200
    assert "Cancelled" in cancel_response.body

    invalid_transition = app.post(
        "/orders",
        authorization_header=header,
        form_data={"action": "cancel", "order_id": "ord-1"},
    )
    assert invalid_transition.status_code == 400
    assert "Invalid order transition" in invalid_transition.body
