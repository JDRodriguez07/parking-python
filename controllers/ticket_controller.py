from services.ticket_service import TicketService


class TicketController:

    def __init__(self):
        self.service = TicketService()

    def register_entry(self, plate, vehicle_type, id_owner=None):
        return self.service.register_entry(plate, vehicle_type, id_owner)

    def close_ticket_by_plate(self, plate):
        return self.service.close_ticket_by_plate(plate)

    def list_tickets(self):
        return self.service.list_tickets()

    def list_tickets_with_details(self):
        return self.service.list_tickets_with_details()