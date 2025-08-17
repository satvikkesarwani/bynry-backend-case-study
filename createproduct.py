from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from decimal import Decimal, InvalidOperation

@app.route('/api/products', methods=['POST'])
def create_product():
    """
    Create a new product in the system and link it to a warehouse inventory.
    Steps:
    1. Validate incoming request data
    2. Ensure SKU uniqueness
    3. Create product (global entity, not tied to a single warehouse)
    4. Create or update inventory for the chosen warehouse
    5. Commit everything safely in one transaction
    """

    # --- 1. Extract request data safely ---
    data = request.json or {}
    name = data.get('name')
    sku = data.get('sku')
    price = data.get('price')
    warehouse_id = data.get('warehouse_id')
    initial_quantity = data.get('initial_quantity', 0)  # default 0 if not given

    # --- 2. Validate inputs ---
    # Required fields
    if not sku or not name:
        return jsonify({"error": "Both 'name' and 'sku' are required fields"}), 400

    # Price validation (must be decimal, cannot be negative)
    try:
        price = Decimal(str(price)) if price is not None else None
        if price is not None and price < 0:
            return jsonify({"error": "Price cannot be negative"}), 400
    except (InvalidOperation, TypeError):
        return jsonify({"error": "Invalid price format"}), 400

    # Quantity validation (must be integer >= 0)
    if not isinstance(initial_quantity, int) or initial_quantity < 0:
        return jsonify({"error": "Initial quantity must be a non-negative integer"}), 400

    # --- 3. SKU uniqueness check ---
    existing_product = Product.query.filter_by(sku=sku).first()
    if existing_product:
        return jsonify({"error": f"Product with SKU '{sku}' already exists"}), 409

    try:
        # --- 4. Create product ---
        # Notice: no warehouse_id here, since product is global and can live in many warehouses
        product = Product(
            name=name,
            sku=sku,
            price=price
        )
        db.session.add(product)
        db.session.flush()  # ensures product.id is available without committing yet

        # --- 5. Create or update inventory record ---
        # Check if this product already has stock entry in this warehouse
        inventory = Inventory.query.filter_by(
            product_id=product.id,
            warehouse_id=warehouse_id
        ).first()

        if inventory:
            # If record exists, just increment stock
            inventory.quantity += initial_quantity
        else:
            # Otherwise, create a new inventory row
            inventory = Inventory(
                product_id=product.id,
                warehouse_id=warehouse_id,
                quantity=initial_quantity
            )
            db.session.add(inventory)

        # --- 6. Commit everything in one transaction ---
        db.session.commit()

    except IntegrityError as e:
        # Rollback to keep DB clean
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 500
    except Exception as e:
        # Any other unexpected error
        db.session.rollback()
        return jsonify({"error": "Unexpected server error", "details": str(e)}), 500

    # --- 7. Respond with success ---
    return jsonify({
        "message": "Product created successfully",
        "product_id": product.id,
        "sku": product.sku,
        "warehouse_id": warehouse_id,
        "initial_quantity": initial_quantity
    }), 201
