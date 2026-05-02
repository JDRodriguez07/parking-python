from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt

from views.entry_vehicle_window import EntryVehicleWindow
from views.exit_vehicle_window import ExitVehicleWindow
from views.tickets_dashboard_window import TicketsDashboardWindow
from views.owner_management_window import OwnerManagementWindow
from views.vehicle_management_window import VehicleManagementWindow


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Parqueadero")
        self.setMinimumSize(400, 500)

        layout = QVBoxLayout()

        title = QLabel("🚗 Sistema de Parqueadero")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")

        btn_entry = QPushButton("Registrar Ingreso")
        btn_exit = QPushButton("Registrar Salida")
        btn_dashboard = QPushButton("Dashboard Tickets")
        btn_owners = QPushButton("Gestionar Dueños")
        btn_vehicles = QPushButton("Gestionar Vehículos")

        layout.addWidget(title)
        layout.addWidget(btn_entry)
        layout.addWidget(btn_exit)
        layout.addWidget(btn_dashboard)
        layout.addWidget(btn_owners)
        layout.addWidget(btn_vehicles)

        self.setLayout(layout)

        btn_entry.clicked.connect(self.open_entry)
        btn_exit.clicked.connect(self.open_exit)
        btn_dashboard.clicked.connect(self.open_dashboard)
        btn_owners.clicked.connect(self.open_owners)
        btn_vehicles.clicked.connect(self.open_vehicles)

    def open_entry(self):
        self.entry_window = EntryVehicleWindow()
        self.entry_window.show()

    def open_exit(self):
        self.exit_window = ExitVehicleWindow()
        self.exit_window.show()

    def open_dashboard(self):
        self.dashboard_window = TicketsDashboardWindow()
        self.dashboard_window.show()

    def open_owners(self):
        self.owners_window = OwnerManagementWindow()
        self.owners_window.show()

    def open_vehicles(self):
        self.vehicles_window = VehicleManagementWindow()
        self.vehicles_window.show()