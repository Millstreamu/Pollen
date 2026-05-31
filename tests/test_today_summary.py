from pollen.app import AppShell
from pollen.services import MaterialService, ProductService


def _auth_header(user_id: str = "today-owner", email: str = "today-owner@example.com") -> str:
    return f"Bearer user:{user_id}:{email}"


def test_today_summary_service_counts_key_buckets() -> None:
    header = _auth_header()
    product_service = ProductService()
    material_service = MaterialService()
    app = AppShell(product_service=product_service, material_service=material_service)

    low_product = product_service.create_product(
        authorization_header=header,
        name="Low Product",
        sku="LOW-1",
        stock_on_hand=1,
        reorder_point=2,
    )
    assert low_product is not None
    ready_product = product_service.create_product(
        authorization_header=header,
        name="Ready Product",
        sku="RDY-1",
        stock_on_hand=10,
        reorder_point=2,
    )
    assert ready_product is not None
    low_material = material_service.create_material(
        authorization_header=header,
        name="Low Wax",
        unit="kg",
        stock_on_hand=1,
        reorder_point=3,
    )
    assert low_material is not None

    app.post(
        "/orders",
        authorization_header=header,
        form_data={"customer_name": "Alex", "product_sku": ready_product.sku, "quantity": "1"},
    )
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "add_to_purchase", "material_id": low_material.material_id},
    )
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create_purchase", "status": "ordered", "supplier": "Acme", "expected_date": "2026-06-01"},
    )
    app.post(
        "/products-stock",
        authorization_header=header,
        form_data={
            "action": "create_recipe_item",
            "product_id": ready_product.product_id,
            "material_id": low_material.material_id,
            "quantity_per_unit": "1",
        },
    )
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create_batch", "product_id": ready_product.product_id, "quantity": "1"},
    )
    batch_id = app._batch_service.list_batches(authorization_header=header)[0].batch_id  # noqa: SLF001
    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "start_batch", "batch_id": batch_id},
    )

    summary = app._today_summary_service.get_summary(authorization_header=header)  # noqa: SLF001

    assert summary == {
        "orders_to_pack": 1,
        "low_stock": 2,
        "materials_to_buy": 1,
        "batches_in_progress": 1,
        "purchases_due": 1,
    }


def test_today_page_renders_summary_counts() -> None:
    header = _auth_header("today-view", "today-view@example.com")
    product_service = ProductService()
    app = AppShell(product_service=product_service)
    created = product_service.create_product(
        authorization_header=header,
        name="Daily Candle",
        sku="DAY-1",
        stock_on_hand=4,
        reorder_point=1,
    )
    assert created is not None
    app.post(
        "/orders",
        authorization_header=header,
        form_data={"customer_name": "Jordan", "product_sku": created.sku, "quantity": "1"},
    )

    response = app.get("/", authorization_header=header)

    assert response.status_code == 200
    assert "Today summary" in response.body
    assert "<span class='metric-value'>1</span><span class='metric-label'>Orders to pack</span>" in response.body
    assert "<span class='metric-value'>0</span><span class='metric-label'>Low-stock products</span>" in response.body


def test_today_page_renders_action_links_to_existing_workflows() -> None:
    header = _auth_header("today-actions", "today-actions@example.com")
    app = AppShell()

    response = app.get("/", authorization_header=header)

    assert response.status_code == 200
    assert "Today actions" in response.body
    assert "href='/orders'" in response.body
    assert "Pack and ship orders" in response.body
    assert "href='/products-stock'" in response.body
    assert "Review low-stock products" in response.body
    assert response.body.count("href='/make-buy'") >= 3
    assert "Create a batch" in response.body
    assert "Create a purchase" in response.body
