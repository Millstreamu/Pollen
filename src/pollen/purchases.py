"""Purchase persistence models for Milestone 5.2."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PurchaseRecord:
    purchase_id: str
    shop_id: str
    status: str
    supplier: str | None
    expected_date: str | None


@dataclass(frozen=True)
class PurchaseItemRecord:
    purchase_item_id: str
    purchase_id: str
    shop_id: str
    item_type: str
    item_id: str
    quantity: int

    @property
    def material_id(self) -> str:
        return self.item_id


class PurchaseRepository:
    """In-memory purchase persistence with strict shop scoping."""

    def __init__(self) -> None:
        self._purchases: dict[str, PurchaseRecord] = {}
        self._items: dict[str, PurchaseItemRecord] = {}
        self._next_purchase_id = 1
        self._next_item_id = 1

    def create(self, *, shop_id: str, status: str, supplier: str | None, expected_date: str | None) -> PurchaseRecord:
        purchase_id = f"pur-{self._next_purchase_id}"
        self._next_purchase_id += 1
        created = PurchaseRecord(
            purchase_id=purchase_id,
            shop_id=shop_id,
            status=status,
            supplier=supplier,
            expected_date=expected_date,
        )
        self._purchases[purchase_id] = created
        return created

    def add_item(
        self,
        *,
        shop_id: str,
        purchase_id: str,
        item_id: str,
        quantity: int,
        item_type: str = "material",
    ) -> PurchaseItemRecord | None:
        purchase = self._purchases.get(purchase_id)
        if purchase is None or purchase.shop_id != shop_id or quantity <= 0:
            return None
        if item_type not in {"material", "product"}:
            return None
        purchase_item_id = f"pit-{self._next_item_id}"
        self._next_item_id += 1
        item = PurchaseItemRecord(
            purchase_item_id=purchase_item_id,
            purchase_id=purchase_id,
            shop_id=shop_id,
            item_type=item_type,
            item_id=item_id,
            quantity=quantity,
        )
        self._items[purchase_item_id] = item
        return item

    def list_for_shop(self, *, shop_id: str) -> list[PurchaseRecord]:
        return [purchase for purchase in self._purchases.values() if purchase.shop_id == shop_id]

    def get_for_shop(self, *, shop_id: str, purchase_id: str) -> PurchaseRecord | None:
        purchase = self._purchases.get(purchase_id)
        if purchase is None or purchase.shop_id != shop_id:
            return None
        return purchase

    def list_items_for_purchase(self, *, shop_id: str, purchase_id: str) -> list[PurchaseItemRecord]:
        return [
            item
            for item in self._items.values()
            if item.shop_id == shop_id and item.purchase_id == purchase_id
        ]

    def update_status_for_shop(self, *, shop_id: str, purchase_id: str, status: str) -> PurchaseRecord | None:
        purchase = self.get_for_shop(shop_id=shop_id, purchase_id=purchase_id)
        if purchase is None:
            return None
        updated = PurchaseRecord(
            purchase_id=purchase.purchase_id,
            shop_id=purchase.shop_id,
            status=status,
            supplier=purchase.supplier,
            expected_date=purchase.expected_date,
        )
        self._purchases[purchase_id] = updated
        return updated
