import sys
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from app.main_window import MainWindow
from app.styles import STYLE


def main():

    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    app.setFont(QFont("Segoe UI", 12))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
