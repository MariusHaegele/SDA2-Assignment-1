import json
import os

# Dateipfad zum Speichern der Ticketanzahl
TICKET_COUNT_FILE = "/tmp/ticket_count.txt"

def handle(req):
    # Prüfen, ob die Anfrage eine Aktualisierung des Ticket Count ist
    try:
        data = json.loads(req)
        if "ticket_count" in data:
            # Ticketanzahl in Datei speichern
            with open(TICKET_COUNT_FILE, "w") as f:
                f.write(str(data["ticket_count"]))
            return f"Ticket count updated to {data['ticket_count']}"
    except json.JSONDecodeError:
        pass

    # Ticketanzahl aus Datei lesen
    if os.path.exists(TICKET_COUNT_FILE):
        with open(TICKET_COUNT_FILE, "r") as f:
            ticket_count = f.read().strip()
            return f"Anzahl der vorhandenen Tickets: {ticket_count}"
    else:
        return "Erstellen Sie zuerst ein neues Ticket mithilfe eines POST-Requests!"