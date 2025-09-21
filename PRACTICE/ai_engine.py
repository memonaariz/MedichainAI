# ai_engine.py - Advanced AI Engine for Healthcare Intelligence
import json
import numpy as np
from datetime import datetime, timedelta
import hashlib
import logging
from typing import Dict, List, Tuple, Optional, Any
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthcareAIEngine:
    """
    Advanced AI Engine for Healthcare Intelligence
    Provides disease prediction, medicine recommendation, and clinical analytics
    """
    
    def __init__(self):
        self.medical_knowledge_base = self._initialize_medical_knowledge()
        self.prediction_models = self._initialize_prediction_models()
        self.medicine_database = self._initialize_medicine_database()
        self.clinical_rules = self._initialize_clinical_rules()
        
    def _initialize_medical_knowledge(self) -> Dict:
        """Initialize comprehensive medical knowledge base"""
        return {
            'diseases': {
                'diabetes': {
                    'symptoms': ['frequent urination', 'excessive thirst', 'fatigue', 'blurred vision'],
                    'risk_factors': ['age > 45', 'family_history', 'obesity', 'sedentary_lifestyle'],
                    'complications': ['heart_disease', 'kidney_disease', 'eye_damage', 'nerve_damage'],
                    'severity_levels': ['mild', 'moderate', 'severe']
                },
                'hypertension': {
                    'symptoms': ['headache', 'shortness of breath', 'nosebleeds', 'chest pain'],
                    'risk_factors': ['high_salt_diet', 'stress', 'alcohol_consumption', 'lack_of_exercise'],
                    'complications': ['stroke', 'heart_attack', 'kidney_disease', 'vision_loss'],
                    'severity_levels': ['pre_hypertension', 'stage_1', 'stage_2', 'crisis']
                },
                'heart_disease': {
                    'symptoms': ['chest_pain', 'shortness_of_breath', 'fatigue', 'irregular_heartbeat'],
                    'risk_factors': ['smoking', 'high_cholesterol', 'diabetes', 'family_history'],
                    'complications': ['heart_attack', 'stroke', 'heart_failure', 'arrhythmia'],
                    'severity_levels': ['low_risk', 'moderate_risk', 'high_risk', 'critical']
                },
                'asthma': {
                    'symptoms': ['wheezing', 'shortness_of_breath', 'chest_tightness', 'coughing'],
                    'risk_factors': ['allergies', 'family_history', 'respiratory_infections', 'environmental_triggers'],
                    'complications': ['respiratory_failure', 'pneumonia', 'sleep_disturbance'],
                    'severity_levels': ['intermittent', 'mild_persistent', 'moderate_persistent', 'severe_persistent']
                }
            },
            'lab_ranges': {
                'glucose_fasting': {'normal': (70, 100), 'prediabetes': (100, 126), 'diabetes': (126, float('inf'))},
                'hba1c': {'normal': (0, 5.7), 'prediabetes': (5.7, 6.4), 'diabetes': (6.4, float('inf'))},
                'cholesterol_total': {'normal': (0, 200), 'borderline': (200, 239), 'high': (240, float('inf'))},
                'blood_pressure_systolic': {'normal': (0, 120), 'elevated': (120, 129), 'high': (130, float('inf'))},
                'blood_pressure_diastolic': {'normal': (0, 80), 'elevated': (80, 89), 'high': (90, float('inf'))}
            }
        }
    
    def _initialize_prediction_models(self) -> Dict:
        """Initialize AI prediction models"""
        return {
            'disease_prediction': self._create_disease_prediction_model(),
            'risk_assessment': self._create_risk_assessment_model(),
            'treatment_effectiveness': self._create_treatment_effectiveness_model()
        }
    
    def _initialize_medicine_database(self) -> Dict:
        """Initialize comprehensive medicine database"""
        return {
            'diabetes_medications': {
                'metformin': {
                    'class': 'biguanide',
                    'mechanism': 'reduces_glucose_production',
                    'side_effects': ['nausea', 'diarrhea', 'stomach_upset'],
                    'contraindications': ['kidney_disease', 'heart_failure'],
                    'dosage': '500-2000mg daily',
                    'effectiveness': 0.85
                },
                'insulin': {
                    'class': 'hormone',
                    'mechanism': 'regulates_blood_glucose',
                    'side_effects': ['hypoglycemia', 'weight_gain', 'injection_site_reactions'],
                    'contraindications': ['hypoglycemia', 'allergy_to_insulin'],
                    'dosage': 'variable_based_on_glucose_levels',
                    'effectiveness': 0.95
                }
            },
            'hypertension_medications': {
                'lisinopril': {
                    'class': 'ace_inhibitor',
                    'mechanism': 'relaxes_blood_vessels',
                    'side_effects': ['dry_cough', 'dizziness', 'fatigue'],
                    'contraindications': ['pregnancy', 'angioedema_history'],
                    'dosage': '10-40mg daily',
                    'effectiveness': 0.80
                },
                'amlodipine': {
                    'class': 'calcium_channel_blocker',
                    'mechanism': 'relaxes_blood_vessels',
                    'side_effects': ['ankle_swelling', 'dizziness', 'flushing'],
                    'contraindications': ['severe_aortic_stenosis'],
                    'dosage': '2.5-10mg daily',
                    'effectiveness': 0.82
                }
            },
            'interactions': {
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
        }
    
    def _initialize_clinical_rules(self) -> Dict:
        """Initialize clinical decision support rules"""
        return {
            'diabetes_management': [
                'if hba1c > 7.0 then consider_medication_adjustment',
                'if glucose_fasting > 130 then increase_monitoring_frequency',
                'if symptoms_present and glucose > 200 then immediate_medical_attention'
            ],
            'hypertension_management': [
                'if bp_systolic > 140 or bp_diastolic > 90 then lifestyle_modifications',
                'if bp_systolic > 160 or bp_diastolic > 100 then medication_consideration',
                'if bp_systolic > 180 or bp_diastolic > 110 then immediate_medical_attention'
            ],
            'medication_safety': [
                'check_allergies_before_prescribing',
                'assess_renal_function_for_dosage_adjustment',
                'monitor_for_drug_interactions'
            ]
        }
    
    def _create_disease_prediction_model(self):
        """Create AI disease prediction model"""
        # Simplified model for demonstration - in production, use trained ML models
        return {
            'weights': {
                'symptoms': 0.4,
                'lab_results': 0.3,
                'risk_factors': 0.2,
                'age_gender': 0.1
            }
        }
    
    def _create_risk_assessment_model(self):
        """Create AI risk assessment model"""
        return {
            'risk_categories': ['low', 'moderate', 'high', 'critical'],
            'thresholds': {
                'low': 0.0,
                'moderate': 0.3,
                'high': 0.6,
                'critical': 0.8
            }
        }
    
    def _create_treatment_effectiveness_model(self):
        """Create AI treatment effectiveness model"""
        return {
            'effectiveness_factors': ['patient_compliance', 'disease_severity', 'medication_appropriateness'],
            'prediction_accuracy': 0.87
        }
    
    def predict_diseases(self, patient_data: Dict) -> Dict[str, Any]:
        """
        Predict potential diseases based on patient data
        
        Args:
            patient_data: Dictionary containing patient symptoms, lab results, etc.
            
        Returns:
            Dictionary with disease predictions and confidence scores
        """
        try:
            predictions = {}
            
            # Extract relevant data
            symptoms = patient_data.get('symptoms', [])
            lab_results = patient_data.get('lab_results', {})
            risk_factors = patient_data.get('risk_factors', [])
            age = patient_data.get('age', 50)
            gender = patient_data.get('gender', 'unknown')
            
            # Analyze each disease
            for disease_name, disease_info in self.medical_knowledge_base['diseases'].items():
                confidence_score = self._calculate_disease_confidence(
                    disease_name, disease_info, symptoms, lab_results, risk_factors, age, gender
                )
                
                if confidence_score > 0.3:  # Only include if confidence > 30%
                    predictions[disease_name] = {
                        'confidence': confidence_score,
                        'severity': self._assess_disease_severity(disease_name, lab_results, symptoms),
                        'risk_level': self._calculate_risk_level(confidence_score),
                        'recommended_actions': self._generate_disease_actions(disease_name, confidence_score),
                        'evidence': self._collect_evidence(disease_name, symptoms, lab_results, risk_factors)
                    }
            
            # Sort by confidence score
            sorted_predictions = dict(sorted(predictions.items(), 
                                          key=lambda x: x[1]['confidence'], 
                                          reverse=True))
            
            return {
                'predictions': sorted_predictions,
                'overall_risk': self._calculate_overall_risk(sorted_predictions),
                'recommendations': self._generate_overall_recommendations(sorted_predictions),
                'confidence_metrics': self._calculate_confidence_metrics(sorted_predictions)
            }
            
        except Exception as e:
            logger.error(f"Error in disease prediction: {str(e)}")
            return {'error': f'Disease prediction failed: {str(e)}'}
    
    def _calculate_disease_confidence(self, disease_name: str, disease_info: Dict, 
                                    symptoms: List, lab_results: Dict, 
                                    risk_factors: List, age: int, gender: str) -> float:
        """Calculate confidence score for a specific disease"""
        try:
            confidence = 0.0
            
            # Symptom matching (40% weight)
            symptom_matches = sum(1 for symptom in symptoms 
                                if symptom.lower() in [s.lower() for s in disease_info['symptoms']])
            symptom_score = min(symptom_matches / len(disease_info['symptoms']), 1.0) * 0.4
            
            # Lab result analysis (30% weight)
            lab_score = self._analyze_lab_results_for_disease(disease_name, lab_results) * 0.3
            
            # Risk factor assessment (20% weight)
            risk_matches = sum(1 for risk in risk_factors 
                             if risk.lower() in [r.lower() for r in disease_info['risk_factors']])
            risk_score = min(risk_matches / len(disease_info['risk_factors']), 1.0) * 0.2
            
            # Age and gender factors (10% weight)
            demographic_score = self._assess_demographic_risk(disease_name, age, gender) * 0.1
            
            confidence = symptom_score + lab_score + risk_score + demographic_score
            
            return min(confidence, 1.0)  # Cap at 100%
            
        except Exception as e:
            logger.error(f"Error calculating disease confidence: {str(e)}")
            return 0.0
    
    def _analyze_lab_results_for_disease(self, disease_name: str, lab_results: Dict) -> float:
        """Analyze lab results for disease-specific indicators"""
        try:
            if disease_name == 'diabetes':
                glucose = lab_results.get('glucose_fasting', 0)
                hba1c = lab_results.get('hba1c', 0)
                
                if glucose > 126 or hba1c > 6.4:
                    return 1.0
                elif glucose > 100 or hba1c > 5.7:
                    return 0.7
                else:
                    return 0.3
                    
            elif disease_name == 'hypertension':
                bp_systolic = lab_results.get('blood_pressure_systolic', 0)
                bp_diastolic = lab_results.get('blood_pressure_diastolic', 0)
                
                if bp_systolic > 140 or bp_diastolic > 90:
                    return 1.0
                elif bp_systolic > 120 or bp_diastolic > 80:
                    return 0.6
                else:
                    return 0.2
                    
            return 0.5  # Default score
            
        except Exception as e:
            logger.error(f"Error analyzing lab results: {str(e)}")
            return 0.5
    
    def _assess_demographic_risk(self, disease_name: str, age: int, gender: str) -> float:
        """Assess demographic risk factors"""
        try:
            if disease_name == 'diabetes':
                if age > 45:
                    return 0.8
                elif age > 35:
                    return 0.6
                else:
                    return 0.3
                    
            elif disease_name == 'hypertension':
                if age > 50:
                    return 0.9
                elif age > 40:
                    return 0.7
                else:
                    return 0.4
                    
            return 0.5
            
        except Exception as e:
            logger.error(f"Error assessing demographic risk: {str(e)}")
            return 0.5
    
    def _assess_disease_severity(self, disease_name: str, lab_results: Dict, symptoms: List) -> str:
        """Assess the severity of a predicted disease"""
        try:
            if disease_name == 'diabetes':
                glucose = lab_results.get('glucose_fasting', 0)
                hba1c = lab_results.get('hba1c', 0)
                
                if glucose > 200 or hba1c > 8.0:
                    return 'severe'
                elif glucose > 150 or hba1c > 7.0:
                    return 'moderate'
                else:
                    return 'mild'
                    
            elif disease_name == 'hypertension':
                bp_systolic = lab_results.get('blood_pressure_systolic', 0)
                bp_diastolic = lab_results.get('blood_pressure_diastolic', 0)
                
                if bp_systolic > 180 or bp_diastolic > 110:
                    return 'severe'
                elif bp_systolic > 160 or bp_diastolic > 100:
                    return 'moderate'
                else:
                    return 'mild'
                    
            return 'unknown'
            
        except Exception as e:
            logger.error(f"Error assessing disease severity: {str(e)}")
            return 'unknown'
    
    def _calculate_risk_level(self, confidence_score: float) -> str:
        """Calculate risk level based on confidence score"""
        if confidence_score > 0.8:
            return 'critical'
        elif confidence_score > 0.6:
            return 'high'
        elif confidence_score > 0.4:
            return 'moderate'
        else:
            return 'low'
    
    def _generate_disease_actions(self, disease_name: str, confidence_score: float) -> List[str]:
        """Generate recommended actions for a disease"""
        actions = []
        
        if confidence_score > 0.8:
            actions.append('Immediate medical consultation required')
            actions.append('Consider emergency care if symptoms severe')
        elif confidence_score > 0.6:
            actions.append('Schedule medical appointment within 1 week')
            actions.append('Monitor symptoms closely')
        elif confidence_score > 0.4:
            actions.append('Schedule medical appointment within 2 weeks')
            actions.append('Consider lifestyle modifications')
        
        # Disease-specific actions
        if disease_name == 'diabetes':
            actions.append('Monitor blood glucose levels')
            actions.append('Maintain healthy diet and exercise')
        elif disease_name == 'hypertension':
            actions.append('Monitor blood pressure regularly')
            actions.append('Reduce salt intake and stress')
        
        return actions
    
    def _collect_evidence(self, disease_name: str, symptoms: List, 
                         lab_results: Dict, risk_factors: List) -> Dict:
        """Collect evidence supporting the disease prediction"""
        evidence = {
            'symptoms_present': [],
            'lab_abnormalities': [],
            'risk_factors_present': [],
            'supporting_data': {}
        }
        
        # Collect symptom evidence
        disease_symptoms = self.medical_knowledge_base['diseases'][disease_name]['symptoms']
        evidence['symptoms_present'] = [s for s in symptoms 
                                      if s.lower() in [ds.lower() for ds in disease_symptoms]]
        
        # Collect lab evidence
        if disease_name == 'diabetes':
            if lab_results.get('glucose_fasting', 0) > 100:
                evidence['lab_abnormalities'].append(f"Elevated fasting glucose: {lab_results['glucose_fasting']}")
            if lab_results.get('hba1c', 0) > 5.7:
                evidence['lab_abnormalities'].append(f"Elevated HbA1c: {lab_results['hba1c']}")
        
        # Collect risk factor evidence
        disease_risks = self.medical_knowledge_base['diseases'][disease_name]['risk_factors']
        evidence['risk_factors_present'] = [r for r in risk_factors 
                                          if r.lower() in [dr.lower() for dr in disease_risks]]
        
        return evidence
    
    def _calculate_overall_risk(self, predictions: Dict) -> str:
        """Calculate overall risk level based on all predictions"""
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
    
    def _generate_overall_recommendations(self, predictions: Dict) -> List[str]:
        """Generate overall recommendations based on all predictions"""
        recommendations = []
        
        if not predictions:
            recommendations.append('Continue regular health monitoring')
            recommendations.append('Maintain healthy lifestyle habits')
            return recommendations
        
        # High confidence predictions
        high_confidence = [name for name, pred in predictions.items() 
                          if pred['confidence'] > 0.6]
        
        if high_confidence:
            recommendations.append(f'Immediate attention needed for: {", ".join(high_confidence)}')
            recommendations.append('Schedule comprehensive medical evaluation')
        
        # General recommendations
        recommendations.append('Monitor all symptoms closely')
        recommendations.append('Keep detailed health diary')
        recommendations.append('Follow up with healthcare provider')
        
        return recommendations
    
    def _calculate_confidence_metrics(self, predictions: Dict) -> Dict:
        """Calculate confidence metrics for the predictions"""
        if not predictions:
            return {
                'average_confidence': 0.0,
                'prediction_count': 0,
                'high_confidence_count': 0
            }
        
        confidences = [pred['confidence'] for pred in predictions.values()]
        
        return {
            'average_confidence': sum(confidences) / len(confidences),
            'prediction_count': len(predictions),
            'high_confidence_count': len([c for c in confidences if c > 0.6])
        }
    
    def recommend_medications(self, patient_data: Dict, disease_predictions: Dict) -> Dict[str, Any]:
        """
        Recommend medications based on disease predictions and patient data
        
        Args:
            patient_data: Patient information including allergies, current medications
            disease_predictions: Disease predictions from predict_diseases method
            
        Returns:
            Dictionary with medication recommendations
        """
        try:
            recommendations = {}
            
            # Extract patient information
            allergies = patient_data.get('allergies', [])
            current_medications = patient_data.get('current_medications', [])
            age = patient_data.get('age', 50)
            weight = patient_data.get('weight', 70)
            kidney_function = patient_data.get('kidney_function', 'normal')
            
            # Generate recommendations for each predicted disease
            for disease_name, prediction in disease_predictions.items():
                if prediction['confidence'] > 0.4:  # Only recommend if confidence > 40%
                    disease_recommendations = self._generate_disease_medication_recommendations(
                        disease_name, prediction, allergies, current_medications, 
                        age, weight, kidney_function
                    )
                    
                    if disease_recommendations:
                        recommendations[disease_name] = disease_recommendations
            
            # Check for drug interactions
            interaction_warnings = self._check_drug_interactions(recommendations, current_medications)
            
            # Generate personalized dosing recommendations
            dosing_recommendations = self._generate_dosing_recommendations(
                recommendations, age, weight, kidney_function
            )
            
            return {
                'medication_recommendations': recommendations,
                'interaction_warnings': interaction_warnings,
                'dosing_recommendations': dosing_recommendations,
                'safety_considerations': self._generate_safety_considerations(recommendations, patient_data),
                'monitoring_requirements': self._generate_monitoring_requirements(recommendations)
            }
            
        except Exception as e:
            logger.error(f"Error in medication recommendation: {str(e)}")
            return {'error': f'Medication recommendation failed: {str(e)}'}
    
    def _generate_disease_medication_recommendations(self, disease_name: str, prediction: Dict,
                                                   allergies: List, current_medications: List,
                                                   age: int, weight: float, kidney_function: str) -> Dict:
        """Generate medication recommendations for a specific disease"""
        try:
            recommendations = {
                'primary_medications': [],
                'alternative_medications': [],
                'contraindications': [],
                'monitoring_required': []
            }
            
            if disease_name == 'diabetes':
                # Primary medications
                if 'metformin' not in allergies and kidney_function != 'severe':
                    recommendations['primary_medications'].append({
                        'name': 'Metformin',
                        'reason': 'First-line treatment for Type 2 diabetes',
                        'dosage': self._calculate_metformin_dosage(age, weight, kidney_function),
                        'effectiveness': 0.85,
                        'side_effects': ['nausea', 'diarrhea', 'stomach_upset']
                    })
                
                # Alternative if metformin contraindicated
                if 'metformin' in allergies or kidney_function == 'severe':
                    recommendations['alternative_medications'].append({
                        'name': 'Sulfonylurea',
                        'reason': 'Alternative when metformin contraindicated',
                        'dosage': 'Variable based on glucose levels',
                        'effectiveness': 0.75,
                        'side_effects': ['hypoglycemia', 'weight_gain']
                    })
                
                recommendations['monitoring_required'].extend([
                    'Blood glucose monitoring',
                    'HbA1c testing every 3-6 months',
                    'Kidney function monitoring'
                ])
                
            elif disease_name == 'hypertension':
                # Primary medications
                if 'ace_inhibitor' not in allergies:
                    recommendations['primary_medications'].append({
                        'name': 'Lisinopril',
                        'reason': 'First-line ACE inhibitor for hypertension',
                        'dosage': self._calculate_lisinopril_dosage(age, weight, kidney_function),
                        'effectiveness': 0.80,
                        'side_effects': ['dry_cough', 'dizziness', 'fatigue']
                    })
                
                # Alternative if ACE inhibitor contraindicated
                if 'ace_inhibitor' in allergies:
                    recommendations['alternative_medications'].append({
                        'name': 'Amlodipine',
                        'reason': 'Alternative calcium channel blocker',
                        'dosage': '5-10mg daily',
                        'effectiveness': 0.82,
                        'side_effects': ['ankle_swelling', 'dizziness', 'flushing']
                    })
                
                recommendations['monitoring_required'].extend([
                    'Blood pressure monitoring',
                    'Kidney function monitoring',
                    'Electrolyte monitoring'
                ])
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating disease medication recommendations: {str(e)}")
            return {}
    
    def _calculate_metformin_dosage(self, age: int, weight: float, kidney_function: str) -> str:
        """Calculate appropriate metformin dosage"""
        if kidney_function == 'severe':
            return 'Contraindicated'
        elif kidney_function == 'moderate':
            return '500mg once daily (reduced dosage)'
        elif age > 65:
            return '500mg twice daily (start low)'
        else:
            return '500mg twice daily, titrate to 2000mg daily'
    
    def _calculate_lisinopril_dosage(self, age: int, weight: float, kidney_function: str) -> str:
        """Calculate appropriate lisinopril dosage"""
        if kidney_function == 'severe':
            return '2.5mg daily (reduced dosage)'
        elif age > 65:
            return '5mg daily (start low)'
        else:
            return '10mg daily, titrate to 40mg daily'
    
    def _check_drug_interactions(self, recommendations: Dict, current_medications: List) -> List[Dict]:
        """Check for potential drug interactions"""
        interactions = []
        
        for disease, recs in recommendations.items():
            for med_type in ['primary_medications', 'alternative_medications']:
                for med in recs.get(med_type, []):
                    med_name = med['name'].lower()
                    
                    # Check interactions with current medications
                    for current_med in current_medications:
                        current_med_lower = current_med.lower()
                        
                        # Check known interactions
                        for interaction_key, interaction_info in self.medicine_database['interactions'].items():
                            if (med_name in interaction_key and current_med_lower in interaction_key) or \
                               (current_med_lower in interaction_key and med_name in interaction_key):
                                interactions.append({
                                    'medication_1': med['name'],
                                    'medication_2': current_med,
                                    'severity': interaction_info['severity'],
                                    'description': interaction_info['description'],
                                    'recommendation': interaction_info['recommendation']
                                })
        
        return interactions
    
    def _generate_dosing_recommendations(self, recommendations: Dict, age: int, 
                                       weight: float, kidney_function: str) -> Dict:
        """Generate personalized dosing recommendations"""
        dosing = {
            'general_guidelines': [],
            'age_adjustments': [],
            'kidney_adjustments': [],
            'monitoring_schedule': []
        }
        
        # General guidelines
        dosing['general_guidelines'].extend([
            'Start with lowest effective dose',
            'Titrate gradually based on response',
            'Monitor for side effects closely'
        ])
        
        # Age adjustments
        if age > 65:
            dosing['age_adjustments'].extend([
                'Use 50% of standard starting dose',
                'Monitor more frequently for side effects',
                'Consider reduced frequency of administration'
            ])
        
        # Kidney function adjustments
        if kidney_function != 'normal':
            dosing['kidney_adjustments'].extend([
                'Reduce dosage based on kidney function',
                'Monitor kidney function regularly',
                'Avoid nephrotoxic medications if possible'
            ])
        
        # Monitoring schedule
        dosing['monitoring_schedule'].extend([
            'Weekly monitoring for first month',
            'Monthly monitoring for first 6 months',
            'Quarterly monitoring thereafter'
        ])
        
        return dosing
    
    def _generate_safety_considerations(self, recommendations: Dict, patient_data: Dict) -> List[str]:
        """Generate safety considerations for medication recommendations"""
        safety = []
        
        allergies = patient_data.get('allergies', [])
        current_medications = patient_data.get('current_medications', [])
        age = patient_data.get('age', 50)
        
        # Allergy considerations
        if allergies:
            safety.append(f'Patient has allergies to: {", ".join(allergies)}')
            safety.append('Verify all medications are safe for patient')
        
        # Polypharmacy considerations
        if len(current_medications) > 5:
            safety.append('Patient on multiple medications - increased interaction risk')
            safety.append('Consider medication review and deprescribing')
        
        # Age considerations
        if age > 65:
            safety.append('Elderly patient - increased sensitivity to medications')
            safety.append('Monitor for adverse effects more closely')
        
        return safety
    
    def _generate_monitoring_requirements(self, recommendations: Dict) -> Dict:
        """Generate monitoring requirements for recommended medications"""
        monitoring = {
            'laboratory_tests': [],
            'vital_signs': [],
            'symptom_monitoring': [],
            'frequency': {}
        }
        
        for disease, recs in recommendations.items():
            if disease == 'diabetes':
                monitoring['laboratory_tests'].extend([
                    'Blood glucose (daily)',
                    'HbA1c (every 3-6 months)',
                    'Kidney function (every 6 months)'
                ])
                monitoring['vital_signs'].extend(['Blood pressure', 'Weight'])
                monitoring['symptom_monitoring'].extend([
                    'Hypoglycemia symptoms',
                    'Gastrointestinal symptoms'
                ])
                
            elif disease == 'hypertension':
                monitoring['laboratory_tests'].extend([
                    'Kidney function (every 3-6 months)',
                    'Electrolytes (every 6 months)'
                ])
                monitoring['vital_signs'].extend(['Blood pressure (weekly)'])
                monitoring['symptom_monitoring'].extend([
                    'Dizziness',
                    'Cough (if on ACE inhibitor)'
                ])
        
        # Set monitoring frequency
        monitoring['frequency'] = {
            'daily': ['Blood glucose', 'Blood pressure'],
            'weekly': ['Weight', 'Symptom assessment'],
            'monthly': ['Kidney function'],
            'quarterly': ['HbA1c', 'Electrolytes']
        }
        
        return monitoring
    
    def generate_clinical_report(self, patient_data: Dict, disease_predictions: Dict, 
                               medication_recommendations: Dict) -> Dict[str, Any]:
        """
        Generate comprehensive clinical report
        
        Args:
            patient_data: Patient information
            disease_predictions: Disease predictions
            medication_recommendations: Medication recommendations
            
        Returns:
            Comprehensive clinical report
        """
        try:
            report = {
                'executive_summary': self._generate_executive_summary(disease_predictions),
                'patient_overview': self._generate_patient_overview(patient_data),
                'clinical_assessment': self._generate_clinical_assessment(disease_predictions),
                'treatment_recommendations': self._generate_treatment_summary(medication_recommendations),
                'risk_assessment': self._generate_risk_summary(disease_predictions),
                'monitoring_plan': self._generate_monitoring_plan(medication_recommendations),
                'follow_up_plan': self._generate_follow_up_plan(disease_predictions),
                'emergency_contacts': self._generate_emergency_contacts(),
                'report_metadata': self._generate_report_metadata()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating clinical report: {str(e)}")
            return {'error': f'Clinical report generation failed: {str(e)}'}
    
    def _generate_executive_summary(self, disease_predictions: Dict) -> str:
        """Generate executive summary of clinical findings"""
        if not disease_predictions:
            return "No significant disease risk detected. Continue routine health monitoring."
        
        high_risk_diseases = [name for name, pred in disease_predictions.items() 
                             if pred['confidence'] > 0.6]
        
        if high_risk_diseases:
            return f"High risk detected for: {', '.join(high_risk_diseases)}. " \
                   f"Immediate medical evaluation recommended."
        else:
            return f"Moderate risk detected for: {', '.join(disease_predictions.keys())}. " \
                   f"Schedule medical consultation within 2 weeks."
    
    def _generate_patient_overview(self, patient_data: Dict) -> Dict:
        """Generate patient overview section"""
        return {
            'demographics': {
                'age': patient_data.get('age', 'Unknown'),
                'gender': patient_data.get('gender', 'Unknown'),
                'weight': patient_data.get('weight', 'Unknown'),
                'height': patient_data.get('height', 'Unknown')
            },
            'current_medications': patient_data.get('current_medications', []),
            'allergies': patient_data.get('allergies', []),
            'medical_history': patient_data.get('medical_history', []),
            'family_history': patient_data.get('family_history', [])
        }
    
    def _generate_clinical_assessment(self, disease_predictions: Dict) -> Dict:
        """Generate clinical assessment section"""
        assessment = {
            'primary_concerns': [],
            'differential_diagnoses': [],
            'clinical_impression': '',
            'severity_assessment': ''
        }
        
        for disease_name, prediction in disease_predictions.items():
            if prediction['confidence'] > 0.4:
                assessment['primary_concerns'].append({
                    'condition': disease_name,
                    'confidence': prediction['confidence'],
                    'severity': prediction['severity'],
                    'evidence': prediction['evidence']
                })
        
        # Sort by confidence
        assessment['primary_concerns'].sort(key=lambda x: x['confidence'], reverse=True)
        
        # Generate clinical impression
        if assessment['primary_concerns']:
            top_concern = assessment['primary_concerns'][0]
            assessment['clinical_impression'] = f"Primary concern: {top_concern['condition']} " \
                                             f"with {top_concern['severity']} severity " \
                                             f"(confidence: {top_concern['confidence']:.1%})"
        
        return assessment
    
    def _generate_treatment_summary(self, medication_recommendations: Dict) -> Dict:
        """Generate treatment recommendations summary"""
        summary = {
            'immediate_actions': [],
            'medication_changes': [],
            'lifestyle_modifications': [],
            'referrals_needed': []
        }
        
        for disease, recs in medication_recommendations.items():
            # Immediate actions
            if any(med.get('reason', '').lower().find('immediate') != -1 
                   for med in recs.get('primary_medications', [])):
                summary['immediate_actions'].append(f"Immediate treatment for {disease}")
            
            # Medication changes
            for med in recs.get('primary_medications', []):
                summary['medication_changes'].append({
                    'medication': med['name'],
                    'reason': med['reason'],
                    'priority': 'high' if med.get('effectiveness', 0) > 0.8 else 'medium'
                })
            
            # Lifestyle modifications
            if disease == 'diabetes':
                summary['lifestyle_modifications'].extend([
                    'Blood glucose monitoring',
                    'Healthy diet and exercise',
                    'Weight management'
                ])
            elif disease == 'hypertension':
                summary['lifestyle_modifications'].extend([
                    'Blood pressure monitoring',
                    'Salt restriction',
                    'Stress management'
                ])
        
        return summary
    
    def _generate_risk_summary(self, disease_predictions: Dict) -> Dict:
        """Generate risk assessment summary"""
        risk_summary = {
            'overall_risk': self._calculate_overall_risk(disease_predictions),
            'high_risk_conditions': [],
            'moderate_risk_conditions': [],
            'low_risk_conditions': [],
            'risk_factors': [],
            'preventive_measures': []
        }
        
        for disease_name, prediction in disease_predictions.items():
            risk_level = prediction['risk_level']
            
            if risk_level == 'critical' or risk_level == 'high':
                risk_summary['high_risk_conditions'].append({
                    'condition': disease_name,
                    'confidence': prediction['confidence'],
                    'severity': prediction['severity']
                })
            elif risk_level == 'moderate':
                risk_summary['moderate_risk_conditions'].append({
                    'condition': disease_name,
                    'confidence': prediction['confidence'],
                    'severity': prediction['severity']
                })
            else:
                risk_summary['low_risk_conditions'].append({
                    'condition': disease_name,
                    'confidence': prediction['confidence'],
                    'severity': prediction['severity']
                })
        
        # Generate preventive measures
        if risk_summary['high_risk_conditions']:
            risk_summary['preventive_measures'].extend([
                'Immediate medical consultation',
                'Close symptom monitoring',
                'Emergency care if symptoms worsen'
            ])
        
        return risk_summary
    
    def _generate_monitoring_plan(self, medication_recommendations: Dict) -> Dict:
        """Generate monitoring plan"""
        monitoring_plan = {
            'laboratory_tests': [],
            'vital_signs': [],
            'symptom_monitoring': [],
            'frequency': {},
            'alerts': []
        }
        
        for disease, recs in medication_recommendations.items():
            if 'monitoring_required' in recs:
                monitoring_plan['laboratory_tests'].extend(recs['monitoring_required'])
        
        # Set monitoring frequency
        monitoring_plan['frequency'] = {
            'daily': ['Blood glucose', 'Blood pressure'],
            'weekly': ['Weight', 'Symptom assessment'],
            'monthly': ['Laboratory tests'],
            'quarterly': ['Comprehensive evaluation']
        }
        
        # Generate alerts
        monitoring_plan['alerts'].extend([
            'Contact healthcare provider if symptoms worsen',
            'Seek emergency care for severe symptoms',
            'Report any medication side effects immediately'
        ])
        
        return monitoring_plan
    
    def _generate_follow_up_plan(self, disease_predictions: Dict) -> Dict:
        """Generate follow-up plan"""
        follow_up = {
            'immediate_follow_up': [],
            'short_term_follow_up': [],
            'long_term_follow_up': [],
            'specialist_referrals': []
        }
        
        for disease_name, prediction in disease_predictions.items():
            if prediction['confidence'] > 0.8:
                follow_up['immediate_follow_up'].append({
                    'condition': disease_name,
                    'timeline': 'Within 24-48 hours',
                    'reason': 'High confidence prediction requiring immediate attention'
                })
            elif prediction['confidence'] > 0.6:
                follow_up['short_term_follow_up'].append({
                    'condition': disease_name,
                    'timeline': 'Within 1 week',
                    'reason': 'Moderate confidence prediction requiring prompt evaluation'
                })
            else:
                follow_up['long_term_follow_up'].append({
                    'condition': disease_name,
                    'timeline': 'Within 2-4 weeks',
                    'reason': 'Low confidence prediction for routine follow-up'
                })
        
        # Specialist referrals
        if any(disease in ['diabetes', 'hypertension'] for disease in disease_predictions.keys()):
            follow_up['specialist_referrals'].append({
                'specialist': 'Endocrinologist/Cardiologist',
                'reason': 'Complex metabolic/cardiovascular management',
                'urgency': 'Moderate'
            })
        
        return follow_up
    
    def _generate_emergency_contacts(self) -> List[Dict]:
        """Generate emergency contact information"""
        return [
            {
                'type': 'Emergency Services',
                'contact': '911',
                'description': 'For life-threatening emergencies'
            },
            {
                'type': 'Poison Control',
                'contact': '1-800-222-1222',
                'description': 'For medication overdose or poisoning'
            },
            {
                'type': 'Healthcare Provider',
                'contact': 'Contact your primary care physician',
                'description': 'For non-emergency medical concerns'
            }
        ]
    
    def _generate_report_metadata(self) -> Dict:
        """Generate report metadata"""
        return {
            'generated_at': datetime.now().isoformat(),
            'ai_engine_version': '2.0.0',
            'confidence_threshold': 0.4,
            'report_type': 'comprehensive_clinical_assessment',
            'data_sources': ['patient_data', 'lab_results', 'symptoms', 'risk_factors']
        }

# Initialize the AI engine
ai_engine = HealthcareAIEngine()

def get_ai_engine():
    """Get the initialized AI engine instance"""
    return ai_engine 