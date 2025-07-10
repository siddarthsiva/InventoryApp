import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from ui.main_ui import InventoryApp
from db.database import initialize_database

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def main():
    initialize_database()
    app = QApplication(sys.argv)
    window = InventoryApp()
    icon_path = resource_path("assets/icon.ico")
    if os.path.exists(icon_path):
        icon = QIcon(icon_path)
        window.setWindowIcon(icon)

    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
