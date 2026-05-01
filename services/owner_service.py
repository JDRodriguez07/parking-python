from repositories.owner_repository import OwnerRepository


class OwnerService:

    def __init__(self):
        self.repo = OwnerRepository()

    def create_owner(self, owner):
        existing = self.repo.get_by_dni(owner.dni)

        if existing:
            return False, "Ya existe un owner con ese DNI"

        if owner.phone and not owner.phone.isdigit():
            return False, "El teléfono debe contener solo números"

        self.repo.create(owner)
        return True, "Owner creado correctamente"

    def update_owner(self, owner):
        existing_owner = self.repo.get_by_id(owner.id_owner)

        if not existing_owner:
            return False, "No existe un owner con ese ID"

        if owner.phone and not owner.phone.isdigit():
            return False, "El teléfono debe contener solo números"

        owner_with_same_dni = self.repo.get_by_dni(owner.dni)

        if owner_with_same_dni and owner_with_same_dni.id_owner != owner.id_owner:
            return False, "Ya existe otro owner con ese DNI"

        updated = self.repo.update(owner)

        if not updated:
            return False, "No se pudo actualizar el owner"

        return True, "Owner actualizado correctamente"

    def list_owners(self):
        return self.repo.get_all()