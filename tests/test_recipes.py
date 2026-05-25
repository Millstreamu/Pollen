from pollen.materials import MaterialRepository
from pollen.products import ProductRepository
from pollen.recipes import RecipeRepository
from pollen.services import MaterialService, ProductService, RecipeService


def _auth_header(user_id: str, email: str) -> str:
    return f"Bearer user:{user_id}:{email}"


def test_recipe_item_crud_and_materials_needed_calculation() -> None:
    auth = _auth_header("owner", "owner@example.com")
    product_repo = ProductRepository()
    material_repo = MaterialRepository()
    recipe_repo = RecipeRepository()

    product_service = ProductService(product_repository=product_repo)
    material_service = MaterialService(material_repository=material_repo)
    recipe_service = RecipeService(
        product_repository=product_repo,
        material_repository=material_repo,
        recipe_repository=recipe_repo,
    )

    product = product_service.create_product(
        authorization_header=auth,
        name="Gift Box",
        sku="BOX-01",
        stock_on_hand=10,
        reorder_point=2,
    )
    material = material_service.create_material(
        authorization_header=auth,
        name="Ribbon",
        unit="m",
        stock_on_hand=7,
        reorder_point=2,
    )
    assert product is not None and material is not None

    recipe_item = recipe_service.create_recipe_item(
        authorization_header=auth,
        product_id=product.product_id,
        material_id=material.material_id,
        quantity_per_unit=2,
    )
    assert recipe_item is not None

    needed = recipe_service.materials_needed(
        authorization_header=auth,
        product_id=product.product_id,
        quantity=5,
    )
    assert needed[0]["needed"] == 10
    assert needed[0]["shortage"] == 3


def test_recipe_validation_and_shop_isolation() -> None:
    owner = _auth_header("owner2", "owner2@example.com")
    other = _auth_header("other2", "other2@example.com")
    product_repo = ProductRepository()
    material_repo = MaterialRepository()

    product_service = ProductService(product_repository=product_repo)
    material_service = MaterialService(material_repository=material_repo)
    recipe_service = RecipeService(product_repository=product_repo, material_repository=material_repo)

    product = product_service.create_product(authorization_header=owner, name="Soap", sku="SP-1", stock_on_hand=3, reorder_point=1)
    material = material_service.create_material(authorization_header=owner, name="Oil", unit="ml", stock_on_hand=100, reorder_point=20)
    assert product is not None and material is not None

    assert recipe_service.create_recipe_item(
        authorization_header=owner,
        product_id=product.product_id,
        material_id=material.material_id,
        quantity_per_unit=0,
    ) is None

    created = recipe_service.create_recipe_item(
        authorization_header=owner,
        product_id=product.product_id,
        material_id=material.material_id,
        quantity_per_unit=3,
    )
    assert created is not None
    assert recipe_service.archive_recipe_item(authorization_header=other, recipe_item_id=created.recipe_item_id) is None


def test_can_make_quantity_uses_limiting_material_and_does_not_change_product_stock() -> None:
    auth = _auth_header("owner3", "owner3@example.com")
    product_repo = ProductRepository()
    material_repo = MaterialRepository()
    recipe_repo = RecipeRepository()

    product_service = ProductService(product_repository=product_repo)
    material_service = MaterialService(material_repository=material_repo)
    recipe_service = RecipeService(
        product_repository=product_repo,
        material_repository=material_repo,
        recipe_repository=recipe_repo,
    )

    product = product_service.create_product(
        authorization_header=auth,
        name="Body Butter",
        sku="BB-1",
        stock_on_hand=12,
        reorder_point=3,
    )
    wax = material_service.create_material(authorization_header=auth, name="Wax", unit="g", stock_on_hand=20, reorder_point=4)
    oil = material_service.create_material(authorization_header=auth, name="Oil", unit="ml", stock_on_hand=15, reorder_point=4)
    assert product is not None and wax is not None and oil is not None

    recipe_service.create_recipe_item(authorization_header=auth, product_id=product.product_id, material_id=wax.material_id, quantity_per_unit=3)
    recipe_service.create_recipe_item(authorization_header=auth, product_id=product.product_id, material_id=oil.material_id, quantity_per_unit=5)

    assert recipe_service.can_make_quantity(authorization_header=auth, product_id=product.product_id) == 3
    assert product_service.get_product(authorization_header=auth, product_id=product.product_id).stock_on_hand == 12
