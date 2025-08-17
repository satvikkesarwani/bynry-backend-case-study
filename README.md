Part 1: Create Product API (create_product)
Changes Made

Input Validation Added

Required fields (name, sku) checked.

price validated as decimal and cannot be negative.

initial_quantity validated as a non-negative integer.

SKU Uniqueness Check

Prevents creation of duplicate products with the same SKU.

Transaction Safety

Used db.session.flush() to get product.id before creating inventory.

Wrapped DB operations in try/except with rollback on failure.

Product ↔ Inventory Linking

Product created globally (unique SKU).

Inventory created per warehouse.

If inventory exists, stock is incremented instead of creating duplicates.

Meaningful API Responses

Returns success message + product ID, SKU, warehouse ID, and quantity.

Returns clear error messages (400 for validation, 409 for duplicates, 500 for server issues).

💡 Logic

Separation of product definition and inventory ensures clean data modeling.

Validation ensures system integrity (no negative prices/stock, no duplicates).

Rollbacks protect database consistency.








Part 2: Database Schema (database.py)
Changes Made

Normalization

Created three tables:

products (global info)

warehouses (locations)

inventories (stock levels)

Relationships

Product ↔ Inventory = one-to-many.

Warehouse ↔ Inventory = one-to-many.

Together, this models a many-to-many relationship between products and warehouses.

Constraints

sku marked unique at database level.

quantity defaults to 0.

💡 Logic

Keeps data normalized and scalable (a product can be in many warehouses).

Enforces business rules at schema level (unique SKUs, valid foreign keys).

Prevents accidental duplicate product-warehouse mappings.







Part 3: Low Stock Endpoint (get_low_stock)
 Changes Made

Configurable Threshold

Query param ?threshold=VALUE (default = 10).

Optional Warehouse Filter

Query param ?warehouse_id=ID to restrict results to one warehouse.

Structured Response

Returns list of items:

{
  "product_id": 1,
  "sku": "ABC123",
  "name": "Laptop",
  "warehouse_id": 2,
  "quantity": 5
}


Includes count of total low-stock items.

💡 Logic

Threshold flexibility supports different alerting policies.

Warehouse filter helps managers focus on their branch.

JSON format is frontend-friendly for dashboards.









Assumptions Made

SKU is unique across the system.

Product can exist in multiple warehouses, but inventory is warehouse-specific.

Negative stock is not allowed (no backorders).

Price may be optional during product creation.

Warehouse IDs provided are assumed valid (basic validation not shown).

Authentication/authorization is not in scope for this case study.

