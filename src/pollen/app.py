"""App shell and core helpers for the Pollen milestone slices."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from urllib.parse import parse_qs, urlsplit

from pollen.auth import AuthService
from pollen.inventory import ActivityLogRepository, InventoryMovementRepository
from pollen.materials import MaterialRepository
from pollen.products import ProductRepository
from pollen.recipes import RecipeRepository
from pollen.services import (
    BatchService,
    MaterialService,
    MoneySummaryService,
    OrderService,
    ProductService,
    RecipeService,
    TodaySummaryService,
)

NAV_ITEMS: tuple[tuple[str, str], ...] = (
    ("Today", "/"),
    ("Orders", "/orders"),
    ("Inventory", "/products-stock"),
    ("Workshop", "/make-buy"),
    ("Money", "/money"),
    ("Settings", "/settings"),
)


@dataclass(frozen=True)
class AppResponse:
    status_code: int
    body: str


PRIVATE_ROUTES: tuple[str, ...] = ("/", "/orders", "/products-stock", "/make-buy", "/money", "/settings")


class AppShell:
    """Minimal app-shell router for placeholder milestone pages."""

    _DESCRIPTIONS = {
        "Today": "Your daily overview will appear here.",
        "Orders": "Order workflow tools will appear here.",
        "Inventory": "See stock, low stock, and restock workflows here.",
        "Workshop": "Create products, materials, and recipes here.",
        "Money": "Estimated money snapshots will appear here.",
        "Settings": "Shop settings and preferences will appear here.",
    }

    def __init__(
        self,
        auth_service: AuthService | None = None,
        product_service: ProductService | None = None,
        material_service: MaterialService | None = None,
    ) -> None:
        self._routes = {url: title for title, url in NAV_ITEMS}
        self._auth_service = auth_service or AuthService()
        product_repository = ProductRepository()
        material_repository = MaterialRepository()
        recipe_repository = RecipeRepository()
        movement_repository = InventoryMovementRepository()
        activity_repository = ActivityLogRepository()
        self._product_service = product_service or ProductService(
            auth_service=self._auth_service,
            product_repository=product_repository
        )
        purchase_product_repository = product_repository
        if product_service is not None:
            purchase_product_repository = product_service._product_repository  # noqa: SLF001
        self._material_service = material_service or MaterialService(
            auth_service=self._auth_service,
            material_repository=material_repository,
            movement_repository=movement_repository,
            activity_repository=activity_repository,
            product_repository=purchase_product_repository,
        )
        self._recipe_service = RecipeService(
            auth_service=self._auth_service,
            recipe_repository=recipe_repository,
            product_repository=product_repository,
            material_repository=material_repository,
        )
        order_product_repository = product_repository
        if product_service is not None:
            order_product_repository = product_service._product_repository  # noqa: SLF001
        batch_product_repository = product_repository
        if product_service is not None:
            batch_product_repository = product_service._product_repository  # noqa: SLF001
        batch_material_repository = material_repository
        if material_service is not None:
            batch_material_repository = material_service._material_repository  # noqa: SLF001
        self._batch_service = BatchService(
            auth_service=self._auth_service,
            product_repository=batch_product_repository,
            recipe_repository=self._recipe_service._recipe_repository,  # noqa: SLF001
            material_repository=batch_material_repository,
        )
        self._order_service = OrderService(
            auth_service=self._auth_service,
            product_repository=order_product_repository,
        )
        self._today_summary_service = TodaySummaryService(
            auth_service=self._auth_service,
            order_repository=self._order_service._order_repository,  # noqa: SLF001
            product_repository=self._product_service._product_repository,  # noqa: SLF001
            material_repository=self._material_service._material_repository,  # noqa: SLF001
            batch_repository=self._batch_service._batch_repository,  # noqa: SLF001
            purchase_repository=self._material_service._purchase_repository,  # noqa: SLF001
        )
        self._money_summary_service = MoneySummaryService(
            auth_service=self._auth_service,
            order_repository=self._order_service._order_repository,  # noqa: SLF001
            product_repository=self._product_service._product_repository,  # noqa: SLF001
        )

    def get(self, path: str, *, authorization_header: str | None = None) -> AppResponse:
        parsed_path = urlsplit(path)
        route_path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if route_path in PRIVATE_ROUTES and self._auth_service.resolve_context(authorization_header) is None:
            return AppResponse(status_code=401, body="Unauthorized")

        page_title = self._routes.get(route_path)
        if page_title is None:
            return AppResponse(status_code=404, body="Not Found")

        return AppResponse(
            status_code=200,
            body=self.render_page(page_title, authorization_header=authorization_header, query=query),
        )

    def post(
        self,
        path: str,
        *,
        authorization_header: str | None = None,
        form_data: dict[str, str] | None = None,
    ) -> AppResponse:
        if path not in {"/products-stock", "/make-buy", "/orders"}:
            return AppResponse(status_code=404, body="Not Found")
        if self._auth_service.resolve_context(authorization_header) is None:
            return AppResponse(status_code=401, body="Unauthorized")

        if path == "/make-buy":
            return self._handle_workshop_post(authorization_header=authorization_header, form_data=form_data)
        if path == "/orders":
            return self._handle_order_post(authorization_header=authorization_header, form_data=form_data)

        payload = form_data or {}
        action = payload.get("action")
        if action == "create":
            self._product_service.create_product(
                authorization_header=authorization_header,
                name=payload.get("name", ""),
                sku=payload.get("sku", ""),
                stock_on_hand=int(payload.get("stock_on_hand", "0")),
                reorder_point=int(payload.get("reorder_point", "0")),
                sale_price=float(payload.get("sale_price", "0") or 0),
                estimated_material_cost=float(payload.get("estimated_material_cost", "0") or 0),
                estimated_packaging_shipping_cost=float(
                    payload.get("estimated_packaging_shipping_cost", "0") or 0
                ),
                platform_fee_percent=float(payload.get("platform_fee_percent", "0") or 0),
            )
        elif action == "create_material":
            self._material_service.create_material(
                authorization_header=authorization_header,
                name=payload.get("name", ""),
                unit=payload.get("unit", ""),
                stock_on_hand=int(payload.get("stock_on_hand", "0")),
                reorder_point=int(payload.get("reorder_point", "0")),
            )
        elif action == "edit":
            product_id = payload.get("product_id")
            if product_id is not None:
                current_product = self._product_service.get_product(
                    authorization_header=authorization_header,
                    product_id=product_id,
                )
                self._product_service.update_product(
                    authorization_header=authorization_header,
                    product_id=product_id,
                    name=payload.get("name", current_product.name),
                    sku=payload.get("sku", current_product.sku),
                    stock_on_hand=int(payload.get("stock_on_hand", str(current_product.stock_on_hand))),
                    reorder_point=int(payload.get("reorder_point", str(current_product.reorder_point))),
                    sale_price=float(payload.get("sale_price", str(current_product.sale_price)) or 0),
                    estimated_material_cost=float(
                        payload.get("estimated_material_cost", str(current_product.estimated_material_cost)) or 0
                    ),
                    estimated_packaging_shipping_cost=float(
                        payload.get(
                            "estimated_packaging_shipping_cost",
                            str(current_product.estimated_packaging_shipping_cost),
                        )
                        or 0
                    ),
                    platform_fee_percent=float(
                        payload.get("platform_fee_percent", str(current_product.platform_fee_percent)) or 0
                    ),
                )
        elif action == "archive":
            product_id = payload.get("product_id")
            if product_id is not None:
                self._product_service.archive_product(
                    authorization_header=authorization_header,
                    product_id=product_id,
                )
        elif action == "restore":
            product_id = payload.get("product_id")
            if product_id is not None:
                self._product_service.restore_product(
                    authorization_header=authorization_header,
                    product_id=product_id,
                )
        elif action == "bulk_archive":
            selected_ids = payload.get("product_ids", "")
            for product_id in [pid.strip() for pid in selected_ids.split(",") if pid.strip()]:
                self._product_service.archive_product(
                    authorization_header=authorization_header,
                    product_id=product_id,
                )
        elif action == "adjust_stock":
            if payload.get("material_id"):
                self._material_service.adjust_material_stock(
                    authorization_header=authorization_header,
                    material_id=payload.get("material_id", ""),
                    delta=int(payload.get("delta", "0")),
                    reason=payload.get("reason", ""),
                )
            else:
                product_id = payload.get("product_id", "")
                self._product_service.adjust_product_stock(
                    authorization_header=authorization_header,
                    product_id=product_id,
                    delta=int(payload.get("delta", "0")),
                    reason=payload.get("reason", ""),
                )
        elif action == "bulk_restore":
            selected_ids = payload.get("product_ids", "")
            for product_id in [pid.strip() for pid in selected_ids.split(",") if pid.strip()]:
                self._product_service.restore_product(
                    authorization_header=authorization_header,
                    product_id=product_id,
                )
        elif action == "create_recipe_item":
            self._recipe_service.create_recipe_item(
                authorization_header=authorization_header,
                product_id=payload.get("product_id", ""),
                material_id=payload.get("material_id", ""),
                quantity_per_unit=int(payload.get("quantity_per_unit", "0")),
            )
        elif action == "edit_recipe_item":
            recipe_item_id = payload.get("recipe_item_id")
            if recipe_item_id:
                self._recipe_service.update_recipe_item(
                    authorization_header=authorization_header,
                    recipe_item_id=recipe_item_id,
                    material_id=payload.get("material_id", ""),
                    quantity_per_unit=int(payload.get("quantity_per_unit", "0")),
                )
        elif action == "archive_recipe_item":
            recipe_item_id = payload.get("recipe_item_id")
            if recipe_item_id:
                self._recipe_service.archive_recipe_item(
                    authorization_header=authorization_header,
                    recipe_item_id=recipe_item_id,
                )
        elif action == "add_to_purchase":
            self._material_service.add_to_purchase_draft(
                authorization_header=authorization_header,
                material_id=payload.get("material_id", ""),
            )
        elif action == "create_purchase":
            item_reference = payload.get("item_reference", "").strip()
            if item_reference:
                self._material_service.create_purchase_for_item(
                    authorization_header=authorization_header,
                    item_reference=item_reference,
                    supplier=payload.get("supplier"),
                    expected_date=payload.get("expected_date"),
                    status=payload.get("status", "draft"),
                )
            else:
                self._material_service.create_purchase_from_draft(
                    authorization_header=authorization_header,
                    supplier=payload.get("supplier"),
                    expected_date=payload.get("expected_date"),
                    status=payload.get("status", "draft"),
                )
        elif action == "receive_purchase":
            self._material_service.receive_purchase(
                authorization_header=authorization_header,
                purchase_id=payload.get("purchase_id", ""),
            )

        return self.get(path, authorization_header=authorization_header)

    def _handle_workshop_post(
        self,
        *,
        authorization_header: str,
        form_data: dict[str, str] | None,
    ) -> AppResponse:
        payload = form_data or {}
        action = payload.get("action")
        if action == "create_product":
            try:
                selling_price = float(payload.get("sale_price", "0") or 0)
                default_batch_size = int(payload.get("default_batch_size", "1"))
                stock_on_hand = int(payload.get("stock_on_hand", "0"))
                reorder_point = int(payload.get("reorder_point", "0"))
            except ValueError:
                return AppResponse(status_code=400, body="Product name, default batch size, and status are required")
            created_product = self._product_service.create_product(
                authorization_header=authorization_header,
                name=payload.get("name", ""),
                sku=payload.get("sku", ""),
                stock_on_hand=stock_on_hand,
                reorder_point=reorder_point,
                sale_price=selling_price,
                category=payload.get("category", ""),
                default_batch_size=default_batch_size,
                workflow_status=payload.get("workflow_status", "Draft"),
                notes=payload.get("notes", ""),
            )
            if created_product is None:
                return AppResponse(status_code=400, body="Product name, default batch size, and status are required")
            return self.get("/make-buy?created=product", authorization_header=authorization_header)
        elif action == "save_recipe":
            product_id = payload.get("product_id", "")
            recipe_rows, error = self._recipe_rows_from_payload(payload)
            if error is not None:
                return AppResponse(status_code=400, body=error)
            if self._product_service.get_product(
                authorization_header=authorization_header,
                product_id=product_id,
            ) is None:
                return AppResponse(status_code=400, body="Choose a product before saving a recipe")
            for existing in self._recipe_service.list_recipe_items(
                authorization_header=authorization_header,
                product_id=product_id,
            ):
                self._recipe_service.archive_recipe_item(
                    authorization_header=authorization_header,
                    recipe_item_id=existing.recipe_item_id,
                )
            for material_id, quantity_per_unit in recipe_rows:
                created = self._recipe_service.create_recipe_item(
                    authorization_header=authorization_header,
                    product_id=product_id,
                    material_id=material_id,
                    quantity_per_unit=quantity_per_unit,
                )
                if created is None:
                    return AppResponse(status_code=400, body="Choose an existing material and a positive quantity per unit")
            return self.get(f"/make-buy?recipe_saved={product_id}", authorization_header=authorization_header)
        elif action == "create_recipe_item":
            self._recipe_service.create_recipe_item(
                authorization_header=authorization_header,
                product_id=payload.get("product_id", ""),
                material_id=payload.get("material_id", ""),
                quantity_per_unit=int(payload.get("quantity_per_unit", "0")),
            )
        elif action == "archive_recipe_item":
            recipe_item_id = payload.get("recipe_item_id")
            if recipe_item_id:
                self._recipe_service.archive_recipe_item(
                    authorization_header=authorization_header,
                    recipe_item_id=recipe_item_id,
                )
        elif action == "create":
            try:
                stock_on_hand = int(payload.get("stock_on_hand", ""))
                reorder_point = int(payload.get("reorder_point", ""))
            except ValueError:
                return AppResponse(status_code=400, body="Material name, unit, current stock, and reorder point are required")
            created_material = self._material_service.create_material(
                authorization_header=authorization_header,
                name=payload.get("name", ""),
                unit=payload.get("unit", ""),
                stock_on_hand=stock_on_hand,
                reorder_point=reorder_point,
                supplier=payload.get("supplier"),
                notes=payload.get("notes"),
            )
            if created_material is None:
                return AppResponse(status_code=400, body="Material name, unit, current stock, and reorder point are required")
            return_to_recipe = payload.get("return_to_recipe", "").strip()
            if return_to_recipe:
                return self.get(f"/make-buy?created=material&return_to_recipe={return_to_recipe}", authorization_header=authorization_header)
        elif action == "edit":
            material_id = payload.get("material_id")
            if material_id is not None:
                current_material = self._material_service.get_material(
                    authorization_header=authorization_header,
                    material_id=material_id,
                )
                if current_material is not None:
                    self._material_service.update_material(
                        authorization_header=authorization_header,
                        material_id=material_id,
                        name=payload.get("name", current_material.name),
                        unit=payload.get("unit", current_material.unit),
                        stock_on_hand=int(payload.get("stock_on_hand", str(current_material.stock_on_hand))),
                        reorder_point=int(payload.get("reorder_point", str(current_material.reorder_point))),
                    )
        elif action == "archive":
            material_id = payload.get("material_id")
            if material_id is not None:
                self._material_service.archive_material(
                    authorization_header=authorization_header,
                    material_id=material_id,
                )
        elif action == "adjust_stock":
            material_id = payload.get("material_id", "")
            self._material_service.adjust_material_stock(
                authorization_header=authorization_header,
                material_id=material_id,
                delta=int(payload.get("delta", "0")),
                reason=payload.get("reason", ""),
            )
        elif action == "create_batch":
            created_batch, error = self._batch_service.create_batch(
                authorization_header=authorization_header,
                product_id=payload.get("product_id", ""),
                quantity=int(payload.get("quantity", "0")),
            )
            if created_batch is None:
                return AppResponse(status_code=400, body=error or "Batch creation failed")
        elif action == "start_batch":
            started_batch, error = self._batch_service.start_batch(
                authorization_header=authorization_header,
                batch_id=payload.get("batch_id", ""),
            )
            if started_batch is None:
                return AppResponse(status_code=400, body=error or "Batch start failed")
        elif action == "complete_batch":
            completed_batch, error = self._batch_service.complete_batch(
                authorization_header=authorization_header,
                batch_id=payload.get("batch_id", ""),
            )
            if completed_batch is None:
                return AppResponse(status_code=400, body=error or "Batch complete failed")
        elif action == "restore":
            material_id = payload.get("material_id")
            if material_id is not None:
                self._material_service.restore_material(
                    authorization_header=authorization_header,
                    material_id=material_id,
                )
        elif action == "add_to_purchase":
            self._material_service.add_to_purchase_draft(
                authorization_header=authorization_header,
                material_id=payload.get("material_id", ""),
            )
        elif action == "create_purchase":
            item_reference = payload.get("item_reference", "").strip()
            if item_reference:
                self._material_service.create_purchase_for_item(
                    authorization_header=authorization_header,
                    item_reference=item_reference,
                    supplier=payload.get("supplier"),
                    expected_date=payload.get("expected_date"),
                    status=payload.get("status", "draft"),
                )
            else:
                self._material_service.create_purchase_from_draft(
                    authorization_header=authorization_header,
                    supplier=payload.get("supplier"),
                    expected_date=payload.get("expected_date"),
                    status=payload.get("status", "draft"),
                )
        elif action == "receive_purchase":
            self._material_service.receive_purchase(
                authorization_header=authorization_header,
                purchase_id=payload.get("purchase_id", ""),
            )

        return self.get("/make-buy", authorization_header=authorization_header)

    def _recipe_rows_from_payload(self, payload: dict[str, str]) -> tuple[list[tuple[str, int]], str | None]:
        indexed_rows: list[tuple[int, str, str]] = []
        for key, value in payload.items():
            if not key.startswith("material_id_"):
                continue
            try:
                row_number = int(key.removeprefix("material_id_"))
            except ValueError:
                continue
            if payload.get(f"remove_{row_number}") == "1":
                continue
            indexed_rows.append((row_number, value.strip(), payload.get(f"quantity_per_unit_{row_number}", "").strip()))

        if not indexed_rows and (payload.get("material_id") or payload.get("quantity_per_unit")):
            indexed_rows.append((1, payload.get("material_id", "").strip(), payload.get("quantity_per_unit", "").strip()))

        rows: list[tuple[str, int]] = []
        seen_material_ids: set[str] = set()
        for _, material_id, quantity_text in sorted(indexed_rows):
            if not material_id and not quantity_text:
                continue
            if not material_id:
                return [], "Material is required for each recipe row"
            if material_id in seen_material_ids:
                return [], "Each material can only be added once to a recipe"
            seen_material_ids.add(material_id)
            try:
                quantity_per_unit = int(quantity_text)
            except ValueError:
                return [], "Quantity per unit must be positive"
            if quantity_per_unit <= 0:
                return [], "Quantity per unit must be positive"
            rows.append((material_id, quantity_per_unit))
        return rows, None

    def _handle_order_post(self, *, authorization_header: str, form_data: dict[str, str] | None) -> AppResponse:
        payload = form_data or {}
        action = payload.get("action", "create")
        if action == "pack":
            updated = self._order_service.mark_order_packed(
                authorization_header=authorization_header,
                order_id=payload.get("order_id", ""),
            )
            if updated is None:
                return AppResponse(status_code=400, body="Invalid order transition")
            return self.get("/orders", authorization_header=authorization_header)
        if action == "ship":
            updated = self._order_service.mark_order_shipped(
                authorization_header=authorization_header,
                order_id=payload.get("order_id", ""),
            )
            if updated is None:
                return AppResponse(status_code=400, body="Invalid order transition")
            return self.get("/orders", authorization_header=authorization_header)
        if action == "cancel":
            updated = self._order_service.cancel_order(
                authorization_header=authorization_header,
                order_id=payload.get("order_id", ""),
            )
            if updated is None:
                return AppResponse(status_code=400, body="Invalid order transition")
            return self.get("/orders", authorization_header=authorization_header)

        created = self._order_service.create_order(
            authorization_header=authorization_header,
            customer_name=payload.get("customer_name", ""),
            items=[
                {
                    "product_sku": payload.get("product_sku", ""),
                    "quantity": payload.get("quantity", "0"),
                }
            ],
        )
        if created is None:
            return AppResponse(status_code=400, body="Invalid order payload")
        return self.get("/orders", authorization_header=authorization_header)


    def _render_workflow_dialog(self, *, dialog_id: str, title: str, description: str, body: str, open_dialog: bool = False) -> str:
        open_class = " modal-open" if open_dialog else ""
        return (
            f"<div class='modal-popover{open_class}' id='{dialog_id}' role='dialog' aria-modal='true' aria-labelledby='{dialog_id}-title'>"
            "<a class='modal-backdrop' aria-label='Close popup' href='#'></a>"
            "<div class='modal-card'>"
            "<div class='modal-header'>"
            f"<div><h3 id='{dialog_id}-title'>{title}</h3><p>{description}</p></div>"
            "<a class='modal-close' aria-label='Close popup' href='#'>×</a>"
            "</div>"
            f"{body}"
            "</div></div>"
        )

    def _render_stock_control_dialog(
        self,
        *,
        dialog_id: str,
        title: str,
        description: str,
        hidden_field: str,
        item_id: str,
        current_stock: str,
        reorder_point: str,
        reason_placeholder: str,
    ) -> str:
        body = (
            "<div class='details-list stock-control-summary'>"
            f"<p><strong>Current stock</strong><span>{self._h(current_stock)}</span></p>"
            f"<p><strong>Reorder point</strong><span>{self._h(reorder_point)}</span></p>"
            "</div>"
            "<form class='form-grid compact-form' method='post' action='/products-stock'>"
            "<input type='hidden' name='action' value='adjust_stock'>"
            f"<input type='hidden' name='{self._h(hidden_field)}' value='{self._h(item_id)}'>"
            "<label>Adjust <input name='delta' type='number' value='0'></label>"
            f"<label>Reason <input name='reason' placeholder='{self._h(reason_placeholder)}'></label>"
            "<div class='dialog-actions'><button class='primary' type='submit'>Save adjustment</button>"
            "<a class='outline' href='#'>Cancel</a></div></form>"
        )
        return self._render_workflow_dialog(
            dialog_id=dialog_id,
            title=self._h(title),
            description=self._h(description),
            body=body,
        )


    def _render_products_page(
        self,
        *,
        authorization_header: str,
        view: str = "active",
        edit_product_id: str | None = None,
        query: dict[str, list[str]] | None = None,
    ) -> str:
        products = self._product_service.list_products(authorization_header=authorization_header)
        archived_products = self._product_service.list_products(
            authorization_header=authorization_header,
            include_archived=True,
        )
        archived_only = [product for product in archived_products if not product.is_active]
        create_form = (
            "<form class='form-grid' method='post' action='/products-stock'>"
            "<input type='hidden' name='action' value='create'>"
            "<label>Name <input name='name' required></label>"
            "<label>SKU <input name='sku' required></label>"
            "<label>Stock <input name='stock_on_hand' type='number' min='0' required></label>"
            "<label>Reorder <input name='reorder_point' type='number' min='0' required></label>"
            "<label>Sale price <input name='sale_price' type='number' min='0' step='0.01' value='0'></label>"
            "<label>Material cost <input name='estimated_material_cost' type='number' min='0' step='0.01' value='0'></label>"
            "<label>Packaging/shipping cost <input name='estimated_packaging_shipping_cost' type='number' min='0' step='0.01' value='0'></label>"
            "<label>Platform fee % <input name='platform_fee_percent' type='number' min='0' step='0.01' value='0'></label>"
            "<div class='dialog-actions'><button class='primary' type='submit'>Save product</button>"
            "<a class='outline' href='#'>Cancel</a></div>"
            "</form>"
        )
        create_dialog = self._render_workflow_dialog(
            dialog_id="add-product-dialog",
            title="Add product",
            description="Create a product without moving the workflow to the bottom of the page.",
            body=create_form,
        )
        if not products and not archived_only:
            return (
            "<section class='workflow-card'><h2>Products list</h2>"
            "<p>No products yet. Add your first product to start tracking stock.</p>"
            "<a class='primary' href='#add-product-dialog'>Add product ＋</a>"
            f"{create_dialog}</section>"
        )

        rows = "".join(
            self._render_product_row(product=product, edit_product_id=edit_product_id)
            for product in products
        )


        archived_rows = "".join(
            "<tr>"
            f"<td><input type='checkbox' disabled aria-label='Select {product.product_id}'></td>"
            f"<td>{product.product_id}</td>"
            f"<td>{product.name}</td>"
            f"<td>{product.sku}</td>"
            "<td>"
            "<form method='post' action='/products-stock'>"
            "<input type='hidden' name='action' value='restore'>"
            f"<input type='hidden' name='product_id' value='{product.product_id}'>"
            "<button type='submit'>Restore</button>"
            "</form>"
            "</td>"
            "</tr>"
            for product in archived_only
        )
        view_controls = (
            "<p class='segmented-label'><strong>View:</strong> "
            "<a href='/products-stock?view=active'>Active</a> · "
            "<a href='/products-stock?view=archived'>Archived</a> · "
            "<a href='/products-stock?view=all'>All</a></p>"
        )

        archived_section = (
            "<section class='workflow-card'><h3>Archived products</h3>"
            "<table><thead><tr><th>Select</th><th>ID</th><th>Name</th><th>SKU</th><th>Action</th></tr></thead><tbody>"
            f"{archived_rows}"
            "</tbody></table></section>"
            if archived_only
            else ""
        )

        normalized_view = view if view in {"active", "archived", "all"} else "active"
        show_active = normalized_view in {"active", "all"}
        show_archived = normalized_view in {"archived", "all"}

        bulk_actions = (
            "<p>Archive or restore several products at once by entering comma-separated IDs.</p>"
            "<form class='inline-form record-tools' method='post' action='/products-stock'>"
            "<label>Product IDs <input name='product_ids' placeholder='prd-1, prd-2'></label>"
            "<button type='submit' name='action' value='bulk_archive'>Archive selected</button>"
            "<button type='submit' name='action' value='bulk_restore'>Restore selected</button>"
            "</form>"
        )

        active_section = (
            "<section class='workflow-card'><h2>Products list</h2>"
            "<p>Review stock levels and use row actions to edit or archive.</p>"
            f"{view_controls}"
            f"{bulk_actions}"
            "<table><thead><tr>"
            "<th>Select</th><th>ID</th><th>Name</th><th>SKU</th><th>Stock</th><th>Reorder</th><th>Status</th><th>Actions</th>"
            "</tr></thead><tbody>"
            f"{rows}"
            "</tbody></table>"
            f"{self._render_recipe_management(authorization_header=authorization_header, query=query)}"f"{self._render_audit_sections(authorization_header=authorization_header)}"
"</section>"
            if show_active
            else ""
        )

        page_intro = (
            "<section class='workflow-intro'><h3>Products workflow</h3>"
            "<p>Add products, monitor stock health, and keep archived products easy to recover.</p>"
            "</section>"
        )
        add_section = (
            "<section class='workflow-card workflow-actions'><h3>Add product</h3>"
            "<p>Open product creation only when you need it.</p>"
            "<a class='primary' href='#add-product-dialog'>Add product ＋</a></section>"
            f"{create_dialog}"
        )

        return (
            f"{page_intro}"
            f"{add_section if show_active else ''}"
            f"{active_section}"
            f"{archived_section if show_archived else ''}"
        )


    def _render_product_row(self, *, product, edit_product_id: str | None) -> str:
        if edit_product_id == product.product_id:
            return (
                "<tr>"
                f"<td><input type='checkbox' disabled aria-label='Select {product.product_id}'></td>"
                f"<td>{product.product_id}</td>"
                "<td colspan='4'>"
                "<form class='form-grid compact-form' method='post' action='/products-stock'>"
                "<input type='hidden' name='action' value='edit'>"
                f"<input type='hidden' name='product_id' value='{product.product_id}'>"
                f"<label>Name <input name='name' value='{product.name}' required></label>"
                f"<label>SKU <input name='sku' value='{product.sku}' required></label>"
                f"<label>Stock <input name='stock_on_hand' type='number' min='0' value='{product.stock_on_hand}' required></label>"
                f"<label>Reorder <input name='reorder_point' type='number' min='0' value='{product.reorder_point}' required></label>"
                f"<label>Sale price <input name='sale_price' type='number' min='0' step='0.01' value='{product.sale_price}'></label>"
                f"<label>Material cost <input name='estimated_material_cost' type='number' min='0' step='0.01' value='{product.estimated_material_cost}'></label>"
                f"<label>Packaging/shipping cost <input name='estimated_packaging_shipping_cost' type='number' min='0' step='0.01' value='{product.estimated_packaging_shipping_cost}'></label>"
                f"<label>Platform fee % <input name='platform_fee_percent' type='number' min='0' step='0.01' value='{product.platform_fee_percent}'></label>"
                "<button type='submit'>Save all fields</button>"
                "</form>"
                "</td>"
                f"<td><strong>{'⚠️ Low stock' if product.is_low_stock else '✅ Healthy'}</strong></td>"
                "<td><a href='/products-stock?view=active'>Cancel edit</a></td>"
                "</tr>"
            )

        return (
            "<tr>"
            f"<td><input type='checkbox' disabled aria-label='Select {product.product_id}'></td>"
            f"<td>{product.product_id}</td>"
            f"<td>{product.name}</td>"
            f"<td>{product.sku}</td>"
            f"<td>{product.stock_on_hand}</td>"
            f"<td>{product.reorder_point}</td>"
            f"<td><strong>{'⚠️ Low stock' if product.is_low_stock else '✅ Healthy'}</strong></td>"
            "<td>"
            f"<a href='/products-stock?view=active&edit={product.product_id}'>Edit</a> "
            "<form method='post' action='/products-stock' style='display:inline'>"
            "<input type='hidden' name='action' value='archive'>"
            f"<input type='hidden' name='product_id' value='{product.product_id}'>"
            "<button type='submit'>Archive</button>"
            "</form>"
            "</td>"
            "</tr>"
        )


    def _render_materials_page(
        self,
        *,
        authorization_header: str,
        view: str = "active",
        edit_material_id: str | None = None,
        query: dict[str, list[str]] | None = None,
    ) -> str:
        materials = self._material_service.list_materials(authorization_header=authorization_header)
        archived_materials = self._material_service.list_materials(
            authorization_header=authorization_header,
            include_archived=True,
        )
        archived_only = [material for material in archived_materials if not material.is_active]
        products = self._product_service.list_products(authorization_header=authorization_header)
        batch_form = (
            "<form class='form-grid compact-form' method='post' action='/make-buy'>"
            "<input type='hidden' name='action' value='create_batch'>"
            "<label>Product <select name='product_id'>"
            + "".join(f"<option value='{product.product_id}'>{product.name}</option>" for product in products)
            + "</select></label>"
            "<label>Quantity <input name='quantity' type='number' min='1' required></label>"
            "<div class='dialog-actions'><button class='primary' type='submit'>Save batch plan</button>"
            "<a class='outline' href='#'>Cancel</a></div>"
            "</form>"
        )
        create_batch_dialog = self._render_workflow_dialog(
            dialog_id="plan-batch-dialog",
            title="Plan a batch",
            description="Choose a product and quantity in a focused popup.",
            body=batch_form,
        )
        material_form = (
            "<form class='form-grid compact-form' method='post' action='/make-buy'>"
            "<input type='hidden' name='action' value='create'>"
            "<label>Name <input name='name' required></label>"
            "<label>Unit <input name='unit' required></label>"
            "<label>Stock <input name='stock_on_hand' type='number' min='0' required></label>"
            "<label>Reorder <input name='reorder_point' type='number' min='0' required></label>"
            "<div class='dialog-actions'><button class='primary' type='submit'>Save material</button>"
            "<a class='outline' href='#'>Cancel</a></div>"
            "</form>"
        )
        create_form = self._render_workflow_dialog(
            dialog_id="add-material-dialog",
            title="Add material",
            description="Add a supply item so stock and buy suggestions stay accurate.",
            body=material_form,
        )
        create_batch_form = create_batch_dialog
        quick_actions = (
            "<section class='workflow-card workflow-actions'><h3>Material actions</h3>"
            "<p>Open add and make-planning forms as popups instead of inline bottom-page panels.</p>"
            "<a class='primary' href='#create-new-material-dialog'>Add material ＋</a>"
            "<a class='outline' href='#plan-batch-dialog'>Plan batch ＋</a></section>"
        )
        if not materials and not archived_only:
            return (
                "<section><h2>Make / Buy workspace</h2>"
                "<p>No materials yet. Add your first material to track supplies.</p>"
                f"{self._render_buy_list(authorization_header=authorization_header)}"
                f"{quick_actions}{create_form}{create_batch_form}</section>"
            )

        rows = "".join(self._render_material_row(material=material, edit_material_id=edit_material_id) for material in materials)
        archived_rows = "".join(
            "<tr>"
            f"<td>{material.material_id}</td>"
            f"<td>{material.name}</td>"
            f"<td>{material.unit}</td>"
            "<td>"
            "<form method='post' action='/make-buy'>"
            "<input type='hidden' name='action' value='restore'>"
            f"<input type='hidden' name='material_id' value='{material.material_id}'>"
            "<button type='submit'>Restore</button>"
            "</form>"
            "</td>"
            "</tr>"
            for material in archived_only
        )
        filter_nav = (
            "<section class='workflow-card'><h3>View</h3>"
            "<p>Switch between active and archived materials without leaving this page.</p>"
            "<nav aria-label='Material view filters'>"
            "<ul class='segmented-list'>"
            "<li><a class='tab active' href='/make-buy?view=active'>Show active</a></li>"
            "<li><a class='tab' href='/make-buy?view=archived'>Show archived</a></li>"
            "<li><a class='tab' href='/make-buy?view=all'>Show all</a></li>"
            "</ul></nav></section>"
        )
        normalized_view = view if view in {"active", "archived", "all"} else "active"
        show_active = normalized_view in {"active", "all"}
        show_archived = normalized_view in {"archived", "all"}
        active_section = (
            "<section class='workflow-card'><h2>Materials</h2>"
            "<p>Manage materials with simple create, per-row edit, archive, and restore controls.</p>"
            f"{quick_actions}{create_form}{create_batch_form}"
            "<table><thead><tr><th>ID</th><th>Name</th><th>Unit</th><th>Stock</th><th>Reorder</th><th>Status</th><th>Actions</th></tr></thead><tbody>"
            f"{rows}"
            "</tbody></table>"
            f"{self._render_recipe_management(authorization_header=authorization_header, query=query)}"f"{self._render_audit_sections(authorization_header=authorization_header)}"
            "</section>"
            if show_active
            else ""
        )
        archived_section = (
            "<section class='workflow-card'><h3>Archived materials</h3>"
            "<table><thead><tr><th>ID</th><th>Name</th><th>Unit</th><th>Action</th></tr></thead><tbody>"
            f"{archived_rows}"
            "</tbody></table></section>"
            if archived_only and show_archived
            else ""
        )
        return (
            f"{filter_nav}"
            f"{self._render_buy_list(authorization_header=authorization_header)}"
            f"{active_section}"
            f"{archived_section}"
        )

    def _render_buy_list(self, *, authorization_header: str) -> str:
        low_materials = self._material_service.list_low_stock_suggestions(authorization_header=authorization_header)
        selected = self._material_service.list_purchase_draft(authorization_header=authorization_header)
        purchases = self._material_service.list_purchases(authorization_header=authorization_header)
        selected_names = ", ".join(material.name for material in selected)
        draft_summary = f"Draft purchase list: {selected_names}" if selected_names else "Draft purchase list: empty"
        purchase_rows = "".join(
            "<tr>"
            f"<td>{purchase.purchase_id}</td>"
            f"<td>{purchase.status}</td>"
            f"<td>{purchase.supplier or '-'}</td>"
            f"<td>{purchase.expected_date or '-'}</td>"
            "<td>"
            + (
                "<form method='post' action='/make-buy'>"
                "<input type='hidden' name='action' value='receive_purchase'>"
                f"<input type='hidden' name='purchase_id' value='{purchase.purchase_id}'>"
                "<button type='submit'>Mark Received</button>"
                "</form>"
                if purchase.status != "Received"
                else "-"
            )
            + "</td>"
            "</tr>"
            for purchase in purchases
        )
        purchase_history = (
            "<h4>Created purchases</h4>"
            "<table><thead><tr><th>ID</th><th>Status</th><th>Supplier</th><th>Expected date</th><th>Action</th></tr></thead>"
            f"<tbody>{purchase_rows}</tbody></table>"
            if purchases
            else "<h4>Created purchases</h4><p>No purchases yet.</p>"
        )
        purchase_form = (
            "<form class='form-grid compact-form' method='post' action='/make-buy'>"
            "<input type='hidden' name='action' value='create_purchase'>"
            "<label>Supplier <input name='supplier' placeholder='Optional supplier'></label>"
            "<label>Expected date <input name='expected_date' placeholder='YYYY-MM-DD (optional)'></label>"
            "<label>Status <select name='status'><option value='draft'>Draft</option><option value='ordered'>Ordered</option></select></label>"
            "<div class='dialog-actions'><button class='primary' type='submit'>Save purchase</button>"
            "<a class='outline' href='#'>Cancel</a></div>"
            "</form>"
        )
        create_form = self._render_workflow_dialog(
            dialog_id="create-purchase-dialog",
            title="Create purchase",
            description="Save supplier and expected-date details without keeping the form open on the page.",
            body=purchase_form,
        )
        purchase_action = "<a class='primary' href='#create-purchase-dialog'>Create purchase ＋</a>"
        if not low_materials:
            return (
                "<section class='workflow-card' id='create-purchase'><h3>Buy list suggestions</h3><p class='empty-state'>No low materials right now. Add materials and reorder points to unlock suggestions.</p>"
                f"<p>{draft_summary}</p>{purchase_action}{create_form}{purchase_history}</section>"
            )

        rows = "".join(
            "<tr>"
            f"<td>{row['name']}</td>"
            f"<td>{row['stock_on_hand']} {row['unit']}</td>"
            f"<td>{row['reorder_point']} {row['unit']}</td>"
            f"<td>{row['suggested_quantity']} {row['unit']}</td>"
            "<td>"
            "<form method='post' action='/make-buy'>"
            "<input type='hidden' name='action' value='add_to_purchase'>"
            f"<input type='hidden' name='material_id' value='{row['material_id']}'>"
            "<button type='submit'>Add to Purchase</button></form>"
            "</td></tr>"
            for row in low_materials
        )
        return (
            "<section class='workflow-card' id='create-purchase'><h3>Buy list suggestions</h3>"
            "<p>Suggested reorder quantity rule: max(1, (reorder point × 2) − stock on hand).</p>"
            "<table><thead><tr><th>Material</th><th>On hand</th><th>Reorder point</th><th>Suggested qty</th><th>Action</th></tr></thead><tbody>"
            f"{rows}</tbody></table>"
            f"<p>{draft_summary}</p>"
            f"{purchase_action}{create_form}"
            f"{purchase_history}"
            "</section>"
        )

    def _render_material_row(self, *, material, edit_material_id: str | None) -> str:
        if edit_material_id == material.material_id:
            return (
                "<tr>"
                f"<td>{material.material_id}</td>"
                "<td colspan='4'>"
                "<form class='form-grid compact-form' method='post' action='/make-buy'>"
                "<input type='hidden' name='action' value='edit'>"
                f"<input type='hidden' name='material_id' value='{material.material_id}'>"
                f"<label>Name <input name='name' value='{material.name}' required></label>"
                f"<label>Unit <input name='unit' value='{material.unit}' required></label>"
                f"<label>Stock <input name='stock_on_hand' type='number' min='0' value='{material.stock_on_hand}' required></label>"
                f"<label>Reorder <input name='reorder_point' type='number' min='0' value='{material.reorder_point}' required></label>"
                "<button type='submit'>Save all fields</button>"
                "</form>"
                "</td>"
                f"<td><strong>{'⚠️ Low stock' if material.is_low_stock else '✅ Healthy'}</strong></td>"
                "<td><a href='/make-buy'>Cancel edit</a></td>"
                "</tr>"
            )

        return (
            "<tr>"
            f"<td>{material.material_id}</td>"
            f"<td>{material.name}</td>"
            f"<td>{material.unit}</td>"
            f"<td>{material.stock_on_hand}</td>"
            f"<td>{material.reorder_point}</td>"
            f"<td><strong>{'⚠️ Low stock' if material.is_low_stock else '✅ Healthy'}</strong></td>"
            "<td>"
            f"<a href='/make-buy?view=active&edit={material.material_id}'>Edit</a> "
            "<form method='post' action='/make-buy' style='display:inline'>"
            "<input type='hidden' name='action' value='archive'>"
            f"<input type='hidden' name='material_id' value='{material.material_id}'>"
            "<button type='submit'>Archive</button>"
            "</form>"
            "</td>"
            "</tr>"
        )


    def _render_recipe_management(self, *, authorization_header: str, query: dict[str, list[str]] | None = None) -> str:
        products = self._product_service.list_products(authorization_header=authorization_header)
        materials = self._material_service.list_materials(authorization_header=authorization_header)
        requested_product = query.get("materials_needed_for", [""])[0] if query is not None else ""
        requested_quantity = query.get("quantity", ["1"])[0] if query is not None else "1"
        try:
            calculation_quantity = max(1, int(requested_quantity))
        except ValueError:
            calculation_quantity = 1

        sections: list[str] = ["<section class='workflow-card'><h3>Product recipes</h3>"]
        for product in products:
            can_make = self._recipe_service.can_make_quantity(
                authorization_header=authorization_header,
                product_id=product.product_id,
            )
            needed_quantity = calculation_quantity if requested_product == product.product_id else 1
            needed = self._recipe_service.materials_needed(
                authorization_header=authorization_header,
                product_id=product.product_id,
                quantity=needed_quantity,
            )
            item_rows = "".join(
                "<li>"
                f"{item['material_name']}: {item['needed']} {item['unit']}"
                "<form method='post' action='/products-stock' style='display:inline'>"
                "<input type='hidden' name='action' value='archive_recipe_item'>"
                f"<input type='hidden' name='recipe_item_id' value='{item['recipe_item_id']}'>"
                "<button type='submit'>Remove</button></form></li>"
                for item in needed
            )
            material_options = "".join(
                f"<option value='{material.material_id}'>{material.name}</option>" for material in materials
            )
            sections.append(
                f"<article class='recipe-card'><h4>{product.name} recipe</h4><p>Can make now: {can_make} units</p>"
                "<form class='inline-form recipe-form' method='post' action='/products-stock'>"
                "<input type='hidden' name='action' value='create_recipe_item'>"
                f"<input type='hidden' name='product_id' value='{product.product_id}'>"
                f"<label>Material <select name='material_id'>{material_options}</select></label>"
                "<label>Qty per unit <input name='quantity_per_unit' type='number' min='1' required></label>"
                "<a class='outline muted' href='#create-new-material-dialog'>+ Create New Material</a><button type='submit'>+ Add Material</button></form>"
                f"<ul>{item_rows}</ul>"
                "<form class='inline-form recipe-form' method='get' action='/products-stock'>"
                f"<input type='hidden' name='materials_needed_for' value='{product.product_id}'>"
                f"<label>Plan quantity <input name='quantity' type='number' min='1' value='{needed_quantity}'></label>"
                "<button type='submit'>Calculate materials needed</button></form></article>"
            )
        sections.append("</section>")
        return "".join(sections)

    def render_page(
        self,
        page_title: str,
        *,
        authorization_header: str | None = None,
        query: dict[str, list[str]] | None = None,
    ) -> str:
        current_path = next((href for label, href in NAV_ITEMS if label == page_title), "")
        icon_map = {
            "Today": "⌂",
            "Orders": "▢",
            "Inventory": "⬡",
            "Workshop": "⚒",
            "Money": "$",
            "Settings": "⚙",
        }
        nav_links = "".join(
            f"<li><a href=\"{href}\"{' aria-current=\'page\'' if href == current_path else ''}>"
            f"<span class='nav-icon'>{icon_map[label]}</span>{label}</a></li>"
            for label, href in NAV_ITEMS
        )
        page_subtitles = {
            "Today": "See what needs attention in your shop.",
            "Orders": "Track new, packed, and shipped orders.",
            "Inventory": "See stock, low stock, buy list, and incoming purchases.",
            "Workshop": "Create products, materials, and recipes.",
            "Money": "See sales, costs, and estimated profit.",
            "Settings": "Manage your shop details and basic connections.",
        }
        page_content = ""
        if page_title == "Today" and authorization_header is not None:
            page_content = self._render_today_dashboard(authorization_header=authorization_header)
        elif page_title == "Orders" and authorization_header is not None:
            page_content = self._render_orders_dashboard(authorization_header=authorization_header)
        elif page_title == "Inventory" and authorization_header is not None:
            view = "active"
            if query is not None:
                requested_view = query.get("view", ["active"])[0]
                if requested_view in {"active", "archived", "all"}:
                    view = requested_view
            edit_product_id = query.get("edit", [None])[0] if query is not None else None
            page_content = self._render_products_dashboard(
                authorization_header=authorization_header,
                view=view,
                edit_product_id=edit_product_id,
                query=query,
            )
        elif page_title == "Workshop" and authorization_header is not None:
            view = "active"
            if query is not None:
                requested_view = query.get("view", ["active"])[0]
                if requested_view in {"active", "archived", "all"}:
                    view = requested_view
            edit_material_id = query.get("edit", [None])[0] if query is not None else None
            page_content = self._render_make_buy_dashboard(
                authorization_header=authorization_header,
                view=view,
                edit_material_id=edit_material_id,
                query=query,
            )
        elif page_title == "Money" and authorization_header is not None:
            page_content = self._render_money_dashboard(authorization_header=authorization_header)
        elif page_title == "Settings" and authorization_header is not None:
            page_content = self._render_settings_dashboard(authorization_header=authorization_header)
        else:
            page_content = f"<p>{self._DESCRIPTIONS[page_title]}</p>"

        context = self._auth_service.resolve_context(authorization_header) if authorization_header else None
        account_name = self._h(context.user.email) if context is not None else "Signed out"
        shop_name = self._h(context.shop.name) if context is not None else "Pollen"
        avatar = self._avatar_label(context.user.email if context is not None else "Pollen")

        return (
            "<!doctype html>"
            "<html lang='en'>"
            "<head>"
            "<meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>{page_title} · Pollen</title>"
            f"{self._render_styles()}"
            "</head>"
            "<body>"
            "<a class='skip-link' href='#main-content'>Skip to main content</a>"
            "<div class='app-shell'>"
            "<aside class='sidebar'>"
            "<a class='brand' href='/' aria-label='Pollen home'><span class='brand-mark'>✿</span><strong>Pollen</strong></a>"
            "<nav aria-label='Primary'><ul>"
            f"{nav_links}"
            "</ul></nav>"
            "<a class='bee-card' href='/settings#help'><span class='bee'>🐝</span><span><strong>Pollen Guide</strong><em>Open guide</em></span><span>›</span></a>"
            "</aside>"
            "<main id='main-content' class='workspace'>"
            "<header class='topbar'>"
            "<div class='page-heading'><p class='eyebrow'>Small seller workspace</p>"
            f"<h1>{page_title}</h1><p>{page_subtitles[page_title]}</p></div>"
            "<form class='search' role='search' action='/orders' method='get'><span>⌕</span><input aria-label='Search' name='q' placeholder='Search orders, products, etc...'></form>"
            "<div class='user-tools'><a class='ghost-icon' aria-label='Notifications' href='/#today-actions'>♧</a>"
            f"<span class='avatar'>{avatar}</span><span class='account'><strong>{account_name}</strong><small>{shop_name}</small></span><span aria-hidden='true'>⌄</span></div>"
            "</header>"
            f"{page_content}"
            "</main></div>"
            f"{self._render_scripts()}"
            "</body></html>"
        )

    def _h(self, value: object) -> str:
        return escape(str(value), quote=True)

    def _avatar_label(self, value: str) -> str:
        pieces = [piece for piece in value.replace("@", " ").replace(".", " ").split() if piece]
        letters = "".join(piece[0] for piece in pieces[:2]).upper()
        return self._h(letters or "P")

    def _metric_card(self, icon: str, label: str, value: str | int, tone: str = "gold", note: str = "") -> str:
        return (
            f"<article class='metric-card tone-{tone}'><span class='metric-icon'>{icon}</span>"
            f"<span class='metric-label'>{label}</span><span class='metric-value'>{value}</span>"
            f"<small>{note}</small></article>"
        )

    def _badge(self, text: str, tone: str = "gold") -> str:
        return f"<span class='status-badge badge-{tone}'>{text}</span>"

    def _money(self, amount: float | int) -> str:
        return f"${float(amount):,.2f}"

    def _render_scripts(self) -> str:
        return (
            "<script>"
            "document.addEventListener('change',function(event){"
            "var select=event.target.closest('select[data-unit-target]');"
            "if(!select){return;}"
            "var target=document.getElementById(select.getAttribute('data-unit-target'));"
            "if(!target){return;}"
            "var option=select.options[select.selectedIndex];"
            "target.textContent=(option&&option.dataset.unit)?option.dataset.unit:target.dataset.emptyUnit;"
            "});"
            "document.addEventListener('click',function(event){"
            "var button=event.target.closest('[data-add-recipe-row]');"
            "if(!button){return;}"
            "var productId=button.getAttribute('data-add-recipe-row');"
            "var rows=document.querySelector('[data-recipe-rows=\\\"'+productId+'\\\"]');"
            "var template=document.querySelector('template[data-recipe-template=\\\"'+productId+'\\\"]');"
            "if(!rows||!template){return;}"
            "var index=parseInt(rows.getAttribute('data-next-index')||'1',10);"
            "rows.insertAdjacentHTML('beforeend',template.innerHTML.replaceAll('__INDEX__',String(index)));"
            "rows.setAttribute('data-next-index',String(index+1));"
            "var empty=rows.parentElement.querySelector('[data-recipe-empty]');"
            "if(empty){empty.remove();}"
            "});"
            "</script>"
        )

    def _render_today_dashboard(self, *, authorization_header: str) -> str:
        summary = self._today_summary_service.get_summary(authorization_header=authorization_header)
        orders = self._order_service.list_orders(authorization_header=authorization_header)
        products = self._product_service.list_products(authorization_header=authorization_header)
        materials = self._material_service.list_materials(authorization_header=authorization_header)
        batches = self._batch_service.list_batches(authorization_header=authorization_header)
        money = self._money_summary_service.get_summary(authorization_header=authorization_header)

        low_products = [product for product in products if product.is_low_stock]
        low_materials = [material for material in materials if material.is_low_stock]
        work_batches = [batch for batch in batches if batch.status in {"planned", "in-progress"}]
        orders_to_pack = [order for order in orders if order.status in {"new", "ready_to_pack", "packed"}]
        empty_note = (
            "<p>No work is waiting right now. Create your first order or add inventory to begin.</p>"
            if not orders and not products and not materials and not batches
            else ""
        )
        task_items: list[str] = []
        for order in orders_to_pack[:3]:
            task_items.append(
                f"<li><span>Review order {self._h(order.order_id)}</span>"
                f"<a class='outline small' href='/orders'>Open</a></li>"
            )
        for product in low_products[:2]:
            task_items.append(
                f"<li><span>Restock {self._h(product.name)}</span>"
                f"<a class='outline small' href='/products-stock'>Open stock</a></li>"
            )
        for material in low_materials[:2]:
            task_items.append(
                f"<li><span>Add {self._h(material.name)} to the buy list</span>"
                f"<a class='outline small' href='/make-buy#buy-list'>Open buy list</a></li>"
            )
        if not task_items:
            task_items.append("<li><span>No urgent tasks yet.</span><a class='outline small' href='/orders'>Create order</a></li>")

        stock_items = "".join(
            f"<li><span class='thumb'>▧</span><strong>{self._h(item.name)}</strong>"
            f"<span>{item.stock_on_hand} {self._h(getattr(item, 'unit', 'left'))}</span>"
            f"<span class='pill high'>Low</span><b>›</b></li>"
            for item in [*low_products, *low_materials][:4]
        ) or "<li><strong>No low stock yet</strong><span>Add reorder points to unlock suggestions.</span></li>"

        recent_rows = "".join(
            f"<tr><td>{self._h(order.order_id)}</td><td>{self._h(order.source)}</td>"
            f"<td>{self._badge(order.status.replace('_', ' ').title(), 'blue')}</td>"
            "<td><a class='outline small' href='/orders'>Open</a></td></tr>"
            for order in orders[:5]
        ) or "<tr><td colspan='4'>No orders yet.</td></tr>"

        return (
            "<section class='metric-grid four'>"
            f"{self._metric_card('▧', 'Orders to Pack', len(orders_to_pack))}"
            f"{self._metric_card('⚠', 'Low Stock Items', len(low_products) + len(low_materials), 'alert')}"
            f"{self._metric_card('⚒', 'Batches to Make', len(work_batches))}"
            f"{self._metric_card('$', 'Estimated Profit', self._format_currency(money['estimated_profit']), 'green', 'All time')}"
            "</section>"
            "<section class='dashboard-grid two-col'>"
            "<article class='panel' id='today-actions'><div class='panel-header'><h3>Today’s Tasks</h3><a class='outline' href='/orders'>Add Order ＋</a></div>"
            f"{empty_note}<ul class='task-list'>{''.join(task_items)}</ul><a class='text-link' href='/orders'>View order queue ›</a></article>"
            "<article class='panel'><div class='panel-header'><h3>Low Stock &amp; Buy Soon</h3><a class='outline' href='/products-stock'>View all stock</a></div>"
            f"<ul class='media-list'>{stock_items}</ul></article></section>"
            "<section class='panel wide'><div class='panel-header'><h3>Recent Orders</h3><div><a class='outline' href='/orders#create-order'>Add Order ＋</a><a class='primary' href='/orders'>View Orders</a></div></div>"
            f"<table><thead><tr><th>Order</th><th>Channel</th><th>Status</th><th></th></tr></thead><tbody>{recent_rows}</tbody></table></section>"
            "<section class='visually-hidden'><h3>Today summary</h3>"
            f"<span class='metric-value'>{summary['orders_to_pack']}</span><span class='metric-label'>Orders to pack</span>"
            f"<span class='metric-value'>{len(low_products)}</span><span class='metric-label'>Low-stock products</span>"
            "<h3>Today actions</h3><a href='/orders'>Pack and ship orders</a><a href='/products-stock'>Review low-stock products</a><a href='/make-buy'>Create a batch</a><a href='/make-buy'>Create a purchase</a><a href='/make-buy'>Open buy list</a><h3>Next steps</h3><a class='button-link' href='/orders'>Open highest-priority workflow</a></section>"
        )

    def _render_orders_dashboard(self, *, authorization_header: str) -> str:
        orders = self._order_service.list_orders(authorization_header=authorization_header)
        context = self._auth_service.resolve_context(authorization_header)
        order_items = {
            order.order_id: self._order_service._order_repository.list_items_for_order(  # noqa: SLF001
                shop_id=context.shop.shop_id,
                order_id=order.order_id,
            )
            if context is not None
            else []
            for order in orders
        }
        status_labels = {
            "new": "New",
            "waiting_on_stock": "Waiting on stock",
            "ready_to_pack": "Ready to pack",
            "packed": "Packed",
            "shipped": "Shipped",
            "cancelled": "Cancelled",
        }
        active_orders = [order for order in orders if order.status not in {"shipped", "cancelled"}]
        ready_orders = [order for order in orders if order.status in {"ready_to_pack", "packed"}]
        shipped_orders = [order for order in orders if order.status == "shipped"]
        rows = "".join(
            "<tr>"
            f"<td>{self._h(order.order_id)}</td><td>{self._h(order.customer_name)}</td>"
            f"<td><span class='channel'>{self._h(order.source[:1].upper() or 'M')}</span> {self._h(order.source)}</td>"
            f"<td>{self._h(order_items[order.order_id][0].product_sku if order_items[order.order_id] else 'No items')} × {order_items[order.order_id][0].quantity if order_items[order.order_id] else 0}</td>"
            f"<td>{self._badge(status_labels.get(order.status, order.status), 'green' if order.status in {'packed', 'shipped'} else 'gold' if order.status == 'ready_to_pack' else 'blue')}</td>"
            "<td>—</td><td>"
            "<form method='post' action='/orders' style='display:inline'><input type='hidden' name='action' value='pack'>"
            f"<input type='hidden' name='order_id' value='{self._h(order.order_id)}'><button type='submit'>Mark packed</button></form> "
            "<form method='post' action='/orders' style='display:inline'><input type='hidden' name='action' value='ship'>"
            f"<input type='hidden' name='order_id' value='{self._h(order.order_id)}'><button type='submit'>Mark shipped</button></form> "
            "<form method='post' action='/orders' style='display:inline'><input type='hidden' name='action' value='cancel'>"
            f"<input type='hidden' name='order_id' value='{self._h(order.order_id)}'><button type='submit'>Cancel order</button></form></td></tr>"
            for order in orders
        ) or "<tr><td colspan='7'>No orders yet. Create an order to start your shipping queue.</td></tr>"
        queue = "".join(
            "<li>"
            f"<strong>{self._h(order.order_id)}</strong><span>{self._h(order.customer_name)}</span>"
            "<form method='post' action='/orders'><input type='hidden' name='action' value='pack'>"
            f"<input type='hidden' name='order_id' value='{self._h(order.order_id)}'><button class='outline' type='submit'>Pack</button></form></li>"
            for order in ready_orders[:4]
        ) or "<li><strong>No packing queue yet</strong><span>Ready orders appear here.</span><a class='outline small' href='#create-order-dialog'>Add order</a></li>"
        order_form = (
            "<form class='form-grid compact-form' method='post' action='/orders'>"
            "<label>Customer <input name='customer_name' required></label>"
            "<label>Product SKU <input name='product_sku' required></label>"
            "<label>Quantity <input type='number' min='1' name='quantity' required></label>"
            "<div class='dialog-actions'><button class='primary' type='submit'>Create order</button>"
            "<a class='outline' href='#'>Cancel</a></div>"
            "</form>"
        )
        create_order_dialog = self._render_workflow_dialog(
            dialog_id="create-order-dialog",
            title="Create order",
            description="Add a customer order in a focused popup instead of a bottom-page form.",
            body=order_form,
        )
        legacy_create = (
            "<section class='panel wide' id='create-order'><div class='workflow-intro'>"
            "<h3>Order actions</h3><p>Create and update orders from one place.</p></div>"
            "<section class='workflow-card workflow-actions'><h3>Create order</h3>"
            "<p>Open the order form when you need it; the queue stays visible.</p>"
            "<a class='primary' href='#create-order-dialog'>Create order ＋</a></section>"
            f"{create_order_dialog}"
            "<section class='workflow-card'><h3>Order queue</h3>"
            "<p class='empty-state'>Orders ready for packing appear in the queue above.</p></section></section>"
        )
        return (
            "<section class='metric-grid three'>"
            f"{self._metric_card('▧', 'New', sum(1 for order in orders if order.status == 'new'))}"
            f"{self._metric_card('▧', 'Ready to Pack', len(ready_orders))}"
            f"{self._metric_card('▰', 'Shipped', len(shipped_orders), 'green')}"
            "</section><section class='dashboard-grid orders-layout'>"
            "<article class='panel'><div class='toolbar'><div><a class='tab active' href='/orders'>All</a><a class='tab' href='/orders?status=new'>New</a><a class='tab' href='/orders?filter=ready-to-pack'>Ready to Pack</a><a class='tab' href='/orders?status=shipped'>Shipped</a></div><div><a class='outline' href='#create-order-dialog'>Add Order ＋</a><a class='primary' href='/settings#sales-channels'>⇧ Import Orders</a></div></div>"
            f"<table><thead><tr><th>Order</th><th>Customer</th><th>Channel</th><th>Items</th><th>Status</th><th>Total</th><th></th></tr></thead><tbody>{rows}</tbody></table></article>"
            f"<aside class='panel side-panel'><h3>Packing Queue</h3><p>{len(active_orders)} active orders need attention.</p><ul class='queue-list'>{queue}</ul><a class='text-link' href='/orders'>View full queue ›</a></aside></section>"
            f"{legacy_create}"
        )

    def _render_products_dashboard(
        self,
        *,
        authorization_header: str,
        view: str = "active",
        edit_product_id: str | None = None,
        query: dict[str, list[str]] | None = None,
    ) -> str:
        _ = edit_product_id, query
        products = self._product_service.list_products(authorization_header=authorization_header)
        materials = self._material_service.list_materials(authorization_header=authorization_header)
        low_materials = self._material_service.list_low_stock_suggestions(authorization_header=authorization_header)
        low_products = [product for product in products if product.is_low_stock]
        purchases = self._material_service.list_purchases(authorization_header=authorization_header)
        draft_items = self._material_service.list_purchase_draft(authorization_header=authorization_header)

        product_rows = "".join(
            "<tr>"
            "<td><span class='thumb'>▧</span> "
            f"<a class='inventory-item-link' href='#stock-product-{self._h(product.product_id)}'>{self._h(product.name)}</a></td>"
            f"<td>{self._h(product.sku)}</td>"
            f"<td>{product.stock_on_hand}</td>"
            f"<td>{product.reserved_stock}</td>"
            f"<td>{product.reorder_point}</td>"
            f"<td>{self._badge('Low' if product.is_low_stock else 'Good', 'gold' if product.is_low_stock else 'green')}</td>"
            "</tr>"
            for product in products
        ) or "<tr><td colspan='6'>No finished products yet. Create products in Workshop, then track stock here.</td></tr>"
        material_rows = "".join(
            "<tr>"
            "<td><span class='thumb'>◫</span> "
            f"<a class='inventory-item-link' href='#stock-material-{self._h(material.material_id)}'>{self._h(material.name)}</a></td>"
            f"<td>{material.stock_on_hand} {self._h(material.unit)}</td>"
            f"<td>{material.reorder_point} {self._h(material.unit)}</td>"
            f"<td>{self._badge('Low' if material.is_low_stock else 'Good', 'gold' if material.is_low_stock else 'green')}</td>"
            "</tr>"
            for material in materials
        ) or "<tr><td colspan='4'>No materials yet. Add materials while defining recipes in Workshop.</td></tr>"
        stock_control_dialogs = "".join(
            self._render_stock_control_dialog(
                dialog_id=f"stock-product-{product.product_id}",
                title=f"Stock Control: {product.name}",
                description="Update finished product stock after a count, correction, or restock.",
                hidden_field="product_id",
                item_id=product.product_id,
                current_stock=str(product.stock_on_hand),
                reorder_point=str(product.reorder_point),
                reason_placeholder="count correction",
            )
            for product in products
        ) + "".join(
            self._render_stock_control_dialog(
                dialog_id=f"stock-material-{material.material_id}",
                title=f"Stock Control: {material.name}",
                description="Update material stock after receiving, counting, or correcting supplies.",
                hidden_field="material_id",
                item_id=material.material_id,
                current_stock=f"{material.stock_on_hand} {material.unit}",
                reorder_point=f"{material.reorder_point} {material.unit}",
                reason_placeholder="stock count",
            )
            for material in materials
        )
        buy_rows = "".join(
            "<tr>"
            f"<td><span class='thumb'>◫</span> {self._h(row['name'])}</td>"
            f"<td>{row['stock_on_hand']} {self._h(row['unit'])}</td>"
            f"<td>{row['suggested_quantity']} {self._h(row['unit'])}</td>"
            "<td><form method='post' action='/products-stock' style='display:inline'>"
            "<input type='hidden' name='action' value='add_to_purchase'>"
            f"<input type='hidden' name='material_id' value='{self._h(str(row['material_id']))}'>"
            "<button class='outline muted' type='submit'>Add to Purchase</button></form></td>"
            "</tr>"
            for row in low_materials[:8]
        ) or "<tr><td colspan='4'>No low materials right now. Reorder suggestions will appear here.</td></tr>"
        purchase_rows = "".join(
            "<tr>"
            f"<td>{self._h(purchase.purchase_id)}</td>"
            f"<td>{self._h(purchase.supplier or '-')}</td>"
            f"<td>{self._h(purchase.expected_date or '-')}</td>"
            f"<td>{self._badge(purchase.status, 'green' if purchase.status == 'Received' else 'blue')}</td>"
            "<td>"
            + (
                "<form method='post' action='/products-stock' style='display:inline'><input type='hidden' name='action' value='receive_purchase'>"
                f"<input type='hidden' name='purchase_id' value='{self._h(purchase.purchase_id)}'><button class='outline muted' type='submit'>Receive Purchase</button></form>"
                if purchase.status != "Received"
                else "—"
            )
            + "</td></tr>"
            for purchase in purchases[:8]
        ) or "<tr><td colspan='5'>No incoming purchases yet. Create a purchase when products or materials run low.</td></tr>"
        draft_note = (
            f"<p class='empty-state'>{len(draft_items)} material(s) staged for the next purchase.</p>"
            if draft_items
            else "<p class='empty-state'>Add low materials to purchase before creating an incoming purchase.</p>"
        )
        purchase_item_options = "".join(
            f"<option value='product:{self._h(product.product_id)}'>Product — {self._h(product.name)}</option>"
            for product in products
        ) + "".join(
            f"<option value='material:{self._h(material.material_id)}'>Material — {self._h(material.name)}</option>"
            for material in materials
        )
        purchase_item_select = (
            "<label>Item to purchase <select name='item_reference' required>"
            "<option value=''>Select a product or material</option>"
            f"{purchase_item_options}</select></label>"
        )
        create_purchase_dialog = self._render_workflow_dialog(
            dialog_id="create-purchase-dialog",
            title="Create purchase",
            description="Save an incoming purchase for an existing product or material.",
            body=(
                "<form class='form-grid compact-form' method='post' action='/products-stock'>"
                "<input type='hidden' name='action' value='create_purchase'>"
                f"{purchase_item_select}"
                "<label>Supplier <input name='supplier' placeholder='Optional supplier'></label>"
                "<label>Expected date <input type='date' name='expected_date'></label>"
                "<label>Status <select name='status'><option value='draft'>Draft</option><option value='ordered'>Ordered</option></select></label>"
                "<div class='dialog-actions'><button class='primary' type='submit'>Save purchase</button>"
                "<a class='outline' href='#'>Cancel</a></div></form>"
            ),
        )
        return (
            "<section class='metric-grid three'>"
            f"{self._metric_card('▧', 'Finished Products in Stock', sum(product.stock_on_hand for product in products), 'green', 'Total units')}"
            f"{self._metric_card('⚠', 'Low Stock Alerts', len(low_materials) + len(low_products), 'alert', 'Need reordering')}"
            f"{self._metric_card('▰', 'Incoming Purchases', len(purchases), 'gold', 'Open orders')}"
            "</section>"
            "<section class='panel wide'><div class='panel-header'><h3>Finished Products</h3><p>Current stock counts for products you sell. Select a product name for stock control.</p></div>"
            f"<table><thead><tr><th>Product</th><th>SKU</th><th>On Hand</th><th>Reserved</th><th>Reorder Point</th><th>Status</th></tr></thead><tbody>{product_rows}</tbody></table></section>"
            "<section class='panel wide'><div class='panel-header'><h3>Materials</h3><p>Current material stock and low-stock status. Select a material name for stock control.</p></div>"
            f"<table><thead><tr><th>Material</th><th>On Hand</th><th>Reorder Point</th><th>Status</th></tr></thead><tbody>{material_rows}</tbody></table></section>"
            "<section class='panel wide' id='buy-list'><div class='panel-header'><h3>Low Stock Alerts</h3><a class='outline' href='#create-purchase-dialog'>Create Purchase</a></div>"
            "<p>Suggested materials to reorder based on stock and reorder points.</p>"
            f"{draft_note}<table><thead><tr><th>Material</th><th>On Hand</th><th>Suggested Qty</th><th></th></tr></thead><tbody>{buy_rows}</tbody></table></section>"
            "<section class='panel wide' id='incoming-purchases'><div class='panel-header'><h3>Incoming Purchases</h3><a class='outline' href='#create-purchase-dialog'>Create Purchase</a></div>"
            "<p>Track and receive purchases when products or materials arrive.</p>"
            f"<table><thead><tr><th>Purchase</th><th>Supplier</th><th>Expected</th><th>Status</th><th></th></tr></thead><tbody>{purchase_rows}</tbody></table></section>"
            f"{stock_control_dialogs}"
            f"{create_purchase_dialog}"
        )

    def _render_make_buy_dashboard(
        self,
        *,
        authorization_header: str,
        view: str = "active",
        edit_material_id: str | None = None,
        query: dict[str, list[str]] | None = None,
    ) -> str:
        _ = view, edit_material_id
        products = self._product_service.list_products(authorization_header=authorization_header)
        materials = self._material_service.list_materials(authorization_header=authorization_header)
        recipe_items_by_product = {
            product.product_id: self._recipe_service.list_recipe_items(
                authorization_header=authorization_header,
                product_id=product.product_id,
            )
            for product in products
        }
        recipes_ready = sum(1 for rows in recipe_items_by_product.values() if rows)
        recipe_saved_product_id = query.get("recipe_saved", [""])[0] if query is not None else ""
        return_to_recipe_product_id = query.get("return_to_recipe", [""])[0] if query is not None else ""
        created_product = query is not None and query.get("created", [""])[0] == "product"
        created_material = query is not None and query.get("created", [""])[0] == "material"
        material_rows = "".join(
            "<tr>"
            f"<td><span class='thumb'>◫</span> <strong>{self._h(material.name)}</strong>"
            f"<small>{self._h(material.notes) if material.notes else 'Ready for product recipes'}</small></td>"
            f"<td>{material.stock_on_hand} {self._h(material.unit)}</td>"
            f"<td>{material.reorder_point} {self._h(material.unit)}</td>"
            f"<td>{self._h(material.supplier) if material.supplier else '—'}</td>"
            f"<td>{self._badge('Low' if material.is_low_stock else 'Ready', 'gold' if material.is_low_stock else 'green')}</td>"
            "</tr>"
            for material in materials
        )
        material_list = (
            "<table><thead><tr><th>Material</th><th>Current Stock</th><th>Reorder Point</th><th>Supplier</th><th>Status</th></tr></thead>"
            f"<tbody>{material_rows}</tbody></table>"
            if materials
            else (
                "<div class='empty-state chart-empty'><p>Create the materials and parts you use to make products. "
                "You’ll choose from these when setting up recipes.</p></div>"
            )
        )
        product_rows = "".join(
            self._render_workshop_product_row(
                product=product,
                recipe_items=recipe_items_by_product[product.product_id],
            )
            for product in products
        )
        product_list = (
            "<div class='table-scroll workshop-table-scroll'><table class='workshop-products-table'><thead><tr><th>Product</th><th>SKU</th><th>Category</th><th>Selling Price</th><th>Default Batch Size / Yield</th><th>Status</th><th>Recipe</th></tr></thead>"
            f"<tbody>{product_rows}</tbody></table></div>"
            if products
            else (
                "<div class='empty-state chart-empty'><p>Create the products you make in your workshop. "
                "After saving a product, set up the materials used for one unit.</p></div>"
            )
        )
        success_banner = ""
        if created_product:
            success_banner = "<div class='notice success' role='status'>Product saved. It is ready for recipe setup.</div>"
        elif recipe_saved_product_id:
            success_banner = "<div class='notice success' role='status'>Recipe saved. Product recipe status is updated.</div>"
        elif created_material:
            success_banner = "<div class='notice success' role='status'>Material saved. Return to the recipe and choose it from the material list.</div>"
        recipe_dialogs = "".join(
            self._render_recipe_dialog(
                product=product,
                materials=materials,
                recipe_items=recipe_items_by_product[product.product_id],
                open_dialog=product.product_id == return_to_recipe_product_id,
            )
            for product in products
        )
        return (
            "<section class='metric-grid three'>"
            f"{self._metric_card('▧', 'Products Defined', len(products), 'gold', 'Products you make')}"
            f"{self._metric_card('◫', 'Materials Defined', len(materials), 'green', 'Reusable workshop items')}"
            f"{self._metric_card('✓', 'Recipes Ready', recipes_ready, 'green', 'Products with materials assigned')}"
            "</section>"
            f"{success_banner}"
            "<section class='panel wide' id='products-you-make'>"
            "<div class='panel-header'><div><h3>Products You Make</h3>"
            "<p>Define the finished products you make, then set up the materials used for one unit.</p></div>"
            "<a class='primary' href='#create-product-dialog'>Create Product</a></div>"
            f"{product_list}"
            "</section>"
            "<section class='panel wide' id='workshop-materials'>"
            "<div class='panel-header'><div><h3>Workshop Materials</h3>"
            "<p>Add reusable items, parts, ingredients, and supplies for the products you make.</p></div>"
            "<a class='primary' href='#create-material-dialog'>Create Material</a></div>"
            f"{material_list}"
            "</section>"
            f"{self._render_create_material_dialog(return_to_recipe_product_id=return_to_recipe_product_id)}"
            f"{self._render_create_product_dialog()}"
            f"{recipe_dialogs}"
        )

    def _render_workshop_product_row(self, *, product, recipe_items: list) -> str:
        recipe_ready = bool(recipe_items)
        recipe_summary = f"{len(recipe_items)} material{'s' if len(recipe_items) != 1 else ''} assigned"
        product_note = self._h(product.notes) if product.notes else (recipe_summary if recipe_ready else "")
        product_note_markup = f"<small>{product_note}</small>" if product_note else ""
        recipe_dialog_href = f"#recipe-dialog-{self._h(product.product_id)}"
        recipe_cell = (
            f"{self._badge('Materials assigned', 'green')} <small>{recipe_summary}</small> "
            f"<a class='outline small' href='{recipe_dialog_href}'>Edit recipe</a>"
            if recipe_ready
            else f"<a class='status-badge badge-gold' href='{recipe_dialog_href}'>No recipe</a>"
        )
        return (
            "<tr>"
            f"<td><span class='thumb'>▧</span> <strong>{self._h(product.name)}</strong>{product_note_markup}</td>"
            f"<td>{self._h(product.sku) if product.sku else '—'}</td>"
            f"<td>{self._h(product.category) if product.category else '—'}</td>"
            f"<td>{self._format_currency(product.sale_price) if product.sale_price else '—'}</td>"
            f"<td>{product.default_batch_size}</td>"
            f"<td>{self._badge(product.workflow_status, 'green' if product.workflow_status == 'Active' else 'gold')}</td>"
            f"<td>{recipe_cell}</td>"
            "</tr>"
        )

    def _render_recipe_dialog(self, *, product, materials: list, recipe_items: list, open_dialog: bool = False) -> str:
        material_options = "".join(
            f"<option value='{self._h(material.material_id)}' data-unit='{self._h(material.unit)}'>{self._h(material.name)}</option>"
            for material in materials
        )
        options = "<option value=''>Choose a material</option>" + material_options

        def recipe_row(*, index: int | str, material_id: str = "", quantity: int | str = "") -> str:
            selected_options = options
            unit = "—"
            if material_id:
                selected_options = selected_options.replace(
                    f"<option value='{self._h(material_id)}'",
                    f"<option value='{self._h(material_id)}' selected",
                    1,
                )
                selected_material = next((material for material in materials if material.material_id == material_id), None)
                unit = selected_material.unit if selected_material is not None else "—"
            return (
                "<div class='recipe-builder-row' data-recipe-row>"
                f"<label>Material<select name='material_id_{index}' data-unit-target='unit-{self._h(product.product_id)}-{index}'>{selected_options}</select></label>"
                f"<label>Qty per unit<input name='quantity_per_unit_{index}' type='number' min='1' value='{self._h(quantity)}'></label>"
                f"<span class='unit-pill' id='unit-{self._h(product.product_id)}-{index}' data-empty-unit='—'>{self._h(unit)}</span>"
                "<label class='remove-row'><input type='checkbox' name='remove_"
                f"{index}' value='1'> Remove</label>"
                "</div>"
            )

        saved_rows = "".join(
            recipe_row(index=index, material_id=item.material_id, quantity=item.quantity_per_unit)
            for index, item in enumerate(recipe_items, start=1)
        )
        next_index = len(recipe_items) + 1
        empty_state = (
            "<div class='empty-state recipe-empty' data-recipe-empty>"
            "<p>No materials added yet. Add the materials or parts used to make this product.</p>"
            "</div>"
            if not recipe_items
            else ""
        )
        no_materials_state = (
            "<div class='empty-state chart-empty'><p>No materials added yet. Create a reusable material first, then return to this recipe and add it.</p></div>"
            if not materials
            else ""
        )
        add_material_button = (
            f"<button class='outline' type='button' data-add-recipe-row='{self._h(product.product_id)}'>+ Add Material</button>"
            if materials
            else "<button class='outline muted' type='button' disabled>+ Add Material</button>"
        )
        blank_template = recipe_row(index="__INDEX__") if materials else ""
        notes_value = self._h(product.notes) if product.notes else ""
        form = (
            "<form class='form-grid compact-form recipe-setup-form' method='post' action='/make-buy'>"
            "<input type='hidden' name='action' value='save_recipe'>"
            f"<input type='hidden' name='product_id' value='{self._h(product.product_id)}'>"
            f"<section class='full-span recipe-product-summary'><h4>Product</h4><p><strong>{self._h(product.name)}</strong></p></section>"
            "<section class='full-span recipe-builder'>"
            "<div class='recipe-section-heading'><div><h4>Materials per unit</h4>"
            "<p>Build the list for one finished item.</p></div>"
            f"{add_material_button}</div>"
            f"{no_materials_state}{empty_state}"
            f"<div class='recipe-builder-rows' data-recipe-rows='{self._h(product.product_id)}' data-next-index='{next_index}'>{saved_rows}</div>"
            f"<template data-recipe-template='{self._h(product.product_id)}'>{blank_template}</template>"
            "</section>"
            f"<label class='full-span recipe-secondary-notes'>Production notes <textarea name='production_notes' placeholder='Optional notes for making this product later.'>{notes_value}</textarea></label>"
            f"<p class='full-span muted recipe-yield-note'>Default batch size / yield: {product.default_batch_size}</p>"
            "<div class='dialog-actions'><a class='outline' href='#'>Cancel</a>"
            "<button class='primary' type='submit'>Save Recipe</button></div></form>"
        )
        return self._render_workflow_dialog(
            dialog_id=f"recipe-dialog-{self._h(product.product_id)}",
            title=f"Set Up Recipe: {self._h(product.name)}",
            description="Choose the materials and quantities needed to make one finished unit.",
            body=form,
            open_dialog=open_dialog,
        )

    def _render_create_material_dialog(self, *, return_to_recipe_product_id: str = "") -> str:
        add_material_form = (
            "<form class='form-grid compact-form' method='post' action='/make-buy'>"
            "<input type='hidden' name='action' value='create'>"
            f"<input type='hidden' name='return_to_recipe' value='{self._h(return_to_recipe_product_id)}'>"
            "<label>Material name <input name='name' required></label>"
            "<label>Unit <input name='unit' required></label>"
            "<label>Current stock <input name='stock_on_hand' type='number' min='0' value='0' required></label>"
            "<label>Reorder point <input name='reorder_point' type='number' min='0' value='0' required></label>"
            "<label>Supplier optional <input name='supplier' placeholder='Optional supplier'></label>"
            "<label class='full-span'>Notes optional <textarea name='notes' placeholder='Anything helpful to remember about this material.'></textarea></label>"
            "<div class='dialog-actions'><button class='primary' type='submit'>Save Material</button>"
            "<a class='outline' href='#'>Cancel</a></div></form>"
        )
        return self._render_workflow_dialog(
            dialog_id="create-material-dialog",
            title="Create Material",
            description="Add a material, part, ingredient, or supply you use in your workshop.",
            body=add_material_form,
        )


    def _render_create_product_dialog(self) -> str:
        create_product_form = (
            "<form class='form-grid compact-form' method='post' action='/make-buy'>"
            "<input type='hidden' name='action' value='create_product'>"
            "<label>Product name <input name='name' required></label>"
            "<label>SKU optional <input name='sku' placeholder='Optional SKU'></label>"
            "<label>Category optional <input name='category' placeholder='Candles, balms, gift sets...'></label>"
            "<label>Selling price optional <input name='sale_price' type='number' min='0' step='0.01' placeholder='0.00'></label>"
            "<label>Default batch size / yield <input name='default_batch_size' type='number' min='1' value='1' required></label>"
            "<label>Status <select name='workflow_status'><option value='Draft'>Draft</option><option value='Active'>Active</option></select></label>"
            "<label class='full-span'>Notes optional <textarea name='notes' placeholder='Anything helpful about this finished product.'></textarea></label>"
            "<div class='dialog-actions'><button class='primary' type='submit'>Save Product</button>"
            "<a class='outline' href='#'>Cancel</a></div></form>"
        )
        return self._render_workflow_dialog(
            dialog_id="create-product-dialog",
            title="Create Product",
            description="Add something you make or sell. You’ll define its materials and recipe next.",
            body=create_product_form,
        )

    def _render_money_dashboard(self, *, authorization_header: str) -> str:
        summary = self._money_summary_service.get_summary(authorization_header=authorization_header)
        products = self._product_service.list_products(authorization_header=authorization_header)
        orders = self._order_service.list_orders(authorization_header=authorization_header)
        if summary["shipped_item_count"] == 0:
            empty = "<div class='empty-state chart-empty'><p>No money data yet. Ship orders with product pricing to unlock estimated totals.</p><a class='button-link' href='/orders'>Ship orders first</a></div>"
        else:
            empty = ""
        rows = "".join(
            f"<tr><td>{self._h(order.order_id)}</td><td>Order</td><td>{self._h(order.customer_name)}</td><td>Estimated after shipment</td><td><a class='outline small' href='/orders'>Open</a></td></tr>"
            for order in orders[:5]
        ) or "<tr><td colspan='5'>No transactions yet.</td></tr>"
        profit_rows = "".join(
            f"<li><span class='thumb'>▧</span><strong>{self._h(product.name)}</strong><b>{self._format_currency(product.estimated_profit_per_sale)}</b></li>"
            for product in products[:5]
        ) or "<li><strong>No product pricing yet</strong><b>$0.00</b></li>"
        return (
            "<section class='metric-grid four'>"
            f"{self._metric_card('$', 'Sales', self._format_currency(summary['estimated_revenue']), 'green', 'Estimated')}"
            f"{self._metric_card('▤', 'Fees', self._format_currency(0), 'gold', 'Not tracked yet')}"
            f"{self._metric_card('▧', 'Material Costs', self._format_currency(summary['estimated_cost']), 'peach', 'Estimated')}"
            f"{self._metric_card('↗', 'Estimated Profit', self._format_currency(summary['estimated_profit']), 'green', 'Estimated')}"
            "</section><section class='dashboard-grid money-layout'>"
            f"<article class='panel chart-panel'><h3>This Month</h3>{empty}<div class='legend'><span class='sales'>Sales</span><span class='costs'>Costs</span></div><div class='bar-chart'><div><i style='height:0%'></i><b style='height:0%'></b><span>Week 1<small>No data</small></span></div><div><i style='height:0%'></i><b style='height:0%'></b><span>Week 2<small>No data</small></span></div><div><i style='height:0%'></i><b style='height:0%'></b><span>Week 3<small>No data</small></span></div><div><i style='height:0%'></i><b style='height:0%'></b><span>Week 4<small>No data</small></span></div></div></article>"
            "<div class='money-actions'><a class='outline' href='/products-stock#create-purchase-dialog'>Add Expense ＋</a><a class='primary' href='/money'>View Reports</a><p>* All values are estimated from recorded products and shipped orders.</p></div></section>"
            f"<section class='dashboard-grid two-col bottom-grid'><article class='panel'><h3>Recent Transactions</h3><table><thead><tr><th>Record</th><th>Type</th><th>Note</th><th>Amount</th><th></th></tr></thead><tbody>{rows}</tbody></table></article>"
            f"<article class='panel'><div class='panel-header'><h3>Top Product Profit</h3><small>Est. profit per unit</small></div><ul class='profit-list'>{profit_rows}</ul><a class='text-link' href='/products-stock'>View all products ›</a></article></section>"
            "<section class='visually-hidden'><h3>Money overview</h3>"
            f"<span class='metric-value'>{summary['shipped_order_count']}</span><span class='metric-label'>Shipped orders</span>"
            f"<span class='metric-value'>{summary['shipped_item_count']}</span><span class='metric-label'>Items shipped</span>"
            f"<span class='metric-value'>{self._format_currency(summary['estimated_revenue'])}</span><span class='metric-label'>Estimated revenue</span>"
            f"<span class='metric-value'>{self._format_currency(summary['estimated_cost'])}</span><span class='metric-label'>Estimated cost</span>"
            f"<span class='metric-value'>{self._format_currency(summary['estimated_profit'])}</span><span class='metric-label'>Estimated profit</span>"
            "<h3>Estimated profit and cost</h3><h3>Next steps</h3></section>"
        )

    def _render_settings_dashboard(self, *, authorization_header: str) -> str:
        context = self._auth_service.resolve_context(authorization_header)
        shop_name = self._h(context.shop.name) if context is not None else "Your shop"
        owner_email = self._h(context.user.email) if context is not None else "Not signed in"
        return (
            "<section class='metric-grid three'>"
            f"{self._metric_card('∪', 'Connected Channels', 0)}{self._metric_card('♙', 'Team Members', 1)}{self._metric_card('♧', 'Alerts Enabled', 0)}"
            "</section><section class='dashboard-grid two-col'>"
            "<article class='panel' id='shop-details'><div class='panel-header'><h3>Shop Details</h3><a class='outline' href='#shop-settings'>✎ Edit</a></div>"
            f"<dl class='details-list'><dt>Shop Name</dt><dd>{shop_name}</dd><dt>Owner Email</dt><dd>{owner_email}</dd><dt>Currency</dt><dd>Not configured</dd><dt>Time Zone</dt><dd>Not configured</dd></dl></article>"
            "<article class='panel' id='sales-channels'><h3>Sales Channels</h3><p>Connect your shop to sell in more places.</p>"
            "<ul class='channel-list'><li><span class='channel-logo etsy'>E</span><span><strong>Etsy</strong><small>Not connected</small></span><span class='status-badge badge-gold'>Not connected</span><a class='outline' href='#shop-settings'>Connect</a></li>"
            "<li><span class='channel-logo fb'>f</span><span><strong>Facebook Marketplace</strong><small>Not connected</small></span><span class='status-badge badge-gold'>Not connected</span><a class='outline' href='#shop-settings'>Connect</a></li></ul><p class='info'>ⓘ Integrations are basic and easy to set up.</p></article></section>"
            "<section class='panel wide' id='shop-settings'><h3>Shop settings</h3><p>Keep your shop details current so orders and labels stay accurate.</p><p class='coming-soon'>Settings forms are coming soon.</p><h3>Sales channels</h3><p>No connected sales channels yet. Add one when you are ready to import orders.</p><p class='coming-soon'>Channel connections are coming soon.</p><h3>Next steps</h3></section>"
        )

    def _render_styles(self) -> str:
        return (
            "<style>"
            "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');"
            ":root{color-scheme:light;--bg:#fffdf8;--surface:#ffffff;--surface-warm:#fff9ec;--ink:#111423;--muted:#69708a;--line:#e8e5df;--accent:#7a4f24;--accent-strong:#ea8a00;--accent-soft:#fff1bf;--honey:#ffc400;--honey-dark:#f2a900;--green:#2f7d24;--green-soft:#e2f2d8;--blue:#1266d6;--blue-soft:#e7f1ff;--red:#d71920;--red-soft:#ffe1e1;--orange-soft:#ffe6d2;--shadow:0 8px 22px rgba(17,20,35,.08)}"
            "*{box-sizing:border-box}html{font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--ink)}body{margin:0;min-height:100vh;background:radial-gradient(circle at 12% 0%,#fff7dc 0,transparent 26rem),#fffdf8;font-size:16px}a{color:var(--accent-strong);font-weight:700;text-decoration:none}a:hover{text-decoration:underline}.skip-link{position:absolute;left:1rem;top:-4rem;z-index:50;background:#111423;color:#fff;padding:.7rem 1rem;border-radius:999px}.skip-link:focus{top:1rem}.visually-hidden{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}"
            ".app-shell{display:grid;grid-template-columns:270px minmax(0,1fr);min-height:100vh}.sidebar{position:sticky;top:0;height:100vh;padding:1.7rem .75rem 1.4rem;border-right:1px solid var(--line);background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(255,250,239,.94));display:flex;flex-direction:column}.brand{display:flex;align-items:center;gap:.72rem;margin:.2rem .8rem 2.25rem;color:var(--ink)}.brand:hover{text-decoration:none}.brand strong{font-size:2.35rem;letter-spacing:-.07em}.brand-mark{display:grid;place-items:center;width:3.9rem;height:3.9rem;border-radius:50%;background:radial-gradient(circle,#ffd600 0 42%,#f7b500 43% 100%);color:#fff;font-size:2rem;box-shadow:inset 0 0 0 8px rgba(255,255,255,.22)}nav ul{display:grid;gap:.45rem;margin:0;padding:0;list-style:none}nav a{display:flex;align-items:center;gap:1rem;min-height:3.35rem;padding:0 1.25rem;border-radius:.6rem;color:#262c3f;font-weight:600;font-size:1.05rem}nav a:hover{background:#fff3c9;text-decoration:none;color:#111423}nav a[aria-current='page']{background:linear-gradient(90deg,#fff1be,#ffe39a);box-shadow:none;color:#111423}.nav-icon{display:grid;place-items:center;width:1.45rem;height:1.45rem;border:1.8px solid currentColor;border-radius:.32rem;font-size:.86rem;color:#111423}.bee-card{margin:auto .75rem 0;padding:1rem;border:1px solid #ffc44e;border-radius:.75rem;background:linear-gradient(135deg,#fff,#fff4d6);display:grid;grid-template-columns:auto 1fr auto;gap:.8rem;align-items:center;color:#111423}.bee-card strong,.bee-card em{display:block}.bee-card em{margin-top:.5rem;color:#ee8a00;font-style:normal}.bee{font-size:2.25rem}"
            ".workspace{min-width:0;padding:0 1.1rem 2.7rem}.topbar{position:sticky;top:0;z-index:10;display:grid;grid-template-columns:1fr minmax(260px,315px) auto;gap:1.5rem;align-items:start;padding:2rem 1.1rem 1.55rem;background:rgba(255,253,248,.92);border-bottom:1px solid var(--line);backdrop-filter:blur(14px)}.page-heading{padding-left:.25rem}.eyebrow{margin:0 0 .2rem;color:var(--accent-strong);font-size:.72rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase}.page-heading h1{margin:0;font-size:2rem;line-height:1.05;letter-spacing:-.06em}.page-heading p{margin:.48rem 0 0;color:#68708d;font-size:1rem}.search{height:46px;border:1px solid #dddfe7;border-radius:.48rem;background:#fff;display:flex;align-items:center;gap:.65rem;padding:0 .9rem;color:#717890}.search input{border:0;min-height:0;width:100%;padding:0;background:transparent;color:#717890;font:inherit}.search input:disabled{opacity:1}.user-tools{display:flex;align-items:center;gap:1rem;white-space:nowrap}.ghost-icon{position:relative;border:0;background:transparent;box-shadow:none;color:#111423;font-size:1.55rem;padding:0;min-height:auto}.notification-dot{position:absolute;right:-.45rem;top:-.55rem;display:grid;place-items:center;min-width:1.45rem;height:1.45rem;border-radius:50%;background:var(--honey);font-size:.75rem;font-weight:800}.avatar{display:grid;place-items:center;width:3rem;height:3rem;border-radius:50%;background:#fff2c8;font-weight:700}.account{display:grid}.account small{color:#68708d;margin-top:.2rem}"
            ".metric-grid{display:grid;gap:1.35rem;margin:1.55rem .55rem}.metric-grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}.metric-grid.four{grid-template-columns:repeat(4,minmax(0,1fr))}.metric-card{min-height:120px;border:1px solid var(--line);border-radius:.72rem;background:#fff;box-shadow:var(--shadow);display:grid;grid-template-columns:auto 1fr;grid-template-rows:auto auto auto;column-gap:1.25rem;align-content:center;padding:1.4rem 1.65rem}.metric-icon{grid-row:1/4;display:grid;place-items:center;width:4rem;height:4rem;border-radius:50%;background:linear-gradient(135deg,#fff7de,#ffe6a6);font-size:2rem;color:#101525}.metric-card.tone-green .metric-icon{background:var(--green-soft);color:var(--green)}.metric-card.tone-alert .metric-icon{background:#fff1cd;color:#ff8900}.metric-card.tone-peach .metric-icon{background:var(--orange-soft)}.metric-label{color:#25283a;font-size:1rem;font-weight:500}.metric-value{font-size:2.45rem;line-height:1;font-weight:800;letter-spacing:-.05em}.tone-alert .metric-value{color:#d80d14}.tone-green .metric-value{color:var(--green)}.metric-card small{color:#777e95;font-size:1rem}"
            ".dashboard-grid{display:grid;gap:1.55rem;margin:1.55rem .55rem}.two-col{grid-template-columns:1fr 1fr}.orders-layout{grid-template-columns:minmax(0,1fr) 265px}.products-layout{grid-template-columns:minmax(0,1.5fr) minmax(340px,.95fr)}.money-layout{grid-template-columns:minmax(0,1fr) 300px;align-items:start}.bottom-grid{grid-template-columns:1.15fr .85fr}.stack{display:grid;gap:1.05rem}.panel{border:1px solid var(--line);border-radius:.72rem;background:#fff;box-shadow:var(--shadow);padding:1.45rem}.panel.wide{margin:1.55rem .55rem}.panel-header,.toolbar{display:flex;align-items:center;justify-content:space-between;gap:1rem;margin-bottom:1rem}.panel h3{margin:0;font-size:1.35rem;letter-spacing:-.04em}.panel p{color:#68708d;margin:.45rem 0 1rem}.outline,.primary,.tab,.button-link{display:inline-flex;align-items:center;justify-content:center;gap:.45rem;min-height:2.55rem;border-radius:.38rem;border:1px solid #d9dce5;background:#fff;color:#111423;padding:.58rem 1rem;font:inherit;font-weight:700;box-shadow:none}.outline{border-color:#ffc21a;color:#e98200}.outline.muted{border-color:#d9dce5;color:#111423}.primary{border-color:var(--honey);background:var(--honey);color:#111423}.small{min-height:2.2rem;padding:.45rem .8rem}.tab{color:#68708d}.tab.active{border-color:#ffc21a;background:#fff8dc;color:#111423}button{cursor:pointer}"
            "table{width:100%;border-collapse:separate;border-spacing:0;background:#fff}th,td{padding:1rem 1.05rem;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle}th{background:#fffdfa;color:#25283a;font-size:.82rem;font-weight:700}tr:last-child td{border-bottom:0}td:first-child,th:first-child{font-weight:700}.status-badge,.coming-soon{display:inline-flex;width:max-content;align-items:center;border-radius:.32rem;padding:.35rem .62rem;font-size:.88rem;font-weight:600;background:#fff1d6;color:#de7d00}.badge-green{background:var(--green-soft);color:var(--green)}.badge-blue{background:var(--blue-soft);color:var(--blue)}.badge-red{background:var(--red-soft);color:var(--red)}.badge-gold{background:#fff1d6;color:#dc7800}.pill{border-radius:.32rem;padding:.35rem .75rem;font-weight:600}.pill.high{background:#fff1d6;color:#dc7800}.pill.medium{background:#e8f2ff;color:#1266d6}.pill.low{background:#eeeef2;color:#222}.pill.danger{background:var(--red-soft);color:var(--red)}.text-link{display:inline-flex;margin-top:1rem;color:#ec8700}.centered{justify-content:center;width:100%}.thumb{display:inline-grid;place-items:center;width:3.2rem;height:3.2rem;margin-right:.75rem;border-radius:.35rem;background:linear-gradient(135deg,#f8f4ed,#eee7db);vertical-align:middle}.channel{display:inline-grid;place-items:center;width:1.35rem;height:1.35rem;border-radius:.18rem;background:#f26d00;color:#fff;font-weight:800}.ready{color:#27943a;font-weight:700}"
            ".task-list,.media-list,.queue-list,.profit-list,.channel-list,.pref-list{list-style:none;margin:0;padding:0}.task-list li,.media-list li,.queue-list li,.profit-list li,.channel-list li,.pref-list li{display:grid;align-items:center;gap:.75rem;border-bottom:1px solid var(--line);padding:.85rem 0}.task-list li{grid-template-columns:auto 1fr auto}.media-list li{grid-template-columns:auto 1fr auto auto auto}.media-list.compact li{grid-template-columns:auto 1fr auto auto}.media-list small{display:block;color:#68708d}.queue-list li{grid-template-columns:1fr auto}.queue-list span{grid-column:1;color:#68708d}.profit-list li{grid-template-columns:auto 1fr auto}.profit-list b{color:#168200;font-size:1.1rem}.details-list{display:grid;grid-template-columns:1fr 1fr;margin:1rem 0 0}.details-list dt,.details-list dd{margin:0;padding:1rem 0;border-bottom:1px solid var(--line)}.details-list dt{color:#25283a}.channel-list li{grid-template-columns:auto 1fr auto auto;border:1px solid var(--line);border-radius:.55rem;padding:1rem;margin:.75rem 0}.channel-logo{display:grid;place-items:center;width:3rem;height:3rem;border-radius:50%;background:#f26d00;color:#fff;font-size:1.8rem;font-weight:800}.channel-logo.fb{background:#1977f3}.channel-list small,.pref-list small{display:block;color:#68708d;margin-top:.25rem}.info{padding:1rem;border-radius:.45rem;background:#f6f7fa}.pref-list li{grid-template-columns:auto 1fr auto}.small-icon{width:2.4rem;height:2.4rem;font-size:1.1rem}.toggle{width:2.6rem;height:1.35rem;border-radius:999px;background:#d5d8df;position:relative}.toggle:after{content:'';position:absolute;top:.16rem;left:.16rem;width:1.03rem;height:1.03rem;border-radius:50%;background:#fff}.toggle.on{background:var(--honey)}.toggle.on:after{left:1.38rem}.form-actions{display:flex;justify-content:flex-end;gap:1rem;margin-top:1.2rem}.legend{display:flex;justify-content:flex-end;gap:2rem;color:#25283a}.legend span:before{content:'';display:inline-block;width:1.2rem;height:.25rem;border-radius:99px;margin-right:.5rem;vertical-align:middle}.legend .sales:before{background:#83b96f}.legend .costs:before{background:#ff992a}.bar-chart{height:265px;border-bottom:1px solid var(--line);background:repeating-linear-gradient(to top,transparent 0 54px,#e9e9e9 55px);display:grid;grid-template-columns:repeat(4,1fr);gap:2.2rem;align-items:end;padding:0 3rem}.bar-chart div{height:100%;display:flex;align-items:end;justify-content:center;gap:.8rem;position:relative}.bar-chart i,.bar-chart b{display:block;width:1.75rem;border-radius:.18rem .18rem 0 0}.bar-chart i{background:linear-gradient(180deg,#91c47d,#cde8bf)}.bar-chart b{background:linear-gradient(180deg,#ff9d37,#ffc079)}.bar-chart span{position:absolute;bottom:-3.1rem;text-align:center;color:#68708d}.bar-chart small{display:block}.money-actions{display:flex;gap:1rem;align-items:start;justify-content:end;flex-wrap:wrap;padding:1rem}.money-actions p{width:100%;text-align:right;color:#68708d}.chart-panel{min-height:330px}.workflow-panel>section,#create-order .workflow-card,.workflow-card{margin:1rem 0;padding:1.25rem;border:1px solid var(--line);border-radius:.72rem;background:#fffdfa}.workflow-intro{margin-bottom:1rem;padding:.25rem 0}.workflow-intro h3,.workflow-card h2,.workflow-card h3,.workflow-card h4{margin-top:0}.workflow-card p{color:#68708d}.form-grid{display:grid;grid-template-columns:repeat(4,minmax(10rem,1fr));gap:1rem;align-items:end;margin:1rem 0}.compact-form{grid-template-columns:repeat(auto-fit,minmax(13rem,1fr))}.form-grid label,.inline-form label{display:grid;gap:.35rem;color:#25283a;font-weight:700}.form-grid input,.form-grid select,.form-grid textarea,.inline-form input,.inline-form select{width:100%;box-sizing:border-box;min-height:2.45rem;border:1px solid #d9dce5;border-radius:.42rem;background:#fff;padding:.45rem .6rem;font:inherit;color:#111423}.form-grid textarea{min-height:5.6rem;resize:vertical}.form-grid .full-span{grid-column:1/-1}.search input{border:0;min-height:0;padding:0}.inline-form{display:flex;flex-wrap:wrap;gap:.75rem;align-items:end;margin:.85rem 0}.record-tools{padding:1rem;border:1px dashed var(--line);border-radius:.6rem;background:#fff}.segmented-list{display:flex;flex-wrap:wrap;gap:.55rem;list-style:none;margin:.85rem 0 0;padding:0}.segmented-label a{display:inline-flex;margin:.2rem .25rem;padding:.35rem .7rem;border:1px solid #ffc21a;border-radius:.35rem}.empty-state{padding:1rem;border-radius:.6rem;background:#f8f9fc;color:#68708d}.notice{margin:1rem .55rem;padding:1rem 1.2rem;border-radius:.65rem;border:1px solid var(--line);background:#fff}.notice.success{border-color:#b9dcae;background:#f0faeb;color:var(--green);font-weight:700}.chart-empty{display:inline-block;margin:.8rem 0 1rem}.recipe-card{margin:1rem 0;padding:1rem;border:1px solid var(--line);border-radius:.6rem;background:#fff}.recipe-card ul{margin:.8rem 0;padding-left:1.2rem}.workflow-card table,.panel table{border:1px solid var(--line);border-radius:.6rem;overflow:hidden}.workflow-card td:first-child,.panel td:first-child{white-space:nowrap}.workflow-card td:last-child,.panel td:last-child{white-space:nowrap}.table-scroll{width:100%;overflow-x:auto}.table-scroll table{min-width:100%}.panel .workshop-products-table td:first-child,.panel .workshop-products-table td:last-child{white-space:normal}.workshop-products-table th,.workshop-products-table td{vertical-align:top}.workshop-products-table td:first-child{min-width:14rem}.workshop-products-table td:last-child{min-width:10rem}.workshop-products-table small{display:block;margin-top:.25rem;white-space:normal}.workflow-card form[style*='display:inline'],.panel form[style*='display:inline']{display:inline-flex!important;margin:.15rem .2rem .15rem 0}.workflow-card button,.panel button{border-color:#d9dce5}.workflow-card button:hover,.panel button:hover{border-color:#ffc21a}.workflow-actions{display:flex;flex-wrap:wrap;align-items:center;gap:.8rem}.workflow-actions h3,.workflow-actions p{width:100%;margin-bottom:0}.modal-popover{display:none;position:fixed;inset:0;z-index:50;padding:clamp(1rem,4vw,3rem);place-items:center}.modal-popover.modal-open{display:grid;z-index:50}.modal-popover:target{display:grid;z-index:70}.modal-backdrop{position:absolute;inset:0;background:rgba(17,20,35,.58);backdrop-filter:blur(2px)}.modal-card{position:relative;z-index:1;width:min(58rem,100%);max-height:min(84vh,52rem);overflow:auto;padding:1.35rem;border:1px solid #ffd262;border-radius:.9rem;background:#fff;box-shadow:0 1.2rem 3.2rem rgba(17,20,35,.24)}.modal-header{display:flex;justify-content:space-between;gap:1rem;align-items:start;margin-bottom:1rem}.modal-header h3{margin:.1rem 0}.modal-header p{margin:.35rem 0 0;color:#68708d}.modal-close{display:grid;place-items:center;flex:0 0 2.35rem;width:2.35rem;height:2.35rem;border:1px solid var(--line);border-radius:50%;background:#fff8df;color:#111423;font-size:1.7rem;line-height:1}.modal-card .form-grid{grid-template-columns:repeat(auto-fit,minmax(13rem,1fr));gap:1.1rem 1.25rem;margin-bottom:0}.modal-card .dialog-actions{grid-column:1/-1;display:flex;flex-wrap:wrap;justify-content:flex-end;gap:1rem;margin-top:.35rem;padding-top:.35rem}.modal-card .dialog-actions .primary,.modal-card .dialog-actions .outline{min-width:13rem}.modal-card .dialog-actions button{border-radius:.38rem;border:1px solid var(--honey);padding:.58rem 1rem;font:inherit;font-weight:700;box-shadow:none}.status-badge{white-space:nowrap}.inventory-item-link{color:#111423;font-weight:800;text-decoration:none}.inventory-item-link:hover,.inventory-item-link:focus{color:#e98200;text-decoration:underline}.stock-control-summary{margin-bottom:1rem}.stock-control-summary p{background:#fffdfa}.recipe-setup-form{gap:.85rem}.recipe-product-summary,.recipe-builder{padding:.85rem 1rem;border:1px solid var(--line);border-radius:.72rem;background:#fffdfa}.recipe-product-summary h4,.recipe-product-summary p,.recipe-section-heading h4,.recipe-section-heading p{margin:.15rem 0}.recipe-section-heading{display:flex;align-items:center;justify-content:space-between;gap:1rem;margin-bottom:.75rem}.recipe-builder-rows{display:grid;gap:.65rem}.recipe-builder-row{display:grid;grid-template-columns:minmax(14rem,1.5fr) minmax(9rem,.75fr) minmax(4.5rem,.35fr) auto;gap:.65rem;align-items:end;padding:.75rem;border:1px solid #efe7d6;border-radius:.65rem;background:#fff}.recipe-builder-row label{margin:0}.recipe-builder-row .unit-pill{display:inline-flex;align-items:center;justify-content:center;min-height:2.45rem;padding:.45rem .75rem;border-radius:999px;background:var(--green-soft);color:var(--green);font-weight:800}.recipe-builder-row .remove-row{display:flex;align-items:center;gap:.35rem;min-height:2.45rem;color:#68708d;font-weight:700}.recipe-empty{margin:.5rem 0 .75rem;background:#fff8df;border:1px dashed #ffd262}.recipe-secondary-action,.recipe-yield-note{margin:.1rem 0}.recipe-secondary-notes textarea{min-height:4rem}.recipe-editor{display:none}"
            "@media (max-width:1100px){.app-shell{grid-template-columns:1fr}.sidebar{position:static;height:auto}.brand{margin-bottom:1rem}nav ul{display:flex;flex-wrap:wrap}.bee-card{display:none}.topbar{grid-template-columns:1fr}.metric-grid.three,.metric-grid.four,.two-col,.orders-layout,.products-layout,.money-layout,.bottom-grid{grid-template-columns:1fr}.user-tools{justify-content:flex-start}.bar-chart{padding:0 1rem}}@media (max-width:720px){.workspace{padding:0 .5rem 1rem}.topbar{padding:1rem .5rem}.metric-grid,.dashboard-grid,.panel.wide{margin:1rem 0}.metric-card{grid-template-columns:1fr}.metric-icon{grid-row:auto}.panel{padding:1rem}table{display:block;overflow-x:auto;white-space:nowrap}.toolbar,.panel-header{align-items:flex-start;flex-direction:column}.details-list{grid-template-columns:1fr}.channel-list li,.pref-list li{grid-template-columns:1fr}.bar-chart{gap:.7rem}.brand strong{font-size:1.8rem}}"
            "</style>"
        )


    def _render_audit_sections(self, *, authorization_header: str) -> str:
        movements = self._material_service.list_inventory_movements(authorization_header=authorization_header)
        activities = self._material_service.list_activity_logs(authorization_header=authorization_header)
        movement_rows = ''.join(f'<li>{m.item_type}:{m.item_id} {m.before_quantity}->{m.after_quantity} ({m.reason})</li>' for m in movements)
        activity_rows = ''.join(f'<li>{a.entity_type}:{a.entity_id} {a.message}</li>' for a in activities)
        return f"<section><h3>Inventory movements</h3><ul>{movement_rows}</ul><h3>Activity log</h3><ul>{activity_rows}</ul></section>"
    def _format_currency(self, amount: float | int) -> str:
        return f"${float(amount):,.2f}"


def create_app() -> AppShell:
    """Create the app shell with milestone auth enforcement."""
    return AppShell()


def healthcheck() -> dict[str, str]:
    """Return a deterministic health payload for smoke tests."""
    return {"status": "ok", "service": "pollen"}


def can_access_shop_record(authorization_header: str | None, shop_id: str) -> bool:
    """Server-side ownership check helper for shop-scoped records."""
    return AuthService().can_access_shop(authorization_header, shop_id)
