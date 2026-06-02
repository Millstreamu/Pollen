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
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create_product",
            "name": "Candle",
            "sku": "C-1",
            "stock_on_hand": "4",
            "reorder_point": "1",
        },
    )
    assert product_response.status_code == 200

    page = app.get("/make-buy", authorization_header=header)
    assert "Workshop Materials" in page.body
    assert "Wax" in page.body
    assert "Selected Product Recipe / Materials Needed" not in page.body

    app.post(
        "/make-buy",
        authorization_header=header,
        form_data={
            "action": "create_recipe_item",
            "product_id": "prd-1",
            "material_id": "mat-1",
            "quantity_per_unit": "3",
        },
    )
    needed = app._recipe_service.materials_needed(  # noqa: SLF001
        authorization_header=header,
        product_id="prd-1",
        quantity=2,
    )
    assert needed[0]["material_name"] == "Wax"
    assert needed[0]["needed"] == 6
    assert app._recipe_service.can_make_quantity(authorization_header=header, product_id="prd-1") == 6  # noqa: SLF001

    updated = app.get("/make-buy", authorization_header=header)
    assert "Wax" in updated.body
    assert "Materials needed for batch size/yield" not in updated.body

    products_page = app.get("/products-stock", authorization_header=header)
    assert "<td>4</td>" in products_page.body
