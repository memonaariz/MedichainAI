#!/usr/bin/env python
"""
Generate sample prescription image for testing
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Create uploads folder if not exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Create a prescription image
width, height = 800, 600
image = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(image)

# Try to use a nice font, fallback to default
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
except:
    title_font = ImageFont.load_default()
    text_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# Draw prescription header
draw.text((50, 30), "MEDICAL PRESCRIPTION", fill='black', font=title_font)
draw.line([(50, 80), (750, 80)], fill='black', width=2)

# Draw doctor info
draw.text((50, 100), "Dr. Sharma", fill='black', font=text_font)
draw.text((50, 140), "City Clinic, Mumbai", fill='black', font=small_font)
draw.text((50, 170), "Phone: 9876543210", fill='black', font=small_font)

# Draw patient info
draw.text((50, 220), "Patient: Rajesh Kumar", fill='black', font=text_font)
draw.text((50, 260), "Age: 65 years", fill='black', font=small_font)
draw.text((50, 290), "Date: 22-02-2025", fill='black', font=small_font)

# Draw medications
draw.text((50, 340), "MEDICATIONS:", fill='black', font=text_font)
draw.text((70, 380), "1. Amlong 5mg - Once daily - 30 days", fill='black', font=small_font)
draw.text((70, 420), "2. Metformin 500mg - Twice daily - 30 days", fill='black', font=small_font)
draw.text((70, 460), "3. Aspirin 75mg - Once daily - 30 days", fill='black', font=small_font)

# Draw notes
draw.text((50, 510), "Notes: Take with food. Avoid dairy with Metformin.", fill='black', font=small_font)

# Save image
filename = 'uploads/sample_prescription.jpg'
image.save(filename)
print(f"✅ Generated sample prescription: {filename}")

print("\n✅ Sample prescription created successfully!")
print("\nHow to use:")
print("1. Patient login as: patient1 / pat123")
print("2. Go to 'Snap Prescription'")
print("3. Upload or take photo of: uploads/sample_prescription.jpg")
print("4. AI will read the prescription automatically")
