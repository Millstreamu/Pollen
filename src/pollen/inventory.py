"""Inventory movements and activity logs for stock adjustments."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InventoryMovementRecord:
    movement_id: str
    shop_id: str
    item_type: str
    item_id: str
    reason: str
    delta: int
    before_quantity: int
    after_quantity: int
    actor_user_id: str


@dataclass(frozen=True)
class ActivityLogRecord:
    activity_id: str
    shop_id: str
    activity_type: str
    entity_type: str
    entity_id: str
    message: str
    actor_user_id: str


class InventoryMovementRepository:
    def __init__(self) -> None:
        self._records: dict[str, InventoryMovementRecord] = {}
        self._next_id = 1

    def create(
        self,
        *,
        shop_id: str,
        item_type: str,
        item_id: str,
        reason: str,
        delta: int,
        before_quantity: int,
        after_quantity: int,
        actor_user_id: str,
    ) -> InventoryMovementRecord:
        movement_id = f"mov-{self._next_id}"
        self._next_id += 1
        created = InventoryMovementRecord(
            movement_id=movement_id,
            shop_id=shop_id,
            item_type=item_type,
            item_id=item_id,
            reason=reason,
            delta=delta,
            before_quantity=before_quantity,
            after_quantity=after_quantity,
            actor_user_id=actor_user_id,
        )
        self._records[movement_id] = created
        return created

    def list_for_shop(self, *, shop_id: str) -> list[InventoryMovementRecord]:
        return [record for record in self._records.values() if record.shop_id == shop_id]


class ActivityLogRepository:
    def __init__(self) -> None:
        self._records: dict[str, ActivityLogRecord] = {}
        self._next_id = 1

    def create(
        self,
        *,
        shop_id: str,
        activity_type: str,
        entity_type: str,
        entity_id: str,
        message: str,
        actor_user_id: str,
    ) -> ActivityLogRecord:
        activity_id = f"act-{self._next_id}"
        self._next_id += 1
        created = ActivityLogRecord(
            activity_id=activity_id,
            shop_id=shop_id,
            activity_type=activity_type,
            entity_type=entity_type,
            entity_id=entity_id,
            message=message,
            actor_user_id=actor_user_id,
        )
        self._records[activity_id] = created
        return created

    def list_for_shop(self, *, shop_id: str) -> list[ActivityLogRecord]:
        return [record for record in self._records.values() if record.shop_id == shop_id]
