import csv
import os
import sys
from datetime import datetime
from db.database import get_all_items

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
EXPORT_FOLDER = os.path.join(BASE_DIR, 'exports')
os.makedirs(EXPORT_FOLDER, exist_ok=True)

def export_to_csv(filename=None) -> str:
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"inventory_export_{timestamp}.csv"

    filepath = os.path.join(EXPORT_FOLDER, filename)
    data = get_all_items()

    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Quantity", "Serial Number", "QR Code", "Threshold"])
        writer.writerows(data)

    return filepath

