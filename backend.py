"""Mock backend for a fictional shop. The agent calls these as tools."""
import itertools

ORDERS = {
    "A1001": {"status": "shipped", "carrier": "Posti", "eta": "2026-11-14"},
    "A1002": {"status": "processing", "carrier": None, "eta": "2026-11-18"},
    "A1003": {"status": "delivered", "carrier": "Posti", "eta": "2026-11-05"},
}

_ticket_ids = itertools.count(1)
TICKETS = []


def get_order_status(order_id: str) -> dict:
    order = ORDERS.get(order_id.strip().upper())
    if order is None:
        return {"error": f"No order found with id {order_id}"}
    return {"order_id": order_id.strip().upper(), **order}


def create_ticket(summary: str) -> dict:
    ticket = {"ticket_id": f"T{next(_ticket_ids):04d}", "summary": summary}
    TICKETS.append(ticket)
    return ticket
