from pollen.app import create_app


def _auth_header(user_id: str, email: str) -> str:
    return f"Bearer user:{user_id}:{email}"


def test_order_fulfillment_to_make_and_buy_replenishment_journey() -> None:
    """Exercise the core seller loop across orders, stock, make, buy, and Today."""
    header = _auth_header("journey-10-1", "journey-10-1@example.com")
    app = create_app()

    product_response = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={
            "action": "create",
            "name": "Lavender Candle",
            "sku": "LC-1",
            "stock_on_hand": "3",
            "reorder_point": "1",
        },
    )
    assert product_response.status_code == 200
    material_response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create",
            "name": "Soy Wax",
            "unit": "g",
            "stock_on_hand": "20",
            "reorder_point": "10",
        },
    )
    assert material_response.status_code == 200

    product = app._product_service.list_products(authorization_header=header)[0]  # noqa: SLF001
    material = app._material_service.list_materials(authorization_header=header)[0]  # noqa: SLF001
    app.post(
        "/products-stock",
        authorization_header=header,
        form_data={
            "action": "create_recipe_item",
            "product_id": product.product_id,
            "material_id": material.material_id,
            "quantity_per_unit": "5",
        },
    )

    order_response = app.post(
        "/orders",
        authorization_header=header,
        form_data={"customer_name": "Ari Buyer", "product_sku": product.sku, "quantity": "2"},
    )
    assert order_response.status_code == 200
    assert "Ready to pack" in order_response.body

    reserved_product = app._product_service.get_product(  # noqa: SLF001
        authorization_header=header,
        product_id=product.product_id,
    )
    assert reserved_product is not None
    assert reserved_product.stock_on_hand == 3
    assert reserved_product.reserved_stock == 2
    assert reserved_product.available_stock == 1

    today_after_order = app.get("/", authorization_header=header)
    assert today_after_order.status_code == 200
    assert "Orders to pack: 1" in today_after_order.body
    assert "Low stock: 1" in today_after_order.body

    pack_response = app.post(
        "/orders",
        authorization_header=header,
        form_data={"action": "pack", "order_id": "ord-1"},
    )
    assert pack_response.status_code == 200
    assert "Packed" in pack_response.body
    ship_response = app.post(
        "/orders",
        authorization_header=header,
        form_data={"action": "ship", "order_id": "ord-1"},
    )
    assert ship_response.status_code == 200
    assert "Shipped" in ship_response.body

    shipped_product = app._product_service.get_product(  # noqa: SLF001
        authorization_header=header,
        product_id=product.product_id,
    )
    assert shipped_product is not None
    assert shipped_product.stock_on_hand == 1
    assert shipped_product.reserved_stock == 0

    create_batch_response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create_batch", "product_id": product.product_id, "quantity": "2"},
    )
    assert create_batch_response.status_code == 200
    start_batch_response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "start_batch", "batch_id": "bat-1"},
    )
    assert start_batch_response.status_code == 200
    complete_batch_response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "complete_batch", "batch_id": "bat-1"},
    )
    assert complete_batch_response.status_code == 200

    replenished_product = app._product_service.get_product(  # noqa: SLF001
        authorization_header=header,
        product_id=product.product_id,
    )
    depleted_material = app._material_service.get_material(  # noqa: SLF001
        authorization_header=header,
        material_id=material.material_id,
    )
    assert replenished_product is not None
    assert replenished_product.stock_on_hand == 3
    assert replenished_product.reserved_stock == 0
    assert depleted_material is not None
    assert depleted_material.stock_on_hand == 10
    assert depleted_material.is_low_stock

    buy_page = app.get("/make-buy", authorization_header=header)
    assert buy_page.status_code == 200
    assert "Soy Wax" in buy_page.body
    assert "10 g" in buy_page.body
    assert "Add to Purchase" in buy_page.body

    add_to_purchase_response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "add_to_purchase", "material_id": material.material_id},
    )
    assert add_to_purchase_response.status_code == 200
    purchase_response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create_purchase",
            "status": "ordered",
            "supplier": "Acme Wax",
            "expected_date": "2026-06-15",
        },
    )
    assert purchase_response.status_code == 200
    assert "Ordered" in purchase_response.body
    assert "Acme Wax" in purchase_response.body

    receive_response = app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "receive_purchase", "purchase_id": "pur-1"},
    )
    assert receive_response.status_code == 200
    assert "Received" in receive_response.body

    restocked_material = app._material_service.get_material(  # noqa: SLF001
        authorization_header=header,
        material_id=material.material_id,
    )
    assert restocked_material is not None
    assert restocked_material.stock_on_hand == 20
    assert not restocked_material.is_low_stock

    final_summary = app._today_summary_service.get_summary(authorization_header=header)  # noqa: SLF001
    assert final_summary == {
        "orders_to_pack": 0,
        "low_stock": 0,
        "materials_to_buy": 0,
        "batches_in_progress": 0,
        "purchases_due": 0,
    }
