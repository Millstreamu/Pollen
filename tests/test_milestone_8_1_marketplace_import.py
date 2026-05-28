from pollen.integrations import (
    ExternalOrder,
    ExternalOrderItem,
    FixtureMarketplaceImportClient,
    MarketplaceImportClient,
)
from pollen.products import ProductRepository
from pollen.services import MarketplaceImportService, OrderService, ProductService


class StubInvalidClient(MarketplaceImportClient):
    def fetch_orders(self) -> list[ExternalOrder]:
        return [
            ExternalOrder(
                external_order_id="broken-1",
                customer_name="",
                items=(ExternalOrderItem(product_sku="", quantity=0),),
            )
        ]


def test_fixture_client_import_and_duplicate_guard(tmp_path) -> None:
    product_repo = ProductRepository()
    product_service = ProductService(product_repository=product_repo)
    product_service.create_product(
        authorization_header="Bearer user:u1:u1@example.com",
        name="Candle",
        sku="SKU-CANDLE",
        stock_on_hand=10,
        reorder_point=2,
    )
    order_service = OrderService(product_repository=product_repo)
    service = MarketplaceImportService(order_service=order_service)
    fixture = FixtureMarketplaceImportClient(fixture_path="tests/fixtures/marketplace_orders_etsy.json")

    first = service.import_orders(
        authorization_header="Bearer user:u1:u1@example.com",
        source="etsy",
        client=fixture,
    )
    second = service.import_orders(
        authorization_header="Bearer user:u1:u1@example.com",
        source="etsy",
        client=fixture,
    )

    assert first == {"created": 2, "duplicates": 0, "failed": 0}
    assert second == {"created": 0, "duplicates": 2, "failed": 0}


def test_import_logs_error_for_invalid_payload(capsys) -> None:
    service = MarketplaceImportService()

    result = service.import_orders(
        authorization_header="Bearer user:u1:u1@example.com",
        source="etsy",
        client=StubInvalidClient(),
    )

    captured = capsys.readouterr()
    assert result == {"created": 0, "duplicates": 0, "failed": 1}
    assert "ERROR marketplace import invalid payload" in captured.out

    events = service.list_import_events()
    assert len(events) == 1
    assert events[0]["code"] == "invalid_payload"
    assert "ERROR marketplace import invalid payload" in events[0]["message"]
