"""Domain models used by the first implementation slice."""

from enum import Enum


class OrderStatus(str, Enum):
    """Order lifecycle statuses through Milestone 3.3 pack-and-ship slice."""

    NEW = "new"
    WAITING_ON_STOCK = "waiting_on_stock"
    READY_TO_PACK = "ready_to_pack"
    PACKED = "packed"
    SHIPPED = "shipped"


def can_transition(current: OrderStatus, target: OrderStatus) -> bool:
    """Allow only safe forward transitions in the early milestone."""
    allowed: dict[OrderStatus, set[OrderStatus]] = {
        OrderStatus.NEW: {OrderStatus.WAITING_ON_STOCK, OrderStatus.READY_TO_PACK},
        OrderStatus.WAITING_ON_STOCK: set(),
        OrderStatus.READY_TO_PACK: {OrderStatus.PACKED},
        OrderStatus.PACKED: {OrderStatus.SHIPPED},
        OrderStatus.SHIPPED: set(),
    }
    return target in allowed[current]
