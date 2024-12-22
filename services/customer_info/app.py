from flask import Flask, request, jsonify

app = Flask(__name__)

customers = {
    1: {
        "customer_id": 1,
        "email": "nicola.bolt@students.bfh.ch",
        "password": "Hallo12345",
        "first_name": "Nicola",
        "last_name": "Bolt",
        "phone_number": "0797483828",
        "rewards": 10.5,
        "street_address": "Musterstrasse 1",
        "city": "Bern",
        "state": "Bern",
        "zip_code": 3000
    },
    2: {
        "customer_id": 2,
        "email": "marius.haegele@students.bfh.ch",
        "password": "Test12345",
        "first_name": "Marius",
        "last_name": "Hägele",
        "phone_number": "0798238392",
        "rewards": 5.0,
        "street_address": "Beispielstrasse 2",
        "city": "Thun",
        "state": "Bern",
        "zip_code": 3604
    }
}

next_customer_id = 3


# Such-Endpunkt, um Kunden basierend auf Vor- und Nachnamen zu finden
@app.route('/customers/search', methods=['GET'])
def search_customer():
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    
    for customer in customers.values():
        if customer["first_name"] == first_name and customer["last_name"] == last_name:
            return jsonify(customer), 200
    
    return jsonify({"error": "Customer not found"}), 404


# Standard-CRUD-Routen

# CREATE
@app.route('/customers', methods=['POST'])
def create_customer():
    global next_customer_id
    data = request.get_json()
    new_customer = {
        "customer_id": next_customer_id,
        "email": data.get("email"),
        "password": data.get("password"),
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "phone_number": data.get("phone_number"),
        "rewards": data.get("rewards", 0.0),
        "street_address": data.get("street_address"),
        "city": data.get("city"),
        "state": data.get("state"),
        "zip_code": data.get("zip_code")
    }
    customers[next_customer_id] = new_customer
    next_customer_id += 1
    return jsonify({"message": "Customer created successfully", "customer": new_customer}), 201

# READ
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = customers.get(customer_id)
    if customer:
        return jsonify(customer), 200
    return jsonify({"error": "Customer not found"}), 404

# UPDATE
@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = customers.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    data = request.get_json()
    customer.update({
        "email": data.get("email", customer["email"]),
        "password": data.get("password", customer["password"]),
        "first_name": data.get("first_name", customer["first_name"]),
        "last_name": data.get("last_name", customer["last_name"]),
        "phone_number": data.get("phone_number", customer["phone_number"]),
        "rewards": data.get("rewards", customer["rewards"]),
        "street_address": data.get("street_address", customer["street_address"]),
        "city": data.get("city", customer["city"]),
        "state": data.get("state", customer["state"]),
        "zip_code": data.get("zip_code", customer["zip_code"])
    })
    return jsonify({"message": "Customer updated successfully", "customer": customer}), 200

# DELETE
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    if customer_id in customers:
        del customers[customer_id]
        return jsonify({"message": "Customer deleted successfully"}), 200
    return jsonify({"error": "Customer not found"}), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8081))
    app.run(host='0.0.0.0', port=port)