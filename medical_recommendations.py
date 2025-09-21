# medical_recommendations.py - Simple Medical Recommendations
from datetime import datetime

class SimpleMedicalEngine:
    """Simple Medical Recommendation Engine"""
    
    def __init__(self):
        self.medical_database = self._initialize_medical_database()
        self.dosage_guidelines = self._initialize_dosage_guidelines()
    
    def _initialize_medical_database(self):
        """Initialize basic medical database"""
        return {
            'diabetes': {
                'condition': 'Type 2 Diabetes Mellitus',
                'medication': 'Metformin Hydrochloride',
                'dosage': '500mg twice daily with meals',
                'titration': 'Increase by 500mg every 1-2 weeks',
                'target_dose': '1000mg twice daily (2000mg total daily)',
                'monitoring': 'Blood glucose 2-4 times daily, HbA1c every 3 months',
                'lifestyle': 'Low glycemic diet, 150 minutes exercise weekly, weight management'
            },
            'hypertension': {
                'condition': 'Essential Hypertension',
                'medication': 'Lisinopril',
                'dosage': '10mg once daily',
                'titration': 'Increase by 10mg every 2-4 weeks',
                'target_dose': '20-40mg once daily',
                'monitoring': 'Blood pressure daily, kidney function every 3-6 months',
                'lifestyle': 'DASH diet, sodium restriction, 30 minutes exercise daily'
            }
        }
    
    def _initialize_dosage_guidelines(self):
        """Initialize dosage guidelines"""
        return {
            'metformin': {
                'starting': '500mg twice daily',
                'maximum': '2550mg daily',
                'frequency': '2-3 times daily with meals',
                'adjustment': 'Every 1-2 weeks based on tolerance'
            },
            'lisinopril': {
                'starting': '10mg once daily',
                'maximum': '80mg daily',
                'frequency': 'Once daily',
                'adjustment': 'Every 2-4 weeks based on response'
            }
        }
    
    def generate_diabetes_recommendations(self, patient_data):
        """Generate diabetes recommendations"""
        base_rec = self.medical_database['diabetes'].copy()
        
        # Add patient-specific adjustments
        if patient_data.get('age', 0) > 65:
            base_rec['dosage'] = '500mg once daily initially'
            base_rec['titration'] = 'Increase more slowly - every 2-3 weeks'
        
        if patient_data.get('weight', 0) > 100:
            base_rec['target_dose'] = '1000mg three times daily (3000mg total daily)'
        
        return base_rec
    
    def generate_hypertension_recommendations(self, patient_data):
        """Generate hypertension recommendations"""
        base_rec = self.medical_database['hypertension'].copy()
        
        # Add patient-specific adjustments
        if patient_data.get('age', 0) > 65:
            base_rec['dosage'] = '5mg once daily initially'
            base_rec['titration'] = 'Increase more slowly - every 3-4 weeks'
        
        if patient_data.get('systolic_bp', 0) > 160:
            base_rec['target_dose'] = '40mg once daily'
        
        return base_rec
    
    def get_general_health_tips(self):
        """Get general health tips"""
        return {
            'diet': 'Eat a balanced diet with plenty of fruits, vegetables, and whole grains',
            'exercise': 'Aim for 150 minutes of moderate exercise per week',
            'sleep': 'Get 7-9 hours of quality sleep each night',
            'stress': 'Practice stress management techniques like meditation or deep breathing',
            'checkups': 'Schedule regular health checkups with your doctor'
        }

# Factory function for compatibility
def get_medical_engine():
    """Get a medical engine instance"""
    return SimpleMedicalEngine()

if __name__ == "__main__":
    # Test the medical engine
    print("🏥 Testing MediChain AI Medical Engine...")
    
    engine = SimpleMedicalEngine()
    
    # Test diabetes recommendations
    patient_data = {'age': 45, 'weight': 80, 'glucose': 180}
    diabetes_rec = engine.generate_diabetes_recommendations(patient_data)
    
    print("Diabetes Recommendations:")
    print(f"Medication: {diabetes_rec['medication']}")
    print(f"Dosage: {diabetes_rec['dosage']}")
    print(f"Target: {diabetes_rec['target_dose']}")
    
    # Test hypertension recommendations
    htn_rec = engine.generate_hypertension_recommendations(patient_data)
    
    print("\nHypertension Recommendations:")
    print(f"Medication: {htn_rec['medication']}")
    print(f"Dosage: {htn_rec['dosage']}")
    print(f"Target: {htn_rec['target_dose']}") 