"""Shop-scoped product persistence for Milestone 2.1."""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class ProductRecord:
    product_id: str
    shop_id: str
    name: str
    sku: str
    stock_on_hand: int
    reserved_stock: int
    reorder_point: int
    is_active: bool
    sale_price: float
    estimated_material_cost: float
    estimated_packaging_shipping_cost: float
    platform_fee_percent: float
    category: str = ""
    default_batch_size: int = 1
    workflow_status: str = "Active"
    notes: str = ""

    @property
    def is_low_stock(self) -> bool:
        return self.available_stock <= self.reorder_point

    @property
    def available_stock(self) -> int:
        return self.stock_on_hand - self.reserved_stock

    @property
    def estimated_platform_fee(self) -> float:
        return self.sale_price * (self.platform_fee_percent / 100)

    @property
    def estimated_profit_per_sale(self) -> float:
        return (
            self.sale_price
            - self.estimated_material_cost
            - self.estimated_packaging_shipping_cost
            - self.estimated_platform_fee
        )


class ProductRepository:
    """In-memory repository with strict shop scoping semantics."""

    def __init__(self) -> None:
        self._records: dict[str, ProductRecord] = {}
        self._next_id = 1

    def create(
        self,
        *,
        shop_id: str,
        name: str,
        sku: str,
        stock_on_hand: int,
        reorder_point: int,
        sale_price: float = 0.0,
        estimated_material_cost: float = 0.0,
        estimated_packaging_shipping_cost: float = 0.0,
        platform_fee_percent: float = 0.0,
        category: str = "",
        default_batch_size: int = 1,
        workflow_status: str = "Active",
        notes: str = "",
    ) -> ProductRecord:
        product_id = f"prd-{self._next_id}"
        self._next_id += 1
        created = ProductRecord(
            product_id=product_id,
            shop_id=shop_id,
            name=name,
            sku=sku,
            stock_on_hand=stock_on_hand,
            reserved_stock=0,
            reorder_point=reorder_point,
            is_active=True,
            sale_price=sale_price,
            estimated_material_cost=estimated_material_cost,
            estimated_packaging_shipping_cost=estimated_packaging_shipping_cost,
            platform_fee_percent=platform_fee_percent,
            category=category,
            default_batch_size=default_batch_size,
            workflow_status=workflow_status,
            notes=notes,
        )
        self._records[product_id] = created
        return created

    def list_for_shop(self, *, shop_id: str, include_archived: bool = False) -> list[ProductRecord]:
        records = [record for record in self._records.values() if record.shop_id == shop_id]
        if include_archived:
            return records
        return [record for record in records if record.is_active]

    def get_for_shop(self, *, shop_id: str, product_id: str) -> ProductRecord | None:
        record = self._records.get(product_id)
        if record is None or record.shop_id != shop_id:
            return None
        return record

    def update_for_shop(
        self,
        *,
        shop_id: str,
        product_id: str,
        name: str,
        sku: str,
        stock_on_hand: int,
        reserved_stock: int,
        reorder_point: int,
        sale_price: float,
        estimated_material_cost: float,
        estimated_packaging_shipping_cost: float,
        platform_fee_percent: float,
        category: str | None = None,
        default_batch_size: int | None = None,
        workflow_status: str | None = None,
        notes: str | None = None,
    ) -> ProductRecord | None:
        existing = self.get_for_shop(shop_id=shop_id, product_id=product_id)
        if existing is None:
            return None

        updated = replace(
            existing,
            name=name,
            sku=sku,
            stock_on_hand=stock_on_hand,
            reserved_stock=reserved_stock,
            reorder_point=reorder_point,
            sale_price=sale_price,
            estimated_material_cost=estimated_material_cost,
            estimated_packaging_shipping_cost=estimated_packaging_shipping_cost,
            platform_fee_percent=platform_fee_percent,
            category=existing.category if category is None else category,
            default_batch_size=existing.default_batch_size if default_batch_size is None else default_batch_size,
            workflow_status=existing.workflow_status if workflow_status is None else workflow_status,
            notes=existing.notes if notes is None else notes,
        )
        self._records[product_id] = updated
        return updated

    def reserve_by_sku_for_shop(self, *, shop_id: str, sku: str, quantity: int) -> ProductRecord | None:
        if quantity <= 0:
            return None
        for product in self.list_for_shop(shop_id=shop_id, include_archived=False):
            if product.sku != sku:
                continue
            if product.available_stock < quantity:
                return None
            updated = replace(product, reserved_stock=product.reserved_stock + quantity)
            self._records[product.product_id] = updated
            return updated
        return None


    def release_by_sku_for_shop(self, *, shop_id: str, sku: str, quantity: int) -> ProductRecord | None:
        if quantity <= 0:
            return None
        for product in self.list_for_shop(shop_id=shop_id, include_archived=False):
            if product.sku != sku:
                continue
            if product.reserved_stock < quantity:
                return None
            updated = replace(product, reserved_stock=product.reserved_stock - quantity)
            self._records[product.product_id] = updated
            return updated
        return None

    def archive_for_shop(self, *, shop_id: str, product_id: str) -> ProductRecord | None:
        existing = self.get_for_shop(shop_id=shop_id, product_id=product_id)
        if existing is None:
            return None

        archived = replace(existing, is_active=False)
        self._records[product_id] = archived
        return archived

    def restore_for_shop(self, *, shop_id: str, product_id: str) -> ProductRecord | None:
        existing = self.get_for_shop(shop_id=shop_id, product_id=product_id)
        if existing is None:
            return None

        restored = replace(existing, is_active=True)
        self._records[product_id] = restored
        return restored
