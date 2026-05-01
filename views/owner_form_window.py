from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox
)

from controllers.owner_controller import OwnerController


class OwnerFormWindow(QWidget):
    owner_created = Signal(int)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Crear dueño")
        self.setMinimumSize(400, 360)

        self.controller = OwnerController()

        layout = QVBoxLayout()

        title = QLabel("👤 Crear dueño")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")

        self.combo_type_dni = QComboBox()
        self.combo_type_dni.addItems(["Seleccionar", "CC", "CE", "NIT", "PAS"])
        self.combo_type_dni.setCurrentIndex(0)
        self.combo_type_dni.model().item(0).setEnabled(False)

        self.input_dni = QLineEdit()
        self.input_dni.setPlaceholderText("Documento")

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Nombre")

        self.input_last_name = QLineEdit()
        self.input_last_name.setPlaceholderText("Apellido")

        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("Correo opcional")

        self.input_phone = QLineEdit()
        self.input_phone.setPlaceholderText("Teléfono opcional")

        self.btn_save = QPushButton("Guardar dueño")

        layout.addWidget(title)
        layout.addWidget(QLabel("Tipo documento:"))
        layout.addWidget(self.combo_type_dni)
        layout.addWidget(self.input_dni)
        layout.addWidget(self.input_name)
        layout.addWidget(self.input_last_name)
        layout.addWidget(self.input_correo)
        layout.addWidget(self.input_phone)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)

        self.btn_save.clicked.connect(self.save_owner)

    def save_owner(self):
        type_dni = self.combo_type_dni.currentText()
        dni = self.input_dni.text().strip()
        name = self.input_name.text().strip()
        last_name = self.input_last_name.text().strip()
        correo = self.input_correo.text().strip() or None
        phone = self.input_phone.text().strip() or None

        if type_dni == "Seleccionar":
            QMessageBox.warning(self, "Validación", "Debe seleccionar el tipo de documento.")
            return

        if not dni or not name or not last_name:
            QMessageBox.warning(self, "Validación", "Documento, nombre y apellido son obligatorios.")
            return

        success, message = self.controller.create_owner(
            type_dni=type_dni,
            dni=dni,
            name=name,
            last_name=last_name,
            correo=correo,
            phone=phone
        )

        if success:
            owner = self.controller.search_by_dni(dni)

            QMessageBox.information(self, "Éxito", message)

            if owner:
                self.owner_created.emit(owner.id_owner)

            self.close()
        else:
            QMessageBox.warning(self, "Error", message)