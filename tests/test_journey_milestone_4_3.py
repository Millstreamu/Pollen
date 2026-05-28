from pollen.app import create_app


def _auth_header(user_id: str, email: str) -> str:
    return f"Bearer user:{user_id}:{email}"


def test_create_start_complete_batch_journey_integrity() -> None:
    header = _auth_header("journey-4-3", "journey-4-3@example.com")
    app = create_app()

    app.post("/make-buy", authorization_header=header, form_data={"action": "create", "name": "Wax", "unit": "g", "stock_on_hand": "100", "reorder_point": "5"})
    app.post("/products-stock", authorization_header=header, form_data={"action": "create", "name": "Candle", "sku": "C-1", "stock_on_hand": "1", "reorder_point": "1"})
    app.post("/products-stock", authorization_header=header, form_data={"action": "create_recipe_item", "product_id": "prd-1", "material_id": "mat-1", "quantity_per_unit": "20"})

    create_response = app.post("/make-buy", authorization_header=header, form_data={"action": "create_batch", "product_id": "prd-1", "quantity": "3"})
    assert create_response.status_code == 200

    start_response = app.post("/make-buy", authorization_header=header, form_data={"action": "start_batch", "batch_id": "bat-1"})
    assert start_response.status_code == 200

    complete_response = app.post("/make-buy", authorization_header=header, form_data={"action": "complete_batch", "batch_id": "bat-1"})
    assert complete_response.status_code == 200

    product = app._product_service.get_product(authorization_header=header, product_id="prd-1")  # noqa: SLF001
    material = app._material_service.get_material(authorization_header=header, material_id="mat-1")  # noqa: SLF001
    batch = app._batch_service.list_batches(authorization_header=header)[0]  # noqa: SLF001
    assert product is not None and product.stock_on_hand == 4
    assert material is not None and material.stock_on_hand == 40
    assert batch.status == "complete"
    assert batch.started_at is not None
    assert batch.completed_at is not None

