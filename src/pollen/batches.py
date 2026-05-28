"""Shop-scoped make batch persistence for Milestone 4.1 create slice."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime


@dataclass(frozen=True)
class BatchRecord:
    batch_id: str
    shop_id: str
    product_id: str
    quantity: int
    status: str
    started_at: str | None = None
    completed_at: str | None = None


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


    def get_for_shop(self, *, shop_id: str, batch_id: str) -> BatchRecord | None:
        record = self._records.get(batch_id)
        if record is None or record.shop_id != shop_id:
            return None
        return record

    def update_for_shop(
        self,
        *,
        shop_id: str,
        batch_id: str,
        status: str,
        started_at: str | None,
        completed_at: str | None,
    ) -> BatchRecord | None:
        existing = self.get_for_shop(shop_id=shop_id, batch_id=batch_id)
        if existing is None:
            return None
        updated = replace(existing, status=status, started_at=started_at, completed_at=completed_at)
        self._records[batch_id] = updated
        return updated

    def now_iso(self) -> str:
        return datetime.now(UTC).isoformat()
