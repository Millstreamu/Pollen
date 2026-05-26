from pollen.services import OrderService


def _auth_header(user_id: str, email: str) -> str:
    return f"Bearer user:{user_id}:{email}"


def test_create_order_uses_server_resolved_shop_scope() -> None:
    service = OrderService()

    created = service.create_order(
        authorization_header=_auth_header("owner", "owner@example.com"),
        customer_name="Owner Customer",
        items=[{"product_sku": "SKU-001", "quantity": 2}],
        requested_shop_id="shop-attacker",
    )

    assert created is not None
    assert created.shop_id == "shop-owner"


def test_list_orders_returns_only_current_shop_records() -> None:
    service = OrderService()
    owner_header = _auth_header("owner", "owner@example.com")
    other_header = _auth_header("other", "other@example.com")

    owner_order = service.create_order(
        authorization_header=owner_header,
        customer_name="Owner Customer",
        items=[{"product_sku": "SKU-001", "quantity": 1}],
    )
    other_order = service.create_order(
        authorization_header=other_header,
        customer_name="Other Customer",
        items=[{"product_sku": "SKU-002", "quantity": 1}],
    )

    owner_orders = service.list_orders(authorization_header=owner_header)

    assert owner_order is not None
    assert other_order is not None
    assert [order.order_id for order in owner_orders] == [owner_order.order_id]


def test_cross_shop_get_denied() -> None:
    service = OrderService()
    owner_header = _auth_header("owner", "owner@example.com")
    other_header = _auth_header("other", "other@example.com")

    owner_order = service.create_order(
        authorization_header=owner_header,
        customer_name="Owner Customer",
        items=[{"product_sku": "SKU-003", "quantity": 3}],
    )

    assert owner_order is not None
    assert service.get_order(authorization_header=owner_header, order_id=owner_order.order_id) is not None
    assert service.get_order(authorization_header=other_header, order_id=owner_order.order_id) is None


def test_unauthenticated_order_access_is_denied() -> None:
    service = OrderService()

    assert service.create_order(
        authorization_header=None,
        customer_name="No Auth",
        items=[{"product_sku": "SKU-001", "quantity": 1}],
    ) is None
    assert service.list_orders(authorization_header=None) == []
    assert service.get_order(authorization_header=None, order_id="ord-1") is None
