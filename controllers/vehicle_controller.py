from services.vehicle_service import VehicleService


class VehicleController:

    def __init__(self):
        self.service = VehicleService()

    def update_plate(self, id_vehicle, new_plate):
        return self.service.update_plate(id_vehicle, new_plate)

    def update_owner(self, id_vehicle, id_owner):
        return self.service.update_owner(id_vehicle, id_owner)

    def list_vehicles(self):
        return self.service.list_vehicles()

    def search_by_plate(self, plate):
        return self.service.search_by_plate(plate)