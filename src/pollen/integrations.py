"""Mocked external marketplace integration boundaries for Milestone 8.1."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExternalOrderItem:
    product_sku: str
    quantity: int


@dataclass(frozen=True)
class ExternalOrder:
    external_order_id: str
    customer_name: str
    items: tuple[ExternalOrderItem, ...]


class MarketplaceImportClient:
    """Interface boundary for marketplace order import clients."""

    def fetch_orders(self) -> list[ExternalOrder]:
        raise NotImplementedError


class FixtureMarketplaceImportClient(MarketplaceImportClient):
    """Fixture-backed client for deterministic import testing."""

    def __init__(self, *, fixture_path: str) -> None:
        self._fixture_path = Path(fixture_path)

    def fetch_orders(self) -> list[ExternalOrder]:
        payload = json.loads(self._fixture_path.read_text(encoding="utf-8"))
        orders: list[ExternalOrder] = []
        for raw_order in payload.get("orders", []):
            items = tuple(
                ExternalOrderItem(
                    product_sku=str(raw_item.get("product_sku", "")).strip(),
                    quantity=int(raw_item.get("quantity", 0)),
                )
                for raw_item in raw_order.get("items", [])
            )
            orders.append(
                ExternalOrder(
                    external_order_id=str(raw_order.get("external_order_id", "")).strip(),
                    customer_name=str(raw_order.get("customer_name", "")).strip(),
                    items=items,
                )
            )
        return orders
