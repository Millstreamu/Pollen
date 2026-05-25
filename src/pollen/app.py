"""App shell and core helpers for the Pollen milestone slices."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import parse_qs, urlsplit

from pollen.auth import AuthService
from pollen.services import MaterialService, ProductService

NAV_ITEMS: tuple[tuple[str, str], ...] = (
    ("Today", "/"),
    ("Orders", "/orders"),
    ("Products & Stock", "/products-stock"),
    ("Make / Buy", "/make-buy"),
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
        "Products & Stock": "Product and stock tools will appear here.",
        "Make / Buy": "Make and buy planning will appear here.",
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
        self._product_service = product_service or ProductService(auth_service=self._auth_service)
        self._material_service = material_service or MaterialService(auth_service=self._auth_service)

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
        if path not in {"/products-stock", "/make-buy"}:
            return AppResponse(status_code=404, body="Not Found")
        if self._auth_service.resolve_context(authorization_header) is None:
            return AppResponse(status_code=401, body="Unauthorized")

        if path == "/make-buy":
            return self._handle_material_post(authorization_header=authorization_header, form_data=form_data)

        payload = form_data or {}
        action = payload.get("action")
        if action == "create":
            self._product_service.create_product(
                authorization_header=authorization_header,
                name=payload.get("name", ""),
                sku=payload.get("sku", ""),
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
        elif action == "bulk_restore":
            selected_ids = payload.get("product_ids", "")
            for product_id in [pid.strip() for pid in selected_ids.split(",") if pid.strip()]:
                self._product_service.restore_product(
                    authorization_header=authorization_header,
                    product_id=product_id,
                )

        return self.get(path, authorization_header=authorization_header)

    def _handle_material_post(
        self,
        *,
        authorization_header: str,
        form_data: dict[str, str] | None,
    ) -> AppResponse:
        payload = form_data or {}
        action = payload.get("action")
        if action == "create":
            self._material_service.create_material(
                authorization_header=authorization_header,
                name=payload.get("name", ""),
                unit=payload.get("unit", ""),
                stock_on_hand=int(payload.get("stock_on_hand", "0")),
                reorder_point=int(payload.get("reorder_point", "0")),
            )
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

        return self.get("/make-buy", authorization_header=authorization_header)


    def _render_products_page(
        self,
        *,
        authorization_header: str,
        view: str = "active",
        edit_product_id: str | None = None,
    ) -> str:
        products = self._product_service.list_products(authorization_header=authorization_header)
        archived_products = self._product_service.list_products(
            authorization_header=authorization_header,
            include_archived=True,
        )
        archived_only = [product for product in archived_products if not product.is_active]
        create_form = (
            "<section><h3>Create product</h3>"
            "<form method='post' action='/products-stock'>"
            "<input type='hidden' name='action' value='create'>"
            "<label>Name <input name='name' required></label>"
            "<label>SKU <input name='sku' required></label>"
            "<label>Stock <input name='stock_on_hand' type='number' min='0' required></label>"
            "<label>Reorder <input name='reorder_point' type='number' min='0' required></label>"
            "<button type='submit'>Create</button>"
            "</form></section>"
        )
        if not products and not archived_only:
            return (
                "<section><h2>Products</h2>"
                "<p>No products yet. Add your first product to start tracking stock.</p>"
                f"{create_form}</section>"
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
        filter_nav = (
            "<nav aria-label='Product view filters'>"
            "<ul>"
            "<li><a href='/products-stock?view=active'>Active</a></li>"
            "<li><a href='/products-stock?view=archived'>Archived</a></li>"
            "<li><a href='/products-stock?view=all'>All</a></li>"
            "</ul></nav>"
        )

        archived_section = (
            "<section><h3>Archived products</h3>"
            "<table><thead><tr><th>Select</th><th>ID</th><th>Name</th><th>SKU</th><th>Action</th></tr></thead><tbody>"
            f"{archived_rows}"
            "</tbody></table></section>"
            if archived_only
            else ""
        )

        show_active = view in {"active", "all"}
        show_archived = view in {"archived", "all"}

        bulk_actions = (
            "<section><h3>Bulk actions</h3>"
            "<p>Archive or restore multiple products by entering comma-separated product IDs.</p>"
            "<form method='post' action='/products-stock'>"
            "<label>Product IDs <input name='product_ids' placeholder='prd-1, prd-2'></label>"
            "<button type='submit' name='action' value='bulk_archive'>Archive selected</button>"
            "<button type='submit' name='action' value='bulk_restore'>Restore selected</button>"
            "</form></section>"
        )

        active_section = (
            "<section><h2>Products</h2>"
            "<p>Manage products with create, per-row edit, archive, restore, and bulk actions.</p>"
            f"{create_form}"
            f"{bulk_actions}"
            "<table><thead><tr>"
            "<th>Select</th><th>ID</th><th>Name</th><th>SKU</th><th>Stock</th><th>Reorder</th><th>Status</th><th>Actions</th>"
            "</tr></thead><tbody>"
            f"{rows}"
            "</tbody></table></section>"
            if show_active
            else ""
        )

        return (
            f"{filter_nav}"
            f"{active_section}"
            f"{archived_section if show_archived else ""}"
        )


    def _render_product_row(self, *, product, edit_product_id: str | None) -> str:
        if edit_product_id == product.product_id:
            return (
                "<tr>"
                f"<td><input type='checkbox' disabled aria-label='Select {product.product_id}'></td>"
                f"<td>{product.product_id}</td>"
                "<td colspan='4'>"
                "<form method='post' action='/products-stock'>"
                "<input type='hidden' name='action' value='edit'>"
                f"<input type='hidden' name='product_id' value='{product.product_id}'>"
                f"<label>Name <input name='name' value='{product.name}' required></label>"
                f"<label>SKU <input name='sku' value='{product.sku}' required></label>"
                f"<label>Stock <input name='stock_on_hand' type='number' min='0' value='{product.stock_on_hand}' required></label>"
                f"<label>Reorder <input name='reorder_point' type='number' min='0' value='{product.reorder_point}' required></label>"
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


    def _render_materials_page(self, *, authorization_header: str, edit_material_id: str | None = None) -> str:
        materials = self._material_service.list_materials(authorization_header=authorization_header)
        create_form = (
            "<section><h3>Create material</h3>"
            "<form method='post' action='/make-buy'>"
            "<input type='hidden' name='action' value='create'>"
            "<label>Name <input name='name' required></label>"
            "<label>Unit <input name='unit' required></label>"
            "<label>Stock <input name='stock_on_hand' type='number' min='0' required></label>"
            "<label>Reorder <input name='reorder_point' type='number' min='0' required></label>"
            "<button type='submit'>Create</button>"
            "</form></section>"
        )
        if not materials:
            return (
                "<section><h2>Materials</h2>"
                "<p>No materials yet. Add your first material to track supplies.</p>"
                f"{create_form}</section>"
            )

        rows = "".join(self._render_material_row(material=material, edit_material_id=edit_material_id) for material in materials)
        return (
            "<section><h2>Materials</h2>"
            "<p>Manage materials with simple create and per-row edit controls.</p>"
            f"{create_form}"
            "<table><thead><tr><th>ID</th><th>Name</th><th>Unit</th><th>Stock</th><th>Reorder</th><th>Status</th><th>Actions</th></tr></thead><tbody>"
            f"{rows}"
            "</tbody></table></section>"
        )

    def _render_material_row(self, *, material, edit_material_id: str | None) -> str:
        if edit_material_id == material.material_id:
            return (
                "<tr>"
                f"<td>{material.material_id}</td>"
                "<td colspan='4'>"
                "<form method='post' action='/make-buy'>"
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
            f"<td><a href='/make-buy?edit={material.material_id}'>Edit</a></td>"
            "</tr>"
        )

    def render_page(
        self,
        page_title: str,
        *,
        authorization_header: str | None = None,
        query: dict[str, list[str]] | None = None,
    ) -> str:
        nav_links = "".join(
            f'<li><a href="{href}">{label}</a></li>' for label, href in NAV_ITEMS
        )
        page_description = self._DESCRIPTIONS[page_title]
        page_content = f"<p>{page_description}</p>"
        if page_title == "Products & Stock" and authorization_header is not None:
            view = "active"
            if query is not None:
                requested_view = query.get("view", ["active"])[0]
                if requested_view in {"active", "archived", "all"}:
                    view = requested_view
            edit_product_id = query.get("edit", [None])[0] if query is not None else None
            page_content = self._render_products_page(
                authorization_header=authorization_header,
                view=view,
                edit_product_id=edit_product_id,
            )
        if page_title == "Make / Buy" and authorization_header is not None:
            edit_material_id = query.get("edit", [None])[0] if query is not None else None
            page_content = self._render_materials_page(
                authorization_header=authorization_header,
                edit_material_id=edit_material_id,
            )

        return (
            "<!doctype html>"
            "<html lang='en'>"
            "<head>"
            "<meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>{page_title} · Pollen</title>"
            "</head>"
            "<body>"
            "<header>"
            "<div><strong>Pollen</strong><p>Simple shop operating system</p></div>"
            "<nav aria-label='Primary'><ul>"
            f"{nav_links}"
            "</ul></nav>"
            "</header>"
            f"<main><h1>{page_title}</h1>{page_content}</main>"
            "</body>"
            "</html>"
        )


def create_app() -> AppShell:
    """Create the app shell with milestone auth enforcement."""
    return AppShell()


def healthcheck() -> dict[str, str]:
    """Return a deterministic health payload for smoke tests."""
    return {"status": "ok", "service": "pollen"}


def can_access_shop_record(authorization_header: str | None, shop_id: str) -> bool:
    """Server-side ownership check helper for shop-scoped records."""
    return AuthService().can_access_shop(authorization_header, shop_id)
