"""Shop-scoped order persistence helpers for Milestone 3.1 manual creation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OrderRecord:
    order_id: str
    shop_id: str
    customer_name: str
    source: str
    status: str


@dataclass(frozen=True)
class OrderItemRecord:
    order_item_id: str
    order_id: str
    shop_id: str
    product_sku: str
    quantity: int


class OrderRepository:
    """In-memory repository with strict shop scoping semantics."""

    def __init__(self) -> None:
        self._records: dict[str, OrderRecord] = {}
        self._items: dict[str, OrderItemRecord] = {}
        self._next_id = 1
        self._next_item_id = 1

    def create(self, *, shop_id: str, customer_name: str, source: str, status: str) -> OrderRecord:
        order_id = f"ord-{self._next_id}"
        self._next_id += 1
        created = OrderRecord(
            order_id=order_id,
            shop_id=shop_id,
            customer_name=customer_name,
            source=source,
            status=status,
        )
        self._records[order_id] = created
        return created

    def add_item(self, *, order_id: str, shop_id: str, product_sku: str, quantity: int) -> OrderItemRecord | None:
        order = self._records.get(order_id)
        if order is None or order.shop_id != shop_id:
            return None
        order_item_id = f"ord-item-{self._next_item_id}"
        self._next_item_id += 1
        created = OrderItemRecord(
            order_item_id=order_item_id,
            order_id=order_id,
            shop_id=shop_id,
            product_sku=product_sku,
            quantity=quantity,
        )
        self._items[order_item_id] = created
        return created

    def list_for_shop(self, *, shop_id: str) -> list[OrderRecord]:
        return [record for record in self._records.values() if record.shop_id == shop_id]

    def get_for_shop(self, *, shop_id: str, order_id: str) -> OrderRecord | None:
        record = self._records.get(order_id)
        if record is None or record.shop_id != shop_id:
            return None
        return record

    def list_items_for_order(self, *, shop_id: str, order_id: str) -> list[OrderItemRecord]:
        return [item for item in self._items.values() if item.shop_id == shop_id and item.order_id == order_id]

    def update_status_for_shop(self, *, shop_id: str, order_id: str, status: str) -> OrderRecord | None:
        existing = self.get_for_shop(shop_id=shop_id, order_id=order_id)
        if existing is None:
            return None
        updated = OrderRecord(
            order_id=existing.order_id,
            shop_id=existing.shop_id,
            customer_name=existing.customer_name,
            source=existing.source,
            status=status,
        )
        self._records[order_id] = updated
        return updated
