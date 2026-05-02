from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)

from views.owner_form_window import OwnerFormWindow
from controllers.vehicle_controller import VehicleController
from controllers.ticket_controller import TicketController


class ExitVehicleWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registrar salida")
        self.setMinimumSize(380, 220)

        self.vehicle_controller = VehicleController()
        self.controller = TicketController()

        layout = QVBoxLayout()

        title = QLabel("🚗 Registrar salida")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")

        self.input_plate = QLineEdit()
        self.input_plate.setPlaceholderText("Placa del vehículo")

        self.btn_close = QPushButton("Registrar salida")

        layout.addWidget(title)
        layout.addWidget(QLabel("Placa:"))
        layout.addWidget(self.input_plate)
        layout.addWidget(self.btn_close)

        self.setLayout(layout)

        self.btn_close.clicked.connect(self.close_ticket)

    def close_ticket(self):
        plate = self.input_plate.text().strip().upper()

        if not plate:
            QMessageBox.warning(self, "Validación", "Debe ingresar la placa.")
            return

        vehicle = self.vehicle_controller.search_by_plate(plate)

        if not vehicle:
            QMessageBox.warning(self, "Error", "No existe ese vehículo.")
            return

        # Validar si es consumidor final
        if vehicle.id_owner == 1:
            reply = QMessageBox.question(
                self,
                "Asignar dueño",
                "Este vehículo está como consumidor final. ¿Desea asignarle un dueño?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.owner_form = OwnerFormWindow()
                self.owner_form.owner_created.connect(
                    lambda owner_id: self.assign_owner_and_close(vehicle.id_vehicle, plate, owner_id)
                )
                self.owner_form.show()
                return

        success, message = self.controller.close_ticket_by_plate(plate)

        if success:
            QMessageBox.information(self, "Éxito", message)
            self.input_plate.clear()
        else:
            QMessageBox.warning(self, "Error", message)

    def assign_owner_and_close(self, id_vehicle, plate, owner_id):
        success_owner, msg_owner = self.vehicle_controller.update_owner(id_vehicle, owner_id)

        if not success_owner:
            QMessageBox.warning(self, "Error", msg_owner)
            return

        success, message = self.controller.close_ticket_by_plate(plate)

        if success:
            QMessageBox.information(self, "Éxito", message)
            self.input_plate.clear()
        else:
            QMessageBox.warning(self, "Error", message)