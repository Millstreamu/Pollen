"""Application services for shop-scoped workflows."""

from __future__ import annotations

from pollen.auth import AuthService
from pollen.batches import BatchRecord, BatchRepository
from pollen.inventory import ActivityLogRepository, InventoryMovementRepository
from pollen.materials import MaterialRecord, MaterialRepository
from pollen.orders import OrderItemRecord, OrderRecord, OrderRepository
from pollen.products import ProductRecord, ProductRepository
from pollen.recipes import RecipeItemRecord, RecipeRepository


class OrderService:
    """Create/read order records with server-owned shop scoping."""

    def __init__(
        self,
        *,
        auth_service: AuthService | None = None,
        order_repository: OrderRepository | None = None,
        product_repository: ProductRepository | None = None,
    ) -> None:
        self._auth_service = auth_service or AuthService()
        self._order_repository = order_repository or OrderRepository()
        self._product_repository = product_repository or ProductRepository()
        self._activity_repository = ActivityLogRepository()

    def create_order(
        self,
        *,
        authorization_header: str | None,
        customer_name: str,
        items: list[dict[str, int | str]],
        requested_shop_id: str | None = None,
    ) -> OrderRecord | None:
        """Create order for current authenticated shop.

        `requested_shop_id` is accepted for compatibility with incoming payloads,
        but intentionally ignored to enforce server-side shop ownership.
        """
        _ = requested_shop_id
        context = self._auth_service.resolve_context(authorization_header)
        if context is None or not customer_name.strip() or not items:
            return None

        normalized_items: list[tuple[str, int]] = []
        status = "ready_to_pack"
        for item in items:
            sku = str(item.get("product_sku", "")).strip()
            quantity = int(item.get("quantity", 0))
            if not sku or quantity <= 0:
                return None
            normalized_items.append((sku, quantity))
            product = self._product_repository_by_sku(context.shop.shop_id, sku)
            if product is None or product.available_stock < quantity:
                status = "waiting_on_stock"

        created = self._order_repository.create(
            shop_id=context.shop.shop_id,
            customer_name=customer_name.strip(),
            source="manual",
            status=status,
        )
        for sku, quantity in normalized_items:
            added = self._order_repository.add_item(
                order_id=created.order_id,
                shop_id=context.shop.shop_id,
                product_sku=sku,
                quantity=quantity,
            )
            if added is None:
                return None
        if status == "ready_to_pack":
            for sku, quantity in normalized_items:
                reserved = self._product_repository.reserve_by_sku_for_shop(
                    shop_id=context.shop.shop_id,
                    sku=sku,
                    quantity=quantity,
                )
                if reserved is None:
                    return None
        return created

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

    def list_order_items(self, *, authorization_header: str | None, order_id: str) -> list[OrderItemRecord]:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return []
        if self._order_repository.get_for_shop(shop_id=context.shop.shop_id, order_id=order_id) is None:
            return []
        return self._order_repository.list_items_for_order(shop_id=context.shop.shop_id, order_id=order_id)

    def mark_order_packed(self, *, authorization_header: str | None, order_id: str) -> OrderRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None
        order = self._order_repository.get_for_shop(shop_id=context.shop.shop_id, order_id=order_id)
        if order is None or order.status != "ready_to_pack":
            return None
        updated = self._order_repository.update_status_for_shop(
            shop_id=context.shop.shop_id,
            order_id=order_id,
            status="packed",
        )
        if updated is None:
            return None
        self._activity_repository.create(
            shop_id=context.shop.shop_id,
            activity_type="order_packed",
            entity_type="order",
            entity_id=order.order_id,
            message=f"Order {order.order_id} moved to packed",
            actor_user_id=context.user.user_id,
        )
        return updated

    def mark_order_shipped(self, *, authorization_header: str | None, order_id: str) -> OrderRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None
        order = self._order_repository.get_for_shop(shop_id=context.shop.shop_id, order_id=order_id)
        if order is None or order.status != "packed":
            return None

        items = self._order_repository.list_items_for_order(shop_id=context.shop.shop_id, order_id=order_id)
        for item in items:
            product = self._product_repository_by_sku(context.shop.shop_id, item.product_sku)
            if product is None or product.reserved_stock < item.quantity:
                return None

        for item in items:
            product = self._product_repository_by_sku(context.shop.shop_id, item.product_sku)
            assert product is not None
            updated = self._product_repository.update_for_shop(
                shop_id=context.shop.shop_id,
                product_id=product.product_id,
                name=product.name,
                sku=product.sku,
                stock_on_hand=product.stock_on_hand - item.quantity,
                reserved_stock=product.reserved_stock - item.quantity,
                reorder_point=product.reorder_point,
            )
            if updated is None:
                return None

        updated_order = self._order_repository.update_status_for_shop(
            shop_id=context.shop.shop_id,
            order_id=order_id,
            status="shipped",
        )
        if updated_order is not None:
            self._activity_repository.create(
                shop_id=context.shop.shop_id,
                activity_type="order_shipped",
                entity_type="order",
                entity_id=order.order_id,
                message=f"Order {order.order_id} moved to shipped",
                actor_user_id=context.user.user_id,
            )
        return updated_order


    def cancel_order(self, *, authorization_header: str | None, order_id: str) -> OrderRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None
        order = self._order_repository.get_for_shop(shop_id=context.shop.shop_id, order_id=order_id)
        if order is None or order.status not in {"ready_to_pack", "packed"}:
            return None

        items = self._order_repository.list_items_for_order(shop_id=context.shop.shop_id, order_id=order_id)
        for item in items:
            released = self._product_repository.release_by_sku_for_shop(
                shop_id=context.shop.shop_id,
                sku=item.product_sku,
                quantity=item.quantity,
            )
            if released is None:
                return None

        updated = self._order_repository.update_status_for_shop(
            shop_id=context.shop.shop_id,
            order_id=order_id,
            status="cancelled",
        )
        if updated is not None:
            self._activity_repository.create(
                shop_id=context.shop.shop_id,
                activity_type="order_cancelled",
                entity_type="order",
                entity_id=order.order_id,
                message=f"Order {order.order_id} cancelled and reservations released",
                actor_user_id=context.user.user_id,
            )
        return updated

    def _product_repository_by_sku(self, shop_id: str, sku: str) -> ProductRecord | None:
        products = self._product_repository.list_for_shop(shop_id=shop_id, include_archived=False)
        for product in products:
            if product.sku == sku:
                return product
        return None


class ProductService:
    """CRUD operations for shop-scoped finished products."""

    def __init__(
        self,
        *,
        auth_service: AuthService | None = None,
        product_repository: ProductRepository | None = None,
        movement_repository: InventoryMovementRepository | None = None,
        activity_repository: ActivityLogRepository | None = None,
    ) -> None:
        self._auth_service = auth_service or AuthService()
        self._product_repository = product_repository or ProductRepository()
        self._activity_repository = ActivityLogRepository()
        self._movement_repository = movement_repository or InventoryMovementRepository()
        self._activity_repository = activity_repository or ActivityLogRepository()

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
        existing = self._product_repository.get_for_shop(shop_id=context.shop.shop_id, product_id=product_id)
        if existing is None:
            return None

        return self._product_repository.update_for_shop(
            shop_id=context.shop.shop_id,
            product_id=product_id,
            name=name,
            sku=sku,
            stock_on_hand=stock_on_hand,
            reserved_stock=existing.reserved_stock,
            reorder_point=reorder_point,
        )

    def archive_product(self, *, authorization_header: str | None, product_id: str) -> ProductRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._product_repository.archive_for_shop(shop_id=context.shop.shop_id, product_id=product_id)



    def adjust_product_stock(
        self,
        *,
        authorization_header: str | None,
        product_id: str,
        delta: int,
        reason: str,
    ) -> ProductRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None or not reason.strip() or delta == 0:
            return None
        existing = self._product_repository.get_for_shop(shop_id=context.shop.shop_id, product_id=product_id)
        if existing is None:
            return None
        updated_stock = existing.stock_on_hand + delta
        if updated_stock < 0:
            return None
        updated = self._product_repository.update_for_shop(
            shop_id=context.shop.shop_id,
            product_id=product_id,
            name=existing.name,
            sku=existing.sku,
            stock_on_hand=updated_stock,
            reserved_stock=existing.reserved_stock,
            reorder_point=existing.reorder_point,
        )
        if updated is None:
            return None
        self._movement_repository.create(
            shop_id=context.shop.shop_id,
            item_type="product",
            item_id=product_id,
            reason=reason.strip(),
            delta=delta,
            before_quantity=existing.stock_on_hand,
            after_quantity=updated.stock_on_hand,
            actor_user_id=context.user.user_id,
        )
        self._activity_repository.create(
            shop_id=context.shop.shop_id,
            activity_type="stock_adjusted",
            entity_type="product",
            entity_id=product_id,
            message=f"Adjusted product stock by {delta}: {reason.strip()}",
            actor_user_id=context.user.user_id,
        )
        return updated

    def list_inventory_movements(self, *, authorization_header: str | None) -> list:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return []
        return self._movement_repository.list_for_shop(shop_id=context.shop.shop_id)

    def list_activity_logs(self, *, authorization_header: str | None) -> list:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return []
        return self._activity_repository.list_for_shop(shop_id=context.shop.shop_id)

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
        self._activity_repository = ActivityLogRepository()
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
            if material is None or not material.is_active:
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

    def can_make_quantity(self, *, authorization_header: str | None, product_id: str) -> int:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return 0
        recipe_items = self._recipe_repository.list_for_product(shop_id=context.shop.shop_id, product_id=product_id)
        if not recipe_items:
            return 0

        max_by_material: list[int] = []
        for item in recipe_items:
            material = self._material_repository.get_for_shop(shop_id=context.shop.shop_id, material_id=item.material_id)
            if material is None or not material.is_active or item.quantity_per_unit <= 0:
                continue
            max_by_material.append(material.stock_on_hand // item.quantity_per_unit)

        if not max_by_material:
            return 0
        return min(max_by_material)


class BatchService:
    """Create planned batches while validating material requirements."""

    def __init__(
        self,
        *,
        auth_service: AuthService | None = None,
        batch_repository: BatchRepository | None = None,
        product_repository: ProductRepository | None = None,
        recipe_repository: RecipeRepository | None = None,
        material_repository: MaterialRepository | None = None,
    ) -> None:
        self._auth_service = auth_service or AuthService()
        self._batch_repository = batch_repository or BatchRepository()
        self._product_repository = product_repository or ProductRepository()
        self._recipe_repository = recipe_repository or RecipeRepository()
        self._material_repository = material_repository or MaterialRepository()

    def create_batch(self, *, authorization_header: str | None, product_id: str, quantity: int) -> tuple[BatchRecord | None, str | None]:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None, "Unauthorized"
        if not product_id.strip() or quantity <= 0:
            return None, "Product and quantity are required"
        product = self._product_repository.get_for_shop(shop_id=context.shop.shop_id, product_id=product_id)
        if product is None:
            return None, "Unknown product"

        recipe_items = self._recipe_repository.list_for_product(shop_id=context.shop.shop_id, product_id=product_id)
        shortages: list[str] = []
        for item in recipe_items:
            material = self._material_repository.get_for_shop(shop_id=context.shop.shop_id, material_id=item.material_id)
            if material is None or not material.is_active:
                shortages.append(f"Missing material {item.material_id}")
                continue
            needed = item.quantity_per_unit * quantity
            if material.stock_on_hand < needed:
                shortages.append(f"{material.name} short by {needed - material.stock_on_hand} {material.unit}")
        if shortages:
            return None, "Insufficient materials: " + "; ".join(shortages)

        return self._batch_repository.create(shop_id=context.shop.shop_id, product_id=product_id, quantity=quantity), None

    def start_batch(self, *, authorization_header: str | None, batch_id: str) -> tuple[BatchRecord | None, str | None]:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None, "Unauthorized"
        if not batch_id.strip():
            return None, "Batch ID is required"

        batch = self._batch_repository.get_for_shop(shop_id=context.shop.shop_id, batch_id=batch_id)
        if batch is None:
            return None, "Unknown batch"
        if batch.status != "planned":
            return None, "Invalid batch transition: only planned batches can be started"

        started_at = self._batch_repository.now_iso()
        updated = self._batch_repository.update_for_shop(
            shop_id=context.shop.shop_id,
            batch_id=batch_id,
            status="in-progress",
            started_at=started_at,
            completed_at=None,
        )
        if updated is None:
            return None, "Batch start failed"
        return updated, None

    def complete_batch(self, *, authorization_header: str | None, batch_id: str) -> tuple[BatchRecord | None, str | None]:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None, "Unauthorized"
        if not batch_id.strip():
            return None, "Batch ID is required"

        batch = self._batch_repository.get_for_shop(shop_id=context.shop.shop_id, batch_id=batch_id)
        if batch is None:
            return None, "Unknown batch"
        if batch.status != "in-progress":
            return None, "Invalid batch transition: only in-progress batches can be completed"

        recipe_items = self._recipe_repository.list_for_product(shop_id=context.shop.shop_id, product_id=batch.product_id)
        material_updates: list[tuple[MaterialRecord, int]] = []
        for item in recipe_items:
            material = self._material_repository.get_for_shop(shop_id=context.shop.shop_id, material_id=item.material_id)
            if material is None or not material.is_active:
                return None, f"Missing material {item.material_id}"
            needed = item.quantity_per_unit * batch.quantity
            if material.stock_on_hand < needed:
                return None, f"Insufficient materials: {material.name} short by {needed - material.stock_on_hand} {material.unit}"
            material_updates.append((material, needed))

        product = self._product_repository.get_for_shop(shop_id=context.shop.shop_id, product_id=batch.product_id)
        if product is None:
            return None, "Unknown product"

        for material, needed in material_updates:
            updated = self._material_repository.update_for_shop(
                shop_id=context.shop.shop_id,
                material_id=material.material_id,
                name=material.name,
                unit=material.unit,
                stock_on_hand=material.stock_on_hand - needed,
                reorder_point=material.reorder_point,
            )
            if updated is None:
                return None, "Batch complete failed"

        product_updated = self._product_repository.update_for_shop(
            shop_id=context.shop.shop_id,
            product_id=product.product_id,
            name=product.name,
            sku=product.sku,
            stock_on_hand=product.stock_on_hand + batch.quantity,
            reserved_stock=product.reserved_stock,
            reorder_point=product.reorder_point,
        )
        if product_updated is None:
            return None, "Batch complete failed"

        completed_at = self._batch_repository.now_iso()
        updated_batch = self._batch_repository.update_for_shop(
            shop_id=context.shop.shop_id,
            batch_id=batch_id,
            status="complete",
            started_at=batch.started_at,
            completed_at=completed_at,
        )
        if updated_batch is None:
            return None, "Batch complete failed"
        return updated_batch, None

    def list_batches(self, *, authorization_header: str | None) -> list[BatchRecord]:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return []
        return self._batch_repository.list_for_shop(shop_id=context.shop.shop_id)


class MaterialService:
    """CRUD operations for shop-scoped materials."""

    def __init__(
        self,
        *,
        auth_service: AuthService | None = None,
        material_repository: MaterialRepository | None = None,
        movement_repository: InventoryMovementRepository | None = None,
        activity_repository: ActivityLogRepository | None = None,
    ) -> None:
        self._auth_service = auth_service or AuthService()
        self._material_repository = material_repository or MaterialRepository()
        self._movement_repository = movement_repository or InventoryMovementRepository()
        self._activity_repository = activity_repository or ActivityLogRepository()
        self._purchase_draft_by_shop: dict[str, set[str]] = {}

    def list_low_stock_suggestions(self, *, authorization_header: str | None) -> list[dict[str, int | str]]:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return []

        rows: list[dict[str, int | str]] = []
        for material in self._material_repository.list_for_shop(shop_id=context.shop.shop_id, include_archived=False):
            if not material.is_low_stock:
                continue
            suggested_quantity = max(1, (material.reorder_point * 2) - material.stock_on_hand)
            rows.append(
                {
                    "material_id": material.material_id,
                    "name": material.name,
                    "unit": material.unit,
                    "stock_on_hand": material.stock_on_hand,
                    "reorder_point": material.reorder_point,
                    "suggested_quantity": suggested_quantity,
                }
            )
        return rows

    def add_to_purchase_draft(self, *, authorization_header: str | None, material_id: str) -> bool:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return False
        material = self._material_repository.get_for_shop(shop_id=context.shop.shop_id, material_id=material_id)
        if material is None or not material.is_active:
            return False
        draft = self._purchase_draft_by_shop.setdefault(context.shop.shop_id, set())
        draft.add(material_id)
        return True

    def list_purchase_draft(self, *, authorization_header: str | None) -> list[MaterialRecord]:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return []
        draft_ids = self._purchase_draft_by_shop.get(context.shop.shop_id, set())
        selected: list[MaterialRecord] = []
        for material_id in draft_ids:
            material = self._material_repository.get_for_shop(shop_id=context.shop.shop_id, material_id=material_id)
            if material is not None and material.is_active:
                selected.append(material)
        return sorted(selected, key=lambda m: m.name)

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


    def adjust_material_stock(
        self,
        *,
        authorization_header: str | None,
        material_id: str,
        delta: int,
        reason: str,
    ) -> MaterialRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None or not reason.strip() or delta == 0:
            return None
        existing = self._material_repository.get_for_shop(shop_id=context.shop.shop_id, material_id=material_id)
        if existing is None:
            return None
        updated_stock = existing.stock_on_hand + delta
        if updated_stock < 0:
            return None
        updated = self._material_repository.update_for_shop(
            shop_id=context.shop.shop_id,
            material_id=material_id,
            name=existing.name,
            unit=existing.unit,
            stock_on_hand=updated_stock,
            reorder_point=existing.reorder_point,
        )
        if updated is None:
            return None
        self._movement_repository.create(
            shop_id=context.shop.shop_id,
            item_type="material",
            item_id=material_id,
            reason=reason.strip(),
            delta=delta,
            before_quantity=existing.stock_on_hand,
            after_quantity=updated.stock_on_hand,
            actor_user_id=context.user.user_id,
        )
        self._activity_repository.create(
            shop_id=context.shop.shop_id,
            activity_type="stock_adjusted",
            entity_type="material",
            entity_id=material_id,
            message=f"Adjusted material stock by {delta}: {reason.strip()}",
            actor_user_id=context.user.user_id,
        )
        return updated

    def list_inventory_movements(self, *, authorization_header: str | None) -> list:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return []
        return self._movement_repository.list_for_shop(shop_id=context.shop.shop_id)

    def list_activity_logs(self, *, authorization_header: str | None) -> list:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return []
        return self._activity_repository.list_for_shop(shop_id=context.shop.shop_id)

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
