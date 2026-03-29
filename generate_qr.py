#!/usr/bin/env python
"""
Generate QR codes for patients
"""
import qrcode
import os
from datetime import datetime

# Create uploads folder if not exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Patient data
patients = {
    "patient1": {
        "id": "patient1",
        "name": "Rajesh Kumar",
        "age": 65,
        "phone": "9876543210",
        "allergies": ["Penicillin", "Aspirin"],
        "medical_history": ["Diabetes", "Hypertension"]
    }
}

# Generate QR codes
for patient_id, patient_data in patients.items():
    # Create QR code data
    qr_data = f"PATIENT_{patient_id}_QR"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code
    filename = f"uploads/qr_code_{patient_id}.png"
    img.save(filename)
    print(f"✅ Generated QR code: {filename}")

print("\n✅ All QR codes generated successfully!")
print("\nHow to use:")
print("1. Doctor login as: doctor1 / doc123")
print("2. Go to 'Scan QR Code'")
print("3. Point camera at the QR code image")
print("4. QR code will be scanned automatically")
