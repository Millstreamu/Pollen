from pollen.services import MaterialService


def _auth_header(user_id: str, email: str) -> str:
    return f"Bearer user:{user_id}:{email}"


def test_create_material_uses_server_resolved_shop_scope() -> None:
    service = MaterialService()

    created = service.create_material(
        authorization_header=_auth_header("owner", "owner@example.com"),
        name="Soy Wax",
        unit="kg",
        stock_on_hand=10,
        reorder_point=3,
        requested_shop_id="shop-attacker",
    )

    assert created is not None
    assert created.shop_id == "shop-owner"


def test_edit_material_updates_fields_for_owner() -> None:
    service = MaterialService()
    header = _auth_header("owner", "owner@example.com")

    created = service.create_material(
        authorization_header=header,
        name="Wick",
        unit="pack",
        stock_on_hand=4,
        reorder_point=2,
    )
    assert created is not None

    updated = service.update_material(
        authorization_header=header,
        material_id=created.material_id,
        name="Cotton Wick",
        unit="packs",
        stock_on_hand=6,
        reorder_point=3,
    )

    assert updated is not None
    assert updated.name == "Cotton Wick"
    assert updated.unit == "packs"
    assert updated.stock_on_hand == 6
    assert updated.reorder_point == 3


def test_cross_shop_and_unauthenticated_material_access_denied() -> None:
    service = MaterialService()
    owner_header = _auth_header("owner", "owner@example.com")
    other_header = _auth_header("other", "other@example.com")

    created = service.create_material(
        authorization_header=owner_header,
        name="Jar",
        unit="each",
        stock_on_hand=20,
        reorder_point=5,
    )
    assert created is not None

    assert service.get_material(authorization_header=other_header, material_id=created.material_id) is None
    assert (
        service.update_material(
            authorization_header=other_header,
            material_id=created.material_id,
            name="Hack",
            unit="each",
            stock_on_hand=0,
            reorder_point=0,
        )
        is None
    )
    assert service.list_materials(authorization_header=None) == []


def test_low_stock_status_appears_correctly_for_materials() -> None:
    service = MaterialService()
    header = _auth_header("owner", "owner@example.com")

    healthy = service.create_material(
        authorization_header=header,
        name="Fragrance Oil",
        unit="ml",
        stock_on_hand=50,
        reorder_point=10,
    )
    low = service.create_material(
        authorization_header=header,
        name="Label",
        unit="each",
        stock_on_hand=10,
        reorder_point=10,
    )

    assert healthy is not None and low is not None
    assert not healthy.is_low_stock
    assert low.is_low_stock
