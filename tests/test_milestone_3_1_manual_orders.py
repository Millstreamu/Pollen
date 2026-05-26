from pollen.app import AppShell
from pollen.services import OrderService, ProductService


def _auth_header(user_id: str = "owner", email: str = "owner@example.com") -> str:
    return f"Bearer user:{user_id}:{email}"


def test_create_manual_order_defaults_source_and_ready_status_when_stock_available() -> None:
    header = _auth_header()
    product_service = ProductService()
    product_service.create_product(
        authorization_header=header,
        name="Candle",
        sku="CNDL-1",
        stock_on_hand=5,
        reorder_point=1,
    )
    service = OrderService(product_repository=product_service._product_repository)  # noqa: SLF001

    created = service.create_order(
        authorization_header=header,
        customer_name="Alice",
        items=[{"product_sku": "CNDL-1", "quantity": 2}],
    )

    assert created is not None
    assert created.source == "manual"
    assert created.status == "ready_to_pack"
    items = service.list_order_items(authorization_header=header, order_id=created.order_id)
    assert len(items) == 1
    assert items[0].shop_id == created.shop_id


def test_create_manual_order_waiting_on_stock_when_insufficient() -> None:
    header = _auth_header()
    product_service = ProductService()
    product_service.create_product(
        authorization_header=header,
        name="Mug",
        sku="MUG-1",
        stock_on_hand=1,
        reorder_point=1,
    )
    service = OrderService(product_repository=product_service._product_repository)  # noqa: SLF001

    created = service.create_order(
        authorization_header=header,
        customer_name="Bob",
        items=[{"product_sku": "MUG-1", "quantity": 4}],
    )

    assert created is not None
    assert created.status == "waiting_on_stock"


def test_orders_page_manual_creation_flow_shows_order_in_list() -> None:
    header = _auth_header("ui-owner", "ui-owner@example.com")
    product_service = ProductService()
    product_service.create_product(
        authorization_header=header,
        name="Bundle",
        sku="BNDL-1",
        stock_on_hand=10,
        reorder_point=2,
    )
    app = AppShell(product_service=product_service)

    response = app.post(
        "/orders",
        authorization_header=header,
        form_data={
            "customer_name": "Chris",
            "product_sku": "BNDL-1",
            "quantity": "3",
        },
    )

    assert response.status_code == 200
    assert "Chris" in response.body
    assert "manual" in response.body
    assert "ready_to_pack" in response.body
