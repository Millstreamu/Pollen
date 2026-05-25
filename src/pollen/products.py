"""Shop-scoped product persistence for Milestone 2.1."""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class ProductRecord:
    product_id: str
    shop_id: str
    name: str
    sku: str
    stock_on_hand: int
    reorder_point: int
    is_active: bool

    @property
    def is_low_stock(self) -> bool:
        return self.stock_on_hand <= self.reorder_point


class ProductRepository:
    """In-memory repository with strict shop scoping semantics."""

    def __init__(self) -> None:
        self._records: dict[str, ProductRecord] = {}
        self._next_id = 1

    def create(self, *, shop_id: str, name: str, sku: str, stock_on_hand: int, reorder_point: int) -> ProductRecord:
        product_id = f"prd-{self._next_id}"
        self._next_id += 1
        created = ProductRecord(
            product_id=product_id,
            shop_id=shop_id,
            name=name,
            sku=sku,
            stock_on_hand=stock_on_hand,
            reorder_point=reorder_point,
            is_active=True,
        )
        self._records[product_id] = created
        return created

    def list_for_shop(self, *, shop_id: str, include_archived: bool = False) -> list[ProductRecord]:
        records = [record for record in self._records.values() if record.shop_id == shop_id]
        if include_archived:
            return records
        return [record for record in records if record.is_active]

    def get_for_shop(self, *, shop_id: str, product_id: str) -> ProductRecord | None:
        record = self._records.get(product_id)
        if record is None or record.shop_id != shop_id:
            return None
        return record

    def update_for_shop(
        self,
        *,
        shop_id: str,
        product_id: str,
        name: str,
        sku: str,
        stock_on_hand: int,
        reorder_point: int,
    ) -> ProductRecord | None:
        existing = self.get_for_shop(shop_id=shop_id, product_id=product_id)
        if existing is None:
            return None

        updated = replace(
            existing,
            name=name,
            sku=sku,
            stock_on_hand=stock_on_hand,
            reorder_point=reorder_point,
        )
        self._records[product_id] = updated
        return updated

    def archive_for_shop(self, *, shop_id: str, product_id: str) -> ProductRecord | None:
        existing = self.get_for_shop(shop_id=shop_id, product_id=product_id)
        if existing is None:
            return None

        archived = replace(existing, is_active=False)
        self._records[product_id] = archived
        return archived
