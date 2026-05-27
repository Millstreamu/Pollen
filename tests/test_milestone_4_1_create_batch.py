from pollen.app import AppShell


def _auth_header(user_id: str = "batch-owner", email: str = "batch-owner@example.com") -> str:
    return f"Bearer user:{user_id}:{email}"


def test_create_batch_succeeds_without_stock_mutation() -> None:
    header = _auth_header()
    app = AppShell()

    app.post("/products-stock", authorization_header=header, form_data={"action": "create", "name": "Candle", "sku": "C-1", "stock_on_hand": "5", "reorder_point": "1"})
    app.post("/make-buy", authorization_header=header, form_data={"action": "create", "name": "Wax", "unit": "g", "stock_on_hand": "200", "reorder_point": "10"})

    product = app._product_service.list_products(authorization_header=header)[0]  # noqa: SLF001
    material = app._material_service.list_materials(authorization_header=header)[0]  # noqa: SLF001

    recipe_response = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "create_recipe_item", "product_id": product.product_id, "material_id": material.material_id, "quantity_per_unit": "20"},
    )
    assert recipe_response.status_code == 200

    before_product = app._product_service.get_product(authorization_header=header, product_id=product.product_id)  # noqa: SLF001
    before_material = app._material_service.get_material(authorization_header=header, material_id=material.material_id)  # noqa: SLF001
    response = app.post("/make-buy", authorization_header=header, form_data={"action": "create_batch", "product_id": product.product_id, "quantity": "3"})
    assert response.status_code == 200

    after_product = app._product_service.get_product(authorization_header=header, product_id=product.product_id)  # noqa: SLF001
    after_material = app._material_service.get_material(authorization_header=header, material_id=material.material_id)  # noqa: SLF001
    assert before_product == after_product
    assert before_material == after_material


def test_create_batch_blocks_when_materials_insufficient() -> None:
    header = _auth_header("batch-low", "batch-low@example.com")
    app = AppShell()

    app.post("/products-stock", authorization_header=header, form_data={"action": "create", "name": "Soap", "sku": "S-1", "stock_on_hand": "1", "reorder_point": "1"})
    app.post("/make-buy", authorization_header=header, form_data={"action": "create", "name": "Oil", "unit": "ml", "stock_on_hand": "30", "reorder_point": "5"})

    product = app._product_service.list_products(authorization_header=header)[0]  # noqa: SLF001
    material = app._material_service.list_materials(authorization_header=header)[0]  # noqa: SLF001

    app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "create_recipe_item", "product_id": product.product_id, "material_id": material.material_id, "quantity_per_unit": "20"},
    )

    response = app.post("/make-buy", authorization_header=header, form_data={"action": "create_batch", "product_id": product.product_id, "quantity": "2"})
    assert response.status_code == 400
    assert "Insufficient materials" in response.body
