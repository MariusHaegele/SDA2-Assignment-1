from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

employees = {
    1: {
        "employee_id": 1,
        "email": "markus.müller@gmail.com",
        "password": "Markus12345",
        "pin_number": 1234,
        "first_name": "Markus",
        "last_name": "Müller",
        "user_id": 7485,
        "phone_number": "0797827381",
        "SSN": 836482947,
        "street_address": "Markusstrasse 1",
        "city": "Interlaken",
        "state": "Bern",
        "zip_code": 3800,
        "start_date": datetime.now().strftime("%Y-%m-%d"),
        "company_name": "Galaxus",
        "number_of_stores": "50",
        "user_type": 1,
        "customer_id": 2000
    },
    2: {
        "employee_id": 2,
        "email": "julia.meier@gmail.com",
        "password": "Julia12345",
        "pin_number": 7584,
        "first_name": "Julia",
        "last_name": "Meier",
        "user_id": 8493,
        "phone_number": "07973812937",
        "SSN": 123456789,
        "street_address": "Juliastrasse 38",
        "city": "Münsigen",
        "state": "Bern",
        "zip_code": 3000,
        "start_date": datetime.now().strftime("%Y-%m-%d"),
        "company_name": "Galaxus",
        "number_of_stores": "30",
        "user_type": 2,
        "customer_id": 2001
    }
}

next_employee_id = 3

# Such-Endpunkt, um Mitarbeiter basierend auf Vor- und Nachnamen zu finden
@app.route('/employees/search', methods=['GET'])
def search_employee():
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    
    for employee in employees.values():
        if employee["first_name"] == first_name and employee["last_name"] == last_name:
            return jsonify(employee), 200
    
    return jsonify({"error": "Employee not found"}), 404

# Standard-CRUD-Routen

# CREATE
@app.route('/employees', methods=['POST'])
def create_employee():
    global next_employee_id
    data = request.get_json()
    new_employee = {
        "employee_id": next_employee_id,
        "email": data.get("email"),
        "password": data.get("password"),
        "pin_number": data.get("pin_number"),
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "user_id": data.get("user_id"),
        "phone_number": data.get("phone_number"),
        "SSN": data.get("SSN"),
        "street_address": data.get("street_address"),
        "city": data.get("city"),
        "state": data.get("state"),
        "zip_code": data.get("zip_code"),
        "start_date": data.get("start_date", datetime.now().strftime("%Y-%m-%d")),
        "company_name": data.get("company_name"),
        "number_of_stores": data.get("number_of_stores"),
        "user_type": data.get("user_type"),
        "customer_id": data.get("customer_id")
    }
    employees[next_employee_id] = new_employee
    next_employee_id += 1
    return jsonify({"message": "Employee created successfully", "employee": new_employee}), 201

# READ
@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = employees.get(employee_id)
    if employee:
        return jsonify(employee), 200
    return jsonify({"error": "Employee not found"}), 404

# UPDATE
@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = employees.get(employee_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    data = request.get_json()
    employee.update({
        "email": data.get("email", employee["email"]),
        "password": data.get("password", employee["password"]),
        "pin_number": data.get("pin_number", employee["pin_number"]),
        "first_name": data.get("first_name", employee["first_name"]),
        "last_name": data.get("last_name", employee["last_name"]),
        "user_id": data.get("user_id", employee["user_id"]),
        "phone_number": data.get("phone_number", employee["phone_number"]),
        "SSN": data.get("SSN", employee["SSN"]),
        "street_address": data.get("street_address", employee["street_address"]),
        "city": data.get("city", employee["city"]),
        "state": data.get("state", employee["state"]),
        "zip_code": data.get("zip_code", employee["zip_code"]),
        "start_date": data.get("start_date", employee["start_date"]),
        "company_name": data.get("company_name", employee["company_name"]),
        "number_of_stores": data.get("number_of_stores", employee["number_of_stores"]),
        "user_type": data.get("user_type", employee["user_type"]),
        "customer_id": data.get("customer_id", employee["customer_id"])
    })
    return jsonify({"message": "Employee updated successfully", "employee": employee}), 200

# DELETE
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    if employee_id in employees:
        del employees[employee_id]
        return jsonify({"message": "Employee deleted successfully"}), 200
    return jsonify({"error": "Employee not found"}), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8082))
    app.run(host='0.0.0.0', port=port)