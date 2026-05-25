"""Application services for shop-scoped workflows."""

from __future__ import annotations

from pollen.auth import AuthService
from pollen.orders import OrderRecord, OrderRepository


class OrderService:
    """Create/read order records with server-owned shop scoping."""

    def __init__(
        self,
        *,
        auth_service: AuthService | None = None,
        order_repository: OrderRepository | None = None,
    ) -> None:
        self._auth_service = auth_service or AuthService()
        self._order_repository = order_repository or OrderRepository()

    def create_order(
        self,
        *,
        authorization_header: str | None,
        product_sku: str,
        quantity: int,
        requested_shop_id: str | None = None,
    ) -> OrderRecord | None:
        """Create order for current authenticated shop.

        `requested_shop_id` is accepted for compatibility with incoming payloads,
        but intentionally ignored to enforce server-side shop ownership.
        """
        _ = requested_shop_id
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._order_repository.create(
            shop_id=context.shop.shop_id,
            product_sku=product_sku,
            quantity=quantity,
        )

    def list_orders(self, *, authorization_header: str | None) -> list[OrderRecord]:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return []

        return self._order_repository.list_for_shop(shop_id=context.shop.shop_id)

    def get_order(self, *, authorization_header: str | None, order_id: str) -> OrderRecord | None:
        context = self._auth_service.resolve_context(authorization_header)
        if context is None:
            return None

        return self._order_repository.get_for_shop(shop_id=context.shop.shop_id, order_id=order_id)
