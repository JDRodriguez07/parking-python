from datetime import datetime
from decimal import Decimal, ROUND_UP

from models.ticket import Ticket
from models.vehicle import Vehicle

from repositories.ticket_repository import TicketRepository
from repositories.vehicle_repository import VehicleRepository
from repositories.rate_repository import RateRepository

from services.vehicle_service import VehicleService


class TicketService:

    def __init__(self):
        self.ticket_repo = TicketRepository()
        self.vehicle_repo = VehicleRepository()
        self.rate_repo = RateRepository()
        self.vehicle_service = VehicleService()

    def register_entry(self, plate, vehicle_type, id_owner=None):
        plate = plate.strip().upper()

        vehicle = self.vehicle_repo.get_by_plate(plate)

        rate = self.rate_repo.get_by_vehicle_type(vehicle_type)

        if not rate:
            return False, "No existe tarifa para ese tipo de vehículo"

        if not vehicle:
            new_vehicle = Vehicle(
                id_owner=id_owner,
                id_rate=rate.id_rate,
                plate=plate
            )

            success, message = self.vehicle_service.create_vehicle(new_vehicle)

            if not success:
                return False, message

            vehicle = self.vehicle_repo.get_by_plate(plate)

        open_ticket = self.ticket_repo.get_open_ticket_by_vehicle(vehicle.id_vehicle)

        if open_ticket:
            return False, "Este vehículo ya tiene un ticket abierto"

        ticket = Ticket(
            id_vehicle=vehicle.id_vehicle,
            entry_time=datetime.now()
        )

        self.ticket_repo.create(ticket)
        return True, "Ingreso registrado correctamente"

    def close_ticket_by_plate(self, plate):
        vehicle_data = self.vehicle_repo.get_with_rate_by_plate(plate)

        if not vehicle_data:
            return False, "No existe un vehículo con esa placa"

        open_ticket = self.ticket_repo.get_open_ticket_by_vehicle(vehicle_data["id_vehicle"])

        if not open_ticket:
            return False, "Este vehículo no tiene un ticket abierto"

        exit_time = datetime.now()

        total_price = self.calculate_total_price(
            open_ticket.entry_time,
            exit_time,
            vehicle_data["cost_per_hour"]
        )

        self.ticket_repo.close_ticket(
            open_ticket.id_ticket,
            exit_time,
            total_price
        )

        return True, f"Ticket cerrado correctamente. Total: {total_price}"

    def calculate_total_price(self, entry_time, exit_time, cost_per_hour):
        total_seconds = (exit_time - entry_time).total_seconds()
        total_hours = Decimal(total_seconds) / Decimal(3600)

        billable_hours = total_hours.quantize(Decimal("1"), rounding=ROUND_UP)

        if billable_hours < 1:
            billable_hours = Decimal("1")

        return billable_hours * Decimal(cost_per_hour)

    def list_tickets(self):
        return self.ticket_repo.get_all()

    def list_tickets_with_details(self):
        return self.ticket_repo.get_all_with_details()