"""Shop-scoped material persistence for Milestone 2.2."""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class MaterialRecord:
    material_id: str
    shop_id: str
    name: str
    unit: str
    stock_on_hand: int
    reorder_point: int
    is_active: bool
    supplier: str | None = None
    notes: str | None = None

    @property
    def is_low_stock(self) -> bool:
        return self.stock_on_hand <= self.reorder_point


class MaterialRepository:
    """In-memory repository with strict shop scoping semantics."""

    def __init__(self) -> None:
        self._records: dict[str, MaterialRecord] = {}
        self._next_id = 1

    def create(
        self,
        *,
        shop_id: str,
        name: str,
        unit: str,
        stock_on_hand: int,
        reorder_point: int,
        supplier: str | None = None,
        notes: str | None = None,
    ) -> MaterialRecord:
        material_id = f"mat-{self._next_id}"
        self._next_id += 1
        created = MaterialRecord(
            material_id=material_id,
            shop_id=shop_id,
            name=name,
            unit=unit,
            stock_on_hand=stock_on_hand,
            reorder_point=reorder_point,
            is_active=True,
            supplier=supplier,
            notes=notes,
        )
        self._records[material_id] = created
        return created

    def list_for_shop(self, *, shop_id: str, include_archived: bool = False) -> list[MaterialRecord]:
        records = [record for record in self._records.values() if record.shop_id == shop_id]
        if include_archived:
            return records
        return [record for record in records if record.is_active]

    def get_for_shop(self, *, shop_id: str, material_id: str) -> MaterialRecord | None:
        record = self._records.get(material_id)
        if record is None or record.shop_id != shop_id:
            return None
        return record

    def update_for_shop(
        self,
        *,
        shop_id: str,
        material_id: str,
        name: str,
        unit: str,
        stock_on_hand: int,
        reorder_point: int,
        supplier: str | None = None,
        notes: str | None = None,
    ) -> MaterialRecord | None:
        existing = self.get_for_shop(shop_id=shop_id, material_id=material_id)
        if existing is None:
            return None

        updated = replace(
            existing,
            name=name,
            unit=unit,
            stock_on_hand=stock_on_hand,
            reorder_point=reorder_point,
            supplier=supplier,
            notes=notes,
        )
        self._records[material_id] = updated
        return updated

    def archive_for_shop(self, *, shop_id: str, material_id: str) -> MaterialRecord | None:
        existing = self.get_for_shop(shop_id=shop_id, material_id=material_id)
        if existing is None:
            return None

        archived = replace(existing, is_active=False)
        self._records[material_id] = archived
        return archived

    def restore_for_shop(self, *, shop_id: str, material_id: str) -> MaterialRecord | None:
        existing = self.get_for_shop(shop_id=shop_id, material_id=material_id)
        if existing is None:
            return None

        restored = replace(existing, is_active=True)
        self._records[material_id] = restored
        return restored
