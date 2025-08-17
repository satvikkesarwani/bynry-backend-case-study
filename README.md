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

Product tied directly to one warehouse → violates requirement (multi-warehouse support)

No SKU uniqueness check

Price was not validated as decimal (risk of negative/invalid inputs)

No proper transaction handling → risk of inconsistent data

Required fields not validated → could crash if missing

Committed twice (inefficient and unsafe)

Fixes Made
✅ Input Validation: Added data.get(), required fields check.

✅ SKU Uniqueness: Enforced uniqueness before insert.

✅ Price Handling: Price stored as Decimal, rejects invalid/negative prices.

✅ Default Quantity: Initial quantity defaults to 0 if not provided.

✅ Decoupled Product: Product created globally, not tied to a single warehouse.

✅ Separate Inventory: Inventory record linked separately to the warehouse.

✅ Atomic Transactions: Used a single transaction for product + inventory creation.

✅ Error Handling: Added proper handling for IntegrityError and generic Exception.

✅ Clear Responses: Returns human-friendly JSON responses.

File: createproduct.py

🔹 Part 2: Database Schema Design
Requirements Addressed
Companies can have multiple warehouses.

Products can exist in multiple warehouses with different stock quantities.

Track inventory changes over time.

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

Inventory table solves the multi-warehouse problem.

InventoryHistory allows for a complete audit trail.

ProductSupplier table supports multiple suppliers per product.

Bundle table supports kits by reusing existing products.

Timestamps are stored in UTC.

File: database.py

🔹 Part 3: API Implementation – Low Stock Alerts
Endpoint
GET /api/companies/{company_id}/alerts/low-stock

Business Rules Covered
Low stock threshold can vary by product.

Alerts are only triggered for recently sold products.

Considers stock across multiple warehouses for a single company.

Includes supplier info for easy reordering.

Calculates an estimated number of days until stockout based on the recent sales rate.

Edge Cases Handled
No recent sales → no alert is generated.

Product exists but has no assigned suppliers → handled gracefully.

Stock is already zero → days until stockout is 0.

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
