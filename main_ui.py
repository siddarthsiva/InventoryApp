import cv2
from PyQt6 import QtGui
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from pyzbar.pyzbar import decode

from db.database import (
    add_item, get_all_items, update_item,
    get_item_by_serial, get_low_stock_items
)
from utils.exporter import export_to_csv
from utils.qr import generate_qr


class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Manager")
        self.resize(800, 600)

        self.layout = QVBoxLayout()
        form_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Item Name")

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity")

        self.serial_input = QLineEdit()
        self.serial_input.setPlaceholderText("Serial Number")

        self.threshold_input = QLineEdit()
        self.threshold_input.setPlaceholderText("Threshold")

        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.quantity_input)
        form_layout.addWidget(self.serial_input)
        form_layout.addWidget(self.threshold_input)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Item")
        self.update_btn = QPushButton("Update Item")
        self.export_btn = QPushButton("Export CSV")
        self.scan_btn = QPushButton("Scan QR")
        self.low_stock_btn = QPushButton("Show Low Stock Only")
        self.show_all_btn = QPushButton("Show All Items")  # NEW BUTTON

        self.add_btn.clicked.connect(self.add_item)
        self.update_btn.clicked.connect(self.update_item)
        self.export_btn.clicked.connect(self.export_csv)
        self.scan_btn.clicked.connect(self.scan_qr)
        self.low_stock_btn.clicked.connect(self.show_low_stock_only)
        self.show_all_btn.clicked.connect(lambda: self.load_data())  # NEW CONNECTION

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.scan_btn)
        btn_layout.addWidget(self.low_stock_btn)
        btn_layout.addWidget(self.show_all_btn)  # ADD TO LAYOUT

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Quantity", "Serial", "QR Path", "Threshold"])
        self.table.cellClicked.connect(self.fill_form_from_table)

        self.layout.addLayout(form_layout)
        self.layout.addLayout(btn_layout)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.load_data()

    def load_data(self, only_low_stock=False):
        self.table.setRowCount(0)
        items = get_low_stock_items() if only_low_stock else get_all_items()
        for row_num, row_data in enumerate(items):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                try:
                    if col_num == 2:  # Quantity column
                        quantity = int(row_data[2])
                        threshold = int(row_data[5])
                        if quantity < threshold:
                            item.setBackground(QtGui.QColor('red'))
                except (IndexError, ValueError):
                    pass
                self.table.setItem(row_num, col_num, item)

    def fill_form_from_table(self, row, _):
        self.name_input.setText(self.table.item(row, 1).text())
        self.quantity_input.setText(self.table.item(row, 2).text())
        self.serial_input.setText(self.table.item(row, 3).text())
        self.threshold_input.setText(self.table.item(row, 5).text())

    def add_item(self):
        try:
            name = self.name_input.text().strip()
            quantity = int(self.quantity_input.text())
            serial = self.serial_input.text().strip()
            threshold = int(self.threshold_input.text())

            if not serial:
                raise ValueError("Serial number cannot be empty.")

            qr_code_path = generate_qr(serial)
            add_item(name, quantity, serial, threshold, qr_code_path)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_item(self):
        try:
            serial = self.serial_input.text().strip()
            item = get_item_by_serial(serial)
            if not item:
                raise Exception("Item not found.")
            name = self.name_input.text().strip()
            quantity = int(self.quantity_input.text())
            threshold = int(self.threshold_input.text())

            update_item(serial, name, quantity, threshold)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def export_csv(self):
        path = export_to_csv()
        QMessageBox.information(self, "Export Complete", f"CSV saved to {path}")

    def scan_qr(self):
        cap = cv2.VideoCapture(0)
        found = False
        qr_data = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            decoded_objects = decode(frame)
            for obj in decoded_objects:
                qr_data = obj.data.decode('utf-8')
                found = True
                break

            cv2.imshow("Scan QR Code - Press 'q' to cancel", frame)

            if cv2.waitKey(1) & 0xFF == ord('q') or found:
                break

        cap.release()
        cv2.destroyAllWindows()

        if qr_data:
            self.serial_input.setText(qr_data)
            item = get_item_by_serial(qr_data)
            if item:
                self.name_input.setText(item[1])
                self.quantity_input.setText(str(item[2]))
                self.threshold_input.setText(str(item[5]))
                QMessageBox.information(self, "QR Scanned", "Item loaded and ready to update.")
            else:
                QMessageBox.warning(self, "Item Not Found", "This QR code does not match any item.")
        else:
            QMessageBox.warning(self, "No QR Found", "No QR code was detected.")

    def show_low_stock_only(self):
        self.load_data(only_low_stock=True)
