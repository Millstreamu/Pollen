"""Shop-scoped product recipe persistence for Milestone 2.3."""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class RecipeItemRecord:
    recipe_item_id: str
    shop_id: str
    product_id: str
    material_id: str
    quantity_per_unit: int
    is_active: bool


class RecipeRepository:
    """In-memory repository for product recipe rows with shop isolation."""

    def __init__(self) -> None:
        self._records: dict[str, RecipeItemRecord] = {}
        self._next_id = 1

    def create(
        self,
        *,
        shop_id: str,
        product_id: str,
        material_id: str,
        quantity_per_unit: int,
    ) -> RecipeItemRecord:
        recipe_item_id = f"rcp-{self._next_id}"
        self._next_id += 1
        created = RecipeItemRecord(
            recipe_item_id=recipe_item_id,
            shop_id=shop_id,
            product_id=product_id,
            material_id=material_id,
            quantity_per_unit=quantity_per_unit,
            is_active=True,
        )
        self._records[recipe_item_id] = created
        return created

    def list_for_shop(self, *, shop_id: str, include_archived: bool = False) -> list[RecipeItemRecord]:
        records = [record for record in self._records.values() if record.shop_id == shop_id]
        if include_archived:
            return records
        return [record for record in records if record.is_active]

    def list_for_product(self, *, shop_id: str, product_id: str, include_archived: bool = False) -> list[RecipeItemRecord]:
        records = [
            record
            for record in self.list_for_shop(shop_id=shop_id, include_archived=include_archived)
            if record.product_id == product_id
        ]
        return records

    def get_for_shop(self, *, shop_id: str, recipe_item_id: str) -> RecipeItemRecord | None:
        record = self._records.get(recipe_item_id)
        if record is None or record.shop_id != shop_id:
            return None
        return record

    def update_for_shop(
        self,
        *,
        shop_id: str,
        recipe_item_id: str,
        material_id: str,
        quantity_per_unit: int,
    ) -> RecipeItemRecord | None:
        existing = self.get_for_shop(shop_id=shop_id, recipe_item_id=recipe_item_id)
        if existing is None:
            return None

        updated = replace(existing, material_id=material_id, quantity_per_unit=quantity_per_unit)
        self._records[recipe_item_id] = updated
        return updated

    def archive_for_shop(self, *, shop_id: str, recipe_item_id: str) -> RecipeItemRecord | None:
        existing = self.get_for_shop(shop_id=shop_id, recipe_item_id=recipe_item_id)
        if existing is None:
            return None
        archived = replace(existing, is_active=False)
        self._records[recipe_item_id] = archived
        return archived

