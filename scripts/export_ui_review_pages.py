"""Export styled app-shell pages for screenshot-driven UI review.

The Codex cloud environment may not have a browser screenshot dependency
available, so this helper uses only the standard library and the app shell. Open
the generated HTML files in a browser or screenshot tool to capture visual
baselines.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from pollen.app import AppShell, create_app

AUTH_HEADER = "Bearer user:ui-review:ui-review@example.com"
PAGES: tuple[tuple[str, str], ...] = (
    ("today", "/"),
    ("orders", "/orders"),
    ("products-stock", "/products-stock"),
    ("make-buy", "/make-buy"),
    ("money", "/money"),
    ("settings", "/settings"),
)


def seed_demo_data(app: AppShell) -> None:
    """Add enough data for visual review pages to show real workflow content."""
    app.post(
        "/products-stock",
        authorization_header=AUTH_HEADER,
        form_data={
            "action": "create",
            "name": "Lavender Candle",
            "sku": "LC-REVIEW",
            "stock_on_hand": "4",
            "reorder_point": "2",
            "sale_price": "24.00",
            "estimated_material_cost": "7.00",
            "estimated_packaging_shipping_cost": "2.50",
            "platform_fee_percent": "8.00",
        },
    )
    app.post(
        "/make-buy",
        authorization_header=AUTH_HEADER,
        form_data={
            "action": "create",
            "name": "Soy Wax",
            "unit": "g",
            "stock_on_hand": "8",
            "reorder_point": "12",
        },
    )
    product = app._product_service.list_products(authorization_header=AUTH_HEADER)[0]  # noqa: SLF001
    material = app._material_service.list_materials(authorization_header=AUTH_HEADER)[0]  # noqa: SLF001
    app.post(
        "/products-stock",
        authorization_header=AUTH_HEADER,
        form_data={
            "action": "create_recipe_item",
            "product_id": product.product_id,
            "material_id": material.material_id,
            "quantity_per_unit": "4",
        },
    )
    app.post(
        "/orders",
        authorization_header=AUTH_HEADER,
        form_data={"customer_name": "Review Buyer", "product_sku": product.sku, "quantity": "1"},
    )


def export_pages(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    app = create_app()
    seed_demo_data(app)
    written: list[Path] = []

    for slug, route in PAGES:
        response = app.get(route, authorization_header=AUTH_HEADER)
        path = output_dir / f"{slug}.html"
        path.write_text(response.body, encoding="utf-8")
        written.append(path)

    return written


def format_paths(paths: Iterable[Path]) -> str:
    return "\n".join(f"- {path}" for path in paths)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Pollen app-shell pages for screenshot review.")
    parser.add_argument("--output-dir", default="docs/ai/ui-review-pages", help="Directory for generated HTML pages.")
    args = parser.parse_args()

    written = export_pages(Path(args.output_dir))
    print("Exported UI review pages:")
    print(format_paths(written))


if __name__ == "__main__":
    main()
