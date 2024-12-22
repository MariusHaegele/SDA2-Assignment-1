import os
import requests
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

next_ticket_id = 3

# Beispielhafte Tickets im Dictionary gespeichert
tickets = {
    1: {
        "ticket_id": 1,
        "date": "2024-11-08",
        "company_name": "Beispiel GmbH",
        "time": "14:30:00",
        "quantity": 2,
        "subtotal": 100.0,
        "total": 120.0,
        "cost": 90.0,
        "discount": 10.0,
        "tax": 10.0,
        "tax_rate": 0.2,
        "cash": 50.0,
        "credit": 70.0,
        "cart_purchase": 1,
        "customer_id": 1,
        "employee_id": 2
    },
    2: {
        "ticket_id": 2,
        "date": "2024-11-09",
        "company_name": "Test AG",
        "time": "15:45:00",
        "quantity": 1,
        "subtotal": 50.0,
        "total": 60.0,
        "cost": 45.0,
        "discount": 5.0,
        "tax": 5.0,
        "tax_rate": 0.1,
        "cash": 30.0,
        "credit": 30.0,
        "cart_purchase": 1,
        "customer_id": 2,
        "employee_id": 1
    }
}

# Funktion zum Abrufen der Customer-ID basierend auf dem Namen
def get_customer_id(first_name, last_name):
    try:
        response = requests.get(f'http://customer_info:8081/customers/search', params={"first_name": first_name, "last_name": last_name})
        if response.status_code == 200:
            customer = response.json()
            return customer.get("customer_id")
        else:
            return None
    except requests.exceptions.RequestException:
        return None

# Funktion zum Abrufen der Employee-ID basierend auf dem Namen
def get_employee_id(first_name, last_name):
    try:
        response = requests.get(f'http://employee_info:8082/employees/search', params={"first_name": first_name, "last_name": last_name})
        if response.status_code == 200:
            employee = response.json()
            return employee.get("employee_id")
        else:
            return None
    except requests.exceptions.RequestException:
        return None

# CREATE - Route zum Erstellen eines Tickets
@app.route('/tickets', methods=['POST'])
def create_ticket():
    global next_ticket_id
    data = request.get_json()
    customer_first_name = data.get("customer_first_name")
    customer_last_name = data.get("customer_last_name")
    employee_first_name = data.get("employee_first_name")
    employee_last_name = data.get("employee_last_name")

    customer_id = get_customer_id(customer_first_name, customer_last_name)
    if not customer_id:
        return jsonify({"error": "Customer not found"}), 404

    employee_id = get_employee_id(employee_first_name, employee_last_name)
    if not employee_id:
        return jsonify({"error": "Employee not found"}), 404

    # Neues Ticket erstellen und in Dictionary speichern
    ticket = {
        "ticket_id": next_ticket_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "company_name": data.get("company_name", "Beispiel GmbH"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "quantity": data.get("quantity", 1),
        "subtotal": data.get("subtotal", 0.0),
        "total": data.get("total", 0.0),
        "cost": data.get("cost", 0.0),
        "discount": data.get("discount", 0.0),
        "tax": data.get("tax", 0.0),
        "tax_rate": data.get("tax_rate", 0.2),
        "cash": data.get("cash", 0.0),
        "credit": data.get("credit", 0.0),
        "cart_purchase": data.get("cart_purchase", 1),
        "customer_id": customer_id,
        "employee_id": employee_id,
    }

    tickets[next_ticket_id] = ticket
    ticket_id = next_ticket_id  # Speichern der aktuellen Ticket-ID
    next_ticket_id += 1

    # Nachricht an die OpenFaaS-Funktion senden
    openfaas_url = os.getenv("OPENFAAS_URL")
    if openfaas_url:
        ticket_count = len(tickets)  # Anzahl der Tickets im Dictionary
        try:
            response = requests.post(openfaas_url, json={"ticket_count": ticket_count})
            response.raise_for_status()
            print(f"Ticketanzahl erfolgreich an OpenFaaS gesendet: {ticket_count}")
        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Senden der Ticketanzahl an OpenFaaS: {e}")

    return jsonify({"message": "Ticket created successfully", "ticket": ticket}), 201

# READ - Route zum Abrufen eines Tickets basierend auf ticket_id
@app.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    ticket = tickets.get(ticket_id)
    if ticket:
        return jsonify(ticket), 200
    return jsonify({"error": "Ticket not found"}), 404

# UPDATE - Route zum Aktualisieren eines Tickets basierend auf ticket_id
@app.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    ticket = tickets.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    data = request.get_json()
    ticket.update({
        "company_name": data.get("company_name", ticket["company_name"]),
        "quantity": data.get("quantity", ticket["quantity"]),
        "subtotal": data.get("subtotal", ticket["subtotal"]),
        "total": data.get("total", ticket["total"]),
        "cost": data.get("cost", ticket["cost"]),
        "discount": data.get("discount", ticket["discount"]),
        "tax": data.get("tax", ticket["tax"]),
        "tax_rate": data.get("tax_rate", ticket["tax_rate"]),
        "cash": data.get("cash", ticket["cash"]),
        "credit": data.get("credit", ticket["credit"]),
        "cart_purchase": data.get("cart_purchase", ticket["cart_purchase"]),
    })
    return jsonify({"message": "Ticket updated successfully", "ticket": ticket}), 200

# DELETE - Route zum Löschen eines Tickets basierend auf ticket_id
@app.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    if ticket_id in tickets:
        del tickets[ticket_id]
        return jsonify({"message": "Ticket deleted successfully"}), 200
    return jsonify({"error": "Ticket not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)