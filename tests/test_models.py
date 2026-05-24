from pollen.models import OrderStatus, can_transition


def test_allows_forward_order_transition() -> None:
    assert can_transition(OrderStatus.NEW, OrderStatus.READY_TO_PACK)


def test_blocks_backward_order_transition() -> None:
    assert not can_transition(OrderStatus.READY_TO_PACK, OrderStatus.NEW)


def test_blocks_from_terminal_state() -> None:
    assert not can_transition(OrderStatus.SHIPPED, OrderStatus.NEW)
