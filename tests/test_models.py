from pollen.models import OrderStatus, can_transition


def test_allows_new_to_ready_to_pack_transition() -> None:
    assert can_transition(OrderStatus.NEW, OrderStatus.READY_TO_PACK)


def test_allows_new_to_waiting_on_stock_transition() -> None:
    assert can_transition(OrderStatus.NEW, OrderStatus.WAITING_ON_STOCK)


def test_allows_ready_to_pack_to_packed_transition() -> None:
    assert can_transition(OrderStatus.READY_TO_PACK, OrderStatus.PACKED)


def test_allows_packed_to_shipped_transition() -> None:
    assert can_transition(OrderStatus.PACKED, OrderStatus.SHIPPED)


def test_blocks_skipping_pack_transition() -> None:
    assert not can_transition(OrderStatus.READY_TO_PACK, OrderStatus.SHIPPED)


def test_blocks_backward_order_transition() -> None:
    assert not can_transition(OrderStatus.READY_TO_PACK, OrderStatus.NEW)


def test_blocks_from_terminal_state() -> None:
    assert not can_transition(OrderStatus.SHIPPED, OrderStatus.NEW)
