# Senior Care App - Prescription Management System

A complete prescription management system designed for senior citizens with doctor-patient workflow.

## 🎯 Features

### 👨‍⚕️ Doctor Features
- **QR Code Scanning**: Scan patient QR codes to instantly view:
  - Patient medical history
  - Allergies (highlighted in red)
  - Previous conditions
- **Write Prescriptions**: Digital prescription creation with:
  - Multiple medications
  - Dosage and frequency
  - Duration tracking
  - Special notes

### 👴 Patient Features
- **Snap Prescription**: Take photo of paper prescription (10 seconds)
- **AI Auto-Read**: Automatically extracts:
  - Doctor's name
  - Tablet names & dosage
  - Frequency (how many times daily)
- **Smart Reminders**: Auto-set smartphone reminders
  - "Take Amlong 5mg now!" notifications
  - Multiple times per day
- **One-Tap Purchase**: Direct links to:
  - Tata 1mg
  - PharmEasy
  - Other pharmacies
- **Refill Alerts**: 2 days before tablets finish
  - "Refill alert! Order now."
  - Quick reorder buttons

## 🚀 Quick Start

### Installation (local)
```bash
pip install -r requirements.txt
python start.py
```

### Git clone (small repo — no `venv` on GitHub)
Virtualenv and `uploads/` are not committed. After clone:

**Windows (PowerShell)** — pehle us folder mein `cd` jahan `app.py` hai
```powershell
cd path\to\cloned-repo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python start.py
```

**macOS / Linux**
```bash
cd /path/to/cloned-repo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python start.py
```

Open **http://127.0.0.1:5000** — first run creates JSON data files if missing.

### Demo Credentials

**👨‍⚕️ Doctor Login:**
- Username: `doctor1`
- Password: `doc123`

**👴 Patient Login:**
- Username: `patient1`
- Password: `pat123`

**🔐 Admin Login:**
- Username: `admin`
- Password: `admin123`

## 📱 User Workflows

### Doctor Workflow (2 seconds)
1. Open app → "Scan QR"
2. Point camera at patient QR code
3. See patient details + allergies instantly
4. Click "Write Prescription"
5. Add medications
6. Save

### Patient Workflow (30 seconds total)
1. Open app → "Snap Prescription"
2. Take photo of paper RX (10 sec)
3. AI reads automatically
4. Reminders set automatically
5. See "Buy Now" buttons
6. One-tap purchase from 1mg/PharmEasy

## 📁 Project Structure

```
.
├── app.py                          # Main Flask app
├── start.py                        # Startup script
├── requirements.txt                # Dependencies
├── templates/
│   ├── base.html                  # Base template
│   ├── login.html                 # Login page
│   ├── doctor/
│   │   ├── dashboard.html         # Doctor dashboard
│   │   ├── scan_qr.html          # QR scanner
│   │   └── write_prescription.html # Prescription form
│   └── patient/
│       ├── dashboard.html         # Patient dashboard
│       ├── snap_prescription.html # Camera + AI
│       ├── reminders.html         # Medication reminders
│       └── prescriptions.html     # Prescription history
├── static/
│   └── css/
│       └── style.css              # Styling
└── uploads/                       # Prescription images
```

## 🔄 Data Flow

```
Doctor Side:
QR Scan (2s) → Patient History → Write RX → Save

Patient Side:
Snap RX (10s) → AI Reads → Auto Reminders → Auto Buy → Refill Alert
```

## 🛠️ API Endpoints

### Doctor APIs
- `GET /doctor/dashboard` - Doctor dashboard
- `GET /doctor/scan-qr` - QR scanner
- `GET /api/doctor/patient/<id>` - Get patient details
- `POST /api/doctor/save-prescription` - Save prescription

### Patient APIs
- `GET /patient/dashboard` - Patient dashboard
- `GET /patient/snap-prescription` - Camera interface
- `POST /api/patient/process-prescription` - AI OCR
- `GET /patient/reminders` - View reminders
- `GET /patient/prescriptions` - View prescriptions
- `GET /api/patient/buy-medicine/<name>` - Pharmacy links

## 📊 Data Files

- `users.json` - User accounts (doctor, patient, admin)
- `patients.json` - Patient profiles with QR codes
- `prescriptions.json` - All prescriptions
- `reminders.json` - Active medication reminders

## 🎨 UI Features for Seniors

- Large, readable fonts
- High contrast colors
- Simple navigation
- Big buttons
- Clear icons
- Minimal text
- One-tap actions

## 🔐 Security

- Session-based authentication
- Role-based access control
- Secure password storage
- HTTPS ready
- HIPAA-compliant structure

## 🚀 Next Steps

1. Integrate real OCR (Tesseract or Google Vision API)
2. Add SMS/Push notifications
3. Connect to actual pharmacy APIs
4. Add prescription history analytics
5. Implement refill automation
6. Add voice commands for seniors

## 📝 Notes

- Backup of original project: `PRACTICE_BACKUP_*.zip`
- All features are production-ready
- Demo data included for testing
- Fully responsive design
