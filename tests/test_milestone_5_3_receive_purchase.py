from pollen.services import MaterialService


def _auth_header(user_id: str = "u1", email: str = "maker@example.com") -> str:
    return f"Bearer user:{user_id}:{email}"


def test_receive_purchase_increases_stock_and_creates_logs() -> None:
    service = MaterialService()
    header = _auth_header("p53", "p53@example.com")
    material = service.create_material(
        authorization_header=header,
        name="Wax",
        unit="kg",
        stock_on_hand=2,
        reorder_point=4,
    )
    assert material is not None
    assert service.add_to_purchase_draft(authorization_header=header, material_id=material.material_id)
    purchase = service.create_purchase_from_draft(
        authorization_header=header,
        supplier="Acme",
        expected_date="2026-06-15",
        status="ordered",
    )
    assert purchase is not None

    updated_purchase = service.receive_purchase(
        authorization_header=header,
        purchase_id=purchase.purchase_id,
    )
    assert updated_purchase is not None
    assert updated_purchase.status == "Received"

    updated_material = service.get_material(authorization_header=header, material_id=material.material_id)
    assert updated_material is not None
    assert updated_material.stock_on_hand == 8

    movements = service.list_inventory_movements(authorization_header=header)
    assert len(movements) == 1
    assert movements[0].reason == "purchase_received"
    assert movements[0].delta == 6

    activities = service.list_activity_logs(authorization_header=header)
    assert len(activities) == 1
    assert activities[0].activity_type == "purchase_received"
    assert purchase.purchase_id in activities[0].message


def test_receive_purchase_twice_is_blocked() -> None:
    service = MaterialService()
    header = _auth_header("p53-double", "p53-double@example.com")
    material = service.create_material(
        authorization_header=header,
        name="Ribbon",
        unit="roll",
        stock_on_hand=1,
        reorder_point=2,
    )
    assert material is not None
    assert service.add_to_purchase_draft(authorization_header=header, material_id=material.material_id)
    purchase = service.create_purchase_from_draft(
        authorization_header=header,
        supplier=None,
        expected_date=None,
        status="ordered",
    )
    assert purchase is not None

    first = service.receive_purchase(authorization_header=header, purchase_id=purchase.purchase_id)
    second = service.receive_purchase(authorization_header=header, purchase_id=purchase.purchase_id)
    assert first is not None
    assert second is None
