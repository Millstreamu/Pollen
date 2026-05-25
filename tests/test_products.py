from pollen.services import ProductService


def _auth_header(user_id: str, email: str) -> str:
    return f"Bearer user:{user_id}:{email}"


def test_create_product_uses_server_resolved_shop_scope() -> None:
    service = ProductService()

    created = service.create_product(
        authorization_header=_auth_header("owner", "owner@example.com"),
        name="Small Candle",
        sku="CNDL-001",
        stock_on_hand=10,
        reorder_point=3,
        requested_shop_id="shop-attacker",
    )

    assert created is not None
    assert created.shop_id == "shop-owner"


def test_edit_product_updates_fields_for_owner() -> None:
    service = ProductService()
    header = _auth_header("owner", "owner@example.com")

    created = service.create_product(
        authorization_header=header,
        name="Small Candle",
        sku="CNDL-001",
        stock_on_hand=10,
        reorder_point=3,
    )
    assert created is not None

    updated = service.update_product(
        authorization_header=header,
        product_id=created.product_id,
        name="Large Candle",
        sku="CNDL-002",
        stock_on_hand=7,
        reorder_point=5,
    )

    assert updated is not None
    assert updated.name == "Large Candle"
    assert updated.sku == "CNDL-002"
    assert updated.stock_on_hand == 7
    assert updated.reorder_point == 5


def test_list_products_returns_only_current_shop_records() -> None:
    service = ProductService()
    owner_header = _auth_header("owner", "owner@example.com")
    other_header = _auth_header("other", "other@example.com")

    owner_product = service.create_product(
        authorization_header=owner_header,
        name="Owner Product",
        sku="OWN-001",
        stock_on_hand=4,
        reorder_point=2,
    )
    other_product = service.create_product(
        authorization_header=other_header,
        name="Other Product",
        sku="OTH-001",
        stock_on_hand=4,
        reorder_point=2,
    )

    owner_products = service.list_products(authorization_header=owner_header)

    assert owner_product is not None
    assert other_product is not None
    assert [product.product_id for product in owner_products] == [owner_product.product_id]


def test_archive_product_hides_from_default_listing() -> None:
    service = ProductService()
    header = _auth_header("owner", "owner@example.com")

    created = service.create_product(
        authorization_header=header,
        name="Starter Kit",
        sku="KIT-001",
        stock_on_hand=2,
        reorder_point=1,
    )
    assert created is not None

    archived = service.archive_product(authorization_header=header, product_id=created.product_id)
    assert archived is not None
    assert not archived.is_active

    visible = service.list_products(authorization_header=header)
    all_records = service.list_products(authorization_header=header, include_archived=True)

    assert visible == []
    assert [record.product_id for record in all_records] == [created.product_id]


def test_low_stock_status_appears_correctly() -> None:
    service = ProductService()
    header = _auth_header("owner", "owner@example.com")

    healthy = service.create_product(
        authorization_header=header,
        name="Healthy Stock",
        sku="HLT-001",
        stock_on_hand=6,
        reorder_point=3,
    )
    low = service.create_product(
        authorization_header=header,
        name="Low Stock",
        sku="LOW-001",
        stock_on_hand=3,
        reorder_point=3,
    )

    assert healthy is not None
    assert low is not None
    assert not healthy.is_low_stock
    assert low.is_low_stock


def test_cross_shop_product_access_denied() -> None:
    service = ProductService()
    owner_header = _auth_header("owner", "owner@example.com")
    other_header = _auth_header("other", "other@example.com")

    created = service.create_product(
        authorization_header=owner_header,
        name="Protected",
        sku="PRT-001",
        stock_on_hand=9,
        reorder_point=2,
    )
    assert created is not None

    assert service.get_product(authorization_header=other_header, product_id=created.product_id) is None
    assert (
        service.update_product(
            authorization_header=other_header,
            product_id=created.product_id,
            name="Hacked",
            sku="HCK-001",
            stock_on_hand=0,
            reorder_point=0,
        )
        is None
    )
    assert service.archive_product(authorization_header=other_header, product_id=created.product_id) is None


def test_unauthenticated_product_access_is_denied() -> None:
    service = ProductService()

    assert (
        service.create_product(
            authorization_header=None,
            name="No Auth",
            sku="NO-001",
            stock_on_hand=1,
            reorder_point=1,
        )
        is None
    )
    assert service.list_products(authorization_header=None) == []
    assert service.get_product(authorization_header=None, product_id="prd-1") is None


def test_restore_product_makes_archived_product_visible_again() -> None:
    service = ProductService()
    header = _auth_header("owner", "owner@example.com")

    created = service.create_product(
        authorization_header=header,
        name="Restorable",
        sku="RST-001",
        stock_on_hand=5,
        reorder_point=2,
    )
    assert created is not None

    service.archive_product(authorization_header=header, product_id=created.product_id)
    restored = service.restore_product(authorization_header=header, product_id=created.product_id)

    assert restored is not None
    assert restored.is_active
    assert [p.product_id for p in service.list_products(authorization_header=header)] == [created.product_id]
