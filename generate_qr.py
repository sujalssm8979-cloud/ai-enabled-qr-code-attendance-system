# generate_qr.py
import qrcode
import os

students = {
    "John Doe": "101",
    "Alice Smith": "102",
    "Rahul Kumar": "103",
    "Priya Sharma": "104",
    "Amit Patel": "105"
}

if not os.path.exists("qr_codes"):
    os.makedirs("qr_codes")

for name, roll in students.items():
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(roll)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"qr_codes/{roll}_{name.replace(' ', '_')}.png")

print("All QR codes generated in 'qr_codes' folder!")