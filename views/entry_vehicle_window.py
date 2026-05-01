from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox
)

from controllers.ticket_controller import TicketController


class EntryVehicleWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registrar ingreso")
        self.setMinimumSize(380, 260)

        self.controller = TicketController()

        layout = QVBoxLayout()

        title = QLabel("🚗 Registrar ingreso")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")

        self.input_plate = QLineEdit()
        self.input_plate.setPlaceholderText("Placa del vehículo")

        self.combo_type = QComboBox()
        self.combo_type.addItems(["Seleccionar", "Carro", "Moto"])
        self.combo_type.setCurrentIndex(0)
        self.combo_type.model().item(0).setEnabled(False)

        self.btn_register = QPushButton("Registrar ingreso")

        layout.addWidget(title)
        layout.addWidget(QLabel("Placa:"))
        layout.addWidget(self.input_plate)
        layout.addWidget(QLabel("Tipo de vehículo:"))
        layout.addWidget(self.combo_type)
        layout.addWidget(self.btn_register)

        self.setLayout(layout)

        self.btn_register.clicked.connect(self.register_entry)

    def register_entry(self):
        plate = self.input_plate.text().strip().upper()
        vehicle_type = self.combo_type.currentText()

        if not plate:
            QMessageBox.warning(self, "Validación", "Debe ingresar la placa.")
            return

        if vehicle_type == "Seleccionar":
            QMessageBox.warning(self, "Validación", "Debe seleccionar el tipo de vehículo.")
            return

        success, message = self.controller.register_entry(
            plate=plate,
            vehicle_type=vehicle_type,
            id_owner=None
        )

        if success:
            QMessageBox.information(self, "Éxito", message)
            self.input_plate.clear()
            self.combo_type.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Error", message)