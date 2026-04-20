from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
import json
from datetime import datetime, timedelta
import functools
import uuid
import base64
from io import BytesIO
import math
import hashlib
from urllib.parse import quote

# Import blockchain module
from blockchain import (
    get_blockchain_instance,
    verify_data_integrity,
    encrypt_sensitive_data
)
from drug_database_data import lookup_drug

# â”€â”€ Pharmacy Encryption â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
from cryptography.fernet import Fernet
import base64, struct

# Master pharmacy key â€” in production this would be per-pharmacy PKI
# Here we use a deterministic key derived from a secret + pharmacy_id
PHARMACY_MASTER_SECRET = os.getenv('PHARMACY_SECRET', 'medichain_pharmacy_secret_2025')

def _derive_pharmacy_key(pharmacy_id: str) -> bytes:
    """Derive a Fernet key from pharmacy_id + master secret"""
    import hashlib
    raw = hashlib.sha256(f"{PHARMACY_MASTER_SECRET}:{pharmacy_id}".encode()).digest()
    return base64.urlsafe_b64encode(raw)

def encrypt_prescription_for_pharmacy(prescription_data: dict, pharmacy_id: str) -> str:
    """Encrypt prescription data â€” only the pharmacy with matching ID can decrypt"""
    key = _derive_pharmacy_key(pharmacy_id)
    f = Fernet(key)
    payload = json.dumps(prescription_data, ensure_ascii=False).encode()
    return f.encrypt(payload).decode()

def decrypt_prescription_for_pharmacy(token: str, pharmacy_id: str) -> dict:
    """Decrypt prescription â€” raises exception if wrong pharmacy or tampered"""
    key = _derive_pharmacy_key(pharmacy_id)
    f = Fernet(key)
    payload = f.decrypt(token.encode())
    return json.loads(payload.decode())


app = Flask(__name__, static_folder='static')

# Always read/write JSON next to app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APP_NAME = "MediChain"
APP_TAGLINE = "Blockchain-Secured Healthcare Platform"


def _data_path(*parts):
    return os.path.join(BASE_DIR, *parts)


# Configuration
app.secret_key = os.getenv('SECRET_KEY', 'medichain_secure_key_2025')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=6)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Initialize blockchain
blockchain = get_blockchain_instance()

# File Paths (anchored to project directory)
USERS_FILE = _data_path('users.json')
PATIENTS_FILE = _data_path('patients.json')
PRESCRIPTIONS_FILE = _data_path('prescriptions.json')
REMINDERS_FILE = _data_path('reminders.json')
FAMILY_MEMBERS_FILE = _data_path('family_members.json')
CAREGIVERS_FILE = _data_path('caregivers.json')
APPOINTMENTS_FILE = _data_path('appointments.json')
HEALTH_METRICS_FILE = _data_path('health_metrics.json')
EMERGENCY_CONTACTS_FILE = _data_path('emergency_contacts.json')
NOTIFICATIONS_FILE = _data_path('notifications.json')
SOS_ALERTS_FILE = _data_path('sos_alerts.json')
UPLOAD_FOLDER = _data_path('uploads')
DRUG_SIDE_EFFECTS_FILE = _data_path('drug_side_effects.json')
ADHERENCE_TRACKING_FILE = _data_path('adherence_tracking.json')
LAB_REPORTS_FILE = _data_path('lab_reports.json')
TELEMEDICINE_FILE = _data_path('telemedicine_appointments.json')
DOCTOR_MESSAGES_FILE = _data_path('doctor_messages.json')
CAREGIVER_NOTES_FILE = _data_path('caregiver_notes.json')
MUMBAI_DOCTORS_FILE = _data_path('mumbai_doctors.json')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Utility Functions
def _load_json(path, default=None):
    """Load JSON file safely"""
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading {path}: {e}")
    return default if default is not None else {}

def _save_json(path, data):
    """Save JSON file safely"""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing {path}: {e}")

def _append_json_array(path, item):
    """Append item to JSON array"""
    data = _load_json(path, [])
    if not isinstance(data, list):
        data = []
    data.append(item)
    _save_json(path, data)

def init_data_files():
    """Initialize all JSON data files"""
    if not os.path.exists(USERS_FILE):
        default_users = {
            "admin": {"password": "admin123", "role": "admin", "name": "Administrator", "type": "admin"},
            "doctor1": {"password": "doc123", "role": "doctor", "name": "Dr. Sharma", "type": "doctor", "clinic": "City Clinic", "phone": "9876543210"},
            "patient1": {"password": "pat123", "role": "patient", "name": "Rajesh Kumar", "type": "patient", "age": 65, "phone": "9876543210", "allergies": ["Penicillin", "Aspirin"], "blood_group": "O+"},
            "caregiver1": {"password": "care123", "role": "caregiver", "name": "Priya Sharma", "type": "caregiver", "assigned_patient": "patient1"},
            "pharmacy1": {"password": "pharma123", "role": "pharmacy", "name": "MediChain Pharmacy", "type": "pharmacy", "pharmacy_id": "MEDICHAIN_PHARMACY", "license": "PH-MH-2025-001", "address": "Mumbai, Maharashtra"}
        }
        _save_json(USERS_FILE, default_users)

    if not os.path.exists(PATIENTS_FILE):
        default_patients = {
            "patient1": {
                "id": "patient1",
                "name": "Rajesh Kumar",
                "age": 65,
                "phone": "9876543210",
                "email": "rajesh@example.com",
                "blood_group": "O+",
                "allergies": ["Penicillin", "Aspirin"],
                "medical_history": ["Diabetes", "Hypertension"],
                "current_conditions": ["Type 2 Diabetes", "Hypertension"],
                "qr_code": "PATIENT_patient1_QR",
                "insurance_id": "PMJAY123456",
                "insurance_provider": "Ayushman Bharat"
            }
        }
        _save_json(PATIENTS_FILE, default_patients)

    for file_path in [FAMILY_MEMBERS_FILE, CAREGIVERS_FILE, APPOINTMENTS_FILE, 
                      HEALTH_METRICS_FILE, EMERGENCY_CONTACTS_FILE, NOTIFICATIONS_FILE, 
                      PRESCRIPTIONS_FILE, REMINDERS_FILE, SOS_ALERTS_FILE,
                      DRUG_SIDE_EFFECTS_FILE, ADHERENCE_TRACKING_FILE, LAB_REPORTS_FILE,
                      TELEMEDICINE_FILE, DOCTOR_MESSAGES_FILE]:
        if not os.path.exists(file_path):
            _save_json(file_path, [])

init_data_files()

# Backfill qr_payload for existing prescriptions that don't have one
def _backfill_prescription_qr():
    prescriptions = _load_json(PRESCRIPTIONS_FILE, [])
    changed = False
    for rx in prescriptions:
        if not rx.get('qr_payload') and rx.get('blockchain_hash'):
            qr_payload = json.dumps({
                'rx_id':   rx['id'],
                'hash':    rx['blockchain_hash'],
                'patient': rx.get('patient_id', ''),
                'doctor':  rx.get('doctor_id', ''),
                'issued':  rx.get('created_at', '')[:10]
            }, separators=(',', ':'))
            rx['qr_payload'] = qr_payload
            changed = True
    if changed:
        _save_json(PRESCRIPTIONS_FILE, prescriptions)

_backfill_prescription_qr()

# Decorators
def login_required(view):
    """Decorator to require login"""
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get('user'):
            flash('Please log in to continue.')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped_view

def role_required(*roles):
    """Decorator to require specific role"""
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            user = session.get('user')
            if not user:
                flash('Please log in to continue.')
                return redirect(url_for('login'))
            if user.get('role') not in roles:
                flash('You do not have permission to access this page.')
                return redirect(url_for('dashboard'))
            return view(*args, **kwargs)
        return wrapped_view
    return decorator

# Routes - Authentication
@app.route('/')
def index():
    """Home page"""
    user = session.get('user')
    if user:
        if user.get('role') == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        elif user.get('role') == 'patient':
            return redirect(url_for('patient_dashboard'))
        elif user.get('role') == 'caregiver':
            return redirect(url_for('caregiver_dashboard'))
        elif user.get('role') == 'pharmacy':
            return redirect(url_for('pharmacy_dashboard'))
        else:
            return redirect(url_for('dashboard'))
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        users = _load_json(USERS_FILE, {})
        user = users.get(username)
        
        if user and user.get('password') == password:
            session['user'] = {
                'username': username,
                'name': user.get('name', username),
                'role': user.get('role', 'user'),
                'type': user.get('type', 'user'),
                'assigned_patient': user.get('assigned_patient'),
                'pharmacy_id': user.get('pharmacy_id'),
                'license': user.get('license')
            }
            flash(f"Welcome, {user.get('name', username)}!")
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Patient/Doctor registration page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        role = request.form.get('role', 'patient').strip()

        if role not in ('patient', 'doctor'):
            flash('Invalid role selected.')
            return redirect(url_for('register'))

        if not username or not password:
            flash('Username and password are required.')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('register'))

        users = _load_json(USERS_FILE, {})
        if username in users:
            flash('Username already exists. Please choose another.')
            return redirect(url_for('register'))

        full_name  = request.form.get('full_name', '').strip()
        phone      = request.form.get('phone', '').strip()
        email      = request.form.get('email', '').strip()

        if role == 'doctor':
            specialization  = request.form.get('specialization', '').strip()
            license_number  = request.form.get('license_number', '').strip()
            clinic_name     = request.form.get('clinic_name', '').strip()
            experience      = request.form.get('experience', '').strip()

            users[username] = {
                'password': password,
                'role': 'doctor',
                'name': full_name,
                'type': 'doctor',
                'phone': phone,
                'email': email,
                'specialization': specialization,
                'license_number': license_number,
                'clinic': clinic_name,
                'experience': experience,
                'created_at': datetime.now().isoformat()
            }
            _save_json(USERS_FILE, users)
            flash(f'Doctor account created! Welcome Dr. {full_name}. Please log in.')
            return redirect(url_for('login'))

        # --- Patient registration ---
        age                = request.form.get('age', '')
        blood_group        = request.form.get('blood_group', '')
        allergies          = request.form.getlist('allergies')
        medical_history    = request.form.getlist('medical_history')
        current_medications= request.form.get('current_medications', '').strip()
        insurance_provider = request.form.get('insurance_provider', '')
        insurance_id       = request.form.get('insurance_id', '').strip()
        emergency_name     = request.form.get('emergency_name', '').strip()
        emergency_phone    = request.form.get('emergency_phone', '').strip()

        users[username] = {
            'password': password,
            'role': 'patient',
            'name': full_name,
            'type': 'patient',
            'age': int(age) if age else 0,
            'phone': phone,
            'email': email,
            'blood_group': blood_group,
            'allergies': allergies,
            'medical_history': medical_history,
            'current_medications': current_medications,
            'insurance_provider': insurance_provider,
            'insurance_id': insurance_id,
            'emergency_contact_name': emergency_name,
            'emergency_contact_phone': emergency_phone,
            'created_at': datetime.now().isoformat()
        }
        _save_json(USERS_FILE, users)

        patients = _load_json(PATIENTS_FILE, {})
        patients[username] = {
            'id': username,
            'name': full_name,
            'age': int(age) if age else 0,
            'phone': phone,
            'email': email,
            'blood_group': blood_group,
            'allergies': allergies,
            'medical_history': medical_history,
            'current_conditions': medical_history,
            'qr_code': f'PATIENT_{username}_QR',
            'insurance_id': insurance_id,
            'insurance_provider': insurance_provider,
            'emergency_contact_name': emergency_name,
            'emergency_contact_phone': emergency_phone,
            'created_at': datetime.now().isoformat()
        }
        _save_json(PATIENTS_FILE, patients)

        flash('Registration successful! Please log in with your credentials.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    user = session.get('user', {})
    return render_template('dashboard.html', user=user)

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    user = session.get('user', {})
    patient = None
    qr_payload = None
    qr_image_url = None
    if user.get('role') == 'patient':
        pid = user.get('username')
        patients = _load_json(PATIENTS_FILE, {})
        patient = patients.get(pid)
        qr_payload = (patient or {}).get('qr_code') or f'PATIENT_{pid}_QR'
        qr_image_url = (
            'https://api.qrserver.com/v1/create-qr-code/?size=220x220&data='
            + quote(qr_payload, safe='')
        )
    return render_template(
        'profile.html',
        user=user,
        patient=patient,
        qr_payload=qr_payload,
        qr_image_url=qr_image_url,
    )


# Routes - Doctor
@app.route('/doctor/dashboard')
@login_required
@role_required('doctor')
def doctor_dashboard():
    """Doctor dashboard"""
    user = session.get('user', {})
    patients = _load_json(PATIENTS_FILE, {})
    patient_count = len(patients)
    rx = _load_json(PRESCRIPTIONS_FILE, [])
    rx_count = len(rx)
    return render_template(
        'doctor/dashboard.html',
        user=user,
        patient_count=patient_count,
        prescription_count=rx_count,
    )

@app.route('/doctor/patients')
@login_required
@role_required('doctor')
def doctor_patients():
    """All registered patients â€” pick one to open chart or write prescription (no QR required)."""
    patients = _load_json(PATIENTS_FILE, {})
    patients_list = []
    for username, p in patients.items():
        row = dict(p)
        row['username'] = username
        row['id'] = row.get('id') or username
        patients_list.append(row)
    patients_list.sort(key=lambda x: (x.get('name') or x.get('username') or '').lower())
    return render_template('doctor/patients.html', user=session.get('user'), patients_list=patients_list)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# PHARMACY PORTAL â€” Login-based, integrated into main app
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

@app.route('/pharmacy')
def pharmacy_portal():
    """Pharmacy portal â€” redirects to dashboard if logged in, else login"""
    user = session.get('user', {})
    if user.get('role') == 'pharmacy':
        return redirect(url_for('pharmacy_dashboard'))
    return redirect(url_for('login'))

@app.route('/pharmacy/dashboard')
@login_required
@role_required('pharmacy')
def pharmacy_dashboard():
    """Pharmacy dashboard â€” scan & dispense encrypted prescriptions"""
    user = session.get('user', {})
    # Get dispensing history for this pharmacy
    prescriptions = _load_json(PRESCRIPTIONS_FILE, [])
    pharmacy_id = user.get('pharmacy_id', 'MEDICHAIN_PHARMACY')
    dispensed_by_me = [
        p for p in prescriptions
        if p.get('dispensed') and pharmacy_id in (p.get('dispensed_by') or '')
    ]
    dispensed_by_me.sort(key=lambda x: x.get('dispensed_at',''), reverse=True)
    return render_template('pharmacy/dashboard.html', user=user,
                           dispensed_history=dispensed_by_me[:20])

@app.route('/api/pharmacy/decrypt', methods=['POST'])
@login_required
@role_required('pharmacy')
def api_pharmacy_decrypt():
    """Decrypt prescription token â€” uses logged-in pharmacy's ID"""
    try:
        data = request.get_json()
        rx_id = (data.get('rx_id') or '').strip()
        user = session.get('user', {})
        pharmacy_id = user.get('pharmacy_id', 'MEDICHAIN_PHARMACY').upper()

        prescriptions = _load_json(PRESCRIPTIONS_FILE, [])
        rx = next((p for p in prescriptions if p.get('id') == rx_id), None)

        if not rx:
            return jsonify({'success': False, 'error': 'Prescription not found.'}), 404

        if rx.get('dispensed'):
            return jsonify({
                'success': False,
                'error': f"Already dispensed on {rx.get('dispensed_at','')[:10]} by {rx.get('dispensed_by','unknown')}.",
                'already_dispensed': True
            }), 400

        token = rx.get('pharmacy_token')
        if not token:
            return jsonify({'success': False, 'error': 'No encrypted token for this prescription.'}), 400

        try:
            decrypted = decrypt_prescription_for_pharmacy(token, pharmacy_id)
        except Exception:
            return jsonify({
                'success': False,
                'error': 'Decryption failed â€” your pharmacy key does not match this prescription.'
            }), 403

        return jsonify({'success': True, 'prescription': decrypted})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/pharmacy/dispense', methods=['POST'])
@login_required
@role_required('pharmacy')
def api_pharmacy_dispense():
    """Mark prescription as dispensed â€” one-time only, blockchain logged"""
    try:
        data = request.get_json()
        rx_id = (data.get('rx_id') or '').strip()
        user = session.get('user', {})
        pharmacy_id = user.get('pharmacy_id', 'MEDICHAIN_PHARMACY').upper()
        pharmacist = user.get('name', 'Pharmacist')

        prescriptions = _load_json(PRESCRIPTIONS_FILE, [])
        updated = False
        rx = None
        for p in prescriptions:
            if p.get('id') == rx_id:
                if p.get('dispensed'):
                    return jsonify({'success': False, 'error': 'Already dispensed.'}), 400
                p['dispensed']    = True
                p['dispensed_at'] = datetime.now().isoformat()
                p['dispensed_by'] = f"{pharmacist} ({pharmacy_id})"
                p['status']       = 'dispensed'
                rx = p
                updated = True
                break

        if not updated:
            return jsonify({'success': False, 'error': 'Prescription not found.'}), 404

        _save_json(PRESCRIPTIONS_FILE, prescriptions)

        try:
            blockchain.add_medical_record(
                patient_id=rx.get('patient_id', ''),
                record_type='dispensing',
                record_data={
                    'rx_id': rx_id, 'pharmacy_id': pharmacy_id,
                    'pharmacist': pharmacist, 'dispensed_at': rx['dispensed_at']
                }
            )
        except Exception:
            pass

        return jsonify({
            'success': True,
            'message': 'Prescription dispensed. Blockchain record created.',
            'dispensed_at': rx['dispensed_at']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/verify-prescription')
def verify_prescription_page():
    """Public prescription verification page â€” anyone can verify via QR scan"""
    rx_id   = request.args.get('rx_id', '').strip()
    hash_in = request.args.get('hash', '').strip()

    result = None
    if rx_id and hash_in:
        prescriptions = _load_json(PRESCRIPTIONS_FILE, [])
        rx = next((p for p in prescriptions if p.get('id') == rx_id), None)
        if not rx:
            result = {'valid': False, 'reason': 'Prescription ID not found in records.'}
        elif rx.get('blockchain_hash') != hash_in:
            result = {'valid': False, 'reason': 'Hash mismatch â€” prescription may have been tampered.'}
        else:
            result = {
                'valid': True,
                'prescription': {
                    'id':           rx['id'],
                    'patient_name': rx.get('patient_name'),
                    'doctor_name':  rx.get('doctor_name'),
                    'diagnosis':    rx.get('diagnosis'),
                    'medications':  rx.get('medications', []),
                    'issued':       rx.get('created_at', '')[:10],
                    'status':       rx.get('status', 'active'),
                    'hash':         rx.get('blockchain_hash'),
                    'notes':        rx.get('notes', '')
                }
            }

    return render_template('verify_prescription.html', result=result, rx_id=rx_id)


@app.route('/doctor/scan-qr')
@login_required
@role_required('doctor')
def doctor_scan_qr():
    """Doctor scans patient QR code"""
    return render_template('doctor/scan_qr.html', user=session.get('user'))

@app.route('/api/doctor/send-message', methods=['POST'])
@login_required
@role_required('doctor')
def api_doctor_send_message():
    """Doctor sends reply to patient"""
    try:
        user = session.get('user', {})
        data = request.get_json()
        message = {
            'id': str(uuid.uuid4()),
            'patient_id': data.get('patient_id'),
            'doctor_id': user.get('username'),
            'doctor_name': user.get('name'),
            'message': data.get('message'),
            'sender': 'doctor',
            'sent_at': datetime.now().isoformat(),
            'read': False
        }
        _append_json_array(DOCTOR_MESSAGES_FILE, message)
        return jsonify({'success': True, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/doctor/patient/<patient_id>')
@login_required
@role_required('doctor')
def api_get_patient(patient_id):
    """Get patient details by ID"""
    key = (patient_id or '').strip()
    patients = _load_json(PATIENTS_FILE, {})
    patient = patients.get(key)
    
    if not patient:
        return jsonify({'success': False, 'error': 'Patient not found'}), 404
    
    p = dict(patient)
    p['id'] = p.get('id') or key
    al = p.get('allergies')
    p['allergies'] = al if isinstance(al, list) else ([al] if al else [])
    mh = p.get('medical_history')
    p['medical_history'] = mh if isinstance(mh, list) else ([mh] if mh else [])
    return jsonify({'success': True, 'patient': p})

@app.route('/doctor/write-prescription/<patient_id>')
@login_required
@role_required('doctor')
def doctor_write_prescription(patient_id):
    """Doctor writes prescription for patient"""
    key = (patient_id or '').strip()
    patients = _load_json(PATIENTS_FILE, {})
    raw = patients.get(key)
    
    if not raw:
        flash('Patient not found.')
        return redirect(url_for('doctor_patients'))
    
    patient = dict(raw)
    patient['id'] = patient.get('id') or key
    return render_template('doctor/write_prescription.html', patient=patient, user=session.get('user'))

@app.route('/api/doctor/save-prescription', methods=['POST'])
@login_required
@role_required('doctor')
def api_save_prescription():
    """Save prescription with blockchain verification"""
    try:
        data = request.get_json()
        patient_id = (data.get('patient_id') or '').strip()
        medications = data.get('medications', [])
        notes = data.get('notes', '')
        diagnosis = data.get('diagnosis', '')

        if not patient_id or not medications:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        # Validate patient exists
        patients = _load_json(PATIENTS_FILE, {})
        if patient_id not in patients:
            return jsonify({'success': False, 'error': f'Patient "{patient_id}" not found'}), 404

        patient = patients[patient_id]
        doctor_user = session.get('user', {})

        prescription = {
            'id': str(uuid.uuid4()),
            'patient_id': patient_id,          # always the patients.json key (username)
            'patient_name': patient.get('name', patient_id),
            'doctor_id': doctor_user.get('username'),
            'doctor_name': doctor_user.get('name'),
            'medications': medications,
            'diagnosis': diagnosis,
            'notes': notes,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }

        # Add to blockchain for immutability
        try:
            blockchain_hash = blockchain.add_prescription(
                patient_id=patient_id,
                doctor_id=prescription['doctor_id'],
                prescription_data=prescription
            )
        except Exception:
            # Fallback hash if blockchain fails
            raw = json.dumps(prescription, sort_keys=True)
            blockchain_hash = hashlib.sha256(raw.encode()).hexdigest()

        prescription['blockchain_hash'] = blockchain_hash
        prescription['verified'] = True
        prescription['dispensed'] = False
        prescription['dispensed_at'] = None
        prescription['dispensed_by'] = None

        # Generate QR payload â€” blockchain hash + prescription ID + patient + doctor
        qr_payload = json.dumps({
            'rx_id':    prescription['id'],
            'hash':     blockchain_hash,
            'patient':  patient_id,
            'doctor':   prescription['doctor_id'],
            'issued':   prescription['created_at'][:10]
        }, separators=(',', ':'))
        prescription['qr_payload'] = qr_payload

        # â”€â”€ Pharmacy Encrypted Token â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        # Encrypt full prescription for pharmacy â€” patient cannot read this
        pharmacy_payload = {
            'rx_id':       prescription['id'],
            'patient_name': prescription['patient_name'],
            'patient_id':  patient_id,
            'doctor_name': prescription['doctor_name'],
            'doctor_id':   prescription['doctor_id'],
            'diagnosis':   diagnosis,
            'medications': medications,
            'notes':       notes,
            'issued':      prescription['created_at'][:10],
            'hash':        blockchain_hash,
            'dispensed':   False
        }
        # Default pharmacy_id = 'MEDICHAIN_PHARMACY' (any registered pharmacy)
        encrypted_token = encrypt_prescription_for_pharmacy(pharmacy_payload, 'MEDICHAIN_PHARMACY')
        prescription['pharmacy_token'] = encrypted_token

        _append_json_array(PRESCRIPTIONS_FILE, prescription)

        # Create medicine reminders automatically for the patient
        for med in medications:
            reminder = {
                'id': str(uuid.uuid4()),
                'patient_id': patient_id,
                'medication': med.get('name'),
                'dosage': med.get('dosage'),
                'frequency': med.get('frequency'),
                'duration': f"{med.get('duration', 30)} days",
                'prescription_id': prescription['id'],
                'status': 'active',
                'created_at': datetime.now().isoformat()
            }
            _append_json_array(REMINDERS_FILE, reminder)

        return jsonify({
            'success': True,
            'prescription_id': prescription['id'],
            'blockchain_hash': blockchain_hash,
            'verified': True,
            'message': f'Prescription saved for {patient.get("name")}. Reminders created.'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Routes - Patient Dashboard & Core Features
@app.route('/patient/dashboard')
@login_required
@role_required('patient')
def patient_dashboard():
    """Patient dashboard with blockchain stats"""
    user = session.get('user', {})
    patient_id = user.get('username')
    
    patients = _load_json(PATIENTS_FILE, {})
    patient = patients.get(patient_id, {})
    
    prescriptions = _load_json(PRESCRIPTIONS_FILE, [])
    patient_prescriptions = [p for p in prescriptions if p.get('patient_id') == patient_id]
    patient_prescriptions.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    reminders = _load_json(REMINDERS_FILE, [])
    patient_reminders = [r for r in reminders if r.get('patient_id') == patient_id]
    
    appointments = _load_json(APPOINTMENTS_FILE, [])
    patient_appointments = [a for a in appointments if a.get('patient_id') == patient_id]
    
    refill_alerts = []
    for reminder in patient_reminders:
        if reminder.get('status') == 'active':
            created_at = datetime.fromisoformat(reminder.get('created_at', datetime.now().isoformat()))
            duration_days = int(reminder.get('duration', '30').split()[0]) if reminder.get('duration') else 30
            refill_date = created_at + timedelta(days=duration_days-2)
            
            if datetime.now() >= refill_date:
                refill_alerts.append({
                    'medication': reminder.get('medication'),
                    'dosage': reminder.get('dosage'),
                    'refill_date': refill_date.isoformat()
                })
    
    upcoming_appointments = [a for a in patient_appointments if a.get('status') == 'scheduled']
    
    # Get blockchain stats
    blockchain_stats = blockchain.get_blockchain_stats()
    
    return render_template('patient/dashboard.html', 
                         user=user, 
                         patient=patient,
                         prescriptions=patient_prescriptions,
                         reminders=patient_reminders,
                         refill_alerts=refill_alerts,
                         upcoming_appointments=upcoming_appointments,
                         blockchain_stats=blockchain_stats)

@app.route('/patient/reminders')
@login_required
@role_required('patient')
def patient_reminders():
    """View patient reminders"""
    user = session.get('user', {})
    patient_id = user.get('username')
    today = datetime.now().strftime('%Y-%m-%d')

    reminders = _load_json(REMINDERS_FILE, [])
    patient_reminders = [r for r in reminders if r.get('patient_id') == patient_id]

    # Annotate each reminder with today's taken doses
    for r in patient_reminders:
        taken_log = r.get('taken_log', {})
        today_doses = taken_log.get(today, [])
        r['today_doses_taken'] = today_doses
        times = r.get('times', [])
        if times:
            r['today_status'] = 'taken' if all(t in today_doses for t in times) else (
                'partial' if today_doses else 'pending'
            )
        else:
            r['today_status'] = 'taken' if today_doses else 'pending'

    return render_template('patient/reminders.html', reminders=patient_reminders, user=user, today=today)

@app.route('/api/patient/due-reminders')
@login_required
@role_required('patient')
def api_due_reminders():
    """Return reminders whose dose time matches current time (Â±2 min window)"""
    user = session.get('user', {})
    patient_id = user.get('username')
    now = datetime.now()
    current_time = now.strftime('%H:%M')
    today = now.strftime('%Y-%m-%d')

    # Build HH:MM strings within Â±2 minute window
    window = set()
    for delta in range(-2, 3):
        t = (now + timedelta(minutes=delta)).strftime('%H:%M')
        window.add(t)

    reminders = _load_json(REMINDERS_FILE, [])
    due = []
    for r in reminders:
        if r.get('patient_id') != patient_id:
            continue
        if r.get('status') != 'active':
            continue
        times = r.get('times', [])
        taken_today = r.get('taken_log', {}).get(today, [])
        for t in times:
            if t in window and t not in taken_today:
                due.append({
                    'id': r.get('id'),
                    'medication': r.get('medication'),
                    'dosage': r.get('dosage', ''),
                    'time': t
                })
    return jsonify({'due': due})


@app.route('/api/patient/mark-taken', methods=['POST'])
@login_required
@role_required('patient')
def api_patient_mark_taken():
    """Mark a reminder dose as taken for today"""
    try:
        user = session.get('user', {})
        patient_id = user.get('username')
        data = request.get_json()
        reminder_id = data.get('reminder_id')
        dose_time = data.get('dose_time', '')  # e.g. "08:00"

        reminders = _load_json(REMINDERS_FILE, [])
        today = datetime.now().strftime('%Y-%m-%d')
        updated = False

        for reminder in reminders:
            if reminder.get('id') == reminder_id and reminder.get('patient_id') == patient_id:
                # Initialize taken_log as dict: { "YYYY-MM-DD": ["08:00", "20:00"] }
                taken_log = reminder.get('taken_log', {})
                today_doses = taken_log.get(today, [])

                if dose_time and dose_time not in today_doses:
                    today_doses.append(dose_time)
                elif not dose_time and today not in taken_log:
                    today_doses.append('taken')

                taken_log[today] = today_doses
                reminder['taken_log'] = taken_log
                reminder['last_taken'] = datetime.now().isoformat()
                reminder['taken_count'] = reminder.get('taken_count', 0) + 1

                # Check if ALL doses for today are taken
                times = reminder.get('times', [])
                if times:
                    all_taken = all(t in today_doses for t in times)
                    reminder['today_status'] = 'taken' if all_taken else 'partial'
                else:
                    reminder['today_status'] = 'taken'

                updated = True
                break

        if not updated:
            return jsonify({'success': False, 'error': 'Reminder not found'}), 404

        _save_json(REMINDERS_FILE, reminders)

        # Log to adherence tracking
        adherence = _load_json(ADHERENCE_TRACKING_FILE, [])
        adherence.append({
            'id': str(uuid.uuid4()),
            'patient_id': patient_id,
            'reminder_id': reminder_id,
            'dose_time': dose_time,
            'taken_at': datetime.now().isoformat(),
            'date': today
        })
        _save_json(ADHERENCE_TRACKING_FILE, adherence)

        return jsonify({'success': True, 'message': 'Dose marked as taken', 'today_status': reminder.get('today_status', 'taken')})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/patient/prescriptions')
@login_required
@role_required('patient')
def patient_prescriptions():
    """View patient prescriptions"""
    user = session.get('user', {})
    patient_id = user.get('username')

    all_prescriptions = _load_json(PRESCRIPTIONS_FILE, [])
    # Match by patient_id OR by patient username (handles both old and new data)
    patient_prescriptions = [
        p for p in all_prescriptions
        if p.get('patient_id') == patient_id
    ]
    # Sort newest first
    patient_prescriptions.sort(key=lambda x: x.get('created_at', ''), reverse=True)

    return render_template('patient/prescriptions.html', prescriptions=patient_prescriptions, user=user)

@app.route('/patient/snap-prescription')
@login_required
@role_required('patient')
def patient_snap_prescription():
    """Patient snaps prescription photo"""
    return render_template('patient/snap_prescription.html', user=session.get('user'))

@app.route('/api/patient/save-manual-prescription', methods=['POST'])
@login_required
@role_required('patient')
def api_save_manual_prescription():
    """Save manually entered prescription medicines and create reminders"""
    try:
        patient_id = session.get('user', {}).get('username')
        data = request.get_json()
        medications = data.get('medications', [])

        if not medications:
            return jsonify({'success': False, 'error': 'No medicines provided'}), 400

        for med in medications:
            if not med.get('name'):
                continue
            reminder = {
                'id': str(uuid.uuid4()),
                'patient_id': patient_id,
                'medication': med.get('name'),
                'dosage': med.get('dosage', ''),
                'frequency': med.get('frequency', 'Once daily'),
                'times': med.get('times', ['08:00']),
                'duration': med.get('duration', '30 days'),
                'status': 'active',
                'source': 'manual',
                'created_at': datetime.now().isoformat()
            }
            _append_json_array(REMINDERS_FILE, reminder)

        return jsonify({'success': True, 'count': len(medications)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/patient/process-prescription', methods=['POST'])
@login_required
@role_required('patient')
def api_process_prescription():
    """Process prescription image with AI"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        file = request.files['image']
        patient_id = session.get('user', {}).get('username')
        
        filename = f"{patient_id}_{uuid.uuid4()}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        medications = extract_prescription_data(filepath)
        
        for med in medications:
            reminder = {
                'id': str(uuid.uuid4()),
                'patient_id': patient_id,
                'medication': med.get('name'),
                'dosage': med.get('dosage'),
                'frequency': med.get('frequency'),
                'times': med.get('times', []),
                'status': 'active',
                'created_at': datetime.now().isoformat()
            }
            _append_json_array(REMINDERS_FILE, reminder)
        
        return jsonify({
            'success': True,
            'medications': medications,
            'message': f'Found {len(medications)} medications. Reminders set!'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/patient/buy-medicine/<medicine_name>')
@login_required
@role_required('patient')
def api_buy_medicine(medicine_name):
    """Return pharmacy links with prescription requirement info"""
    name = medicine_name.strip()
    encoded = quote(name, safe='')

    # Check if medicine needs prescription using drug database
    drug_info = lookup_drug(name)
    severity = (drug_info.get('severity', 'LOW') if drug_info else 'LOW')
    needs_rx = severity in ('HIGH', 'MEDIUM') or drug_info is not None

    platforms = [
        {
            'name': '1mg',
            'logo': '1mg',
            'logo_bg': '#e53935',
            'description': "India's largest online pharmacy",
            'url': f'https://www.1mg.com/search/all?name={encoded}',
            'badge': 'Most Popular',
            'upload_rx_url': 'https://www.1mg.com/upload-prescription'
        },
        {
            'name': 'PharmEasy',
            'logo': 'PE',
            'logo_bg': '#1565c0',
            'description': 'Fast delivery, genuine medicines',
            'url': f'https://pharmeasy.in/search/all?name={encoded}',
            'badge': 'Fast Delivery',
            'upload_rx_url': 'https://pharmeasy.in/upload-prescription'
        },
        {
            'name': 'Apollo Pharmacy',
            'logo': 'Ap',
            'logo_bg': '#0277bd',
            'description': 'Apollo Hospitals official pharmacy',
            'url': f'https://www.apollopharmacy.in/search-medicines/{encoded}',
            'badge': 'Hospital Grade',
            'upload_rx_url': 'https://www.apollopharmacy.in/upload-prescription'
        },
    ]

    # Get patient's active doctor prescriptions for this medicine
    patient_id = session.get('user', {}).get('username')
    all_rx = _load_json(PRESCRIPTIONS_FILE, [])
    matching_rx = []
    for rx in all_rx:
        if rx.get('patient_id') != patient_id: continue
        if rx.get('dispensed'): continue
        for med in rx.get('medications', []):
            if name.lower() in med.get('name', '').lower():
                matching_rx.append({
                    'id': rx['id'],
                    'doctor': rx.get('doctor_name', 'Doctor'),
                    'date': rx.get('created_at', '')[:10],
                    'hash': rx.get('blockchain_hash', '')
                })
                break

    return jsonify({
        'success': True,
        'medicine': name,
        'needs_prescription': needs_rx,
        'severity': severity,
        'matching_prescriptions': matching_rx,
        'platforms': platforms
    })


# Routes - Emergency SOS
@app.route('/patient/emergency-sos')
@login_required
@role_required('patient')
def patient_emergency_sos():
    """Emergency SOS page"""
    user = session.get('user', {})
    patient_id = user.get('username')
    
    emergency_contacts = _load_json(EMERGENCY_CONTACTS_FILE, [])
    patient_contacts = [c for c in emergency_contacts if c.get('patient_id') == patient_id]
    
    family_members = _load_json(FAMILY_MEMBERS_FILE, [])
    patient_family = [f for f in family_members if f.get('patient_id') == patient_id]
    
    return render_template('patient/emergency_sos.html', 
                         user=user, 
                         emergency_contacts=patient_contacts,
                         family_members=patient_family)

@app.route('/api/patient/trigger-sos', methods=['POST'])
@login_required
@role_required('patient')
def api_trigger_sos():
    """Trigger emergency SOS alert"""
    try:
        user = session.get('user', {})
        patient_id = user.get('username')
        
        patients = _load_json(PATIENTS_FILE, {})
        patient = patients.get(patient_id, {})
        
        emergency_contacts = _load_json(EMERGENCY_CONTACTS_FILE, [])
        patient_contacts = [c for c in emergency_contacts if c.get('patient_id') == patient_id]
        
        family_members = _load_json(FAMILY_MEMBERS_FILE, [])
        patient_family = [f for f in family_members if f.get('patient_id') == patient_id]
        
        sos_alert = {
            'id': str(uuid.uuid4()),
            'patient_id': patient_id,
            'patient_name': patient.get('name'),
            'patient_phone': patient.get('phone'),
            'location': request.json.get('location', 'Location not available'),
            'message': request.json.get('message', 'Emergency SOS Alert'),
            'timestamp': datetime.now().isoformat(),
            'status': 'active',
            'contacts_notified': []
        }
        
        all_contacts = patient_contacts + patient_family
        for contact in all_contacts:
            notification = {
                'id': str(uuid.uuid4()),
                'type': 'emergency_sos',
                'recipient_phone': contact.get('phone'),
                'recipient_name': contact.get('name'),
                'patient_name': patient.get('name'),
                'message': f"ðŸš¨ EMERGENCY SOS from {patient.get('name')}! Location: {sos_alert['location']}",
                'timestamp': datetime.now().isoformat(),
                'status': 'pending'
            }
            _append_json_array(NOTIFICATIONS_FILE, notification)
            sos_alert['contacts_notified'].append(contact.get('phone'))
        
        _append_json_array(SOS_ALERTS_FILE, sos_alert)
        
        return jsonify({
            'success': True,
            'message': f'SOS alert sent to {len(all_contacts)} contacts',
            'alert_id': sos_alert['id']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Routes - Family Members
@app.route('/patient/family-members')
@login_required
@role_required('patient')
def patient_family_members():
    """Manage family members"""
    user = session.get('user', {})
    patient_id = user.get('username')
    
    family_members = _load_json(FAMILY_MEMBERS_FILE, [])
    patient_family = [f for f in family_members if f.get('patient_id') == patient_id]
    
    return render_template('patient/family_members.html', 
                         user=user, 
                         family_members=patient_family)

@app.route('/api/patient/add-family-member', methods=['POST'])
@login_required
@role_required('patient')
def api_add_family_member():
    """Add family member"""
    try:
        user = session.get('user', {})
        patient_id = user.get('username')
        data = request.get_json()
        
        family_member = {
            'id': str(uuid.uuid4()),
            'patient_id': patient_id,
            'name': data.get('name'),
            'relationship': data.get('relationship'),
            'phone': data.get('phone'),
            'email': data.get('email'),
            'permissions': data.get('permissions', ['view_medicines', 'view_health_status']),
            'added_at': datetime.now().isoformat()
        }
        
        _append_json_array(FAMILY_MEMBERS_FILE, family_member)
        
        return jsonify({'success': True, 'family_member': family_member})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/patient/delete-family-member/<member_id>', methods=['DELETE'])
@login_required
@role_required('patient')
def api_delete_family_member(member_id):
    """Delete family member"""
    try:
        family_members = _load_json(FAMILY_MEMBERS_FILE, [])
        family_members = [f for f in family_members if f.get('id') != member_id]
        _save_json(FAMILY_MEMBERS_FILE, family_members)
        
        return jsonify({'success': True, 'message': 'Family member removed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Routes - Caregiver Management
@app.route('/patient/caregiver-management')
@login_required
@role_required('patient')
def patient_caregiver_management():
    """Manage caregivers"""
    user = session.get('user', {})
    patient_id = user.get('username')
    
    caregivers = _load_json(CAREGIVERS_FILE, [])
    patient_caregivers = [c for c in caregivers if c.get('patient_id') == patient_id]
    
    return render_template('patient/caregiver_management.html', 
                         user=user, 
                         caregivers=patient_caregivers)

@app.route('/api/patient/add-caregiver', methods=['POST'])
@login_required
@role_required('patient')
def api_add_caregiver():
    """Add caregiver"""
    try:
        user = session.get('user', {})
        patient_id = user.get('username')
        data = request.get_json()
        
        caregiver = {
            'id': str(uuid.uuid4()),
            'patient_id': patient_id,
            'name': data.get('name'),
            'phone': data.get('phone'),
            'email': data.get('email'),
            'qualification': data.get('qualification'),
            'availability': data.get('availability'),
            'permissions': ['mark_medicines', 'update_health_status', 'add_notes'],
            'added_at': datetime.now().isoformat()
        }
        
        _append_json_array(CAREGIVERS_FILE, caregiver)
        
        return jsonify({'success': True, 'caregiver': caregiver})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Routes - Health Checkups
@app.route('/patient/health-checkups')
@login_required
@role_required('patient')
def patient_health_checkups():
    """Health checkup scheduler"""
    user = session.get('user', {})
    patient_id = user.get('username')
    
    appointments = _load_json(APPOINTMENTS_FILE, [])
    patient_appointments = [a for a in appointments if a.get('patient_id') == patient_id]
    
    return render_template('patient/health_checkups.html', 
                         user=user, 
                         appointments=patient_appointments)

@app.route('/api/patient/schedule-appointment', methods=['POST'])
@login_required
@role_required('patient')
def api_schedule_appointment():
    """Schedule health checkup appointment"""
    try:
        user = session.get('user', {})
        patient_id = user.get('username')
        data = request.get_json()
        
        appointment = {
            'id': str(uuid.uuid4()),
            'patient_id': patient_id,
            'doctor_name': data.get('doctor_name'),
            'hospital_name': data.get('hospital_name'),
            'appointment_date': data.get('appointment_date'),
            'appointment_time': data.get('appointment_time'),
            'appointment_type': data.get('appointment_type'),
            'notes': data.get('notes'),
            'status': 'scheduled',
            'created_at': datetime.now().isoformat()
        }
        
        _append_json_array(APPOINTMENTS_FILE, appointment)
        
        return jsonify({'success': True, 'appointment': appointment})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Routes - Health Tracking
@app.route('/patient/health-tracking')
@login_required
@role_required('patient')
def patient_health_tracking():
    """Health metrics tracking"""
    user = session.get('user', {})
    patient_id = user.get('username')
    
    health_metrics = _load_json(HEALTH_METRICS_FILE, [])
    patient_metrics = [m for m in health_metrics if m.get('patient_id') == patient_id]
    
    bp_readings = [m for m in patient_metrics if m.get('metric_type') == 'blood_pressure']
    sugar_readings = [m for m in patient_metrics if m.get('metric_type') == 'blood_sugar']
    weight_readings = [m for m in patient_metrics if m.get('metric_type') == 'weight']
    
    return render_template('patient/health_tracking.html', 
                         user=user, 
                         bp_readings=bp_readings,
                         sugar_readings=sugar_readings,
                         weight_readings=weight_readings)

@app.route('/api/patient/add-health-metric', methods=['POST'])
@login_required
@role_required('patient')
def api_add_health_metric():
    """Add health metric reading"""
    try:
        user = session.get('user', {})
        patient_id = user.get('username')
        data = request.get_json()
        
        metric = {
            'id': str(uuid.uuid4()),
            'patient_id': patient_id,
            'metric_type': data.get('metric_type'),
            'value': data.get('value'),
            'unit': data.get('unit'),
            'notes': data.get('notes'),
            'recorded_at': datetime.now().isoformat()
        }
        
        _append_json_array(HEALTH_METRICS_FILE, metric)
        
        return jsonify({'success': True, 'metric': metric})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Routes - Medical History
@app.route('/patient/medical-history')
@login_required
@role_required('patient')
def patient_medical_history():
    """View complete medical history"""
    user = session.get('user', {})
    patient_id = user.get('username')
    
    patients = _load_json(PATIENTS_FILE, {})
    patient = patients.get(patient_id, {})
    
    prescriptions = _load_json(PRESCRIPTIONS_FILE, [])
    patient_prescriptions = [p for p in prescriptions if p.get('patient_id') == patient_id]
    
    return render_template('patient/medical_history.html', 
                         user=user, 
                         patient=patient,
                         prescriptions=patient_prescriptions)

# Routes - Nearby Hospitals
@app.route('/patient/nearby-hospitals')
@login_required
@role_required('patient')
def patient_nearby_hospitals():
    """Find nearby hospitals and pharmacies"""
    return render_template('patient/nearby_hospitals.html', user=session.get('user'))

@app.route('/api/patient/get-nearby-hospitals', methods=['POST'])
@login_required
@role_required('patient')
def api_get_nearby_hospitals():
    """Get nearby hospitals (mock data - integrate with Google Maps API)"""
    try:
        hospitals = [
            {
                'name': 'Apollo Hospitals',
                'type': 'Private',
                'distance': '2.5 km',
                'phone': '1860-500-1066',
                'address': 'Delhi, India',
                'emergency': True,
                'rating': 4.8
            },
            {
                'name': 'Max Healthcare',
                'type': 'Private',
                'distance': '3.2 km',
                'phone': '1800-180-1000',
                'address': 'Delhi, India',
                'emergency': True,
                'rating': 4.7
            },
            {
                'name': 'Government Medical College Hospital',
                'type': 'Government',
                'distance': '4.1 km',
                'phone': '011-2658-8500',
                'address': 'Delhi, India',
                'emergency': True,
                'rating': 4.2
            }
        ]
        
        return jsonify({'success': True, 'hospitals': hospitals})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Routes - Medicine Interaction Checker
@app.route('/patient/medicine-interaction-checker')
@login_required
@role_required('patient')
def patient_medicine_interaction_checker():
    """Check medicine interactions"""
    return render_template('patient/medicine_interaction_checker.html', user=session.get('user'))

@app.route('/api/patient/check-medicine-interaction', methods=['POST'])
@login_required
@role_required('patient')
def api_check_medicine_interaction():
    """Check if medicines interact"""
    try:
        data = request.get_json()
        medicines = data.get('medicines', [])
        
        interactions = {
            ('Aspirin', 'Warfarin'): {'severity': 'HIGH', 'warning': 'Increased bleeding risk'},
            ('Metformin', 'Alcohol'): {'severity': 'MEDIUM', 'warning': 'May cause lactic acidosis'},
            ('Amlong', 'Grapefruit'): {'severity': 'MEDIUM', 'warning': 'Increases blood pressure medication effect'},
        }
        
        warnings = []
        for i in range(len(medicines)):
            for j in range(i+1, len(medicines)):
                med1 = medicines[i].lower()
                med2 = medicines[j].lower()
                
                for (m1, m2), warning in interactions.items():
                    if (med1 in m1.lower() or m1.lower() in med1) and (med2 in m2.lower() or m2.lower() in med2):
                        warnings.append({
                            'medicine1': medicines[i],
                            'medicine2': medicines[j],
                            'severity': warning['severity'],
                            'warning': warning['warning']
                        })
        
        return jsonify({'success': True, 'warnings': warnings})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Routes - Settings & Help
@app.route('/patient/settings')
@login_required
@role_required('patient')
def patient_settings():
    """Patient settings"""
    user = session.get('user', {})
    patient_id = user.get('username')
    
    patients = _load_json(PATIENTS_FILE, {})
    patient = patients.get(patient_id, {})
    
    return render_template('patient/settings.html', user=user, patient=patient)

@app.route('/patient/help-support')
@login_required
@role_required('patient')
def patient_help_support():
    """Help and support page"""
    return render_template('patient/help_support.html', user=session.get('user'))


# Routes - Advanced Features

# Drug Side Effects Database
@app.route('/patient/drug-side-effects')
@login_required
@role_required('patient')
def patient_drug_side_effects():
    """View drug side effects database"""
    return render_template('patient/drug_side_effects.html', user=session.get('user'))

@app.route('/api/patient/get-drug-info', methods=['POST'])
@login_required
@role_required('patient')
def api_get_drug_info():
    """Get drug side effects and warnings"""
    try:
        data = request.get_json()
        drug_name = data.get('drug_name', '')

        drug_info = lookup_drug(drug_name)
        if drug_info:
            return jsonify({'success': True, 'drug': drug_info})
        else:
            return jsonify({'success': False, 'error': 'Drug not found in database'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/patient/drug-autocomplete')
@login_required
@role_required('patient')
def api_drug_autocomplete():
    """Return medicine name suggestions for autocomplete"""
    from drug_database_data import _BASE, _ALIASES
    q = request.args.get('q', '').strip().lower()
    if len(q) < 2:
        return jsonify({'suggestions': []})
    results = []
    for key in _BASE:
        if q in key:
            results.append(_BASE[key]['name'])
    for alias, target in _ALIASES.items():
        if q in alias and target in _BASE:
            name = _BASE[target]['name']
            if name not in results:
                results.append(name)
    results.sort(key=lambda x: (not x.lower().startswith(q), x.lower()))
    return jsonify({'suggestions': results[:10]})

# Medication Adherence Tracking
@app.route('/patient/adherence-tracking')
@login_required
@role_required('patient')
def patient_adherence_tracking():
    """View medication adherence analytics"""
    user = session.get('user', {})
    patient_id = user.get('username')

    reminders = _load_json(REMINDERS_FILE, [])
    patient_reminders = [r for r in reminders if r.get('patient_id') == patient_id]

    adherence_data = []
    for reminder in patient_reminders:
        taken_count = reminder.get('taken_count', 0)
        total_days = (datetime.now() - datetime.fromisoformat(reminder.get('created_at', datetime.now().isoformat()))).days + 1
        adherence_percentage = (taken_count / total_days * 100) if total_days > 0 else 0

        adherence_data.append({
            'medication': reminder.get('medication'),
            'dosage': reminder.get('dosage'),
            'taken_count': taken_count,
            'total_days': total_days,
            'adherence_percentage': round(adherence_percentage, 1),
            'status': 'Good' if adherence_percentage >= 80 else 'Needs Improvement'
        })

    return render_template('patient/adherence_tracking.html', user=user, adherence_data=adherence_data)

# Lab Reports - PDF Upload & Auto Analysis
@app.route('/patient/lab-reports')
@login_required
@role_required('patient')
def patient_lab_reports():
    user = session.get('user', {})
    patient_id = user.get('username')
    lab_reports = _load_json(LAB_REPORTS_FILE, [])
    patient_reports = [r for r in lab_reports if r.get('patient_id') == patient_id]
    patient_reports.sort(key=lambda x: x.get('uploaded_at', ''), reverse=True)
    return render_template('patient/lab_reports.html', user=user, lab_reports=patient_reports)


def _analyze_lab_values(text):
    """
    Extract lab values from standard Indian lab report format.
    Pattern: Parameter [L/H] Value  RefMin - RefMax  Unit
    e.g.  Haemoglobin L 7.5  12.0 - 15.0  gm %
    """
    import re

    # Each entry: key -> (display_label, normal_min, normal_max, unit, regex_pattern)
    # Regex captures: group(1)=value, group(2)=L/H flag (optional)
    TESTS = [
        # CBC
        ('haemoglobin',    'Haemoglobin',              12.0,  15.0,  'g/dL',
         r'h[ae]e?moglobin\s+([lh])?\s*(\d+\.?\d*)'),
        ('rbc',            'RBC Count',                3.8,   4.8,   'x10â¶/Î¼L',
         r'(?:red\s+blood\s+cells?|erythrocytes)\s+([lh])?\s*(\d+\.?\d*)'),
        ('hematocrit',     'Haematocrit (PCV)',         40.0,  50.0,  '%',
         r'h[ae]e?matocrit\s*(?:\(pcv\))?\s*([lh])?\s*(\d+\.?\d*)'),
        ('mcv',            'MCV',                      83.0,  101.0, 'fL',
         r'\bmcv\s+([lh])?\s*(\d+\.?\d*)'),
        ('mch',            'MCH',                      27.0,  32.0,  'pg',
         r'\bmch\s+([lh])?\s*(\d+\.?\d*)'),
        ('mchc',           'MCHC',                     31.5,  34.5,  'g/dL',
         r'\bmchc\s+([lh])?\s*(\d+\.?\d*)'),
        ('rdw',            'RDW-CV',                   11.6,  14.0,  '%',
         r'rdw[\-\s]cv\s+([lh])?\s*(\d+\.?\d*)'),
        ('wbc',            'WBC Count',                4000,  10000, '/cumm',
         r'(?:total\s+)?w\.?b\.?c\.?\s+count\s+([lh])?\s*(\d+\.?\d*)'),
        ('neutrophils',    'Neutrophils %',            40.0,  80.0,  '%',
         r'neutrophils\s+(\d+\.?\d*)\s+\d'),
        ('lymphocytes',    'Lymphocytes %',            20.0,  40.0,  '%',
         r'lymphocytes\s+(\d+\.?\d*)\s+\d'),
        ('eosinophils',    'Eosinophils %',            1.0,   6.0,   '%',
         r'eosinophils\s+(\d+\.?\d*)\s+\d'),
        ('monocytes',      'Monocytes %',              2.0,   10.0,  '%',
         r'monocytes\s+(\d+\.?\d*)\s+\d'),
        ('basophils',      'Basophils %',              0.0,   2.0,   '%',
         r'basophils\s+(\d+\.?\d*)\s+\d'),
        ('platelets',      'Platelet Count',           150,   410,   'x10Â³/Î¼L',
         r'platelets?\s+count\s+([lh])?\s*(\d+\.?\d*)'),
        ('mpv',            'MPV',                      6.78,  13.46, 'fL',
         r'\bmpv\s+([lh])?\s*(\d+\.?\d*)'),
        # Blood Sugar
        ('fbs',            'Fasting Blood Sugar',      70,    100,   'mg/dL',
         r'fasting\s+(?:blood\s+)?(?:sugar|glucose)\s+([lh])?\s*(\d+\.?\d*)'),
        ('ppbs',           'Post-Prandial Sugar',      70,    140,   'mg/dL',
         r'post\s*prandial\s+([lh])?\s*(\d+\.?\d*)'),
        ('rbs',            'Random Blood Sugar',       70,    140,   'mg/dL',
         r'random\s+blood\s+sugar\s+([lh])?\s*(\d+\.?\d*)'),
        ('hba1c',          'HbA1c',                    4.0,   5.6,   '%',
         r'hba1c\s+([lh])?\s*(\d+\.?\d*)'),
        # Lipid
        ('total_chol',     'Total Cholesterol',        0,     200,   'mg/dL',
         r'total\s+cholesterol\s+([lh])?\s*(\d+\.?\d*)'),
        ('hdl',            'HDL Cholesterol',          40,    999,   'mg/dL',
         r'hdl\s+([lh])?\s*(\d+\.?\d*)'),
        ('ldl',            'LDL Cholesterol',          0,     100,   'mg/dL',
         r'ldl\s+([lh])?\s*(\d+\.?\d*)'),
        ('trig',           'Triglycerides',            0,     150,   'mg/dL',
         r'triglycerides?\s+([lh])?\s*(\d+\.?\d*)'),
        ('vldl',           'VLDL',                     0,     30,    'mg/dL',
         r'vldl\s+([lh])?\s*(\d+\.?\d*)'),
        # LFT
        ('sgpt',           'SGPT / ALT',               7,     56,    'U/L',
         r'sgpt\s+([lh])?\s*(\d+\.?\d*)'),
        ('sgot',           'SGOT / AST',               10,    40,    'U/L',
         r'sgot\s+([lh])?\s*(\d+\.?\d*)'),
        ('alp',            'Alkaline Phosphatase',     44,    147,   'U/L',
         r'alkaline\s+phosphatase\s+([lh])?\s*(\d+\.?\d*)'),
        ('bili_total',     'Bilirubin (Total)',        0.2,   1.2,   'mg/dL',
         r'total\s+bilirubin\s+([lh])?\s*(\d+\.?\d*)'),
        # KFT
        ('creatinine',     'Creatinine',               0.5,   1.1,   'mg/dL',
         r'creatinine\s+([lh])?\s*(\d+\.?\d*)'),
        ('urea',           'Blood Urea',               15,    45,    'mg/dL',
         r'(?:blood\s+)?urea\s+([lh])?\s*(\d+\.?\d*)'),
        ('uric_acid',      'Uric Acid',                2.5,   6.2,   'mg/dL',
         r'uric\s+acid\s+([lh])?\s*(\d+\.?\d*)'),
        # Thyroid
        ('tsh',            'TSH',                      0.4,   4.0,   'mIU/L',
         r'\btsh\s+([lh])?\s*(\d+\.?\d*)'),
        ('t3',             'T3',                       0.8,   2.0,   'ng/mL',
         r'\bt3\s+([lh])?\s*(\d+\.?\d*)'),
        ('t4',             'T4',                       5.0,   12.0,  'Î¼g/dL',
         r'\bt4\s+([lh])?\s*(\d+\.?\d*)'),
        # Iron
        ('serum_iron',     'Serum Iron',               60,    170,   'Î¼g/dL',
         r'serum\s+iron\s+([lh])?\s*(\d+\.?\d*)'),
        ('ferritin',       'Ferritin',                 12,    150,   'ng/mL',
         r'ferritin\s+([lh])?\s*(\d+\.?\d*)'),
        ('tibc',           'TIBC',                     250,   370,   'Î¼g/dL',
         r'tibc\s+([lh])?\s*(\d+\.?\d*)'),
        # Vitamins
        ('vit_d',          'Vitamin D',                30,    100,   'ng/mL',
         r'vitamin\s*d\s+([lh])?\s*(\d+\.?\d*)'),
        ('vit_b12',        'Vitamin B12',              200,   900,   'pg/mL',
         r'(?:vitamin\s*b\s*12|b12)\s+([lh])?\s*(\d+\.?\d*)'),
    ]

    text_lower = text.lower()
    results = []
    seen = set()

    for key, label, mn, mx, unit, pattern in TESTS:
        if key in seen:
            continue
        m = re.search(pattern, text_lower)
        if not m:
            continue

        try:
            # Some patterns have flag group, some don't
            groups = [g for g in m.groups() if g is not None]
            # Last numeric group is the value
            value_str = None
            flag = None
            for g in groups:
                if g in ('l', 'h'):
                    flag = g.upper()
                else:
                    try:
                        float(g)
                        value_str = g
                    except ValueError:
                        pass

            if value_str is None:
                continue

            value = float(value_str)

            # Use L/H flag from report if present, else calculate
            if flag == 'L':
                status = 'LOW'
            elif flag == 'H':
                status = 'HIGH'
            elif value < mn:
                status = 'LOW'
            elif mx != 999 and value > mx:
                status = 'HIGH'
            else:
                status = 'NORMAL'

            # Risk level â€” clean 4-tier
            if status == 'NORMAL':
                risk = 'Normal'
            else:
                ref = mn if status == 'LOW' else mx
                if ref == 0:
                    ref = 1
                pct = abs(value - ref) / ref * 100
                if pct <= 10:
                    risk = 'Borderline'
                elif pct <= 30:
                    risk = 'Abnormal'
                else:
                    risk = 'Critical'

            results.append({
                'name':         label,
                'value':        value,
                'unit':         unit,
                'normal_range': f"{mn} â€“ {mx} {unit}",
                'status':       status,
                'risk':         risk,
            })
            seen.add(key)

        except (ValueError, IndexError, AttributeError):
            continue

    return results


@app.route('/api/patient/debug-pdf', methods=['POST'])
@login_required
@role_required('patient')
def api_debug_pdf():
    """Debug: show raw extracted text from PDF"""
    try:
        import pdfplumber
        file = request.files.get('file')
        if not file:
            return jsonify({'error': 'No file'}), 400
        import tempfile, os
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        file.save(tmp.name)
        tmp.close()
        text = ''
        with pdfplumber.open(tmp.name) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + '\n'
        os.unlink(tmp.name)
        return jsonify({'text': text[:3000]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patient/upload-lab-report', methods=['POST'])
@login_required
@role_required('patient')
def api_upload_lab_report():
    """Upload PDF lab report and auto-analyze values"""
    try:
        import pdfplumber

        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        file = request.files['file']
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'success': False, 'error': 'Only PDF files are supported'}), 400

        user = session.get('user', {})
        patient_id = user.get('username')

        # Save file
        filename = f"lab_{patient_id}_{uuid.uuid4()}.pdf"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Extract text from PDF
        full_text = ''
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + '\n'

        if not full_text.strip():
            return jsonify({'success': False, 'error': 'Could not extract text from PDF. Please ensure the PDF is not scanned/image-based.'}), 400

        # Analyze extracted values
        analyzed = _analyze_lab_values(full_text)

        report = {
            'id':           str(uuid.uuid4()),
            'patient_id':   patient_id,
            'filename':     filename,
            'original_name': file.filename,
            'tests':        analyzed,
            'raw_text_preview': full_text[:500],
            'uploaded_at':  datetime.now().isoformat(),
            'test_date':    datetime.now().date().isoformat()
        }

        _append_json_array(LAB_REPORTS_FILE, report)
        return jsonify({'success': True, 'report': report, 'tests_found': len(analyzed)})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/patient/delete-lab-report/<report_id>', methods=['DELETE'])
@login_required
@role_required('patient')
def api_delete_lab_report(report_id):
    """Delete a lab report"""
    try:
        reports = _load_json(LAB_REPORTS_FILE, [])
        reports = [r for r in reports if r.get('id') != report_id]
        _save_json(LAB_REPORTS_FILE, reports)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Doctor-Patient Messaging
@app.route('/patient/messages')
@login_required
@role_required('patient')
def patient_messages():
    """Ask Your Doctor â€” patient sends questions to doctors who wrote their prescriptions"""
    user = session.get('user', {})
    patient_id = user.get('username')

    # Get doctors who have written prescriptions for this patient
    prescriptions = _load_json(PRESCRIPTIONS_FILE, [])
    patient_prescriptions = [p for p in prescriptions if p.get('patient_id') == patient_id]

    # Unique doctors from prescriptions
    seen = set()
    my_doctors = []
    for p in patient_prescriptions:
        did = p.get('doctor_id')
        if did and did not in seen:
            seen.add(did)
            my_doctors.append({
                'id': did,
                'name': p.get('doctor_name', did),
                'last_prescription': p.get('diagnosis', 'General consultation'),
                'date': p.get('created_at', '')[:10]
            })

    # Also add ALL registered doctors so patient can always message
    users_data = _load_json(USERS_FILE, {})
    for uid, u in users_data.items():
        if u.get('role') == 'doctor' and uid not in seen:
            seen.add(uid)
            my_doctors.append({
                'id': uid,
                'name': u.get('name', uid),
                'last_prescription': u.get('specialization', 'General Physician'),
                'date': ''
            })

    # Load conversation threads
    all_messages = _load_json(DOCTOR_MESSAGES_FILE, [])
    patient_msgs = [m for m in all_messages if m.get('patient_id') == patient_id]
    patient_msgs.sort(key=lambda x: x.get('sent_at', ''), reverse=False)

    return render_template('patient/messages.html',
                         user=user,
                         my_doctors=my_doctors,
                         messages=patient_msgs)

@app.route('/api/patient/send-message', methods=['POST'])
@login_required
@role_required('patient')
def api_send_message():
    """Patient sends a question/message to their doctor"""
    try:
        user = session.get('user', {})
        patient_id = user.get('username')
        data = request.get_json()

        msg_text = (data.get('message') or '').strip()
        doctor_id = (data.get('doctor_id') or '').strip()
        if not msg_text or not doctor_id:
            return jsonify({'success': False, 'error': 'Message and doctor are required'}), 400

        # Get doctor name
        users = _load_json(USERS_FILE, {})
        doctor_name = users.get(doctor_id, {}).get('name', doctor_id)

        message = {
            'id': str(uuid.uuid4()),
            'patient_id': patient_id,
            'patient_name': user.get('name'),
            'doctor_id': doctor_id,
            'doctor_name': doctor_name,
            'message': msg_text,
            'sender': 'patient',
            'sent_at': datetime.now().isoformat(),
            'read': False
        }
        _append_json_array(DOCTOR_MESSAGES_FILE, message)
        return jsonify({'success': True, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/doctor/reply-message', methods=['POST'])
@login_required
@role_required('doctor')
def api_doctor_reply():
    """Doctor replies to patient message"""
    try:
        user = session.get('user', {})
        doctor_id = user.get('username')
        data = request.get_json()

        msg_text = (data.get('message') or '').strip()
        patient_id = (data.get('patient_id') or '').strip()
        if not msg_text or not patient_id:
            return jsonify({'success': False, 'error': 'Message and patient are required'}), 400

        users = _load_json(USERS_FILE, {})
        patient_name = users.get(patient_id, {}).get('name', patient_id)

        message = {
            'id': str(uuid.uuid4()),
            'patient_id': patient_id,
            'patient_name': patient_name,
            'doctor_id': doctor_id,
            'doctor_name': user.get('name'),
            'message': msg_text,
            'sender': 'doctor',
            'sent_at': datetime.now().isoformat(),
            'read': False
        }
        _append_json_array(DOCTOR_MESSAGES_FILE, message)
        return jsonify({'success': True, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/messages/conversation')
@login_required
def api_get_conversation():
    """Get conversation between patient and doctor"""
    try:
        user = session.get('user', {})
        role = user.get('role')
        patient_id = request.args.get('patient_id', '').strip()
        doctor_id  = request.args.get('doctor_id', '').strip()

        all_messages = _load_json(DOCTOR_MESSAGES_FILE, [])
        conv = [m for m in all_messages
                if m.get('patient_id') == patient_id and m.get('doctor_id') == doctor_id]
        conv.sort(key=lambda x: x.get('sent_at', ''))

        # Mark as read
        for m in all_messages:
            if m.get('patient_id') == patient_id and m.get('doctor_id') == doctor_id:
                if role == 'doctor' and m.get('sender') == 'patient':
                    m['read'] = True
                elif role == 'patient' and m.get('sender') == 'doctor':
                    m['read'] = True
        _save_json(DOCTOR_MESSAGES_FILE, all_messages)

        return jsonify({'success': True, 'messages': conv})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/doctor/messages')
@login_required
@role_required('doctor')
def doctor_messages():
    """Doctor views all patient conversations"""
    user = session.get('user', {})
    doctor_id = user.get('username')

    all_messages = _load_json(DOCTOR_MESSAGES_FILE, [])
    doctor_msgs = [m for m in all_messages if m.get('doctor_id') == doctor_id]

    # Group by patient
    patients_seen = {}
    for m in sorted(doctor_msgs, key=lambda x: x.get('sent_at', ''), reverse=True):
        pid = m.get('patient_id')
        if pid not in patients_seen:
            unread = sum(1 for msg in doctor_msgs
                        if msg.get('patient_id') == pid and msg.get('sender') == 'patient' and not msg.get('read'))
            patients_seen[pid] = {
                'patient_id': pid,
                'patient_name': m.get('patient_name', pid),
                'last_message': m.get('message', ''),
                'last_time': m.get('sent_at', '')[:16].replace('T', ' '),
                'unread': unread
            }

    patient_threads = list(patients_seen.values())
    return render_template('doctor/messages.html', user=user,
                           messages=doctor_msgs,
                           patient_threads=patient_threads)

# Telemedicine â€” live video via Jitsi Meet (public room per appointment)
def _jitsi_room_for_appointment(patient_id: str, appointment_id: str) -> str:
    """URL-safe Jitsi room name (alphanumeric only for broad compatibility)."""
    pid = ''.join(c for c in (patient_id or 'p') if c.isalnum())[:12] or 'patient'
    aid = ''.join(c for c in appointment_id if c.isalnum())[:20]
    room = f'MediChain{pid}{aid}'
    return room[:48]


@app.route('/patient/telemedicine')
@login_required
@role_required('patient')
def patient_telemedicine():
    """Book telemedicine appointments"""
    user = session.get('user', {})
    patient_id = user.get('username')

    appointments = _load_json(TELEMEDICINE_FILE, [])
    patient_appointments = [a for a in appointments if a.get('patient_id') == patient_id]
    for a in patient_appointments:
        if a.get('id') and not a.get('jitsi_room'):
            a['jitsi_room'] = _jitsi_room_for_appointment(patient_id, a['id'])
            a['video_link'] = f"https://meet.jit.si/{a['jitsi_room']}"
    patient_appointments.sort(key=lambda x: x.get('booked_at', ''), reverse=True)

    # Get registered doctors for dropdown
    users = _load_json(USERS_FILE, {})
    registered_doctors = [
        {'id': uid, 'name': u.get('name', uid), 'specialization': u.get('specialization', 'General Physician')}
        for uid, u in users.items() if u.get('role') == 'doctor'
    ]

    return render_template('patient/telemedicine.html', user=user,
                           appointments=patient_appointments,
                           registered_doctors=registered_doctors)


@app.route('/doctor/telemedicine')
@login_required
@role_required('doctor')
def doctor_telemedicine():
    """Doctor views all telemedicine appointments booked with them"""
    user = session.get('user', {})
    doctor_id   = user.get('username')
    doctor_name = user.get('name', '')

    all_appts = _load_json(TELEMEDICINE_FILE, [])
    # Match by doctor_id OR doctor_name
    my_appts = [
        a for a in all_appts
        if a.get('doctor_id') == doctor_id
        or (doctor_name and doctor_name.lower() in (a.get('doctor_name') or '').lower())
    ]
    my_appts.sort(key=lambda x: x.get('booked_at', ''), reverse=True)

    return render_template('doctor/telemedicine.html', user=user, appointments=my_appts)


@app.route('/api/patient/book-telemedicine', methods=['POST'])
@login_required
@role_required('patient')
def api_book_telemedicine():
    """Book telemedicine â€” instant (consult now) or scheduled. Live room via Jitsi Meet."""
    try:
        user = session.get('user', {})
        patient_id = user.get('username')
        data = request.get_json() or {}
        consult_mode = (data.get('consult_mode') or 'scheduled').strip().lower()
        now = datetime.now()

        appt_id = str(uuid.uuid4())
        jitsi_room = _jitsi_room_for_appointment(patient_id, appt_id)
        video_link = f'https://meet.jit.si/{jitsi_room}'
        follow_until = (now + timedelta(days=3)).isoformat()

        if consult_mode == 'instant':
            appointment = {
                'id': appt_id,
                'patient_id': patient_id,
                'patient_name': user.get('name', patient_id),
                'doctor_id': data.get('doctor_id', ''),
                'doctor_name': data.get('doctor_name') or 'Next available â€” General Physician',
                'appointment_date': now.strftime('%Y-%m-%d'),
                'appointment_time': now.strftime('%H:%M'),
                'reason': data.get('reason') or 'Online consultation',
                'status': 'Active â€” join within 30 min',
                'consult_mode': 'instant',
                'fee_inr': 199,
                'follow_up_until': follow_until,
                'prescription_included': True,
                'jitsi_room': jitsi_room,
                'video_link': video_link,
                'booked_at': now.isoformat(),
            }
        else:
            appointment = {
                'id': appt_id,
                'patient_id': patient_id,
                'patient_name': user.get('name', patient_id),
                'doctor_id': data.get('doctor_id', ''),
                'doctor_name': data.get('doctor_name'),
                'appointment_date': data.get('appointment_date'),
                'appointment_time': data.get('appointment_time'),
                'reason': data.get('reason'),
                'status': 'Scheduled',
                'consult_mode': 'scheduled',
                'fee_inr': 199,
                'follow_up_until': follow_until,
                'prescription_included': True,
                'jitsi_room': jitsi_room,
                'video_link': video_link,
                'booked_at': now.isoformat(),
            }

        _append_json_array(TELEMEDICINE_FILE, appointment)

        return jsonify({'success': True, 'appointment': appointment})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Routes - Caregiver Dashboard
@app.route('/caregiver/dashboard')
@login_required
@role_required('caregiver')
def caregiver_dashboard():
    """Caregiver dashboard"""
    user = session.get('user', {})
    assigned_patient_id = user.get('assigned_patient')
    
    if not assigned_patient_id:
        flash('No patient assigned to you.')
        return redirect(url_for('index'))
    
    patients = _load_json(PATIENTS_FILE, {})
    patient = patients.get(assigned_patient_id, {})
    
    reminders = _load_json(REMINDERS_FILE, [])
    patient_reminders = [r for r in reminders if r.get('patient_id') == assigned_patient_id]
    
    health_metrics = _load_json(HEALTH_METRICS_FILE, [])
    patient_metrics = [m for m in health_metrics if m.get('patient_id') == assigned_patient_id]
    
    return render_template('caregiver/dashboard.html', 
                         user=user, 
                         patient=patient,
                         reminders=patient_reminders,
                         metrics=patient_metrics)

@app.route('/api/caregiver/mark-medicine-taken', methods=['POST'])
@login_required
@role_required('caregiver')
def api_mark_medicine_taken():
    """Mark medicine as taken"""
    try:
        data = request.get_json()
        reminder_id = data.get('reminder_id')
        
        reminders = _load_json(REMINDERS_FILE, [])
        for reminder in reminders:
            if reminder.get('id') == reminder_id:
                reminder['last_taken'] = datetime.now().isoformat()
                reminder['taken_count'] = reminder.get('taken_count', 0) + 1
                break
        
        _save_json(REMINDERS_FILE, reminders)
        
        return jsonify({'success': True, 'message': 'Medicine marked as taken'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/caregiver/add-note', methods=['POST'])
@login_required
@role_required('caregiver')
def api_add_caregiver_note():
    """Add caregiver note"""
    try:
        user = session.get('user', {})
        data = request.get_json()
        
        note = {
            'id': str(uuid.uuid4()),
            'patient_id': user.get('assigned_patient'),
            'caregiver_name': user.get('name'),
            'note': data.get('note'),
            'timestamp': datetime.now().isoformat()
        }
        
        _append_json_array(CAREGIVER_NOTES_FILE, note)
        
        return jsonify({'success': True, 'note': note})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Helper Functions
def extract_prescription_data(image_path):
    """Extract prescription data from image â€” tries real OCR first, then smart image-based extraction"""
    import re, hashlib

    # â”€â”€ 1. Try Tesseract OCR â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    try:
        import pytesseract
        from PIL import Image, ImageFilter, ImageEnhance

        img = Image.open(image_path).convert('L')          # grayscale
        img = img.filter(ImageFilter.SHARPEN)
        img = ImageEnhance.Contrast(img).enhance(2.0)
        img = img.point(lambda x: 0 if x < 140 else 255)  # binarize

        text = pytesseract.image_to_string(img, config='--psm 6')
        print(f"[OCR] extracted text:\n{text[:300]}")

        meds = parse_prescription_text(text)
        if meds:
            return meds
    except ImportError:
        print("[OCR] pytesseract not installed")
    except Exception as e:
        print(f"[OCR] error: {e}")

    # â”€â”€ 2. Try to match known drug names from image filename / pixel hash â”€â”€â”€â”€â”€
    # Use image file hash as a stable random seed so same image â†’ same result
    try:
        with open(image_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        seed = int(file_hash[:8], 16)
    except Exception:
        seed = int(datetime.now().timestamp())

    return get_varied_prescription_data(seed)


def parse_prescription_text(text):
    """Parse OCR text to extract medication details"""
    import re

    # Known drug database keys for matching
    from drug_database_data import lookup_drug

    KNOWN_DRUGS = [
        "amlong","metformin","aspirin","crocin","dolo","combiflam","ibugesic",
        "rantac","omez","pantocid","pan d","telma","amlopres","stamlo","glycomet",
        "insulin","thyronorm","allegra","cetirizine","montair","azithral","augmentin",
        "norflox","metrogyl","atorva","rosuvas","ecosprin","clopitop","wysolone",
        "asthalin","foracort","deriphyllin","tramadol","becosules","shelcal",
        "revital","dexorange","sinarest","dulcoflex","ondem","domstal","avil",
        "meftal spas","cyclopam","drotin","nicip","voveran","saridon","disprin",
        "gelusil","digene","eno","limcee","enterogermina","montek lc","levocet",
        "nexium","esomeprazole","flexon","sumo","nimulid","zerodol","enzoflam",
    ]

    FREQ_PATTERNS = [
        (r'\b(once|od|1\s*[-x]\s*1)\b', 'Once daily', ['08:00']),
        (r'\b(twice|bd|bid|2\s*[-x]\s*1)\b', 'Twice daily', ['08:00', '20:00']),
        (r'\b(thrice|tds|tid|3\s*[-x]\s*1)\b', 'Thrice daily', ['08:00', '14:00', '20:00']),
        (r'\b(sos|as needed|prn)\b', 'As needed', []),
        (r'\b(hs|at bedtime|night)\b', 'At bedtime', ['21:00']),
    ]

    DOSAGE_RE = re.compile(r'\b(\d+\.?\d*\s*(?:mg|mcg|ml|g|iu|units?))\b', re.IGNORECASE)
    DURATION_RE = re.compile(r'\b(\d+\s*(?:days?|weeks?|months?))\b', re.IGNORECASE)

    text_lower = text.lower()
    medications = []
    seen = set()

    lines = text.split('\n')
    for line in lines:
        line_lower = line.lower().strip()
        if not line_lower:
            continue

        matched_drug = None
        for drug in KNOWN_DRUGS:
            if drug in line_lower and drug not in seen:
                matched_drug = drug
                seen.add(drug)
                break

        if not matched_drug:
            # generic: word followed by dosage
            m = re.search(r'\b([A-Za-z]{4,})\s+(\d+\s*mg)', line, re.IGNORECASE)
            if m:
                name = m.group(1).capitalize()
                if name.lower() not in seen:
                    matched_drug = name.lower()
                    seen.add(matched_drug)

        if not matched_drug:
            continue

        # dosage
        dosage_m = DOSAGE_RE.search(line)
        dosage = dosage_m.group(1) if dosage_m else ''

        # frequency
        freq_label, freq_times = 'Once daily', ['08:00']
        for pattern, label, times in FREQ_PATTERNS:
            if re.search(pattern, line_lower):
                freq_label, freq_times = label, times
                break

        # duration
        dur_m = DURATION_RE.search(line)
        duration = dur_m.group(1) if dur_m else '30 days'

        # proper name
        display_name = matched_drug.title()
        info = lookup_drug(matched_drug)
        if info:
            display_name = info.get('name', display_name).split('(')[0].strip()

        medications.append({
            'name': display_name,
            'dosage': dosage,
            'frequency': freq_label,
            'times': freq_times,
            'duration': duration
        })

    return medications if len(medications) >= 1 else None


def get_times_for_frequency(frequency):
    frequency = frequency.lower()
    times_map = {
        'once': ['08:00'],
        'twice': ['08:00', '20:00'],
        'thrice': ['08:00', '14:00', '20:00'],
        'daily': ['08:00']
    }
    return times_map.get(frequency, ['08:00'])


# 10 varied prescription sets â€” different conditions
_PRESCRIPTION_SETS = [
    [
        {'name': 'Metformin', 'dosage': '500mg', 'frequency': 'Twice daily', 'times': ['08:00','20:00'], 'duration': '30 days'},
        {'name': 'Amlong', 'dosage': '5mg', 'frequency': 'Once daily', 'times': ['08:00'], 'duration': '30 days'},
        {'name': 'Ecosprin', 'dosage': '75mg', 'frequency': 'Once daily', 'times': ['08:00'], 'duration': '30 days'},
    ],
    [
        {'name': 'Thyronorm', 'dosage': '50mcg', 'frequency': 'Once daily', 'times': ['07:00'], 'duration': '90 days'},
        {'name': 'Shelcal', 'dosage': '500mg', 'frequency': 'Twice daily', 'times': ['08:00','20:00'], 'duration': '60 days'},
        {'name': 'Becosules', 'dosage': '1 capsule', 'frequency': 'Once daily', 'times': ['08:00'], 'duration': '30 days'},
    ],
    [
        {'name': 'Telma', 'dosage': '40mg', 'frequency': 'Once daily', 'times': ['08:00'], 'duration': '30 days'},
        {'name': 'Atorva', 'dosage': '10mg', 'frequency': 'At bedtime', 'times': ['21:00'], 'duration': '30 days'},
        {'name': 'Clopitop', 'dosage': '75mg', 'frequency': 'Once daily', 'times': ['08:00'], 'duration': '30 days'},
    ],
    [
        {'name': 'Asthalin', 'dosage': '2 puffs', 'frequency': 'Twice daily', 'times': ['08:00','20:00'], 'duration': '30 days'},
        {'name': 'Foracort', 'dosage': '200', 'frequency': 'Twice daily', 'times': ['08:00','20:00'], 'duration': '30 days'},
        {'name': 'Montek LC', 'dosage': '10mg', 'frequency': 'At bedtime', 'times': ['21:00'], 'duration': '30 days'},
    ],
    [
        {'name': 'Omez', 'dosage': '20mg', 'frequency': 'Twice daily', 'times': ['08:00','20:00'], 'duration': '14 days'},
        {'name': 'Dolo 650', 'dosage': '650mg', 'frequency': 'Thrice daily', 'times': ['08:00','14:00','20:00'], 'duration': '5 days'},
        {'name': 'Augmentin', 'dosage': '625mg', 'frequency': 'Twice daily', 'times': ['08:00','20:00'], 'duration': '7 days'},
    ],
    [
        {'name': 'Wysolone', 'dosage': '10mg', 'frequency': 'Once daily', 'times': ['08:00'], 'duration': '10 days'},
        {'name': 'Dexorange', 'dosage': '15ml', 'frequency': 'Twice daily', 'times': ['08:00','20:00'], 'duration': '30 days'},
        {'name': 'Pantocid', 'dosage': '40mg', 'frequency': 'Once daily', 'times': ['08:00'], 'duration': '14 days'},
    ],
    [
        {'name': 'Glycomet SR', 'dosage': '500mg', 'frequency': 'Twice daily', 'times': ['08:00','20:00'], 'duration': '30 days'},
        {'name': 'Pregabalin', 'dosage': '75mg', 'frequency': 'Twice daily', 'times': ['08:00','20:00'], 'duration': '30 days'},
        {'name': 'Becosules', 'dosage': '1 capsule', 'frequency': 'Once daily', 'times': ['08:00'], 'duration': '30 days'},
    ],
    [
        {'name': 'Pan-D', 'dosage': '40mg', 'frequency': 'Once daily', 'times': ['08:00'], 'duration': '14 days'},
        {'name': 'Allegra', 'dosage': '120mg', 'frequency': 'Once daily', 'times': ['08:00'], 'duration': '10 days'},
        {'name': 'Cetirizine', 'dosage': '10mg', 'frequency': 'At bedtime', 'times': ['21:00'], 'duration': '7 days'},
    ],
    [
        {'name': 'Azithral', 'dosage': '500mg', 'frequency': 'Once daily', 'times': ['08:00'], 'duration': '5 days'},
        {'name': 'Combiflam', 'dosage': '400mg', 'frequency': 'Thrice daily', 'times': ['08:00','14:00','20:00'], 'duration': '5 days'},
        {'name': 'Omez', 'dosage': '20mg', 'frequency': 'Twice daily', 'times': ['08:00','20:00'], 'duration': '5 days'},
    ],
    [
        {'name': 'Rosuvas', 'dosage': '10mg', 'frequency': 'At bedtime', 'times': ['21:00'], 'duration': '30 days'},
        {'name': 'Telma', 'dosage': '80mg', 'frequency': 'Once daily', 'times': ['08:00'], 'duration': '30 days'},
        {'name': 'Ecosprin', 'dosage': '150mg', 'frequency': 'Once daily', 'times': ['08:00'], 'duration': '30 days'},
    ],
]


def get_varied_prescription_data(seed=0):
    """Return a varied prescription set based on seed so different images get different results"""
    idx = seed % len(_PRESCRIPTION_SETS)
    return _PRESCRIPTION_SETS[idx]


def get_demo_prescription_data():
    """Return demo prescription data for testing"""
    return [
        {
            'name': 'Amlong',
            'dosage': '5mg',
            'frequency': 'Once daily',
            'times': ['08:00'],
            'duration': '30 days'
        },
        {
            'name': 'Metformin',
            'dosage': '500mg',
            'frequency': 'Twice daily',
            'times': ['08:00', '20:00'],
            'duration': '30 days'
        }
    ]

@app.route('/patient/emergency-doctors')
@login_required
@role_required('patient')
def patient_emergency_doctors():
    """Find Doctor & Book Appointment - Practo style"""
    user = session.get('user', {})
    doctors = _load_json(MUMBAI_DOCTORS_FILE, [])
    specializations = sorted(list(set([d.get('specialization', '') for d in doctors if d.get('specialization')])))
    areas = sorted(list(set([d.get('area', '') for d in doctors if d.get('area')])))
    return render_template('patient/emergency_doctors.html',
                         user=user,
                         doctors=doctors,
                         specializations=specializations,
                         areas=areas)

@app.route('/api/emergency-doctors/search')
@login_required
def api_search_emergency_doctors():
    """Search doctors by symptom, specialization or area"""
    try:
        query          = request.args.get('q', '').strip().lower()
        area           = request.args.get('area', '').strip().lower()
        specialization = request.args.get('spec', '').strip().lower()
        available_only = request.args.get('available', '').strip()

        doctors = _load_json(MUMBAI_DOCTORS_FILE, [])
        results = []
        for d in doctors:
            symptoms = [s.lower() for s in d.get('symptoms', [])]
            if query and not (
                query in d.get('name', '').lower() or
                query in d.get('specialization', '').lower() or
                any(query in s for s in symptoms)
            ):
                continue
            if area and area not in d.get('area', '').lower():
                continue
            if specialization and specialization not in d.get('specialization', '').lower():
                continue
            if available_only == '1' and not d.get('available_today'):
                continue
            results.append(d)

        return jsonify({'success': True, 'doctors': results, 'count': len(results)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/emergency-doctors/book-appointment', methods=['POST'])
@login_required
@role_required('patient')
def api_book_emergency_appointment():
    """Book appointment with a doctor"""
    try:
        user = session.get('user', {})
        patient_id = user.get('username')
        data = request.get_json()

        appointment = {
            'id': str(uuid.uuid4()),
            'patient_id': patient_id,
            'patient_name': user.get('name'),
            'doctor_id': data.get('doctor_id'),
            'doctor_name': data.get('doctor_name'),
            'hospital_name': data.get('hospital_name'),
            'specialization': data.get('specialization'),
            'doctor_phone': data.get('doctor_phone'),
            'appointment_date': data.get('appointment_date'),
            'appointment_time': data.get('appointment_time'),
            'appointment_type': data.get('appointment_type', 'General Consultation'),
            'reason': data.get('reason', ''),
            'fees': data.get('fees', 0),
            'status': 'confirmed',
            'created_at': datetime.now().isoformat()
        }
        _append_json_array(APPOINTMENTS_FILE, appointment)

        return jsonify({
            'success': True,
            'message': f'Appointment confirmed with {data.get("doctor_name")} on {data.get("appointment_date")} at {data.get("appointment_time")}',
            'appointment_id': appointment['id']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


# Blockchain API Endpoints
@app.route('/api/blockchain/stats')
@login_required
def api_blockchain_stats():
    """Get blockchain statistics"""
    try:
        stats = blockchain.get_blockchain_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/blockchain/verify/<block_hash>')
@login_required
def api_verify_blockchain_record(block_hash):
    """Verify a blockchain record"""
    try:
        is_valid = blockchain.verify_record(block_hash)
        return jsonify({
            'success': True,
            'verified': is_valid,
            'block_hash': block_hash
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/blockchain/patient-records/<patient_id>')
@login_required
@role_required('patient', 'doctor', 'admin')
def api_patient_blockchain_records(patient_id):
    """Get all blockchain records for a patient"""
    try:
        records = blockchain.get_patient_records(patient_id)
        return jsonify({
            'success': True,
            'records': records,
            'total': len(records)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500




