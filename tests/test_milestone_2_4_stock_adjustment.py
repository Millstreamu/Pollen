from pollen.app import create_app
from pollen.services import MaterialService, ProductService


def _auth_header(user_id: str, email: str) -> str:
    return f"Bearer user:{user_id}:{email}"


def test_material_adjustment_requires_reason_and_blocks_negative() -> None:
    service = MaterialService()
    header = _auth_header("owner", "owner@example.com")
    created = service.create_material(
        authorization_header=header,
        name="Wax",
        unit="g",
        stock_on_hand=10,
        reorder_point=2,
    )
    assert created is not None
    assert service.adjust_material_stock(authorization_header=header, material_id=created.material_id, delta=2, reason="") is None
    assert service.adjust_material_stock(authorization_header=header, material_id=created.material_id, delta=-11, reason="count") is None

    updated = service.adjust_material_stock(
        authorization_header=header,
        material_id=created.material_id,
        delta=-3,
        reason="cycle count",
    )
    assert updated is not None
    assert updated.stock_on_hand == 7
    assert len(service.list_inventory_movements(authorization_header=header)) == 1
    assert len(service.list_activity_logs(authorization_header=header)) == 1


def test_product_adjustment_creates_audit_records() -> None:
    service = ProductService()
    header = _auth_header("owner", "owner@example.com")
    created = service.create_product(
        authorization_header=header,
        name="Candle",
        sku="C-1",
        stock_on_hand=4,
        reorder_point=1,
    )
    assert created is not None
    updated = service.adjust_product_stock(
        authorization_header=header,
        product_id=created.product_id,
        delta=5,
        reason="found box",
    )
    assert updated is not None
    assert updated.stock_on_hand == 9
    movement = service.list_inventory_movements(authorization_header=header)[0]
    assert movement.before_quantity == 4
    assert movement.after_quantity == 9


def test_milestone_2_4_journey_material_adjustment_and_audit_visible() -> None:
    header = _auth_header("journey24", "journey24@example.com")
    app = create_app()
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create", "name": "Dye", "unit": "ml", "stock_on_hand": "8", "reorder_point": "3"},
    )
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "adjust_stock", "material_id": "mat-1", "delta": "4", "reason": "received spare"},
    )
    page = app.get("/make-buy", authorization_header=header)
    assert page.status_code == 200
    assert "Inventory movements" not in page.body
    assert "Activity log" not in page.body
    material = app._material_service.get_material(authorization_header=header, material_id="mat-1")  # noqa: SLF001
    assert material is not None
    assert material.stock_on_hand == 12
    movements = app._material_service.list_inventory_movements(authorization_header=header)  # noqa: SLF001
    activities = app._material_service.list_activity_logs(authorization_header=header)  # noqa: SLF001
    assert movements[0].reason == "received spare"
    assert activities[0].message == "Adjusted material stock by 4: received spare"
