class Owner:
    def __init__(
        self,
        id_owner=None,
        type_dni=None,
        dni=None,
        name=None,
        last_name=None,
        correo=None,
        phone=None
    ):
        self.id_owner = id_owner
        self.type_dni = type_dni
        self.dni = dni
        self.name = name
        self.last_name = last_name
        self.correo = correo
        self.phone = phone

    def full_name(self):
        return f"{self.name} {self.last_name}"