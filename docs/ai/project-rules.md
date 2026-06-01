# Project Rules

This file stores project-specific AI rules and constraints.

Current project-specific rule state:
- Pollen uses a Workshop vs Inventory split even while legacy URLs remain in place.
- Workshop (`/make-buy`) is where products are created/formalised, materials or parts are defined while building recipes/BOMs, quantities per unit are maintained, batches are planned, material needs for batches are reviewed, and batches are started/completed.
- Inventory (`/products-stock`) is where current finished-product and material stock is viewed/controlled, low-stock warnings are reviewed, buy-list/reorder suggestions are staged, incoming purchases are tracked, and received materials are recorded.
- Buying/restock UI must not be reintroduced to Workshop; product/recipe creation UI must not be reintroduced to Inventory unless a future scoped IA task explicitly changes this split.
- Workshop recipe UI should use the clear actions `+ Add material to recipe` for adding a requirement row and `+ Create new material` for creating a missing material without navigating away from product definition.
- Inventory stock controls should post from Inventory whenever practical, including material stock adjustments, so normal users do not have to visit Workshop to correct counts.

When project-specific constraints are introduced, record them here (not in generic AI kit files).
