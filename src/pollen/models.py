"""Domain models used by the first implementation slice."""

from enum import Enum


class OrderStatus(str, Enum):
    """Simple lifecycle statuses for early order workflow tests."""

    NEW = "new"
    READY_TO_PACK = "ready_to_pack"
    SHIPPED = "shipped"


def can_transition(current: OrderStatus, target: OrderStatus) -> bool:
    """Allow only safe forward transitions in the early milestone."""
    allowed: dict[OrderStatus, set[OrderStatus]] = {
        OrderStatus.NEW: {OrderStatus.READY_TO_PACK},
        OrderStatus.READY_TO_PACK: {OrderStatus.SHIPPED},
        OrderStatus.SHIPPED: set(),
    }
    return target in allowed[current]
