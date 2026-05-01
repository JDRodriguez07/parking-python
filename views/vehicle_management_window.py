from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)

from controllers.vehicle_controller import VehicleController
from controllers.owner_controller import OwnerController


class VehicleManagementWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestionar vehículos")
        self.setMinimumSize(460, 350)

        self.vehicle_controller = VehicleController()
        self.owner_controller = OwnerController()

        self.current_vehicle_id = None

        layout = QVBoxLayout()

        title = QLabel("🚘 Gestionar vehículos")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")

        search_layout = QHBoxLayout()
        self.input_search_plate = QLineEdit()
        self.input_search_plate.setPlaceholderText("Buscar por placa")
        self.btn_search = QPushButton("Buscar")

        search_layout.addWidget(self.input_search_plate)
        search_layout.addWidget(self.btn_search)

        self.input_plate = QLineEdit()
        self.input_plate.setPlaceholderText("Placa")

        self.label_owner_current = QLabel("Dueño actual: -")

        self.input_owner_dni = QLineEdit()
        self.input_owner_dni.setPlaceholderText("Documento del nuevo dueño")

        self.btn_update_plate = QPushButton("Actualizar placa")
        self.btn_update_owner = QPushButton("Cambiar dueño")
        self.btn_clear = QPushButton("Limpiar")

        layout.addWidget(title)
        layout.addLayout(search_layout)
        layout.addWidget(QLabel("Placa:"))
        layout.addWidget(self.input_plate)
        layout.addWidget(self.label_owner_current)
        layout.addWidget(QLabel("Nuevo dueño:"))
        layout.addWidget(self.input_owner_dni)
        layout.addWidget(self.btn_update_plate)
        layout.addWidget(self.btn_update_owner)
        layout.addWidget(self.btn_clear)

        self.setLayout(layout)

        self.btn_search.clicked.connect(self.search_vehicle)
        self.btn_update_plate.clicked.connect(self.update_plate)
        self.btn_update_owner.clicked.connect(self.update_owner)
        self.btn_clear.clicked.connect(self.clear_form)

    def search_vehicle(self):
        plate = self.input_search_plate.text().strip().upper()

        if not plate:
            QMessageBox.warning(self, "Validación", "Debe ingresar una placa.")
            return

        vehicle = self.vehicle_controller.search_by_plate(plate)

        if not vehicle:
            QMessageBox.warning(self, "No encontrado", "No existe un vehículo con esa placa.")
            self.clear_form()
            return

        self.current_vehicle_id = vehicle.id_vehicle
        self.input_plate.setText(vehicle.plate)

        owner = self.owner_controller.search_by_id(vehicle.id_owner)

        if owner:
            self.label_owner_current.setText(
                f"Dueño actual: {owner.name} {owner.last_name} - DNI: {owner.dni}"
            )
        else:
            self.label_owner_current.setText("Dueño actual: No encontrado")

    def update_plate(self):
        if not self.current_vehicle_id:
            QMessageBox.warning(self, "Validación", "Primero debe buscar un vehículo.")
            return

        new_plate = self.input_plate.text().strip().upper()

        if not new_plate:
            QMessageBox.warning(self, "Validación", "Debe ingresar la placa.")
            return

        success, message = self.vehicle_controller.update_plate(
            self.current_vehicle_id,
            new_plate
        )

        if success:
            QMessageBox.information(self, "Éxito", message)
            self.input_search_plate.setText(new_plate)
        else:
            QMessageBox.warning(self, "Error", message)

    def update_owner(self):
        if not self.current_vehicle_id:
            QMessageBox.warning(self, "Validación", "Primero debe buscar un vehículo.")
            return

        owner_dni = self.input_owner_dni.text().strip()

        if not owner_dni:
            QMessageBox.warning(self, "Validación", "Debe ingresar el documento del nuevo dueño.")
            return

        owner = self.owner_controller.search_by_dni(owner_dni)

        if not owner:
            QMessageBox.warning(self, "No encontrado", "No existe un dueño con ese documento.")
            return

        success, message = self.vehicle_controller.update_owner(
            self.current_vehicle_id,
            owner.id_owner
        )

        if success:
            QMessageBox.information(self, "Éxito", message)
            self.label_owner_current.setText(
                f"Dueño actual: {owner.name} {owner.last_name} - DNI: {owner.dni}"
            )
            self.input_owner_dni.clear()
        else:
            QMessageBox.warning(self, "Error", message)

    def clear_form(self):
        self.current_vehicle_id = None
        self.input_search_plate.clear()
        self.input_plate.clear()
        self.input_owner_dni.clear()
        self.label_owner_current.setText("Dueño actual: -")