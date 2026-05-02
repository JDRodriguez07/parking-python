import sys

from PySide6.QtWidgets import QApplication
from views.main_window import MainWindow
from views.styles import APP_STYLE


def main():
    print("Starting application...")
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()