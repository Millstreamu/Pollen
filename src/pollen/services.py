"""Application services for shop-scoped workflows."""

from __future__ import annotations

from pollen.auth import AuthService
from pollen.materials import MaterialRecord, MaterialRepository
from pollen.orders import OrderRecord, OrderRepository
from pollen.products import ProductRecord, ProductRepository
from pollen.recipes import RecipeItemRecord, RecipeRepository


class OrderService:
    """Create/read order records with server-owned shop scoping."""

    def __init__(
        self,
        *,
        auth_service: AuthService | None = None,
        order_repository: OrderRepository | None = None,
    ) -> None:
        self._auth_service = auth_service or AuthService()
        self._order_repository = order_repository or OrderRepository()

    def create_order(
        self,
        *,
        authorization_header: str | None,
        product_sku: str,
        quantity: int,
        requested_shop_id: str | None = None,
    ) -> OrderRecord | None:
        """Create order for current authenticated shop.

        `requested_shop_id` is accepted for compatibility with incoming payloads,
        but intentionally ignored to enforce server-side shop ownership.
        """
        _ = requested_shop_id
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._order_repository.create(
            shop_id=context.shop.shop_id,
            product_sku=product_sku,
            quantity=quantity,
        )

    def list_orders(self, *, authorization_header: str | None) -> list[OrderRecord]:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return []

        return self._order_repository.list_for_shop(shop_id=context.shop.shop_id)

    def get_order(self, *, authorization_header: str | None, order_id: str) -> OrderRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._order_repository.get_for_shop(shop_id=context.shop.shop_id, order_id=order_id)


class ProductService:
    """CRUD operations for shop-scoped finished products."""

    def __init__(
        self,
        *,
        auth_service: AuthService | None = None,
        product_repository: ProductRepository | None = None,
    ) -> None:
        self._auth_service = auth_service or AuthService()
        self._product_repository = product_repository or ProductRepository()

    def create_product(
        self,
        *,
        authorization_header: str | None,
        name: str,
        sku: str,
        stock_on_hand: int,
        reorder_point: int,
        requested_shop_id: str | None = None,
    ) -> ProductRecord | None:
        _ = requested_shop_id
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._product_repository.create(
            shop_id=context.shop.shop_id,
            name=name,
            sku=sku,
            stock_on_hand=stock_on_hand,
            reorder_point=reorder_point,
        )

    def list_products(self, *, authorization_header: str | None, include_archived: bool = False) -> list[ProductRecord]:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return []

        return self._product_repository.list_for_shop(
            shop_id=context.shop.shop_id,
            include_archived=include_archived,
        )

    def get_product(self, *, authorization_header: str | None, product_id: str) -> ProductRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._product_repository.get_for_shop(shop_id=context.shop.shop_id, product_id=product_id)

    def update_product(
        self,
        *,
        authorization_header: str | None,
        product_id: str,
        name: str,
        sku: str,
        stock_on_hand: int,
        reorder_point: int,
    ) -> ProductRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._product_repository.update_for_shop(
            shop_id=context.shop.shop_id,
            product_id=product_id,
            name=name,
            sku=sku,
            stock_on_hand=stock_on_hand,
            reorder_point=reorder_point,
        )

    def archive_product(self, *, authorization_header: str | None, product_id: str) -> ProductRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._product_repository.archive_for_shop(shop_id=context.shop.shop_id, product_id=product_id)


    def restore_product(self, *, authorization_header: str | None, product_id: str) -> ProductRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._product_repository.restore_for_shop(shop_id=context.shop.shop_id, product_id=product_id)


class RecipeService:
    """Recipe item CRUD and materials-needed calculations."""

    def __init__(
        self,
        *,
        auth_service: AuthService | None = None,
        recipe_repository: RecipeRepository | None = None,
        product_repository: ProductRepository | None = None,
        material_repository: MaterialRepository | None = None,
    ) -> None:
        self._auth_service = auth_service or AuthService()
        self._recipe_repository = recipe_repository or RecipeRepository()
        self._product_repository = product_repository or ProductRepository()
        self._material_repository = material_repository or MaterialRepository()

    def create_recipe_item(self, *, authorization_header: str | None, product_id: str, material_id: str, quantity_per_unit: int) -> RecipeItemRecord | None:
        if quantity_per_unit <= 0:
            return None
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None
        if self._product_repository.get_for_shop(shop_id=context.shop.shop_id, product_id=product_id) is None:
            return None
        if self._material_repository.get_for_shop(shop_id=context.shop.shop_id, material_id=material_id) is None:
            return None
        return self._recipe_repository.create(
            shop_id=context.shop.shop_id,
            product_id=product_id,
            material_id=material_id,
            quantity_per_unit=quantity_per_unit,
        )

    def list_recipe_items(self, *, authorization_header: str | None, product_id: str) -> list[RecipeItemRecord]:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return []
        return self._recipe_repository.list_for_product(shop_id=context.shop.shop_id, product_id=product_id)

    def update_recipe_item(self, *, authorization_header: str | None, recipe_item_id: str, material_id: str, quantity_per_unit: int) -> RecipeItemRecord | None:
        if quantity_per_unit <= 0:
            return None
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None
        if self._material_repository.get_for_shop(shop_id=context.shop.shop_id, material_id=material_id) is None:
            return None
        return self._recipe_repository.update_for_shop(
            shop_id=context.shop.shop_id,
            recipe_item_id=recipe_item_id,
            material_id=material_id,
            quantity_per_unit=quantity_per_unit,
        )

    def archive_recipe_item(self, *, authorization_header: str | None, recipe_item_id: str) -> RecipeItemRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None
        return self._recipe_repository.archive_for_shop(shop_id=context.shop.shop_id, recipe_item_id=recipe_item_id)

    def materials_needed(self, *, authorization_header: str | None, product_id: str, quantity: int) -> list[dict[str, int | str]]:
        if quantity <= 0:
            return []
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return []
        rows: list[dict[str, int | str]] = []
        recipe_items = self._recipe_repository.list_for_product(shop_id=context.shop.shop_id, product_id=product_id)
        for item in recipe_items:
            material = self._material_repository.get_for_shop(shop_id=context.shop.shop_id, material_id=item.material_id)
            if material is None:
                continue
            needed = item.quantity_per_unit * quantity
            rows.append({
                "recipe_item_id": item.recipe_item_id,
                "material_id": material.material_id,
                "material_name": material.name,
                "unit": material.unit,
                "needed": needed,
                "on_hand": material.stock_on_hand,
                "shortage": max(0, needed - material.stock_on_hand),
            })
        return rows


class MaterialService:
    """CRUD operations for shop-scoped materials."""

    def __init__(
        self,
        *,
        auth_service: AuthService | None = None,
        material_repository: MaterialRepository | None = None,
    ) -> None:
        self._auth_service = auth_service or AuthService()
        self._material_repository = material_repository or MaterialRepository()

    def create_material(
        self,
        *,
        authorization_header: str | None,
        name: str,
        unit: str,
        stock_on_hand: int,
        reorder_point: int,
        requested_shop_id: str | None = None,
    ) -> MaterialRecord | None:
        _ = requested_shop_id
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._material_repository.create(
            shop_id=context.shop.shop_id,
            name=name,
            unit=unit,
            stock_on_hand=stock_on_hand,
            reorder_point=reorder_point,
        )

    def list_materials(self, *, authorization_header: str | None, include_archived: bool = False) -> list[MaterialRecord]:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return []

        return self._material_repository.list_for_shop(
            shop_id=context.shop.shop_id,
            include_archived=include_archived,
        )

    def get_material(self, *, authorization_header: str | None, material_id: str) -> MaterialRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._material_repository.get_for_shop(shop_id=context.shop.shop_id, material_id=material_id)

    def update_material(
        self,
        *,
        authorization_header: str | None,
        material_id: str,
        name: str,
        unit: str,
        stock_on_hand: int,
        reorder_point: int,
    ) -> MaterialRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._material_repository.update_for_shop(
            shop_id=context.shop.shop_id,
            material_id=material_id,
            name=name,
            unit=unit,
            stock_on_hand=stock_on_hand,
            reorder_point=reorder_point,
        )

    def archive_material(self, *, authorization_header: str | None, material_id: str) -> MaterialRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._material_repository.archive_for_shop(shop_id=context.shop.shop_id, material_id=material_id)

    def restore_material(self, *, authorization_header: str | None, material_id: str) -> MaterialRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._material_repository.restore_for_shop(shop_id=context.shop.shop_id, material_id=material_id)
