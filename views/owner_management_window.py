from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox
)

from controllers.owner_controller import OwnerController


class OwnerManagementWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestionar dueños")
        self.setMinimumSize(450, 420)

        self.controller = OwnerController()
        self.current_owner_id = None

        layout = QVBoxLayout()

        title = QLabel("👤 Gestionar dueños")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")

        search_layout = QHBoxLayout()
        self.input_search_dni = QLineEdit()
        self.input_search_dni.setPlaceholderText("Buscar por documento")
        self.btn_search = QPushButton("Buscar")

        search_layout.addWidget(self.input_search_dni)
        search_layout.addWidget(self.btn_search)

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
        self.input_correo.setPlaceholderText("Correo")

        self.input_phone = QLineEdit()
        self.input_phone.setPlaceholderText("Teléfono")

        self.btn_save = QPushButton("Guardar cambios")
        self.btn_clear = QPushButton("Limpiar")

        layout.addWidget(title)
        layout.addLayout(search_layout)
        layout.addWidget(QLabel("Tipo documento:"))
        layout.addWidget(self.combo_type_dni)
        layout.addWidget(self.input_dni)
        layout.addWidget(self.input_name)
        layout.addWidget(self.input_last_name)
        layout.addWidget(self.input_correo)
        layout.addWidget(self.input_phone)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_clear)

        self.setLayout(layout)

        self.btn_search.clicked.connect(self.search_owner)
        self.btn_save.clicked.connect(self.save_changes)
        self.btn_clear.clicked.connect(self.clear_form)

    def search_owner(self):
        dni = self.input_search_dni.text().strip()

        if not dni:
            QMessageBox.warning(self, "Validación", "Debe ingresar un documento para buscar.")
            return

        owner = self.controller.search_by_dni(dni)

        if not owner:
            QMessageBox.warning(self, "No encontrado", "No existe un dueño con ese documento.")
            self.clear_form()
            return

        self.current_owner_id = owner.id_owner

        index = self.combo_type_dni.findText(owner.type_dni)
        self.combo_type_dni.setCurrentIndex(index if index >= 0 else 0)

        self.input_dni.setText(owner.dni)
        self.input_name.setText(owner.name)
        self.input_last_name.setText(owner.last_name)
        self.input_correo.setText(owner.correo or "")
        self.input_phone.setText(owner.phone or "")

    def save_changes(self):
        if not self.current_owner_id:
            QMessageBox.warning(self, "Validación", "Primero debe buscar un dueño.")
            return

        type_dni = self.combo_type_dni.currentText()
        dni = self.input_dni.text().strip()
        name = self.input_name.text().strip()
        last_name = self.input_last_name.text().strip()
        correo = self.input_correo.text().strip() or None
        phone = self.input_phone.text().strip() or None

        if type_dni == "Seleccionar":
            QMessageBox.warning(self, "Validación", "Debe seleccionar tipo de documento.")
            return

        if not dni or not name or not last_name:
            QMessageBox.warning(self, "Validación", "Documento, nombre y apellido son obligatorios.")
            return

        success, message = self.controller.update_owner(
            id_owner=self.current_owner_id,
            type_dni=type_dni,
            dni=dni,
            name=name,
            last_name=last_name,
            correo=correo,
            phone=phone
        )

        if success:
            QMessageBox.information(self, "Éxito", message)
        else:
            QMessageBox.warning(self, "Error", message)

    def clear_form(self):
        self.current_owner_id = None
        self.input_search_dni.clear()
        self.combo_type_dni.setCurrentIndex(0)
        self.input_dni.clear()
        self.input_name.clear()
        self.input_last_name.clear()
        self.input_correo.clear()
        self.input_phone.clear()