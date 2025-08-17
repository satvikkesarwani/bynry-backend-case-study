This repository contains my solution for the Bynry Backend Intern Case Study.
It includes bug fixes, database schema design, and API implementation.

Repository Structure
├── createproduct.py   # Fixed "Create Product" API  
├── database.py        # Database schema (SQLAlchemy ORM)  
├── lowstock.py        # Low-stock alerts API  
├── requirements.txt   # Dependencies (Flask + SQLAlchemy)  
└── README.md          # Documentation  



Part 1: Code Review & Debugging
Problem
The original create_product endpoint had several issues:
Product was tied directly to one warehouse → violates multi-warehouse support requirement
No SKU uniqueness check
Price was not validated as a decimal → risk of negative/invalid inputs
Lacked proper transaction handling → risk of inconsistent data
Required fields not validated → could crash server
Committed to DB twice → inefficient and unsafe


Fixes Made
Input Validation → used data.get() and required field checks
SKU Uniqueness → enforced before insert
Price Handling → stored as Decimal, rejects invalid/negative values
Default Quantity → defaults to 0 if not provided
Decoupled Product → created globally, not tied to a single warehouse
Separate Inventory → linked warehouse via Inventory
Atomic Transactions → one commit for both product + inventory
Error Handling → IntegrityError + generic Exception
Clear Responses → user-friendly JSON

File: createproduct.py






 Part 2: Database Schema Design

Requirements Addressed
Companies can have multiple warehouses
Products can exist in multiple warehouses with different stock quantities
Track inventory changes over time
Suppliers provide products
Products can be bundles (kits)

Schema Implemented
Company → Owns warehouses
Warehouse → Belongs to a company
Product → Global entity, unique SKU
Inventory → Maps products ↔ warehouses with stock quantity
InventoryHistory → Logs stock changes (audit trail)
Supplier → Supplier info
ProductSupplier → Many-to-Many (suppliers ↔ products)
Bundle → Parent product made of child products

Key Decisions & Assumptions
SKU uniqueness enforced at DB level
Inventory solves multi-warehouse problem
InventoryHistory ensures auditability
ProductSupplier supports multiple suppliers per product
Bundle supports product kits
Timestamps stored in UTC

File: database.py




Part 3: API Implementation – Low Stock Alerts
Endpoint : GET /api/companies/{company_id}/alerts/low-stock

Business Rules Covered
Threshold varies per product
Only alerts for recently sold products
Works across multiple warehouses
Includes supplier info for reordering
Estimates days until stockout from recent sales rate
Edge Cases Handled
No recent sales → no alert
Product with no suppliers → handled gracefully
Stock = 0 → days until stockout = 0


Response Format
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


