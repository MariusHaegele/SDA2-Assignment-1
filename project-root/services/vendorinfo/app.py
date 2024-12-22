from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

vendors = {
    1: {
        "vendor_id": 1,
        "company_name": "Lieferant GmbH",
        "department": "Vertrieb",
        "street_address": "Lieferstr. 1",
        "city": "Lieferstadt",
        "zip_code": 12345,
        "phone_number": 1234567890.0,
        "fax_number": 1234567891.0,
        "email": "kontakt@lieferant.de"
    },
    2: {
        "vendor_id": 2,
        "company_name": "Provider AG",
        "department": "Einkauf",
        "street_address": "Providerweg 2",
        "city": "Providstadt",
        "zip_code": 54321,
        "phone_number": 9876543210.0,
        "fax_number": 9876543211.0,
        "email": "info@provider.de"
    },
}

next_vendor_id = 3

# CREATE
@app.route('/vendors', methods=['POST'])
def create_vendor():
    global next_vendor_id
    data = request.get_json()
    data["vendor_id"] = next_vendor_id
    vendors[next_vendor_id] = data
    next_vendor_id += 1
    return jsonify({"message": "Vendor created successfully", "vendor": data}), 201

# READ
@app.route('/vendors/<int:vendor_id>', methods=['GET'])
def get_vendor(vendor_id):
    vendor = vendors.get(vendor_id)
    if vendor:
        return jsonify(vendor), 200
    return jsonify({"error": "Vendor not found"}), 404

# UPDATE
@app.route('/vendors/<int:vendor_id>', methods=['PUT'])
def update_vendor(vendor_id):
    vendor = vendors.get(vendor_id)
    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404
    data = request.get_json()
    vendor.update(data)
    return jsonify({"message": "Vendor updated successfully", "vendor": vendor}), 200

# DELETE
@app.route('/vendors/<int:vendor_id>', methods=['DELETE'])
def delete_vendor(vendor_id):
    if vendor_id in vendors:
        del vendors[vendor_id]
        return jsonify({"message": "Vendor deleted successfully"}), 200
    return jsonify({"error": "Vendor not found"}), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8084))
    app.run(host='0.0.0.0', port=port)