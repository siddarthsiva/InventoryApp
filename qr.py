import qrcode
import os
import sys

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
QR_FOLDER = os.path.join(BASE_DIR, 'qr_codes')
os.makedirs(QR_FOLDER, exist_ok=True)

def generate_qr(data: str, filename: str = None) -> str:
    data = str(data).strip()
    if not data:
        raise ValueError("QR data cannot be empty.")

    if filename is None:
        safe_filename = "".join(c for c in data if c.isalnum() or c in ('-', '_'))
        filename = f"{safe_filename}.png"

    filepath = os.path.abspath(os.path.join(QR_FOLDER, filename))

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)

    return filepath
