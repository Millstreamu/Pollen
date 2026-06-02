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


def test_create_material_stores_optional_supplier_and_notes() -> None:
    service = MaterialService()
    header = _auth_header("supplier-owner", "supplier@example.com")

    created = service.create_material(
        authorization_header=header,
        name="Lavender Oil",
        unit="ml",
        stock_on_hand=30,
        reorder_point=10,
        supplier="Botanical Supply",
        notes="Keep away from sunlight",
    )

    assert created is not None
    assert created.supplier == "Botanical Supply"
    assert created.notes == "Keep away from sunlight"


def test_create_material_rejects_missing_required_fields() -> None:
    service = MaterialService()
    header = _auth_header("required-owner", "required@example.com")

    created = service.create_material(
        authorization_header=header,
        name="",
        unit="g",
        stock_on_hand=1,
        reorder_point=0,
    )

    assert created is None
    assert service.list_materials(authorization_header=header) == []


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


def test_low_stock_suggestions_and_purchase_draft_flow() -> None:
    service = MaterialService()
    header = _auth_header("owner-buy", "buy@example.com")
    low = service.create_material(
        authorization_header=header,
        name="Fragrance",
        unit="ml",
        stock_on_hand=3,
        reorder_point=10,
    )
    assert low is not None

    suggestions = service.list_low_stock_suggestions(authorization_header=header)
    assert len(suggestions) == 1
    assert suggestions[0]["material_id"] == low.material_id
    assert suggestions[0]["suggested_quantity"] == 17

    added = service.add_to_purchase_draft(authorization_header=header, material_id=low.material_id)
    assert added is True
    draft = service.list_purchase_draft(authorization_header=header)
    assert [row.material_id for row in draft] == [low.material_id]


def test_archive_restore_and_list_scoping_for_materials() -> None:
    service = MaterialService()
    owner_header = _auth_header("owner2", "owner2@example.com")
    other_header = _auth_header("other2", "other2@example.com")

    created = service.create_material(
        authorization_header=owner_header,
        name="Pigment",
        unit="g",
        stock_on_hand=12,
        reorder_point=4,
    )
    assert created is not None

    archived = service.archive_material(authorization_header=owner_header, material_id=created.material_id)
    assert archived is not None
    assert not archived.is_active
    assert service.list_materials(authorization_header=owner_header) == []
    assert len(service.list_materials(authorization_header=owner_header, include_archived=True)) == 1

    assert service.restore_material(authorization_header=other_header, material_id=created.material_id) is None
    restored = service.restore_material(authorization_header=owner_header, material_id=created.material_id)
    assert restored is not None
    assert restored.is_active
    assert [material.material_id for material in service.list_materials(authorization_header=owner_header)] == [
        created.material_id
    ]
