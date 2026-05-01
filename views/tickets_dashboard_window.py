from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QHBoxLayout,
    QAbstractItemView, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from controllers.ticket_controller import TicketController


class TicketsDashboardWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dashboard de Tickets")
        self.setMinimumSize(950, 500)

        self.controller = TicketController()

        main_layout = QVBoxLayout()

        title = QLabel("📊 Dashboard de Tickets")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")

        button_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("🔄 Actualizar")
        button_layout.addWidget(self.btn_refresh)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Placa", "Tipo", "Dueño Vehículo", "Teléfono",
            "Entrada", "Salida", "Total", "Estado"
        ])

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        self.configure_table_columns()

        main_layout.addWidget(title)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.btn_refresh.clicked.connect(self.load_tickets)
        self.load_tickets()

    def configure_table_columns(self):
        header = self.table.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.Stretch)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)

    def format_money(self, value):
        if value is None:
            return "Pendiente"

        return f"${int(value):,}".replace(",", ".")

    def load_tickets(self):
        tickets = self.controller.list_tickets_with_details()

        self.table.setRowCount(len(tickets))

        for row_index, ticket in enumerate(tickets):
            entry_time = ticket[5].strftime("%Y-%m-%d %H:%M") if ticket[5] else ""
            exit_time = ticket[6].strftime("%Y-%m-%d %H:%M") if ticket[6] else "Pendiente"
            total_price = self.format_money(ticket[7])

            values = [
                ticket[0],
                ticket[1],
                ticket[2],
                ticket[3],
                ticket[4] or "",
                entry_time,
                exit_time,
                total_price,
                ticket[8],
            ]

            for col_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)

                if col_index == 8:
                    status = str(value)

                    if status == "Abierto":
                        item.setBackground(QColor("#dcfce7"))
                        item.setForeground(QColor("#166534"))
                    else:
                        item.setBackground(QColor("#fee2e2"))
                        item.setForeground(QColor("#991b1b"))

                self.table.setItem(row_index, col_index, item)

        self.configure_table_columns()