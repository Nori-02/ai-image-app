import os
import qrcode

def generate_qr(image_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    qr = qrcode.make(f"file://{os.path.abspath(image_path)}")
    qr_filename = os.path.join(output_dir, os.path.basename(image_path).replace(".png", "_qr.png"))
    qr.save(qr_filename)
    return qr_filename
