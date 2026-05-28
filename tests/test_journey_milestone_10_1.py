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
            "sale_price": "25.00",
            "estimated_material_cost": "8.50",
            "estimated_packaging_shipping_cost": "3.00",
            "platform_fee_percent": "10.00",
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

    money_page_after_shipping = app.get("/money", authorization_header=header)
    assert money_page_after_shipping.status_code == 200
    assert "Shipped orders: 1" in money_page_after_shipping.body
    assert "Items shipped: 2" in money_page_after_shipping.body
    assert "Estimated revenue: $50.00" in money_page_after_shipping.body
    assert "Estimated cost: $28.00" in money_page_after_shipping.body
    assert "Estimated profit: $22.00" in money_page_after_shipping.body

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


def test_money_summary_service_counts_shipped_orders_only() -> None:
    header = _auth_header("money-summary", "money-summary@example.com")
    app = create_app()

    app.post(
        "/products-stock",
        authorization_header=header,
        form_data={
            "action": "create",
            "name": "Profit Candle",
            "sku": "PC-1",
            "stock_on_hand": "3",
            "reorder_point": "0",
            "sale_price": "20.00",
            "estimated_material_cost": "6.00",
            "estimated_packaging_shipping_cost": "2.00",
            "platform_fee_percent": "5.00",
        },
    )
    app.post(
        "/orders",
        authorization_header=header,
        form_data={"customer_name": "Buyer One", "product_sku": "PC-1", "quantity": "1"},
    )
    app.post(
        "/orders",
        authorization_header=header,
        form_data={"customer_name": "Buyer Two", "product_sku": "PC-1", "quantity": "1"},
    )
    app.post(
        "/orders",
        authorization_header=header,
        form_data={"action": "pack", "order_id": "ord-1"},
    )
    app.post(
        "/orders",
        authorization_header=header,
        form_data={"action": "ship", "order_id": "ord-1"},
    )

    summary = app._money_summary_service.get_summary(authorization_header=header)  # noqa: SLF001

    assert summary == {
        "shipped_order_count": 1,
        "shipped_item_count": 1,
        "estimated_revenue": 20.0,
        "estimated_cost": 9.0,
        "estimated_profit": 11.0,
    }
