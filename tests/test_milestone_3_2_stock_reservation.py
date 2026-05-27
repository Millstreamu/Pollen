from pollen.services import OrderService, ProductService


def _auth_header(user_id: str = "owner", email: str = "owner@example.com") -> str:
    return f"Bearer user:{user_id}:{email}"


def test_order_creation_reserves_stock_when_available() -> None:
    header = _auth_header()
    product_service = ProductService()
    created_product = product_service.create_product(
        authorization_header=header,
        name="Candle",
        sku="CNDL-1",
        stock_on_hand=5,
        reorder_point=1,
    )
    assert created_product is not None

    service = OrderService(product_repository=product_service._product_repository)  # noqa: SLF001
    created_order = service.create_order(
        authorization_header=header,
        customer_name="Alice",
        items=[{"product_sku": "CNDL-1", "quantity": 2}],
    )

    assert created_order is not None
    assert created_order.status == "ready_to_pack"
    updated_product = product_service.get_product(
        authorization_header=header,
        product_id=created_product.product_id,
    )
    assert updated_product is not None
    assert updated_product.reserved_stock == 2
    assert updated_product.available_stock == 3


def test_insufficient_stock_does_not_overallocate_reservations() -> None:
    header = _auth_header()
    product_service = ProductService()
    created_product = product_service.create_product(
        authorization_header=header,
        name="Mug",
        sku="MUG-1",
        stock_on_hand=1,
        reorder_point=1,
    )
    assert created_product is not None

    service = OrderService(product_repository=product_service._product_repository)  # noqa: SLF001
    created_order = service.create_order(
        authorization_header=header,
        customer_name="Bob",
        items=[{"product_sku": "MUG-1", "quantity": 4}],
    )

    assert created_order is not None
    assert created_order.status == "waiting_on_stock"
    unchanged_product = product_service.get_product(
        authorization_header=header,
        product_id=created_product.product_id,
    )
    assert unchanged_product is not None
    assert unchanged_product.reserved_stock == 0
    assert unchanged_product.available_stock == 1


def test_available_stock_calculation_considers_existing_reservations() -> None:
    header = _auth_header()
    product_service = ProductService()
    created_product = product_service.create_product(
        authorization_header=header,
        name="Bundle",
        sku="BNDL-1",
        stock_on_hand=6,
        reorder_point=1,
    )
    assert created_product is not None

    service = OrderService(product_repository=product_service._product_repository)  # noqa: SLF001
    first_order = service.create_order(
        authorization_header=header,
        customer_name="First",
        items=[{"product_sku": "BNDL-1", "quantity": 4}],
    )
    second_order = service.create_order(
        authorization_header=header,
        customer_name="Second",
        items=[{"product_sku": "BNDL-1", "quantity": 3}],
    )

    assert first_order is not None
    assert first_order.status == "ready_to_pack"
    assert second_order is not None
    assert second_order.status == "waiting_on_stock"

    updated_product = product_service.get_product(
        authorization_header=header,
        product_id=created_product.product_id,
    )
    assert updated_product is not None
    assert updated_product.reserved_stock == 4
    assert updated_product.available_stock == 2
