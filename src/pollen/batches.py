"""Shop-scoped make batch persistence for Milestone 4.1 create slice."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BatchRecord:
    batch_id: str
    shop_id: str
    product_id: str
    quantity: int
    status: str


class BatchRepository:
    def __init__(self) -> None:
        self._records: dict[str, BatchRecord] = {}
        self._next_id = 1

    def create(self, *, shop_id: str, product_id: str, quantity: int, status: str = "planned") -> BatchRecord:
        batch_id = f"bat-{self._next_id}"
        self._next_id += 1
        created = BatchRecord(batch_id=batch_id, shop_id=shop_id, product_id=product_id, quantity=quantity, status=status)
        self._records[batch_id] = created
        return created

    def list_for_shop(self, *, shop_id: str) -> list[BatchRecord]:
        return [r for r in self._records.values() if r.shop_id == shop_id]
