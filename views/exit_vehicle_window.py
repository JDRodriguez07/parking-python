from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)

from controllers.ticket_controller import TicketController


class ExitVehicleWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registrar salida")
        self.setMinimumSize(380, 220)

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

        success, message = self.controller.close_ticket_by_plate(plate)

        if success:
            QMessageBox.information(self, "Éxito", message)
            self.input_plate.clear()
        else:
            QMessageBox.warning(self, "Error", message)