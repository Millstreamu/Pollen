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
    assert purchase.status == "Ordered"
    assert purchase.supplier == "Acme Supply"
    assert purchase.expected_date == "2026-06-10"
    assert service.list_purchase_draft(authorization_header=header) == []
    after_material = service.get_material(authorization_header=header, material_id=material.material_id)
    assert after_material is not None
    assert after_material.stock_on_hand == before_stock


def test_inventory_ui_shows_incoming_purchases_list() -> None:
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
        "/products-stock",
        authorization_header=header,
        form_data={
            "action": "create_purchase",
            "supplier": "Northwind",
            "expected_date": "2026-06-30",
            "status": "draft",
            "item_reference": "material:mat-1",
        },
    )
    assert response.status_code == 200
    assert "Incoming Purchases" in response.body
    assert "Created purchases" not in response.body
    assert "pur-1" in response.body
    assert "Draft" in response.body
    assert "Northwind" in response.body


def test_inventory_create_purchase_dialog_selects_existing_material_or_product() -> None:
    app = create_app()
    header = _auth_header("p52-dialog", "p52-dialog@example.com")
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create_product",
            "name": "Candle",
            "sku": "CAN-1",
            "stock_on_hand": "1",
            "reorder_point": "3",
            "sale_price": "12",
            "default_batch_size": "4",
            "workflow_status": "Active",
        },
    )
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create", "name": "Wax", "unit": "lb", "stock_on_hand": "2", "reorder_point": "5"},
    )

    response = app.get("/products-stock#create-purchase-dialog", authorization_header=header)

    assert response.status_code == 200
    assert "Item to purchase" in response.body
    assert "<select name='item_reference' required>" in response.body
    assert "Product — Candle" in response.body
    assert "Material — Wax" in response.body
    assert "<input type='date' name='expected_date'>" in response.body


def test_inventory_purchase_can_receive_finished_product() -> None:
    app = create_app()
    header = _auth_header("p52-product", "p52-product@example.com")
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create_product",
            "name": "Restock Candle",
            "sku": "RESTOCK",
            "stock_on_hand": "1",
            "reorder_point": "3",
            "sale_price": "15",
            "default_batch_size": "4",
            "workflow_status": "Active",
        },
    )

    created = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={
            "action": "create_purchase",
            "item_reference": "product:prd-1",
            "supplier": "Finished Goods Co",
            "expected_date": "2026-07-01",
            "status": "ordered",
        },
    )
    assert created.status_code == 200
    assert "Finished Goods Co" in created.body

    received = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "receive_purchase", "purchase_id": "pur-1"},
    )

    assert received.status_code == 200
    product = app._product_service.get_product(authorization_header=header, product_id="prd-1")  # noqa: SLF001
    assert product is not None
    assert product.stock_on_hand == 6
