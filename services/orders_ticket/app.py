from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

orders = {
    1: {
        "OTID": 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "quantity": 2,
        "subtotal": 200.0,
        "total": 220.0,
        "discount": 10.0,
        "tax": 20.0,
        "tax_rate": 0.1,
        "cash": 50.0,
        "credit": 170.0,
        "status": 1,
        "employee_id": 2000,
        "vendor_id": 1
    },
    2: {
        "OTID": 2,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "quantity": 1,
        "subtotal": 100.0,
        "total": 110.0,
        "discount": 5.0,
        "tax": 10.0,
        "tax_rate": 0.1,
        "cash": 110.0,
        "credit": 0.0,
        "status": 2,
        "employee_id": 2001,
        "vendor_id": 2
    },
}

next_OTID = 3

# CREATE
@app.route('/orders', methods=['POST'])
def create_order():
    global next_OTID
    data = request.get_json()
    data["OTID"] = next_OTID
    orders[next_OTID] = data
    next_OTID += 1
    return jsonify({"message": "Order created successfully", "order": data}), 201

# READ
@app.route('/orders/<int:OTID>', methods=['GET'])
def get_order(OTID):
    order = orders.get(OTID)
    if order:
        return jsonify(order), 200
    return jsonify({"error": "Order not found"}), 404

# UPDATE
@app.route('/orders/<int:OTID>', methods=['PUT'])
def update_order(OTID):
    order = orders.get(OTID)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    data = request.get_json()
    order.update(data)
    return jsonify({"message": "Order updated successfully", "order": order}), 200

# DELETE
@app.route('/orders/<int:OTID>', methods=['DELETE'])
def delete_order(OTID):
    if OTID in orders:
        del orders[OTID]
        return jsonify({"message": "Order deleted successfully"}), 200
    return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8083))
    app.run(host='0.0.0.0', port=port)