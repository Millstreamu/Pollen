from pollen.app import create_app


def _auth_header(user_id: str, email: str) -> str:
    return f"Bearer user:{user_id}:{email}"


def test_recipe_management_and_materials_needed_journey() -> None:
    header = _auth_header("journey", "journey@example.com")
    app = create_app()

    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={"action": "create", "name": "Wax", "unit": "g", "stock_on_hand": "20", "reorder_point": "5"},
    )
    product_response = app.post(
        "/products-stock",
        authorization_header=header,
        form_data={"action": "create", "name": "Candle", "sku": "C-1", "stock_on_hand": "4", "reorder_point": "1"},
    )
    assert product_response.status_code == 200

    page = app.get("/products-stock", authorization_header=header)
    assert "Product recipes" in page.body
    assert "Add recipe row" in page.body

    app.post(
        "/products-stock",
        authorization_header=header,
        form_data={
            "action": "create_recipe_item",
            "product_id": "prd-1",
            "material_id": "mat-1",
            "quantity_per_unit": "3",
        },
    )
    updated = app.get("/products-stock", authorization_header=header)
    assert "Wax: 3 g" in updated.body
    assert "Calculate materials needed" in updated.body
    assert "Can make now: 6 units" in updated.body

    planned = app.get("/products-stock?materials_needed_for=prd-1&quantity=4", authorization_header=header)
    assert "Wax: 12 g" in planned.body

    products_page = app.get("/products-stock", authorization_header=header)
    assert "<td>4</td>" in products_page.body
