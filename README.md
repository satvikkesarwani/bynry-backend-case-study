This repository contains my solution for the Bynry Backend Intern Case Study. It includes bug fixes, database schema design, and API implementation.

📂 Repository Structure
├── createproduct.py   # Fixed "Create Product" API
├── database.py        # Database schema (SQLAlchemy ORM)
├── lowstock.py        # Low-stock alerts API
├── requirements.txt   # Dependencies (Flask + SQLAlchemy)
└── README.md          # Documentation
🔹 Part 1: Code Review & Debugging
Problem
The original create_product endpoint had several issues:

Product was tied directly to one warehouse, which violates the multi-warehouse support requirement.

No SKU uniqueness check was performed.

Price was not validated as a decimal, risking negative or invalid inputs.

Lacked proper transaction handling, creating a risk of inconsistent data.

Required fields were not validated, which could crash the server if they were missing.

The code committed to the database twice, which is inefficient and unsafe.

Fixes Made
✅ Input Validation: Added data.get() and checks for required fields.

✅ SKU Uniqueness: Enforced uniqueness before inserting a new product.

✅ Price Handling: Price is stored as a Decimal and rejects invalid or negative prices.

✅ Default Quantity: The initial quantity now defaults to 0 if not provided.

✅ Decoupled Product: Products are now created globally and are not tied to a single warehouse.

✅ Separate Inventory: Inventory records are linked separately to the warehouse.

✅ Atomic Transactions: Used a single transaction for creating both the product and inventory records.

✅ Error Handling: Added proper handling for IntegrityError and generic Exception.

✅ Clear Responses: The API now returns human-friendly JSON responses.

File: createproduct.py

🔹 Part 2: Database Schema Design
Requirements Addressed
Companies can have multiple warehouses.

Products can exist in multiple warehouses with different stock quantities.

Inventory changes are tracked over time.

Suppliers provide products.

Products can be bundles (kits).

Schema Implemented
Company → Owns warehouses

Warehouse → Belongs to a company

Product → Global entity with a unique SKU

Inventory → Maps products to warehouses with a stock quantity

InventoryHistory → Logs all stock changes for auditing

Supplier → Contains supplier information

ProductSupplier → Many-to-Many relationship between suppliers and products

Bundle → Defines a parent product made of child products

Key Decisions & Assumptions
SKU uniqueness is enforced at the database level.

The Inventory table solves the multi-warehouse problem.

The InventoryHistory table allows for a complete audit trail.

The ProductSupplier table supports multiple suppliers per product.

The Bundle table supports kits by reusing existing products.

Timestamps are stored in UTC.

File: database.py

🔹 Part 3: API Implementation – Low Stock Alerts
Endpoint
GET /api/companies/{company_id}/alerts/low-stock

Business Rules Covered
The low stock threshold can vary by product.

Alerts are only triggered for recently sold products.

Considers stock across multiple warehouses for a single company.

Includes supplier info for easy reordering.

Calculates an estimated number of days until stockout based on the recent sales rate.

Edge Cases Handled
If there are no recent sales, no alert is generated.

If a product exists but has no assigned suppliers, it is handled gracefully.

If the stock is already zero, the days until stockout is 0.

Response Format
JSON

{
  "alerts": [
    {
      "product_id": 123,
      "product_name": "Widget A",
      "sku": "WID-001",
      "warehouse_id": 456,
      "warehouse_name": "Main Warehouse",
      "current_stock": 5,
      "threshold": 20,
      "days_until_stockout": 12,
      "supplier": {
        "id": 789,
        "name": "Supplier Corp",
        "contact_email": "orders@supplier.com"
      }
    }
  ],
  "total_alerts": 1
}
File: lowstock.py
