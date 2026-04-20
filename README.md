<div align="center">

<img src="static/icons/icon-192.png" alt="MediChain Logo" width="100"/>

# 🔗 MediChain
### Blockchain-Secured Healthcare Management System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Blockchain](https://img.shields.io/badge/Blockchain-SHA--256-F7931A?style=for-the-badge&logo=bitcoin&logoColor=white)](https://en.wikipedia.org/wiki/SHA-2)
[![AES-256](https://img.shields.io/badge/Encryption-AES--256-00C853?style=for-the-badge&logo=letsencrypt&logoColor=white)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
[![PWA](https://img.shields.io/badge/PWA-Ready-5A0FC8?style=for-the-badge&logo=pwa&logoColor=white)](https://web.dev/progressive-web-apps/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

**The only open-source healthcare platform with blockchain-secured prescriptions + AES-256 encrypted one-time pharmacy dispensing.**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🔐 Security](#-security-architecture) • [📸 Screenshots](#-screenshots) • [🤝 Contributing](#-contributing)

</div>

---

## 🎯 The Problem

> **$300 billion** is lost annually in the US due to medication non-adherence.
> **125,000 Americans** die every year from missed medications.
> **13.8 million** people abuse prescription drugs — often reusing the same prescription at multiple pharmacies.

**No existing platform solves all three.** MediChain does.

---

## ✨ Features

### 🔗 Blockchain-Secured Prescriptions
- Every prescription is hashed with **SHA-256** and stored on a **custom private blockchain**
- Proof of Work implementation — tamper detection is **mathematically guaranteed**
- `is_chain_valid()` verifies integrity at any time — any modification = instant detection
- Each prescription gets a **unique blockchain QR code** for verification

### 🔐 AES-256 Encrypted Pharmacy Dispensing *(Industry First)*
- Doctor writes prescription → **Fernet AES-256 encryption** with pharmacy-specific key
- Patient receives an **encrypted QR** — unreadable without pharmacy credentials
- Pharmacy scans QR → decrypts with their unique key → dispenses medicines
- **One-time use** — dispensed prescriptions are permanently locked on blockchain
- Prevents prescription reuse, doctor shopping, and controlled substance abuse

### 💊 Dose-Level Medication Adherence Tracking
- Track **individual doses** — not just "taken/not taken"
- Per-dose, per-date `taken_log` — `{"2025-04-15": ["08:00", "20:00"]}`
- Real-time status: `pending` → `partial` → `taken`
- Visual progress bar + adherence percentage
- Logs to `adherence_tracking.json` for doctor/caregiver review

### 📱 Push Notifications (PWA)
- Service Worker checks due doses every **60 seconds**
- Browser push notifications — works on **mobile and desktop**
- Install as native app — no App Store needed (PWA)

### 🧪 Lab Report PDF Auto-Analysis
- Upload PDF lab reports → automatic text extraction via `pdfplumber`
- Regex-based value parsing for CBC, Blood Sugar, Thyroid, Lipid Profile, LFT, KFT
- Compares against normal ranges → flags **NORMAL / HIGH / LOW / CRITICAL**

### 🚨 Emergency SOS with GPS
- One-tap GPS capture via `navigator.geolocation`
- Instant alert to all emergency contacts + family members
- Timestamped log in `sos_alerts.json`

### 🏥 Pharmacy Portal (Integrated Role)
- Pharmacy is a **first-class login role** — not a separate app
- 3 scan methods: **Camera** | **QR Image Upload** | **Manual ID**
- Full dispensing history with audit trail
- Blockchain-logged every dispense event

### 👨‍⚕️ Telemedicine
- Book video consultations with doctors
- **Jitsi Meet** open-source integration — no API key needed
- Unique room per appointment: `medichain-{uuid4()}`

### 🔍 Drug Interaction Checker
- **80+ Indian medicines** local database — no external API
- Checks dangerous combinations (e.g., Aspirin + Warfarin = bleeding risk)
- Severity levels: LOW / MEDIUM / HIGH

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                       │
├─────────────────────────────────────────────────────────┤
│  Layer 1: SHA-256 Blockchain                            │
│  • Every prescription = immutable block                 │
│  • Proof of Work (difficulty=2)                         │
│  • Chain validation on every read                       │
├─────────────────────────────────────────────────────────┤
│  Layer 2: AES-256 Fernet Encryption                     │
│  • Pharmacy-specific key derivation                     │
│  • SHA-256(master_secret + pharmacy_id) → Fernet key    │
│  • Wrong key = InvalidToken exception                   │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Role-Based Access Control                     │
│  • @login_required + @role_required decorators          │
│  • 5 roles: doctor, patient, pharmacy, caregiver, admin │
│  • Zero-trust — every route independently verified      │
├─────────────────────────────────────────────────────────┤
│  Layer 4: One-Time Dispensing                           │
│  • dispensed: true flag + blockchain log                │
│  • Replay attack = 400 error                            │
│  • Immutable audit trail                                │
└─────────────────────────────────────────────────────────┘
```

### Live Security Demo
```bash
python demo_security.py
```
```
[3] HACKER attempts to change dose from 500mg to 5000mg...
    Chain Valid after tamper: ❌ False
    TAMPER DETECTED — blockchain rejected the change!

[5] FAKE PHARMACY tries to decrypt with wrong key...
    Result: ❌ DECRYPTION FAILED — InvalidToken

[6] SHA-256 Avalanche Effect:
    'Metformin 500mg' → 4c8e5eda2db7fa668bf3652dee498a1f...
    'Metformin 501mg' → db370428059f7314289aa2e45e6eb4ca...
    Characters different: 63/64 — COMPLETELY DIFFERENT!
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/memonaariz/MedichainAI.git
cd MedichainAI

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install flask cryptography pdfplumber Pillow

# Run
python app.py
```

Open **http://127.0.0.1:5000**

### Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| 👨‍⚕️ Doctor | `doctor1` | `doc123` |
| 🧑‍💼 Patient | `patient1` | `pat123` |
| 🏪 Pharmacy | `pharmacy1` | `pharma123` |
| 👩‍⚕️ Caregiver | `caregiver1` | `care123` |
| 🔐 Admin | `admin` | `admin123` |

---

## 📁 Project Structure

```
MedichainAI/
├── app.py                    # Flask backend — 2500+ lines, 50+ routes
├── blockchain.py             # Custom SHA-256 blockchain from scratch
├── drug_database_data.py     # 80+ medicines database
├── demo_security.py          # Live security demonstration script
│
├── templates/
│   ├── base.html             # Base layout + PWA + notifications
│   ├── doctor/               # Doctor dashboard, prescriptions, messages
│   ├── patient/              # Patient dashboard, reminders, lab reports
│   ├── pharmacy/             # Pharmacy dispensing portal
│   └── verify_prescription.html  # Public QR verification page
│
├── static/
│   ├── sw.js                 # Service Worker — offline + push notifications
│   ├── manifest.json         # PWA manifest
│   └── icons/                # App icons (192px, 512px)
│
└── *.json                    # Data files (users, patients, prescriptions...)
```

---

## 🔄 Complete Flow

```
DOCTOR                    PATIENT                   PHARMACY
  │                          │                          │
  ├─ Login                   ├─ Login                   ├─ Login (pharmacy1)
  ├─ Select patient          ├─ View prescriptions      ├─ Scan patient QR
  ├─ Write prescription      ├─ See blockchain QR       ├─ AES-256 decrypt
  │                          ├─ Get dose reminders      ├─ View full Rx
  ▼                          ├─ Mark doses taken        ├─ Confirm dispense
SHA-256 hash                 ├─ Upload lab reports      │
AES-256 encrypt              ├─ Emergency SOS           ▼
Blockchain log               └─ Telemedicine       Blockchain log
                                                   One-time locked
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.10 + Flask 2.3.3 |
| Blockchain | Custom SHA-256 (from scratch) |
| Encryption | AES-256 via `cryptography.fernet` |
| Frontend | HTML5 + CSS3 + Vanilla JS + Jinja2 |
| PDF Analysis | `pdfplumber` + Regex |
| Video Calls | Jitsi Meet (open-source) |
| QR Scanning | jsQR (browser-side) |
| Push Notifications | Service Worker API |
| Mobile | PWA (Progressive Web App) |
| Data | JSON flat files (SQLAlchemy-ready) |

---

## 📊 API Reference

<details>
<summary>Doctor APIs</summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/doctor/dashboard` | Doctor dashboard |
| GET | `/doctor/patients` | All registered patients |
| GET | `/doctor/write-prescription/<id>` | Write prescription form |
| POST | `/api/doctor/save-prescription` | Save + blockchain hash |
| GET | `/doctor/messages` | Patient messages |
| GET | `/doctor/telemedicine` | Video appointments |

</details>

<details>
<summary>Patient APIs</summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/patient/dashboard` | Patient dashboard |
| GET | `/patient/reminders` | Medication reminders |
| POST | `/api/patient/mark-taken` | Mark dose as taken |
| GET | `/api/patient/due-reminders` | Due doses (for notifications) |
| GET | `/patient/prescriptions` | View prescriptions |
| POST | `/api/patient/process-prescription` | OCR prescription image |
| POST | `/api/patient/save-manual-prescription` | Manual medicine entry |
| GET | `/patient/lab-reports` | Lab report analysis |
| POST | `/api/patient/upload-lab-report` | Upload + analyze PDF |
| POST | `/api/patient/trigger-sos` | Emergency SOS |
| GET | `/api/patient/buy-medicine/<name>` | Pharmacy comparison links |

</details>

<details>
<summary>Pharmacy APIs</summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/pharmacy/dashboard` | Pharmacy dispensing portal |
| POST | `/api/pharmacy/decrypt` | Decrypt prescription (AES-256) |
| POST | `/api/pharmacy/dispense` | One-time dispense + blockchain log |

</details>

<details>
<summary>Public APIs</summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/verify-prescription` | Public QR verification page |

</details>

---

## 🗺️ Roadmap

- [ ] bcrypt password hashing
- [ ] PostgreSQL database migration
- [ ] Real SMS alerts via Twilio
- [ ] Tesseract OCR for prescription images
- [ ] Per-pharmacy PKI key infrastructure
- [ ] ABDM (Ayushman Bharat Digital Mission) API integration
- [ ] Multi-language support (Hindi, Marathi, Tamil)
- [ ] Doctor NPI verification

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👥 Team

Built with ❤️ as a Major Project

| Member | Role |
|--------|------|
| Aariz Memon | Technical Lead — Blockchain, Backend, APIs |
| Samruddhi | Frontend — UI/UX, Templates |
| Anas | Database — Data Architecture, Testing |
| Parth | Research — Documentation, Integrations |

---

<div align="center">

**⭐ Star this repo if you find it useful!**

[![GitHub stars](https://img.shields.io/github/stars/memonaariz/MedichainAI?style=social)](https://github.com/memonaariz/MedichainAI/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/memonaariz/MedichainAI?style=social)](https://github.com/memonaariz/MedichainAI/network/forkers)

*MediChain — Because every prescription matters.*

</div>
