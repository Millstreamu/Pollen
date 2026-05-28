from pollen.app import create_app
from pollen.services import MaterialService


def _auth_header(user_id: str = "u1", email: str = "maker@example.com") -> str:
    return f"Bearer user:{user_id}:{email}"


def test_create_purchase_persists_and_does_not_mutate_stock() -> None:
    service = MaterialService()
    header = _auth_header("p52", "p52@example.com")
    material = service.create_material(
        authorization_header=header,
        name="Wick",
        unit="each",
        stock_on_hand=1,
        reorder_point=4,
    )
    assert material is not None
    before_stock = material.stock_on_hand
    assert service.add_to_purchase_draft(authorization_header=header, material_id=material.material_id)

    purchase = service.create_purchase_from_draft(
        authorization_header=header,
        supplier="Acme Supply",
        expected_date="2026-06-10",
        status="ordered",
    )
    assert purchase is not None
    assert purchase.status == "ordered"
    assert purchase.supplier == "Acme Supply"
    assert purchase.expected_date == "2026-06-10"
    assert service.list_purchase_draft(authorization_header=header) == []
    after_material = service.get_material(authorization_header=header, material_id=material.material_id)
    assert after_material is not None
    assert after_material.stock_on_hand == before_stock


def test_make_buy_ui_shows_created_purchases_list() -> None:
    app = create_app()
    header = _auth_header("p52-ui", "p52-ui@example.com")
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create", "name": "Jar", "unit": "each", "stock_on_hand": "1", "reorder_point": "3"},
    )
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "add_to_purchase", "material_id": "mat-1"},
    )
    response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create_purchase",
            "supplier": "Northwind",
            "expected_date": "2026-06-30",
            "status": "draft",
        },
    )
    assert response.status_code == 200
    assert "Created purchases" in response.body
    assert "pur-1" in response.body
    assert "draft" in response.body
    assert "Northwind" in response.body
