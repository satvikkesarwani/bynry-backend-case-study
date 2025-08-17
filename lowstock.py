"""
Part 3: Low Stock Alerts API
-----------------------------
Endpoint: GET /api/companies/<company_id>/alerts/low-stock

Business Rules:
- Low stock threshold varies by product type -> Simplified assumption: threshold stored in Product or set default=10
- Only alert for products with recent sales -> Assume "recent" means sales in last 30 days
- Must handle multiple warehouses
- Include supplier info for reordering

Edge Cases:
- No recent sales → skip product
- No suppliers linked → supplier=null
- Negative/zero stock → immediate alert
"""

from flask import Flask, jsonify
from datetime import datetime, timedelta
from models import db, Product, Inventory, Warehouse, Supplier, ProductSupplier

app = Flask(__name__)

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    alerts = []
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    # Query all inventories for this company
    inventories = (
        db.session.query(Inventory, Product, Warehouse)
        .join(Product, Product.id == Inventory.product_id)
        .join(Warehouse, Warehouse.id == Inventory.warehouse_id)
        .filter(Warehouse.company_id == company_id)
        .all()
    )

    for inv, product, warehouse in inventories:
        threshold = getattr(product, "low_stock_threshold", 10)  # fallback default
        current_stock = inv.quantity

        # Check recent sales activity (stubbed for demo: assume all had sales)
        recent_sales = True  
        if not recent_sales:
            continue

        if current_stock < threshold:
            days_until_stockout = max(1, current_stock // 1)  # fake formula

            # Fetch supplier info
            supplier_rel = ProductSupplier.query.filter_by(product_id=product.id).first()
            supplier = None
            if supplier_rel:
                supplier = Supplier.query.get(supplier_rel.supplier_id)

            alerts.append({
                "product_id": product.id,
                "product_name": product.name,
                "sku": product.sku,
                "warehouse_id": warehouse.id,
                "warehouse_name": warehouse.name,
                "current_stock": current_stock,
                "threshold": threshold,
                "days_until_stockout": days_until_stockout,
                "supplier": {
                    "id": supplier.id if supplier else None,
                    "name": supplier.name if supplier else None,
                    "contact_email": supplier.contact_email if supplier else None
                } if supplier else None
            })

    return jsonify({"alerts": alerts, "total_alerts": len(alerts)})
