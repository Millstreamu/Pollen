"""Shop-scoped order persistence helpers for Milestone 1.2 continuation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OrderRecord:
    order_id: str
    shop_id: str
    product_sku: str
    quantity: int


class OrderRepository:
    """In-memory repository with strict shop scoping semantics."""

    def __init__(self) -> None:
        self._records: dict[str, OrderRecord] = {}
        self._next_id = 1

    def create(self, *, shop_id: str, product_sku: str, quantity: int) -> OrderRecord:
        order_id = f"ord-{self._next_id}"
        self._next_id += 1
        created = OrderRecord(
            order_id=order_id,
            shop_id=shop_id,
            product_sku=product_sku,
            quantity=quantity,
        )
        self._records[order_id] = created
        return created

    def list_for_shop(self, *, shop_id: str) -> list[OrderRecord]:
        return [record for record in self._records.values() if record.shop_id == shop_id]

    def get_for_shop(self, *, shop_id: str, order_id: str) -> OrderRecord | None:
        record = self._records.get(order_id)
        if record is None or record.shop_id != shop_id:
            return None
        return record
