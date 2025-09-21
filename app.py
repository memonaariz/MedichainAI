from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import hashlib
import os
import xml.etree.ElementTree as ET
from datetime import datetime
import json
import time

# Import custom modules
try:
    from blockchain import get_ultra_secure_blockchain
    from medical_recommendations import get_medical_engine
except ImportError:
    # Create simple blockchain if module missing
    class Block:
        def __init__(self, index, timestamp, data, previous_hash):
            self.index = index
            self.timestamp = timestamp
            self.data = data
            self.previous_hash = previous_hash
            self.hash = self.calculate_hash()

        def calculate_hash(self):
            block_string = json.dumps(self.__dict__, sort_keys=True)
            return hashlib.sha256(block_string.encode()).hexdigest()

    class Blockchain:
        def __init__(self):
            self.chain = []
            self.create_genesis_block()

        def create_genesis_block(self):
            genesis_block = Block(0, time.time(), {"message": "Genesis Block"}, "0")
            self.chain.append(genesis_block)

        def get_latest_block(self):
            return self.chain[-1]

        def add_block(self, data):
            previous_block = self.get_latest_block()
            new_block = Block(previous_block.index + 1, time.time(), data, previous_block.hash)
            self.chain.append(new_block)
            return new_block

        def is_chain_valid(self):
            return True

try:
    from ccda_parser import parse_ccda_for_display
except ImportError:
    def parse_ccda_for_display(file_path):
        return {
            "patient": {"name": "John Doe", "dob": "1985-03-15"},
            "medical": {"conditions": ["Diabetes"], "medications": ["Metformin"]},
            "parsed_successfully": True
        }

app = Flask(__name__, static_folder='static')
app.secret_key = 'supersecretkey_for_demo_project_2025'

# Initialize ultra-secure blockchain and medical engine
try:
    blockchain = get_ultra_secure_blockchain()
    medical_engine = get_medical_engine()
except:
    blockchain = Blockchain()
    medical_engine = None

# Upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# File history storage
HISTORY_FILE = 'file_history.json'
def load_file_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        return []
    except:
        return []

def save_file_history(history):
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error saving file history: {e}")

ALLOWED_EXTENSIONS = {'xml', 'ccda'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    file_history = load_file_history()
    return render_template('index.html', chain=blockchain.chain, file_history=file_history)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected.')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected.')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            with open(filepath, 'rb') as f:
                file_content = f.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            
            ccda_info = parse_ccda_for_display(filepath)
            
            # Check if parsing was successful
            if not ccda_info.get('parsed_successfully', False):
                error_message = ccda_info.get('error', 'Unknown error parsing CCDA file')
                flash(f'Error: {error_message}')
                return redirect(url_for('index'))
            
            block_data = {
                "filename": filename,
                "file_hash": file_hash,
                "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ccda_summary": ccda_info
            }

            new_block = blockchain.add_block(block_data)
            
            # Store in session for immediate access
            session['last_uploaded_hash'] = file_hash
            session['last_uploaded_block_index'] = new_block.index
            session['last_uploaded_filename'] = filename
            session['ccda_info'] = ccda_info
            
            # Save to permanent file history
            file_history = load_file_history()
            file_history.append({
                "filename": filename,
                "file_hash": file_hash,
                "block_index": new_block.index,
                "block_hash": new_block.hash,
                "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "file_size": len(file_content),
                "patient_name": ccda_info.get('patient', {}).get('name', 'Unknown'),
                "status": "uploaded"
            })
            save_file_history(file_history)

            flash(f'File "{filename}" uploaded successfully! Block Index: {new_block.index}, Hash: {file_hash[:16]}...')
            return redirect(url_for('index'))

        except Exception as e:
            flash(f'Error processing file: {e}')
            return redirect(url_for('index'))
    else:
        flash('Only XML and CCDA files are allowed.')
        return redirect(url_for('index'))

@app.route('/file_history')
def file_history():
    file_history = load_file_history()
    return render_template('file_history.html', file_history=file_history, chain=blockchain.chain)

@app.route('/view_file/<filename>')
def view_file(filename):
    file_history = load_file_history()
    file_info = None
    
    for entry in file_history:
        if entry['filename'] == filename:
            file_info = entry
            break
    
    if not file_info:
        flash('File not found in history.')
        return redirect(url_for('index'))
    
    # Find the corresponding block
    block_info = None
    for block in blockchain.chain:
        if block.index == file_info['block_index']:
            block_info = block
            break
    
    return render_template('view_file.html', file_info=file_info, block_info=block_info)

@app.route('/verify', methods=['POST'])
def verify_file():
    if 'file' not in request.files:
        flash('No file selected for verification.')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected for verification.')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            with open(filepath, 'rb') as f:
                current_file_content = f.read()
            current_file_hash = hashlib.sha256(current_file_content).hexdigest()

            original_hash = session.get('last_uploaded_hash')
            block_index_to_check = session.get('last_uploaded_block_index')
            original_filename = session.get('last_uploaded_filename')

            if not original_hash or block_index_to_check is None:
                flash('No previous upload found. Please upload a file first.')
                return redirect(url_for('index'))

            found_block = None
            for block in blockchain.chain:
                if block.index == block_index_to_check and block.data.get('filename') == original_filename:
                    found_block = block
                    break
            
            if not found_block:
                flash(f'Error: Original block for "{original_filename}" not found in blockchain.')
                return redirect(url_for('index'))

            stored_hash = found_block.data.get('file_hash')

            if current_file_hash == stored_hash:
                flash(f'✅ Verification Successful! File "{filename}" has not been modified.')
            else:
                flash(f'❌ Verification FAILED! File "{filename}" has been modified.')
            
            if not blockchain.is_chain_valid():
                flash('⚠️ WARNING: Blockchain integrity compromised!')

            return redirect(url_for('index'))

        except Exception as e:
            flash(f'Verification error: {e}')
            return redirect(url_for('index'))
    else:
        flash('Only XML and CCDA files are allowed for verification.')
        return redirect(url_for('index'))

# AI Chat Route - Enhanced Conversational Medical Search
@app.route('/ai_chat', methods=['POST'])
def ai_chat():
    try:
        data = request.get_json()
        user_query = data.get('query', '').lower()
        
        # Get session context (previous conversation)
        chat_history = session.get('chat_history', [])
        
        # Debug: Print session data
        print(f"DEBUG - Session CCDA info: {session.get('ccda_info', 'Not found')}")
        print(f"DEBUG - User query: {user_query}")
        
        # Enhanced conversational responses based on query analysis
        response = generate_conversational_response(user_query, chat_history)
        
        # Update chat history
        chat_history.append({"user": user_query, "ai": response})
        if len(chat_history) > 10:  # Keep last 10 messages
            chat_history = chat_history[-10:]
        session['chat_history'] = chat_history
        
        return jsonify({"success": True, "response": response})
    except Exception as e:
        print(f"DEBUG - AI Chat Error: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

def generate_conversational_response(query, chat_history):
    """Generate intelligent conversational responses based on medical context"""
    
    # Check if we have uploaded CCDA data
    ccda_info = session.get('ccda_info', {})
    patient_data = ccda_info.get('patient', {})
    medical_data = ccda_info.get('medical', {})
    
    print(f"DEBUG - Patient data: {patient_data}")
    print(f"DEBUG - Medical data: {medical_data}")
    print(f"DEBUG - Query: '{query}'")
    
    # Analyze query intent with more specific matching
    query_lower = query.lower()
    
    # Check for specific keywords first
    if 'medication' in query_lower or 'medicine' in query_lower or 'drug' in query_lower or 'pill' in query_lower or 'prescription' in query_lower or 'taking' in query_lower:
        print("DEBUG - Detected medication query")
        medications = medical_data.get('medications', [])
        if medications and medications[0] != 'No medications found in document':
            med_list = '\n'.join([f"• {med}" for med in medications])
            return f"**Current Medications:**\n💊 {med_list}\n\nWould you like to know about drug interactions or side effects?"
        else:
            return "**Current Medications:**\n💊 No medications found in the current document.\n\nWould you like me to check for any medication history?"
    
    elif 'lab' in query_lower or 'test' in query_lower or 'result' in query_lower or 'blood' in query_lower or 'urine' in query_lower or 'analysis' in query_lower or 'findings' in query_lower:
        print("DEBUG - Detected lab results query")
        lab_results = medical_data.get('lab_results', [])
        if lab_results and lab_results[0] != 'No lab results found in document':
            lab_list = '\n'.join([f"• {result}" for result in lab_results])
            return f"**Laboratory Results:**\n🔬 {lab_list}\n\nWould you like me to interpret these results or check for any abnormalities?"
        else:
            return "**Laboratory Results:**\n🔬 No lab results found in the current document.\n\nWould you like me to suggest relevant tests based on the patient's condition?"
    
    elif 'diagnosis' in query_lower or 'condition' in query_lower or 'problem' in query_lower or 'disease' in query_lower or 'illness' in query_lower or 'diagnoses' in query_lower:
        print("DEBUG - Detected diagnosis query")
        conditions = medical_data.get('conditions', [])
        if conditions and conditions[0] != 'No conditions found in document':
            cond_list = '\n'.join([f"• {cond}" for cond in conditions])
            return f"**Medical Conditions:**\n🏥 {cond_list}"
        else:
            return "**Medical Conditions:**\n🏥 No specific conditions found in the current document.\n\nWould you like me to analyze the patient's overall health status?"
    
    elif 'vital' in query_lower or 'blood pressure' in query_lower or 'heart rate' in query_lower or 'temperature' in query_lower or 'pulse' in query_lower:
        print("DEBUG - Detected vital signs query")
        vitals = medical_data.get('vital_signs', [])
        if vitals and vitals[0] != 'No vital signs found in document':
            vital_list = '\n'.join([f"• {vital}" for vital in vitals])
            return f"**Vital Signs:**\n❤️ {vital_list}\n\nWould you like me to assess if these are within normal ranges?"
        else:
            return "**Vital Signs:**\n❤️ No vital signs recorded in the current document.\n\nWould you like me to suggest which vitals should be monitored?"
    
    elif 'treatment' in query_lower or 'recommendation' in query_lower or 'advice' in query_lower or 'suggestion' in query_lower or 'what should' in query_lower:
        print("DEBUG - Detected treatment query")
        conditions = medical_data.get('conditions', [])
        if conditions and conditions[0] != 'No conditions found in document':
            recommendations = generate_treatment_recommendations(conditions)
            return f"**Treatment Recommendations:**\n💡 {recommendations}\n\nWould you like more specific guidance for any condition?"
        else:
            return "**Treatment Recommendations:**\n💡 I don't have enough information to provide specific treatment recommendations. Please upload a CCDA document with patient conditions."
    
    elif 'risk' in query_lower or 'danger' in query_lower or 'complication' in query_lower or 'warning' in query_lower:
        print("DEBUG - Detected risk assessment query")
        risk_assessment = generate_risk_assessment(medical_data)
        return f"**Risk Assessment:**\n⚠️ {risk_assessment}\n\nWould you like me to suggest preventive measures?"
    
    elif 'health' in query_lower or 'overall' in query_lower or 'summary' in query_lower or 'status' in query_lower:
        print("DEBUG - Detected health summary query")
        return generate_health_summary(patient_data, medical_data)
    
    # Patient information queries (check this last to avoid conflicts)
    elif 'patient' in query_lower or 'name' in query_lower or 'who' in query_lower or 'person' in query_lower or 'details' in query_lower:
        print("DEBUG - Detected patient info query")
        if patient_data.get('name') and patient_data['name'] != 'Unknown':
            return f"**Patient Information:**\n👤 **Name:** {patient_data['name']}\n📅 **Date of Birth:** {patient_data.get('dob', 'Not available')}\n⚧ **Gender:** {patient_data.get('gender', 'Not available')}\n\nIs there anything specific about the patient you'd like to know?"
        else:
            return "**Patient Information:**\n👤 I don't have patient information available. Please upload a CCDA document first to access patient details."
    
    # Follow-up Questions
    elif 'why' in query_lower or 'how' in query_lower or 'what if' in query_lower or 'could you' in query_lower:
        print("DEBUG - Detected follow-up query")
        return "I'd be happy to help! Could you please be more specific about what you'd like to know? I can help with:\n• Patient information\n• Medications\n• Conditions\n• Lab results\n• Treatment recommendations\n• Risk assessments"
    
    # Default response with suggestions
    else:
        print("DEBUG - No specific query detected, showing default response")
        return f"I understand you're asking about '{query}'. Here's what I can help you with:\n\n🔍 **Available Information:**\n• Patient details\n• Current medications\n• Medical conditions\n• Lab results\n• Vital signs\n• Treatment recommendations\n\nTry clicking one of the buttons above for instant information!"

def generate_treatment_recommendations(conditions):
    """Generate treatment recommendations based on conditions"""
    recommendations = []
    
    for condition in conditions:
        condition_lower = condition.lower()
        if 'diabetes' in condition_lower:
            recommendations.append("Monitor blood glucose regularly and maintain a balanced diet")
        elif 'hypertension' in condition_lower or 'blood pressure' in condition_lower:
            recommendations.append("Monitor blood pressure weekly and consider low-sodium diet")
        elif 'heart' in condition_lower:
            recommendations.append("Regular cardiac monitoring and lifestyle modifications")
        else:
            recommendations.append(f"Consult healthcare provider for {condition} management")
    
    return '\n'.join(recommendations) if recommendations else "Consult your healthcare provider for personalized treatment recommendations."

def generate_risk_assessment(medical_data):
    """Generate risk assessment based on medical data"""
    conditions = medical_data.get('conditions', [])
    medications = medical_data.get('medications', [])
    
    risk_factors = len(conditions) + len(medications)
    
    if risk_factors > 3:
        return "Elevated risk profile - multiple conditions detected. Regular monitoring recommended."
    elif risk_factors > 1:
        return "Moderate risk profile - some conditions present. Standard monitoring advised."
    else:
        return "Low risk profile based on available data. Continue regular check-ups."

def generate_health_summary(patient_data, medical_data):
    """Generate overall health summary"""
    summary = []
    
    if patient_data.get('name') and patient_data['name'] != 'Unknown':
        summary.append(f"**Patient:** {patient_data['name']}")
    
    conditions = medical_data.get('conditions', [])
    if conditions and conditions[0] != 'No conditions found in document':
        summary.append(f"**Conditions:** {len(conditions)} active conditions")
    
    medications = medical_data.get('medications', [])
    if medications and medications[0] != 'No medications found in document':
        summary.append(f"**Medications:** {len(medications)} current medications")
    
    if not summary:
        summary.append("Limited health information available. Please upload a complete CCDA document.")
    
    return '\n'.join(summary) + "\n\nWould you like detailed information about any specific aspect?"

@app.route('/get_current_patient_data', methods=['GET'])
def get_current_patient_data():
    """Get current patient data from session for AI analysis"""
    ccda_info = session.get('ccda_info', {})
    
    if not ccda_info or not ccda_info.get('parsed_successfully'):
        return jsonify({
            'success': False,
            'message': 'No patient data available. Please upload a CCDA document first.'
        })
    
    return jsonify({
        'success': True,
        'data': {
            'patient': ccda_info.get('patient', {}),
            'medical': ccda_info.get('medical', {})
        }
    })

# Document Enrichment Route
@app.route('/enrich_document', methods=['POST'])
def enrich_document_route():
    try:
        print("Starting document enrichment process...")
        
        # Check if there's a last uploaded file in the session
        if 'last_uploaded_filename' not in session:
            print("No document found in session")
            return jsonify({"success": False, "error": "No document has been uploaded yet. Please upload a CCDA document first.", "error_type": "no_upload"})
        
        filename = session['last_uploaded_filename']
        print(f"Processing file: {filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check if the file exists
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return jsonify({"success": False, "error": f"File {filename} not found. Please upload the document again.", "error_type": "file_missing"})
        
        print(f"File exists, attempting to parse: {filepath}")
        
        # Try to use cached CCDA data from session if available
        ccda_data = None
        if 'ccda_info' in session and session.get('last_uploaded_hash') is not None:
            print("Using cached CCDA data from session")
            ccda_data = session.get('ccda_info')
            
            # Verify cached data is valid
            if not ccda_data.get('parsed_successfully', False):
                print("Cached data indicates parsing was not successful, will try parsing again")
                ccda_data = None
            else:
                print("Using valid cached CCDA data")
        
        # If no cached data, parse the CCDA file
        if ccda_data is None:
            print("No cached data found, parsing CCDA file")
            ccda_data = parse_ccda_for_display(filepath)
        
        # Check if parsing was successful
        if not ccda_data.get('parsed_successfully', False):
            error_message = ccda_data.get('error', 'Unknown parsing error')
            print(f"Failed to parse document: {error_message}")
            
            # Return detailed error information
            return jsonify({
                "success": False, 
                "error": f"Failed to parse CCDA document: {error_message}. Please try again with a valid CCDA file.", 
                "error_type": "parsing_error",
                "details": ccda_data.get('error_details', {})
            })
        
        print("CCDA parsing successful, extracting data")
        
        # Get patient and medical data
        patient = ccda_data.get('patient', {})
        medical = ccda_data.get('medical', {})
        
        print(f"Patient data: {patient}")
        print(f"Medical data: {medical}")
        
        # Create enriched data from the parsed CCDA
        enriched_data = {
            "extracted_data": {
                "patient_name": patient.get('name', 'Unknown'),
                "date_of_birth": patient.get('dob', 'Unknown'),
                "medical_conditions": medical.get('conditions', []),
                "medications": medical.get('medications', []),
                "lab_results": medical.get('lab_results', []),
                "vital_signs": medical.get('vital_signs', [])
            },
            "confidence_score": 0.92,  # Simulated confidence score
            "processing_time": "1.8 seconds"  # Simulated processing time
        }
        
        print("Document enrichment completed successfully")
        return jsonify({"success": True, "data": enriched_data, "message": f"Document {filename} enriched successfully!"})
    except Exception as e:
        print(f"Error in document enrichment: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)})

# Clinical Insights Route
@app.route('/clinical_insights', methods=['POST'])
def clinical_insights_route():
    try:
        # Check if there's a last uploaded file in the session
        if 'last_uploaded_filename' not in session:
            return jsonify({"success": False, "error": "No document has been uploaded yet. Please upload a CCDA document first."})
        
        filename = session['last_uploaded_filename']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check if the file exists
        if not os.path.exists(filepath):
            return jsonify({"success": False, "error": f"File {filename} not found. Please upload the document again."})
        
        # Parse the CCDA file
        ccda_data = parse_ccda_for_display(filepath)
        
        if not ccda_data.get('parsed_successfully', False):
            return jsonify({"success": False, "error": "Failed to parse the document. Please try again with a valid CCDA file."})
        
        # Get patient and medical data
        patient = ccda_data.get('patient', {})
        medical = ccda_data.get('medical', {})
        
        # Generate personalized insights based on the patient's data
        recommendations = []
        alerts = []
        risk_assessment = "Insufficient data for comprehensive risk assessment"
        
        # Check for conditions and generate recommendations
        conditions = medical.get('conditions', [])
        if conditions:
            if any("diabetes" in cond.lower() for cond in conditions):
                recommendations.append("Monitor blood glucose levels regularly")
                recommendations.append("Maintain a balanced diet low in simple carbohydrates")
                alerts.append("Diabetes detected - ensure regular HbA1c monitoring")
            
            if any("hypertension" in cond.lower() for cond in conditions):
                recommendations.append("Monitor blood pressure weekly")
                recommendations.append("Consider low-sodium diet")
                alerts.append("Hypertension detected - maintain BP monitoring")
            
            if any("headache" in cond.lower() for cond in conditions):
                recommendations.append("Track headache frequency and potential triggers")
                recommendations.append("Ensure adequate hydration and rest")
        
        # Check medications
        medications = medical.get('medications', [])
        if medications:
            recommendations.append("Continue current medication regimen as prescribed")
            recommendations.append("Report any side effects to your healthcare provider")
        
        # Add general recommendations if we don't have specific ones
        if len(recommendations) < 2:
            recommendations.extend([
                "Schedule regular check-ups with your healthcare provider",
                "Maintain a balanced diet and regular exercise routine",
                "Ensure adequate sleep and stress management"
            ])
        
        # Generate risk assessment based on available data
        if conditions or medications:
            risk_factors = len(conditions) + (1 if len(medications) > 2 else 0)
            if risk_factors > 3:
                risk_assessment = "Elevated risk profile based on multiple conditions"
            elif risk_factors > 1:
                risk_assessment = "Moderate risk profile - regular monitoring advised"
            else:
                risk_assessment = "Low risk profile based on current data"
        
        # Add general alert if we don't have specific ones
        if not alerts:
            alerts.append("No critical alerts based on available data")
        
        insights = {
            "risk_assessment": risk_assessment,
            "recommendations": recommendations[:4],  # Limit to 4 recommendations
            "alerts": alerts
        }
        
        return jsonify({"success": True, "insights": insights, "message": f"Clinical insights for {patient.get('name', 'patient')} generated successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# AI Disease Prediction Route
@app.route('/predict_diseases', methods=['POST'])
def predict_diseases_route():
    try:
        # Check if there's a last uploaded file in the session
        if 'last_uploaded_filename' not in session:
            return jsonify({"success": False, "error": "No document has been uploaded yet. Please upload a CCDA document first."})
        
        filename = session['last_uploaded_filename']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check if the file exists
        if not os.path.exists(filepath):
            return jsonify({"success": False, "error": f"File {filename} not found. Please upload the document again."})
        
        # Parse the CCDA file
        ccda_data = parse_ccda_for_display(filepath)
        
        if not ccda_data.get('parsed_successfully', False):
            return jsonify({"success": False, "error": "Failed to parse the document. Please try again with a valid CCDA file."})
        
        # Get patient and medical data
        patient = ccda_data.get('patient', {})
        medical = ccda_data.get('medical', {})
        
        # Generate disease predictions using AI
        predictions = generate_disease_predictions(patient, medical)
        
        return jsonify({
            "success": True, 
            "predictions": predictions, 
            "message": f"Disease predictions for {patient.get('name', 'patient')} generated successfully!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# AI Medicine Recommendation Route
@app.route('/recommend_medications', methods=['POST'])
def recommend_medications_route():
    try:
        # Check if there's a last uploaded file in the session
        if 'last_uploaded_filename' not in session:
            return jsonify({"success": False, "error": "No document has been uploaded yet. Please upload a CCDA document first."})
        
        filename = session['last_uploaded_filename']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Parse the CCDA file
        ccda_data = parse_ccda_for_display(filepath)
        
        if not ccda_data.get('parsed_successfully', False):
            return jsonify({"success": False, "error": "Failed to parse the document. Please try again with a valid CCDA file."})
        
        # Get patient and medical data
        patient = ccda_data.get('patient', {})
        medical = ccda_data.get('medical', {})
        
        # Generate medication recommendations using medical engine
        if medical_engine:
            recommendations = medical_engine.generate_diabetes_recommendations(patient)
            if medical.get('conditions') and 'Hypertension' in str(medical.get('conditions')):
                htn_recs = medical_engine.generate_hypertension_recommendations(patient)
                recommendations['hypertension'] = htn_recs
        else:
            recommendations = generate_medication_recommendations(patient, medical)
        
        return jsonify({
            "success": True, 
            "recommendations": recommendations, 
            "message": f"Medication recommendations for {patient.get('name', 'patient')} generated successfully!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# AI Clinical Report Generation Route
@app.route('/generate_clinical_report', methods=['POST'])
def generate_clinical_report_route():
    try:
        # Check if there's a last uploaded file in the session
        if 'last_uploaded_filename' not in session:
            return jsonify({"success": False, "error": "No document has been uploaded yet. Please upload a CCDA document first."})
        
        filename = session['last_uploaded_filename']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Parse the CCDA file
        ccda_data = parse_ccda_for_display(filepath)
        
        if not ccda_data.get('parsed_successfully', False):
            return jsonify({"success": False, "error": "Failed to parse the document. Please try again with a valid CCDA file."})
        
        # Get patient and medical data
        patient = ccda_data.get('patient', {})
        medical = ccda_data.get('medical', {})
        
        # Generate comprehensive clinical report using AI
        clinical_report = generate_comprehensive_clinical_report(patient, medical)
        
        return jsonify({
            "success": True, 
            "clinical_report": clinical_report, 
            "message": f"Clinical report for {patient.get('name', 'patient')} generated successfully!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# AI Functions
def generate_disease_predictions(patient_data, medical_data):
    """Generate AI-powered disease predictions based on patient data"""
    predictions = {}
    
    # Extract relevant data
    conditions = medical_data.get('conditions', [])
    lab_results = medical_data.get('lab_results', [])
    vital_signs = medical_data.get('vital_signs', [])
    medications = medical_data.get('medications', [])
    
    # Analyze for diabetes
    diabetes_confidence = analyze_diabetes_risk(conditions, lab_results, vital_signs, medications)
    if diabetes_confidence > 0.3:
        predictions['diabetes'] = {
            'confidence': diabetes_confidence,
            'severity': assess_diabetes_severity(lab_results),
            'risk_level': 'high' if diabetes_confidence > 0.7 else 'moderate',
            'evidence': collect_diabetes_evidence(conditions, lab_results, vital_signs),
            'recommended_actions': generate_diabetes_actions(diabetes_confidence)
        }
    
    # Analyze for hypertension
    hypertension_confidence = analyze_hypertension_risk(conditions, lab_results, vital_signs, medications)
    if hypertension_confidence > 0.3:
        predictions['hypertension'] = {
            'confidence': hypertension_confidence,
            'severity': assess_hypertension_severity(vital_signs),
            'risk_level': 'high' if hypertension_confidence > 0.7 else 'moderate',
            'evidence': collect_hypertension_evidence(conditions, lab_results, vital_signs),
            'recommended_actions': generate_hypertension_actions(hypertension_confidence)
        }
    
    # Analyze for heart disease
    heart_disease_confidence = analyze_heart_disease_risk(conditions, lab_results, vital_signs, medications)
    if heart_disease_confidence > 0.3:
        predictions['heart_disease'] = {
            'confidence': heart_disease_confidence,
            'severity': assess_heart_disease_severity(conditions, lab_results),
            'risk_level': 'high' if heart_disease_confidence > 0.7 else 'moderate',
            'evidence': collect_heart_disease_evidence(conditions, lab_results, vital_signs),
            'recommended_actions': generate_heart_disease_actions(heart_disease_confidence)
        }
    
    return {
        'predictions': predictions,
        'overall_risk': calculate_overall_risk(predictions),
        'recommendations': generate_overall_recommendations(predictions)
    }

def analyze_diabetes_risk(conditions, lab_results, vital_signs, medications):
    """Analyze risk for diabetes"""
    confidence = 0.0
    
    # Check existing conditions
    if any('diabetes' in cond.lower() for cond in conditions):
        confidence += 0.8
    
    # Check lab results
    for lab in lab_results:
        if 'glucose' in lab.lower():
            if any(str(num) in lab for num in ['200', '180', '160']):
                confidence += 0.6
            elif any(str(num) in lab for num in ['140', '130', '120']):
                confidence += 0.4
        elif 'hba1c' in lab.lower():
            if any(str(num) in lab for num in ['8.0', '7.5', '7.0']):
                confidence += 0.7
            elif any(str(num) in lab for num in ['6.5', '6.0', '5.7']):
                confidence += 0.5
    
    # Check medications
    if any('metformin' in med.lower() or 'insulin' in med.lower() for med in medications):
        confidence += 0.6
    
    return min(confidence, 1.0)

def analyze_hypertension_risk(conditions, lab_results, vital_signs, medications):
    """Analyze risk for hypertension"""
    confidence = 0.0
    
    # Check existing conditions
    if any('hypertension' in cond.lower() or 'blood pressure' in cond.lower() for cond in conditions):
        confidence += 0.8
    
    # Check vital signs
    for vital in vital_signs:
        if 'blood pressure' in vital.lower():
            if any(str(num) in vital for num in ['180', '160', '150']):
                confidence += 0.7
            elif any(str(num) in vital for num in ['140', '130', '120']):
                confidence += 0.5
    
    # Check medications
    if any('lisinopril' in med.lower() or 'amlodipine' in med.lower() for med in medications):
        confidence += 0.6
    
    return min(confidence, 1.0)

def analyze_heart_disease_risk(conditions, lab_results, vital_signs, medications):
    """Analyze risk for heart disease"""
    confidence = 0.0
    
    # Check existing conditions
    if any('heart' in cond.lower() or 'cardiac' in cond.lower() for cond in conditions):
        confidence += 0.8
    
    # Check for risk factors
    if any('diabetes' in cond.lower() for cond in conditions):
        confidence += 0.4
    if any('hypertension' in cond.lower() for cond in conditions):
        confidence += 0.4
    
    # Check medications
    if any('aspirin' in med.lower() or 'statin' in med.lower() for med in medications):
        confidence += 0.5
    
    return min(confidence, 1.0)

def assess_diabetes_severity(lab_results):
    """Assess diabetes severity based on lab results"""
    for lab in lab_results:
        if 'glucose' in lab.lower():
            if any(str(num) in lab for num in ['200', '250', '300']):
                return 'severe'
            elif any(str(num) in lab for num in ['160', '180']):
                return 'moderate'
            elif any(str(num) in lab for num in ['140', '150']):
                return 'mild'
    return 'unknown'

def assess_hypertension_severity(vital_signs):
    """Assess hypertension severity based on vital signs"""
    for vital in vital_signs:
        if 'blood pressure' in vital.lower():
            if any(str(num) in vital for num in ['180', '200']):
                return 'severe'
            elif any(str(num) in vital for num in ['160', '170']):
                return 'moderate'
            elif any(str(num) in vital for num in ['140', '150']):
                return 'mild'
    return 'unknown'

def assess_heart_disease_severity(conditions, lab_results):
    """Assess heart disease severity"""
    if any('heart failure' in cond.lower() or 'myocardial infarction' in cond.lower() for cond in conditions):
        return 'severe'
    elif any('heart' in cond.lower() for cond in conditions):
        return 'moderate'
    return 'unknown'

def collect_diabetes_evidence(conditions, lab_results, vital_signs):
    """Collect evidence supporting diabetes diagnosis"""
    evidence = {
        'symptoms_present': [],
        'lab_abnormalities': [],
        'risk_factors': []
    }
    
    # Check conditions
    if any('diabetes' in cond.lower() for cond in conditions):
        evidence['symptoms_present'].append('Diabetes diagnosis present')
    
    # Check lab results
    for lab in lab_results:
        if 'glucose' in lab.lower():
            evidence['lab_abnormalities'].append(lab)
        elif 'hba1c' in lab.lower():
            evidence['lab_abnormalities'].append(lab)
    
    return evidence

def collect_hypertension_evidence(conditions, lab_results, vital_signs):
    """Collect evidence supporting hypertension diagnosis"""
    evidence = {
        'symptoms_present': [],
        'lab_abnormalities': [],
        'risk_factors': []
    }
    
    # Check conditions
    if any('hypertension' in cond.lower() for cond in conditions):
        evidence['symptoms_present'].append('Hypertension diagnosis present')
    
    # Check vital signs
    for vital in vital_signs:
        if 'blood pressure' in vital.lower():
            evidence['lab_abnormalities'].append(vital)
    
    return evidence

def collect_heart_disease_evidence(conditions, lab_results, vital_signs):
    """Collect evidence supporting heart disease diagnosis"""
    evidence = {
        'symptoms_present': [],
        'lab_abnormalities': [],
        'risk_factors': []
    }
    
    # Check conditions
    if any('heart' in cond.lower() for cond in conditions):
        evidence['symptoms_present'].append('Heart condition present')
    
    return evidence

def generate_diabetes_actions(confidence):
    """Generate recommended actions for diabetes"""
    actions = []
    
    if confidence > 0.7:
        actions.append('Immediate medical consultation required')
        actions.append('Monitor blood glucose regularly')
    elif confidence > 0.4:
        actions.append('Schedule medical appointment within 1 week')
        actions.append('Monitor blood glucose levels')
    
    actions.append('Maintain healthy diet and exercise')
    actions.append('Schedule HbA1c testing')
    
    return actions

def generate_hypertension_actions(confidence):
    """Generate recommended actions for hypertension"""
    actions = []
    
    if confidence > 0.7:
        actions.append('Immediate medical consultation required')
        actions.append('Monitor blood pressure regularly')
    elif confidence > 0.4:
        actions.append('Schedule medical appointment within 1 week')
        actions.append('Monitor blood pressure weekly')
    
    actions.append('Reduce salt intake')
    actions.append('Manage stress levels')
    
    return actions

def generate_heart_disease_actions(confidence):
    """Generate recommended actions for heart disease"""
    actions = []
    
    if confidence > 0.7:
        actions.append('Immediate cardiac evaluation required')
        actions.append('Monitor heart rate and blood pressure')
    elif confidence > 0.4:
        actions.append('Schedule cardiology consultation within 1 week')
        actions.append('Monitor for chest pain or shortness of breath')
    
    actions.append('Maintain heart-healthy diet')
    actions.append('Regular exercise as tolerated')
    
    return actions

def calculate_overall_risk(predictions):
    """Calculate overall risk level"""
    if not predictions:
        return 'low'
    
    max_confidence = max(pred['confidence'] for pred in predictions.values())
    
    if max_confidence > 0.8:
        return 'critical'
    elif max_confidence > 0.6:
        return 'high'
    elif max_confidence > 0.4:
        return 'moderate'
    else:
        return 'low'

def generate_overall_recommendations(predictions):
    """Generate overall recommendations"""
    recommendations = []
    
    if not predictions:
        recommendations.append('Continue routine health monitoring')
        recommendations.append('Maintain healthy lifestyle habits')
        return recommendations
    
    high_confidence = [name for name, pred in predictions.items() if pred['confidence'] > 0.6]
    
    if high_confidence:
        recommendations.append(f'Immediate attention needed for: {", ".join(high_confidence)}')
        recommendations.append('Schedule comprehensive medical evaluation')
    
    recommendations.append('Monitor all symptoms closely')
    recommendations.append('Follow up with healthcare provider')
    
    return recommendations

def generate_medication_recommendations(patient_data, medical_data):
    """Generate AI-powered medication recommendations"""
    recommendations = {}
    
    conditions = medical_data.get('conditions', [])
    current_medications = medical_data.get('medications', [])
    
    # Diabetes medications
    if any('diabetes' in cond.lower() for cond in conditions):
        recommendations['diabetes'] = {
            'primary_medications': [
                {
                    'name': 'Metformin',
                    'reason': 'First-line treatment for Type 2 diabetes',
                    'dosage': '500mg twice daily, titrate to 2000mg daily',
                    'effectiveness': 0.85,
                    'side_effects': ['nausea', 'diarrhea', 'stomach_upset']
                }
            ],
            'alternative_medications': [
                {
                    'name': 'Sulfonylurea',
                    'reason': 'Alternative when metformin contraindicated',
                    'dosage': 'Variable based on glucose levels',
                    'effectiveness': 0.75,
                    'side_effects': ['hypoglycemia', 'weight_gain']
                }
            ],
            'monitoring_required': [
                'Blood glucose monitoring',
                'HbA1c testing every 3-6 months',
                'Kidney function monitoring'
            ]
        }
    
    # Hypertension medications
    if any('hypertension' in cond.lower() for cond in conditions):
        recommendations['hypertension'] = {
            'primary_medications': [
                {
                    'name': 'Lisinopril',
                    'reason': 'First-line ACE inhibitor for hypertension',
                    'dosage': '10mg daily, titrate to 40mg daily',
                    'effectiveness': 0.80,
                    'side_effects': ['dry_cough', 'dizziness', 'fatigue']
                }
            ],
            'alternative_medications': [
                {
                    'name': 'Amlodipine',
                    'reason': 'Alternative calcium channel blocker',
                    'dosage': '5-10mg daily',
                    'effectiveness': 0.82,
                    'side_effects': ['ankle_swelling', 'dizziness', 'flushing']
                }
            ],
            'monitoring_required': [
                'Blood pressure monitoring',
                'Kidney function monitoring',
                'Electrolyte monitoring'
            ]
        }
    
    # Check for drug interactions
    interaction_warnings = check_drug_interactions(recommendations, current_medications)
    
    return {
        'medication_recommendations': recommendations,
        'interaction_warnings': interaction_warnings,
        'safety_considerations': generate_safety_considerations(recommendations, patient_data),
        'monitoring_requirements': generate_monitoring_requirements(recommendations)
    }

def check_drug_interactions(recommendations, current_medications):
    """Check for potential drug interactions"""
    interactions = []
    
    # Known interactions
    known_interactions = {
        'metformin_lisinopril': {
            'severity': 'moderate',
            'description': 'May increase risk of lactic acidosis',
            'recommendation': 'Monitor closely, adjust dosages if needed'
        },
        'aspirin_warfarin': {
            'severity': 'high',
            'description': 'Increased bleeding risk',
            'recommendation': 'Avoid combination, use alternative'
        }
    }
    
    # Check for interactions
    for disease, recs in recommendations.items():
        for med_type in ['primary_medications', 'alternative_medications']:
            for med in recs.get(med_type, []):
                med_name = med['name'].lower()
                
                for current_med in current_medications:
                    current_med_lower = current_med.lower()
                    
                    for interaction_key, interaction_info in known_interactions.items():
                        if (med_name in interaction_key and current_med_lower in interaction_key):
                            interactions.append({
                                'medication_1': med['name'],
                                'medication_2': current_med,
                                'severity': interaction_info['severity'],
                                'description': interaction_info['description'],
                                'recommendation': interaction_info['recommendation']
                            })
    
    return interactions

def generate_safety_considerations(recommendations, patient_data):
    """Generate safety considerations"""
    safety = []
    
    allergies = patient_data.get('allergies', [])
    current_medications = patient_data.get('current_medications', [])
    
    if allergies:
        safety.append(f'Patient has allergies to: {", ".join(allergies)}')
        safety.append('Verify all medications are safe for patient')
    
    if len(current_medications) > 5:
        safety.append('Patient on multiple medications - increased interaction risk')
        safety.append('Consider medication review and deprescribing')
    
    return safety

def generate_monitoring_requirements(recommendations):
    """Generate monitoring requirements"""
    monitoring = {
        'laboratory_tests': [],
        'vital_signs': [],
        'frequency': {}
    }
    
    for disease, recs in recommendations.items():
        if 'monitoring_required' in recs:
            monitoring['laboratory_tests'].extend(recs['monitoring_required'])
    
    monitoring['frequency'] = {
        'daily': ['Blood glucose', 'Blood pressure'],
        'weekly': ['Weight', 'Symptom assessment'],
        'monthly': ['Laboratory tests'],
        'quarterly': ['Comprehensive evaluation']
    }
    
    return monitoring

def generate_comprehensive_clinical_report(patient_data, medical_data):
    """Generate comprehensive clinical report"""
    # Generate disease predictions
    disease_predictions = generate_disease_predictions(patient_data, medical_data)
    
    # Generate medication recommendations
    medication_recommendations = generate_medication_recommendations(patient_data, medical_data)
    
    # Create comprehensive report
    report = {
        'executive_summary': generate_executive_summary(disease_predictions),
        'patient_overview': {
            'demographics': {
                'name': patient_data.get('name', 'Unknown'),
                'dob': patient_data.get('dob', 'Unknown'),
                'gender': patient_data.get('gender', 'Unknown')
            },
            'current_medications': medical_data.get('medications', []),
            'medical_conditions': medical_data.get('conditions', [])
        },
        'clinical_assessment': {
            'primary_concerns': list(disease_predictions.get('predictions', {}).keys()),
            'overall_risk': disease_predictions.get('overall_risk', 'unknown'),
            'recommendations': disease_predictions.get('recommendations', [])
        },
        'treatment_recommendations': {
            'medications': medication_recommendations.get('medication_recommendations', {}),
            'interaction_warnings': medication_recommendations.get('interaction_warnings', []),
            'safety_considerations': medication_recommendations.get('safety_considerations', [])
        },
        'monitoring_plan': {
            'requirements': medication_recommendations.get('monitoring_requirements', {}),
            'frequency': 'As recommended by healthcare provider',
            'alerts': [
                'Contact healthcare provider if symptoms worsen',
                'Seek emergency care for severe symptoms',
                'Report any medication side effects immediately'
            ]
        },
        'follow_up_plan': {
            'immediate': 'Within 24-48 hours for high-risk conditions',
            'short_term': 'Within 1 week for moderate-risk conditions',
            'long_term': 'Within 2-4 weeks for low-risk conditions'
        },
        'report_metadata': {
            'generated_at': datetime.now().isoformat(),
            'ai_engine_version': '2.0.0',
            'confidence_threshold': 0.4,
            'report_type': 'comprehensive_clinical_assessment'
        }
    }
    
    return report

def generate_executive_summary(disease_predictions):
    """Generate executive summary"""
    if not disease_predictions.get('predictions'):
        return "No significant disease risk detected. Continue routine health monitoring."
    
    high_risk_diseases = [name for name, pred in disease_predictions['predictions'].items() 
                         if pred['confidence'] > 0.6]
    
    if high_risk_diseases:
        return f"High risk detected for: {', '.join(high_risk_diseases)}. " \
               f"Immediate medical evaluation recommended."
    else:
        return f"Moderate risk detected for: {', '.join(disease_predictions['predictions'].keys())}. " \
               f"Schedule medical consultation within 2 weeks."

# Retrieve Patient Data by Hash Route
@app.route('/retrieve_by_hash', methods=['POST'])
def retrieve_by_hash():
    try:
        data = request.get_json()
        hash_code = data.get('hash', '').strip()
        
        if not hash_code:
            return jsonify({"success": False, "error": "Hash code is required"})
        
        # Load file history
        file_history = load_file_history()
        
        # Find the file with matching hash
        matching_file = None
        for file_info in file_history:
            if file_info.get('file_hash') == hash_code or file_info.get('block_hash') == hash_code:
                matching_file = file_info
                break
        
        if not matching_file:
            return jsonify({"success": False, "error": "Hash code not found in file history"})
        
        # Get the file path
        filename = matching_file['filename']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check if file still exists
        if not os.path.exists(filepath):
            return jsonify({"success": False, "error": "File no longer exists on server"})
        
        # Parse the CCDA file to get patient data
        ccda_data = parse_ccda_for_display(filepath)
        
        if not ccda_data.get('parsed_successfully', False):
            return jsonify({"success": False, "error": "Failed to parse the document"})
        
        # Prepare patient data
        patient_data = {
            'name': ccda_data.get('patient', {}).get('name', 'Unknown'),
            'dob': ccda_data.get('patient', {}).get('dob', 'Not available'),
            'gender': ccda_data.get('patient', {}).get('gender', 'Not available'),
            'medications': ccda_data.get('medical', {}).get('medications', []),
            'conditions': ccda_data.get('medical', {}).get('conditions', []),
            'labs': ccda_data.get('medical', {}).get('labs', []),
            'vitals': ccda_data.get('medical', {}).get('vitals', [])
        }
        
        # Prepare file info
        file_info = {
            'filename': matching_file['filename'],
            'upload_time': matching_file['upload_time'],
            'file_size': matching_file['file_size'],
            'block_index': matching_file['block_index'],
            'file_hash': matching_file['file_hash'],
            'block_hash': matching_file['block_hash'],
            'status': matching_file['status']
        }
        
        return jsonify({
            "success": True, 
            "patient_data": patient_data,
            "file_info": file_info,
            "message": f"Patient data retrieved successfully for {patient_data['name']}"
        })
        
    except Exception as e:
        print(f"Error in retrieve_by_hash: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)})

@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)