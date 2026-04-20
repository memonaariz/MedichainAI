"""
Generate 10 demo patient QR code cards — saves as demo_qr_cards.html
Open that HTML file in browser and print/screenshot each card.
"""

import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEMO_PATIENTS = [
    {
        "id": "demo_p1",
        "name": "Rajesh Kumar",
        "age": 65, "blood_group": "O+",
        "phone": "9876543210",
        "allergies": ["Penicillin", "Aspirin"],
        "conditions": ["Type 2 Diabetes", "Hypertension"],
        "doctor": "Dr. Sharma",
        "medicines": ["Metformin 500mg", "Amlong 5mg", "Ecosprin 75mg"]
    },
    {
        "id": "demo_p2",
        "name": "Sunita Patel",
        "age": 58, "blood_group": "B+",
        "phone": "9823456710",
        "allergies": ["Sulfa drugs"],
        "conditions": ["Hypothyroidism", "Obesity"],
        "doctor": "Dr. Mehta",
        "medicines": ["Thyronorm 50mcg", "Shelcal 500mg", "Revital"]
    },
    {
        "id": "demo_p3",
        "name": "Arun Sharma",
        "age": 72, "blood_group": "A+",
        "phone": "9712345678",
        "allergies": ["Ibuprofen"],
        "conditions": ["Hypertension", "High Cholesterol"],
        "doctor": "Dr. Patel",
        "medicines": ["Telma 40mg", "Atorva 10mg", "Rosuvas 10mg"]
    },
    {
        "id": "demo_p4",
        "name": "Meena Joshi",
        "age": 45, "blood_group": "AB+",
        "phone": "9654321098",
        "allergies": ["None known"],
        "conditions": ["Asthma", "Allergic Rhinitis"],
        "doctor": "Dr. Kulkarni",
        "medicines": ["Asthalin Inhaler", "Foracort 200", "Montek LC"]
    },
    {
        "id": "demo_p5",
        "name": "Vikram Singh",
        "age": 55, "blood_group": "O-",
        "phone": "9543210987",
        "allergies": ["Penicillin"],
        "conditions": ["Type 2 Diabetes", "Neuropathy"],
        "doctor": "Dr. Gupta",
        "medicines": ["Glycomet 1g", "Pregabalin 75mg", "Becosules"]
    },
    {
        "id": "demo_p6",
        "name": "Priya Nair",
        "age": 38, "blood_group": "B-",
        "phone": "9432109876",
        "allergies": ["Aspirin", "Codeine"],
        "conditions": ["GERD", "Anxiety"],
        "doctor": "Dr. Iyer",
        "medicines": ["Pan-D 40mg", "Omez 20mg", "Nexito 10mg"]
    },
    {
        "id": "demo_p7",
        "name": "Suresh Reddy",
        "age": 68, "blood_group": "A-",
        "phone": "9321098765",
        "allergies": ["NSAIDs"],
        "conditions": ["Coronary Artery Disease", "Hypertension"],
        "doctor": "Dr. Rao",
        "medicines": ["Ecosprin 150mg", "Clopitop 75mg", "Telma 80mg", "Atorva 40mg"]
    },
    {
        "id": "demo_p8",
        "name": "Kavita Desai",
        "age": 50, "blood_group": "AB-",
        "phone": "9210987654",
        "allergies": ["Latex", "Sulfa"],
        "conditions": ["Rheumatoid Arthritis", "Anaemia"],
        "doctor": "Dr. Shah",
        "medicines": ["Wysolone 10mg", "Dexorange Syrup", "Shelcal HD"]
    },
    {
        "id": "demo_p9",
        "name": "Mohan Verma",
        "age": 62, "blood_group": "O+",
        "phone": "9109876543",
        "allergies": ["None known"],
        "conditions": ["COPD", "Type 2 Diabetes"],
        "doctor": "Dr. Jain",
        "medicines": ["Deriphyllin", "Glycomet SR 500mg", "Limcee 500mg"]
    },
    {
        "id": "demo_p10",
        "name": "Anita Bose",
        "age": 42, "blood_group": "B+",
        "phone": "9098765432",
        "allergies": ["Penicillin", "Dust"],
        "conditions": ["Migraine", "Iron Deficiency"],
        "doctor": "Dr. Chatterjee",
        "medicines": ["Saridon", "Dexorange", "Allegra 120mg"]
    },
]

# Add to patients.json
patients_path = os.path.join(BASE_DIR, 'patients.json')
try:
    with open(patients_path, 'r', encoding='utf-8') as f:
        patients = json.load(f)
except:
    patients = {}

users_path = os.path.join(BASE_DIR, 'users.json')
try:
    with open(users_path, 'r', encoding='utf-8') as f:
        users = json.load(f)
except:
    users = {}

for p in DEMO_PATIENTS:
    pid = p['id']
    patients[pid] = {
        "id": pid,
        "name": p['name'],
        "age": p['age'],
        "blood_group": p['blood_group'],
        "phone": p['phone'],
        "allergies": p['allergies'],
        "medical_history": p['conditions'],
        "current_conditions": p['conditions'],
        "qr_code": f"PATIENT_{pid}_QR",
        "insurance_provider": "Ayushman Bharat",
        "insurance_id": f"PMJAY{pid.upper()}"
    }
    if pid not in users:
        users[pid] = {
            "password": "demo123",
            "role": "patient",
            "name": p['name'],
            "type": "patient",
            "age": p['age'],
            "phone": p['phone'],
            "blood_group": p['blood_group'],
            "allergies": p['allergies'],
            "medical_history": p['conditions']
        }

with open(patients_path, 'w', encoding='utf-8') as f:
    json.dump(patients, f, indent=2, ensure_ascii=False)

with open(users_path, 'w', encoding='utf-8') as f:
    json.dump(users, f, indent=2, ensure_ascii=False)

print(f"✅ Added {len(DEMO_PATIENTS)} demo patients to patients.json and users.json")

# ── Generate HTML cards ──────────────────────────────────────────────────────
def qr_url(text):
    from urllib.parse import quote
    return f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={quote(text, safe='')}"

cards_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MediChain — Demo Patient QR Cards</title>
<style>
  body { font-family: Arial, sans-serif; background: #f0f4ff; padding: 20px; }
  h1 { text-align:center; color:#667eea; margin-bottom:30px; }
  .grid { display:grid; grid-template-columns: repeat(2, 1fr); gap:24px; max-width:900px; margin:0 auto; }
  .card {
    background:white; border-radius:16px; padding:20px;
    box-shadow:0 4px 16px rgba(0,0,0,0.1);
    border-top:5px solid #667eea;
    display:flex; gap:16px; align-items:flex-start;
    page-break-inside: avoid;
  }
  .qr-side img { border-radius:8px; border:2px solid #e5e7eb; }
  .info h2 { margin:0 0 4px; font-size:1.1rem; color:#1a1a2e; }
  .info .pid { font-size:0.75rem; color:#9ca3af; margin-bottom:8px; font-family:monospace; }
  .row { font-size:0.82rem; margin:3px 0; color:#374151; }
  .row strong { color:#1a1a2e; }
  .allergy { color:#dc2626; font-weight:700; }
  .meds { margin-top:8px; }
  .med-tag {
    display:inline-block; background:#ede9fe; color:#7c3aed;
    padding:2px 8px; border-radius:20px; font-size:0.72rem;
    margin:2px 2px 0 0;
  }
  .footer { text-align:center; margin-top:8px; font-size:0.7rem; color:#9ca3af; }
  .logo { text-align:center; font-weight:800; color:#667eea; font-size:0.9rem; margin-bottom:4px; }
  @media print {
    body { background:white; padding:0; }
    .grid { gap:12px; }
  }
</style>
</head>
<body>
<h1>🏥 MediChain — Demo Patient QR Cards</h1>
<p style="text-align:center;color:#6b7280;margin-bottom:24px;">
  Doctor scans these QR codes to instantly view patient details. Password for all demo patients: <strong>demo123</strong>
</p>
<div class="grid">
"""

for p in DEMO_PATIENTS:
    qr = qr_url(f"PATIENT_{p['id']}_QR")
    allergies_str = ', '.join(p['allergies'])
    conditions_str = ', '.join(p['conditions'])
    meds_tags = ''.join(f'<span class="med-tag">{m}</span>' for m in p['medicines'])

    cards_html += f"""
  <div class="card">
    <div class="qr-side">
      <div class="logo">MediChain</div>
      <img src="{qr}" width="150" height="150" alt="QR">
      <div class="footer">Scan to view record</div>
    </div>
    <div class="info">
      <h2>{p['name']}</h2>
      <div class="pid">ID: {p['id']}</div>
      <div class="row"><strong>Age:</strong> {p['age']} &nbsp;|&nbsp; <strong>Blood:</strong> {p['blood_group']}</div>
      <div class="row"><strong>Phone:</strong> {p['phone']}</div>
      <div class="row"><strong>Doctor:</strong> {p['doctor']}</div>
      <div class="row"><strong>Conditions:</strong> {conditions_str}</div>
      <div class="row allergy">⚠️ Allergies: {allergies_str}</div>
      <div class="meds"><strong style="font-size:0.78rem;">Current Medicines:</strong><br>{meds_tags}</div>
    </div>
  </div>
"""

cards_html += """
</div>
<p style="text-align:center;margin-top:30px;color:#9ca3af;font-size:0.8rem;">
  Generated by MediChain · For demo purposes only
</p>
</body>
</html>
"""

out_path = os.path.join(BASE_DIR, 'demo_qr_cards.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(cards_html)

print(f"✅ QR cards saved → demo_qr_cards.html")
print("   Open in browser → Ctrl+P to print or screenshot each card")
print()
print("Demo patient login credentials:")
for p in DEMO_PATIENTS:
    print(f"  {p['id']:12s} | {p['name']:20s} | password: demo123")
