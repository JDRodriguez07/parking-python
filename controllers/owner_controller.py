from services.owner_service import OwnerService
from models.owner import Owner


class OwnerController:

    def __init__(self):
        self.service = OwnerService()

    def create_owner(self, type_dni, dni, name, last_name, correo, phone):
        owner = Owner(
            type_dni=type_dni,
            dni=dni,
            name=name,
            last_name=last_name,
            correo=correo,
            phone=phone
        )

        return self.service.create_owner(owner)

    def update_owner(self, id_owner, type_dni, dni, name, last_name, correo, phone):
        owner = Owner(
            id_owner=id_owner,
            type_dni=type_dni,
            dni=dni,
            name=name,
            last_name=last_name,
            correo=correo,
            phone=phone
        )

        return self.service.update_owner(owner)

    def list_owners(self):
        return self.service.list_owners()

    def search_by_dni(self, dni):
        return self.service.search_by_dni(dni)

    def search_by_id(self, id_owner):
        return self.service.search_by_id(id_owner)