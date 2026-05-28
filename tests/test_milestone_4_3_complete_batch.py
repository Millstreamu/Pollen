from pollen.app import AppShell


def _auth_header(user_id: str = "complete-owner", email: str = "complete-owner@example.com") -> str:
    return f"Bearer user:{user_id}:{email}"


def _create_started_batch(app: AppShell, header: str) -> str:
    app.post("/products-stock", authorization_header=header, form_data={"action": "create", "name": "Candle", "sku": "C-1", "stock_on_hand": "5", "reorder_point": "1"})
    app.post("/make-buy", authorization_header=header, form_data={"action": "create", "name": "Wax", "unit": "g", "stock_on_hand": "200", "reorder_point": "10"})
    product = app._product_service.list_products(authorization_header=header)[0]  # noqa: SLF001
    material = app._material_service.list_materials(authorization_header=header)[0]  # noqa: SLF001
    app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "create_recipe_item", "product_id": product.product_id, "material_id": material.material_id, "quantity_per_unit": "10"},
    )
    app.post("/make-buy", authorization_header=header, form_data={"action": "create_batch", "product_id": product.product_id, "quantity": "2"})
    batch_id = app._batch_service.list_batches(authorization_header=header)[0].batch_id  # noqa: SLF001
    app.post("/make-buy", authorization_header=header, form_data={"action": "start_batch", "batch_id": batch_id})
    return batch_id


def test_complete_batch_updates_material_and_product_stock_and_status() -> None:
    header = _auth_header()
    app = AppShell()
    batch_id = _create_started_batch(app, header)
    product = app._product_service.list_products(authorization_header=header)[0]  # noqa: SLF001
    material = app._material_service.list_materials(authorization_header=header)[0]  # noqa: SLF001

    response = app.post("/make-buy", authorization_header=header, form_data={"action": "complete_batch", "batch_id": batch_id})
    assert response.status_code == 200

    updated_product = app._product_service.get_product(authorization_header=header, product_id=product.product_id)  # noqa: SLF001
    updated_material = app._material_service.get_material(authorization_header=header, material_id=material.material_id)  # noqa: SLF001
    updated_batch = app._batch_service.list_batches(authorization_header=header)[0]  # noqa: SLF001
    assert updated_product is not None and updated_product.stock_on_hand == 7
    assert updated_material is not None and updated_material.stock_on_hand == 180
    assert updated_batch.status == "complete"
    assert updated_batch.completed_at is not None


def test_complete_batch_blocks_invalid_transitions() -> None:
    header = _auth_header("complete-owner-2", "complete-owner-2@example.com")
    app = AppShell()
    batch_id = _create_started_batch(app, header)

    first = app.post("/make-buy", authorization_header=header, form_data={"action": "complete_batch", "batch_id": batch_id})
    assert first.status_code == 200
    second = app.post("/make-buy", authorization_header=header, form_data={"action": "complete_batch", "batch_id": batch_id})
    assert second.status_code == 400
    assert "Invalid batch transition" in second.body

