from repositories.vehicle_repository import VehicleRepository
from repositories.owner_repository import OwnerRepository

DEFAULT_OWNER_DNI = "000000000"


class VehicleService:

    def __init__(self):
        self.vehicle_repo = VehicleRepository()
        self.owner_repo = OwnerRepository()

    def create_vehicle(self, vehicle):
        existing_vehicle = self.vehicle_repo.get_by_plate(vehicle.plate)

        if existing_vehicle:
            return False, "Ya existe un vehículo con esa placa"

        if not vehicle.id_owner:
            default_owner = self.owner_repo.get_by_dni(DEFAULT_OWNER_DNI)

            if not default_owner:
                return False, "No existe el owner por defecto"

            vehicle.id_owner = default_owner.id_owner
        else:
            owner_exists = self.owner_repo.get_by_id(vehicle.id_owner)

            if not owner_exists:
                return False, "No existe un propietario con ese ID"

        self.vehicle_repo.create(vehicle)
        return True, "Vehículo creado correctamente"

    def update_plate(self, id_vehicle, new_plate):
        vehicle = self.vehicle_repo.get_by_id(id_vehicle)

        if not vehicle:
            return False, "No existe un vehículo con ese ID"

        existing_plate = self.vehicle_repo.get_by_plate(new_plate)

        if existing_plate and existing_plate.id_vehicle != id_vehicle:
            return False, "Ya existe otro vehículo con esa placa"

        updated = self.vehicle_repo.update_plate(id_vehicle, new_plate)

        if not updated:
            return False, "No se pudo actualizar la placa"

        return True, "Placa actualizada correctamente"

    def update_owner(self, id_vehicle, id_owner):
        vehicle = self.vehicle_repo.get_by_id(id_vehicle)

        if not vehicle:
            return False, "No existe el vehículo"

        owner = self.owner_repo.get_by_id(id_owner)

        if not owner:
            return False, "No existe el owner"

        updated = self.vehicle_repo.update_owner(id_vehicle, id_owner)

        if not updated:
            return False, "No se pudo actualizar el owner"

        return True, "Owner actualizado correctamente"

    def list_vehicles(self):
        return self.vehicle_repo.get_all()

    def search_by_plate(self, plate):
        return self.vehicle_repo.get_by_plate(plate)