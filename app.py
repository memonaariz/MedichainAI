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

# Import blockchain module
from blockchain import (
    get_blockchain_instance,
    verify_data_integrity,
    encrypt_sensitive_data
)

app = Flask(__name__, static_folder='static')

# Configuration
app.secret_key = os.getenv('SECRET_KEY', 'medichain_secure_key_2025')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=6)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Initialize blockchain
blockchain = get_blockchain_instance()

# File Paths
USERS_FILE = 'users.json'
PATIENTS_FILE = 'patients.json'
PRESCRIPTIONS_FILE = 'prescriptions.json'
REMINDERS_FILE = 'reminders.json'
FAMILY_MEMBERS_FILE = 'family_members.json'
CAREGIVERS_FILE = 'caregivers.json'
APPOINTMENTS_FILE = 'appointments.json'
HEALTH_METRICS_FILE = 'health_metrics.json'
EMERGENCY_CONTACTS_FILE = 'emergency_contacts.json'
NOTIFICATIONS_FILE = 'notifications.json'
SOS_ALERTS_FILE = 'sos_alerts.json'
UPLOAD_FOLDER = 'uploads'
DRUG_SIDE_EFFECTS_FILE = 'drug_side_effects.json'
ADHERENCE_TRACKING_FILE = 'adherence_tracking.json'
LAB_REPORTS_FILE = 'lab_reports.json'
TELEMEDICINE_FILE = 'telemedicine_appointments.json'
DOCTOR_MESSAGES_FILE = 'doctor_messages.json'
DRUG_SIDE_EFFECTS_FILE = 'drug_side_effects.json'
ADHERENCE_TRACKING_FILE = 'adherence_tracking.json'
LAB_REPORTS_FILE = 'lab_reports.json'
TELEMEDICINE_FILE = 'telemedicine_appointments.json'
DOCTOR_MESSAGES_FILE = 'doctor_messages.json'

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
            "caregiver1": {"password": "care123", "role": "caregiver", "name": "Priya Sharma", "type": "caregiver", "assigned_patient": "patient1"}
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
                'assigned_patient': user.get('assigned_patient')
            }
            flash(f"Welcome, {user.get('name', username)}!")
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Patient registration page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validation
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
        
        # Get form data
        full_name = request.form.get('full_name', '').strip()
        age = request.form.get('age', '')
        blood_group = request.form.get('blood_group', '')
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        allergies = request.form.getlist('allergies')
        medical_history = request.form.getlist('medical_history')
        current_medications = request.form.get('current_medications', '').strip()
        insurance_provider = request.form.get('insurance_provider', '')
        insurance_id = request.form.get('insurance_id', '').strip()
        emergency_name = request.form.get('emergency_name', '').strip()
        emergency_phone = request.form.get('emergency_phone', '').strip()
        
        # Create user
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
        
        # Create patient profile
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
    return render_template('profile.html', user=user)


# Routes - Doctor
@app.route('/doctor/dashboard')
@login_required
@role_required('doctor')
def doctor_dashboard():
    """Doctor dashboard"""
    user = session.get('user', {})
    return render_template('doctor/dashboard.html', user=user)

@app.route('/doctor/scan-qr')
@login_required
@role_required('doctor')
def doctor_scan_qr():
    """Doctor scans patient QR code"""
    return render_template('doctor/scan_qr.html', user=session.get('user'))

@app.route('/api/doctor/patient/<patient_id>')
@login_required
@role_required('doctor')
def api_get_patient(patient_id):
    """Get patient details by ID"""
    patients = _load_json(PATIENTS_FILE, {})
    patient = patients.get(patient_id)
    
    if not patient:
        return jsonify({'success': False, 'error': 'Patient not found'}), 404
    
    return jsonify({'success': True, 'patient': patient})

@app.route('/doctor/write-prescription/<patient_id>')
@login_required
@role_required('doctor')
def doctor_write_prescription(patient_id):
    """Doctor writes prescription for patient"""
    patients = _load_json(PATIENTS_FILE, {})
    patient = patients.get(patient_id)
    
    if not patient:
        flash('Patient not found.')
        return redirect(url_for('doctor_dashboard'))
    
    return render_template('doctor/write_prescription.html', patient=patient, user=session.get('user'))

@app.route('/api/doctor/save-prescription', methods=['POST'])
@login_required
@role_required('doctor')
def api_save_prescription():
    """Save prescription with blockchain verification"""
    try:
        data = request.get_json()
        patient_id = data.get('patient_id')
        medications = data.get('medications', [])
        notes = data.get('notes', '')
        
        if not patient_id or not medications:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        prescription = {
            'id': str(uuid.uuid4()),
            'patient_id': patient_id,
            'doctor_id': session.get('user', {}).get('username'),
            'doctor_name': session.get('user', {}).get('name'),
            'medications': medications,
            'notes': notes,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        # Add to blockchain for immutability
        blockchain_hash = blockchain.add_prescription(
            patient_id=patient_id,
            doctor_id=prescription['doctor_id'],
            prescription_data=prescription
        )
        
        # Add blockchain hash to prescription
        prescription['blockchain_hash'] = blockchain_hash
        prescription['verified'] = True
        
        _append_json_array(PRESCRIPTIONS_FILE, prescription)
        
        return jsonify({
            'success': True,
            'prescription_id': prescription['id'],
            'blockchain_hash': blockchain_hash,
            'verified': True
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
    
    reminders = _load_json(REMINDERS_FILE, [])
    patient_reminders = [r for r in reminders if r.get('patient_id') == patient_id]
    
    return render_template('patient/reminders.html', reminders=patient_reminders, user=user)

@app.route('/patient/prescriptions')
@login_required
@role_required('patient')
def patient_prescriptions():
    """View patient prescriptions"""
    user = session.get('user', {})
    patient_id = user.get('username')
    
    prescriptions = _load_json(PRESCRIPTIONS_FILE, [])
    patient_prescriptions = [p for p in prescriptions if p.get('patient_id') == patient_id]
    
    return render_template('patient/prescriptions.html', prescriptions=patient_prescriptions, user=user)

@app.route('/patient/snap-prescription')
@login_required
@role_required('patient')
def patient_snap_prescription():
    """Patient snaps prescription photo"""
    return render_template('patient/snap_prescription.html', user=session.get('user'))

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
    """Redirect to pharmacy to buy medicine"""
    pharmacy_links = {
        'amlong': 'https://www.1mg.com/search?name=amlong',
        'metformin': 'https://www.1mg.com/search?name=metformin',
        'aspirin': 'https://www.1mg.com/search?name=aspirin'
    }
    
    link = pharmacy_links.get(medicine_name.lower(), f'https://www.1mg.com/search?name={medicine_name}')
    return jsonify({'success': True, 'link': link})


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
                'message': f"🚨 EMERGENCY SOS from {patient.get('name')}! Location: {sos_alert['location']}",
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
        drug_name = data.get('drug_name', '').lower()

        drug_database = {
            'amlong': {
                'name': 'Amlodipine (Amlong)',
                'type': 'Blood Pressure Medication',
                'common_side_effects': ['Swelling in feet/ankles', 'Headache', 'Dizziness', 'Fatigue'],
                'serious_side_effects': ['Chest pain', 'Severe dizziness', 'Fainting'],
                'interactions': ['Grapefruit juice', 'Simvastatin'],
                'warnings': 'Do not stop suddenly. May cause rebound hypertension.',
                'severity': 'MEDIUM'
            },
            'metformin': {
                'name': 'Metformin',
                'type': 'Diabetes Medication',
                'common_side_effects': ['Nausea', 'Diarrhea', 'Stomach upset', 'Metallic taste'],
                'serious_side_effects': ['Lactic acidosis (rare)', 'Vitamin B12 deficiency'],
                'interactions': ['Alcohol', 'Contrast dye', 'Certain antibiotics'],
                'warnings': 'Take with food. Monitor kidney function regularly.',
                'severity': 'MEDIUM'
            },
            'aspirin': {
                'name': 'Aspirin',
                'type': 'Pain Reliever / Blood Thinner',
                'common_side_effects': ['Stomach upset', 'Heartburn', 'Nausea'],
                'serious_side_effects': ['Bleeding', 'Allergic reaction', 'Asthma attack'],
                'interactions': ['Warfarin', 'NSAIDs', 'Alcohol'],
                'warnings': 'Do not use if allergic. May increase bleeding risk.',
                'severity': 'HIGH'
            }
        }

        drug_info = drug_database.get(drug_name)
        if drug_info:
            return jsonify({'success': True, 'drug': drug_info})
        else:
            return jsonify({'success': False, 'error': 'Drug not found in database'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

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

# Lab Reports Upload
@app.route('/patient/lab-reports')
@login_required
@role_required('patient')
def patient_lab_reports():
    """Upload and view lab reports"""
    user = session.get('user', {})
    patient_id = user.get('username')

    lab_reports = _load_json(LAB_REPORTS_FILE, [])
    patient_reports = [r for r in lab_reports if r.get('patient_id') == patient_id]

    return render_template('patient/lab_reports.html', user=user, lab_reports=patient_reports)

@app.route('/api/patient/upload-lab-report', methods=['POST'])
@login_required
@role_required('patient')
def api_upload_lab_report():
    """Upload lab report"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        file = request.files['file']
        patient_id = session.get('user', {}).get('username')

        filename = f"lab_{patient_id}_{uuid.uuid4()}.pdf"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        report = {
            'id': str(uuid.uuid4()),
            'patient_id': patient_id,
            'test_name': request.form.get('test_name', 'Lab Report'),
            'test_date': request.form.get('test_date', datetime.now().isoformat()),
            'file_path': filename,
            'uploaded_at': datetime.now().isoformat()
        }

        _append_json_array(LAB_REPORTS_FILE, report)

        return jsonify({'success': True, 'report': report})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Doctor-Patient Messaging
@app.route('/patient/messages')
@login_required
@role_required('patient')
def patient_messages():
    """View messages from doctors"""
    user = session.get('user', {})
    patient_id = user.get('username')

    messages = _load_json(DOCTOR_MESSAGES_FILE, [])
    patient_messages = [m for m in messages if m.get('patient_id') == patient_id]

    return render_template('patient/messages.html', user=user, messages=patient_messages)

@app.route('/api/patient/send-message', methods=['POST'])
@login_required
@role_required('patient')
def api_send_message():
    """Send message to doctor"""
    try:
        user = session.get('user', {})
        patient_id = user.get('username')
        data = request.get_json()

        message = {
            'id': str(uuid.uuid4()),
            'patient_id': patient_id,
            'patient_name': user.get('name'),
            'doctor_id': data.get('doctor_id'),
            'message': data.get('message'),
            'sent_at': datetime.now().isoformat(),
            'read': False
        }

        _append_json_array(DOCTOR_MESSAGES_FILE, message)

        return jsonify({'success': True, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Telemedicine Appointment Booking
@app.route('/patient/telemedicine')
@login_required
@role_required('patient')
def patient_telemedicine():
    """Book telemedicine appointments"""
    user = session.get('user', {})
    patient_id = user.get('username')

    appointments = _load_json(TELEMEDICINE_FILE, [])
    patient_appointments = [a for a in appointments if a.get('patient_id') == patient_id]

    return render_template('patient/telemedicine.html', user=user, appointments=patient_appointments)

@app.route('/api/patient/book-telemedicine', methods=['POST'])
@login_required
@role_required('patient')
def api_book_telemedicine():
    """Book telemedicine appointment"""
    try:
        user = session.get('user', {})
        patient_id = user.get('username')
        data = request.get_json()

        appointment = {
            'id': str(uuid.uuid4()),
            'patient_id': patient_id,
            'doctor_name': data.get('doctor_name'),
            'appointment_date': data.get('appointment_date'),
            'appointment_time': data.get('appointment_time'),
            'reason': data.get('reason'),
            'status': 'Scheduled',
            'video_link': f'https://meet.medichain.local/{uuid.uuid4()}',
            'booked_at': datetime.now().isoformat()
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
        
        _append_json_array('caregiver_notes.json', note)
        
        return jsonify({'success': True, 'note': note})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Helper Functions
def extract_prescription_data(image_path):
    """Extract prescription data from image using AI/OCR"""
    try:
        try:
            import pytesseract
            from PIL import Image
            
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            
            medications = parse_prescription_text(text)
            if medications:
                return medications
        except ImportError:
            print("Tesseract not installed, using demo data")
        except Exception as e:
            print(f"OCR error: {e}, using demo data")
        
        return get_demo_prescription_data()
    except Exception as e:
        print(f"Error in extract_prescription_data: {e}")
        return get_demo_prescription_data()

def parse_prescription_text(text):
    """Parse OCR text to extract medication details"""
    import re
    
    medications = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        match = re.search(r'([A-Za-z]+)\s+(\d+\s*mg)\s+(once|twice|thrice|daily|times)', line, re.IGNORECASE)
        if match:
            med = {
                'name': match.group(1),
                'dosage': match.group(2),
                'frequency': match.group(3) + ' daily',
                'times': get_times_for_frequency(match.group(3)),
                'duration': '30 days'
            }
            medications.append(med)
    
    return medications if medications else None

def get_times_for_frequency(frequency):
    """Get medication times based on frequency"""
    frequency = frequency.lower()
    times_map = {
        'once': ['08:00'],
        'twice': ['08:00', '20:00'],
        'thrice': ['08:00', '14:00', '20:00'],
        'daily': ['08:00']
    }
    return times_map.get(frequency, ['08:00'])

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
    """Emergency doctors directory for Mumbai areas"""
    user = session.get('user', {})
    doctors = _load_json('mumbai_doctors.json', [])
    
    # Get unique areas for filtering
    areas = sorted(list(set([d.get('area') for d in doctors])))
    
    return render_template('patient/emergency_doctors.html', 
                         user=user, 
                         doctors=doctors,
                         areas=areas)

@app.route('/api/emergency-doctors/search')
@login_required
def api_search_emergency_doctors():
    """Search emergency doctors by area or specialization"""
    try:
        area = request.args.get('area', '').strip()
        specialization = request.args.get('specialization', '').strip()
        
        doctors = _load_json('mumbai_doctors.json', [])
        
        if area:
            doctors = [d for d in doctors if d.get('area', '').lower() == area.lower()]
        
        if specialization:
            doctors = [d for d in doctors if specialization.lower() in d.get('specialization', '').lower()]
        
        return jsonify({'success': True, 'doctors': doctors})
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
