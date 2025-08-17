"""
Part 2: Database Schema Design
-------------------------------
Schema for StockFlow Inventory System
- Companies → Warehouses → Products (via Inventory)
- Suppliers supply products
- Inventory history tracks changes
- Products can be bundles

Assumptions:
- A product can exist in multiple warehouses.
- SKU is unique across the platform.
- Inventory changes must be logged for auditing.
- Bundles link parent product to child products.
"""

from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models import db

class Company(db.Model):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    warehouses = relationship("Warehouse", backref="company")

class Warehouse(db.Model):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

class Product(db.Model):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    inventories = relationship("Inventory", backref="product")

class Inventory(db.Model):
    __tablename__ = "inventories"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)

class InventoryHistory(db.Model):
    __tablename__ = "inventory_history"
    id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, ForeignKey("inventories.id"))
    change = Column(Integer, nullable=False)
    timestamp = Column(DateTime)

class Supplier(db.Model):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_email = Column(String, nullable=False)

class ProductSupplier(db.Model):
    __tablename__ = "product_suppliers"
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), primary_key=True)

class Bundle(db.Model):
    __tablename__ = "bundles"
    parent_product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    child_product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)
