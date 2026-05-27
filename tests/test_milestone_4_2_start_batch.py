from pollen.app import AppShell


def _auth_header(user_id: str = "start-owner", email: str = "start-owner@example.com") -> str:
    return f"Bearer user:{user_id}:{email}"


def _create_planned_batch(app: AppShell, header: str) -> str:
    app.post("/products-stock", authorization_header=header, form_data={"action": "create", "name": "Candle", "sku": "C-1", "stock_on_hand": "5", "reorder_point": "1"})
    app.post("/make-buy", authorization_header=header, form_data={"action": "create", "name": "Wax", "unit": "g", "stock_on_hand": "200", "reorder_point": "10"})

    product = app._product_service.list_products(authorization_header=header)[0]  # noqa: SLF001
    material = app._material_service.list_materials(authorization_header=header)[0]  # noqa: SLF001

    app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "create_recipe_item", "product_id": product.product_id, "material_id": material.material_id, "quantity_per_unit": "10"},
    )
    response = app.post("/make-buy", authorization_header=header, form_data={"action": "create_batch", "product_id": product.product_id, "quantity": "2"})
    assert response.status_code == 200
    return app._batch_service.list_batches(authorization_header=header)[0].batch_id  # noqa: SLF001


def test_start_batch_transitions_planned_to_in_progress_with_timestamp() -> None:
    header = _auth_header()
    app = AppShell()

    batch_id = _create_planned_batch(app, header)
    response = app.post("/make-buy", authorization_header=header, form_data={"action": "start_batch", "batch_id": batch_id})
    assert response.status_code == 200

    started = app._batch_service.list_batches(authorization_header=header)[0]  # noqa: SLF001
    assert started.status == "in-progress"
    assert started.started_at is not None


def test_start_batch_blocks_invalid_transitions() -> None:
    header = _auth_header("start-owner-2", "start-owner-2@example.com")
    app = AppShell()

    batch_id = _create_planned_batch(app, header)
    first = app.post("/make-buy", authorization_header=header, form_data={"action": "start_batch", "batch_id": batch_id})
    assert first.status_code == 200

    second = app.post("/make-buy", authorization_header=header, form_data={"action": "start_batch", "batch_id": batch_id})
    assert second.status_code == 400
    assert "Invalid batch transition" in second.body
