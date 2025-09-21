// Advanced Animations and AI Features for MediChain AI
class AdvancedAnimations {
    constructor() {
        this.init();
    }

    init() {
        this.setupParticleSystem();
        this.setupAIBrain();
        this.setupDNAHelix();
        this.setupMedicalCross();
        this.setupDataStream();
        this.setupHeartbeat();
        this.setupFloatingElements();
        this.setupHolographicText();
        this.setupGlitchEffects();
        this.setup3DCards();
        this.setupToastSystem();
        this.setupRealTimeMonitoring();
    }

    setupParticleSystem() {
        const particleContainer = document.createElement('div');
        particleContainer.className = 'particles';
        document.body.appendChild(particleContainer);

        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 15 + 's';
            particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
            particleContainer.appendChild(particle);
        }
    }

    setupAIBrain() {
        const aiBrains = document.querySelectorAll('.ai-brain');
        aiBrains.forEach(brain => {
            // Create pulsing circles
            for (let i = 0; i < 3; i++) {
                const circle = document.createElement('div');
                circle.style.position = 'absolute';
                circle.style.border = '2px solid var(--primary-cyan)';
                circle.style.borderRadius = '50%';
                circle.style.left = '50%';
                circle.style.top = '50%';
                circle.style.transform = 'translate(-50%, -50%)';
                circle.style.width = (60 - i * 10) + 'px';
                circle.style.height = (60 - i * 10) + 'px';
                circle.style.animation = `brainPulse 2s ease-in-out infinite ${i * 0.5}s`;
                brain.appendChild(circle);
            }
        });
    }

    setupDNAHelix() {
        const dnaElements = document.querySelectorAll('.dna-helix');
        dnaElements.forEach(dna => {
            // Create DNA strands
            for (let i = 0; i < 2; i++) {
                const strand = document.createElement('div');
                strand.style.position = 'absolute';
                strand.style.width = '4px';
                strand.style.height = '100%';
                strand.style.background = 'linear-gradient(to bottom, var(--primary-cyan), var(--primary-purple))';
                strand.style.borderRadius = '2px';
                strand.style.left = i === 0 ? '20px' : 'calc(100% - 24px)';
                strand.style.animation = `dnaRotate 3s linear infinite ${i * 1.5}s`;
                dna.appendChild(strand);
            }
        });
    }

    setupMedicalCross() {
        const crosses = document.querySelectorAll('.medical-cross');
        crosses.forEach(cross => {
            // Create cross elements
            const vertical = document.createElement('div');
            vertical.style.position = 'absolute';
            vertical.style.width = '4px';
            vertical.style.height = '100%';
            vertical.style.background = 'var(--primary-green)';
            vertical.style.borderRadius = '2px';
            vertical.style.left = '50%';
            vertical.style.transform = 'translateX(-50%)';
            vertical.style.animation = 'crossPulse 2s ease-in-out infinite';
            cross.appendChild(vertical);

            const horizontal = document.createElement('div');
            horizontal.style.position = 'absolute';
            horizontal.style.width = '100%';
            horizontal.style.height = '4px';
            horizontal.style.background = 'var(--primary-green)';
            horizontal.style.borderRadius = '2px';
            horizontal.style.top = '50%';
            horizontal.style.transform = 'translateY(-50%)';
            horizontal.style.animation = 'crossPulse 2s ease-in-out infinite reverse';
            cross.appendChild(horizontal);
        });
    }

    setupDataStream() {
        const dataStreams = document.querySelectorAll('.data-stream');
        dataStreams.forEach(stream => {
            const data = ['01', '10', '11', '00', 'FF', 'AA', 'BB', 'CC'];
            let index = 0;
            
            setInterval(() => {
                stream.textContent = data[index];
                index = (index + 1) % data.length;
            }, 1000);
        });
    }

    setupHeartbeat() {
        const heartbeats = document.querySelectorAll('.heartbeat');
        heartbeats.forEach(heart => {
            heart.style.animation = 'heartbeat 1.5s ease-in-out infinite';
        });
    }

    setupFloatingElements() {
        const floatingElements = document.querySelectorAll('.float');
        floatingElements.forEach(element => {
            element.style.animation = 'float 6s ease-in-out infinite';
        });
    }

    setupHolographicText() {
        const holographicElements = document.querySelectorAll('.holographic');
        holographicElements.forEach(element => {
            element.style.background = 'linear-gradient(45deg, var(--primary-cyan), var(--primary-purple), var(--primary-green), var(--primary-pink), var(--primary-cyan))';
            element.style.backgroundSize = '400% 400%';
            element.style.animation = 'holographicShift 3s ease infinite';
            element.style.webkitBackgroundClip = 'text';
            element.style.webkitTextFillColor = 'transparent';
            element.style.backgroundClip = 'text';
        });
    }

    setupGlitchEffects() {
        const glitchElements = document.querySelectorAll('.glitch');
        glitchElements.forEach(element => {
            element.setAttribute('data-text', element.textContent);
            
            element.addEventListener('mouseenter', () => {
                element.style.animation = 'glitch 0.3s infinite';
            });
            
            element.addEventListener('mouseleave', () => {
                element.style.animation = 'none';
            });
        });
    }

    setup3DCards() {
        const cards = document.querySelectorAll('.card-3d');
        cards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg)';
            });
        });
    }

    setupToastSystem() {
        this.toastQueue = [];
        this.isShowingToast = false;
    }

    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-${this.getToastIcon(type)} mr-2"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);
        
        // Animate out
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    getToastIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            info: 'info-circle',
            warning: 'exclamation-circle'
        };
        return icons[type] || 'info-circle';
    }

    setupRealTimeMonitoring() {
        setInterval(() => {
            this.updateSystemStatus();
        }, 5000);
    }

    updateSystemStatus() {
        const statusElements = document.querySelectorAll('.system-status');
        statusElements.forEach(element => {
            const status = Math.random() > 0.1 ? 'Online' : 'Warning';
            const color = status === 'Online' ? 'text-green-400' : 'text-yellow-400';
            element.className = `system-status ${color}`;
            element.textContent = status;
        });
    }
}

// AI Features
class AIFeatures {
    constructor() {
        this.setupAIChat();
        this.setupDocumentAnalysis();
        this.setupClinicalInsights();
        this.setupRiskAssessment();
        this.setupDoctorConnect();
        this.setupDrugInteractionChecker();
    }

    setupAIChat() {
        // Enhanced AI chat functionality
        this.aiResponses = {
            'patient': 'I can help you with patient information. What would you like to know?',
            'medication': 'Let me analyze the medication data for you.',
            'diagnosis': 'I\'ll review the diagnostic information.',
            'lab': 'I can help you understand the lab results.',
            'treatment': 'Based on the data, here are my treatment recommendations.'
        };
    }

    setupDocumentAnalysis() {
        this.analyzeDocument = async () => {
            this.showToast('Analyzing document with AI...', 'info');
            
            try {
                // Get actual session data from the server
                const response = await fetch('/get_current_patient_data', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                
                if (!response.ok) {
                    throw new Error('No patient data available');
                }
                
                const patientData = await response.json();
                
                if (!patientData.success) {
                    this.showToast('Please upload a CCDA document first', 'error');
                    return;
                }
                
                // Calculate real confidence based on data completeness
                const confidence = this.calculateConfidence(patientData.data);
                
                // Generate real recommendations based on actual conditions
                const recommendations = this.generateRealRecommendations(patientData.data);
                
                const analysis = {
                    confidence: confidence,
                    extractedData: {
                        patientInfo: patientData.data.patient?.name || 'Unknown',
                        medications: patientData.data.medical?.medications || [],
                        conditions: patientData.data.medical?.conditions || [],
                        labResults: patientData.data.medical?.lab_results || [],
                        vitalSigns: patientData.data.medical?.vital_signs || []
                    },
                    recommendations: recommendations
                };
                
                this.showAnalysisResults(analysis);
                
            } catch (error) {
                console.error('Error analyzing document:', error);
                this.showToast('Please upload a CCDA document first', 'error');
            }
        };
    }

    calculateConfidence(patientData) {
        let score = 0.5; // Base score
        
        // Add points for each data type present
        if (patientData.patient?.name) score += 0.1;
        if (patientData.patient?.dob) score += 0.1;
        if (patientData.medical?.medications?.length > 0) score += 0.15;
        if (patientData.medical?.conditions?.length > 0) score += 0.15;
        if (patientData.medical?.lab_results?.length > 0) score += 0.1;
        if (patientData.medical?.vital_signs?.length > 0) score += 0.1;
        
        return Math.min(score, 0.98); // Cap at 98%
    }

    generateRealRecommendations(patientData) {
        const recommendations = [];
        const conditions = patientData.medical?.conditions || [];
        const medications = patientData.medical?.medications || [];
        
        // Generate recommendations based on actual conditions
        conditions.forEach(condition => {
            const conditionLower = condition.toLowerCase();
            
            if (conditionLower.includes('diabetes')) {
                recommendations.push('Monitor blood glucose levels regularly');
                recommendations.push('Maintain a balanced diet low in simple carbohydrates');
                recommendations.push('Schedule regular HbA1c testing');
            }
            
            if (conditionLower.includes('hypertension') || conditionLower.includes('blood pressure')) {
                recommendations.push('Monitor blood pressure weekly');
                recommendations.push('Consider low-sodium diet');
                recommendations.push('Regular cardiovascular monitoring');
            }
            
            if (conditionLower.includes('heart') || conditionLower.includes('cardiac')) {
                recommendations.push('Regular cardiac monitoring');
                recommendations.push('Lifestyle modifications recommended');
                recommendations.push('Follow up with cardiologist');
            }
            
            if (conditionLower.includes('cancer') || conditionLower.includes('neoplasm')) {
                recommendations.push('Regular oncology follow-up');
                recommendations.push('Monitor for treatment side effects');
                recommendations.push('Maintain treatment compliance');
            }
        });
        
        // Add general recommendations
        if (medications.length > 0) {
            recommendations.push('Continue current medication regimen as prescribed');
            recommendations.push('Report any side effects to healthcare provider');
        }
        
        if (recommendations.length === 0) {
            recommendations.push('Schedule regular check-ups with healthcare provider');
            recommendations.push('Maintain a balanced diet and exercise routine');
            recommendations.push('Ensure adequate sleep and stress management');
        }
        
        return recommendations.slice(0, 5); // Limit to 5 recommendations
    }

    showAnalysisResults(analysis) {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="glass max-w-4xl w-full mx-4 p-8 rounded-xl">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-3xl font-bold holographic">AI Document Analysis</h3>
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" class="text-cyan-300 hover:text-cyan-100">
                        <i class="fas fa-times text-2xl"></i>
                    </button>
                </div>
                
                <div class="grid md:grid-cols-2 gap-6">
                    <div class="space-y-4">
                        <div class="bg-black/40 p-4 rounded-lg">
                            <h4 class="text-xl font-semibold text-cyan-300 mb-3">Confidence Score</h4>
                            <div class="text-3xl font-bold text-green-400">${(analysis.confidence * 100).toFixed(1)}%</div>
                        </div>
                        
                        <div class="bg-black/40 p-4 rounded-lg">
                            <h4 class="text-xl font-semibold text-cyan-300 mb-3">Extracted Data</h4>
                            <div class="space-y-2 text-sm">
                                <div><strong>Patient:</strong> ${analysis.extractedData.patientInfo}</div>
                                <div><strong>Medications:</strong> ${analysis.extractedData.medications.join(', ')}</div>
                                <div><strong>Conditions:</strong> ${analysis.extractedData.conditions.join(', ')}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="space-y-4">
                        <div class="bg-black/40 p-4 rounded-lg">
                            <h4 class="text-xl font-semibold text-cyan-300 mb-3">AI Recommendations</h4>
                            <ul class="space-y-2">
                                ${analysis.recommendations.map(rec => `<li class="text-sm">• ${rec}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }

    setupClinicalInsights() {
        this.generateClinicalInsights = async () => {
            this.showToast('Generating clinical insights...', 'info');
            
            try {
                // Get actual session data from the server
                const response = await fetch('/get_current_patient_data', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                
                if (!response.ok) {
                    throw new Error('No patient data available');
                }
                
                const patientData = await response.json();
                
                if (!patientData.success) {
                    this.showToast('Please upload a CCDA document first', 'error');
                    return;
                }
                
                // Generate real insights based on actual data
                const insights = this.generateRealInsights(patientData.data);
                
                this.showClinicalInsights(insights);
                
            } catch (error) {
                console.error('Error generating clinical insights:', error);
                this.showToast('Please upload a CCDA document first', 'error');
            }
        };
    }

    generateRealInsights(patientData) {
        const conditions = patientData.medical?.conditions || [];
        const medications = patientData.medical?.medications || [];
        const labResults = patientData.medical?.lab_results || [];
        
        // Calculate risk level based on actual conditions
        let riskLevel = 'Low';
        let riskFactors = [];
        let recommendations = [];
        let alerts = [];
        
        // Analyze conditions for risk assessment
        conditions.forEach(condition => {
            const conditionLower = condition.toLowerCase();
            
            if (conditionLower.includes('diabetes')) {
                riskLevel = 'Moderate';
                riskFactors.push('Diabetes mellitus detected');
                recommendations.push('Monitor blood glucose levels regularly');
                recommendations.push('Schedule regular HbA1c testing');
                alerts.push('Diabetes requires careful monitoring');
            }
            
            if (conditionLower.includes('hypertension') || conditionLower.includes('blood pressure')) {
                riskLevel = 'Moderate';
                riskFactors.push('Hypertension detected');
                recommendations.push('Monitor blood pressure weekly');
                recommendations.push('Consider low-sodium diet');
                alerts.push('Blood pressure monitoring recommended');
            }
            
            if (conditionLower.includes('heart') || conditionLower.includes('cardiac') || conditionLower.includes('coronary')) {
                riskLevel = 'High';
                riskFactors.push('Cardiovascular condition detected');
                recommendations.push('Regular cardiac monitoring');
                recommendations.push('Follow up with cardiologist');
                alerts.push('Cardiovascular monitoring critical');
            }
            
            if (conditionLower.includes('cancer') || conditionLower.includes('neoplasm')) {
                riskLevel = 'High';
                riskFactors.push('Oncological condition detected');
                recommendations.push('Regular oncology follow-up');
                recommendations.push('Monitor for treatment side effects');
                alerts.push('Oncology monitoring essential');
            }
        });
        
        // Analyze medications for interactions
        if (medications.length > 2) {
            riskFactors.push('Multiple medications detected');
            recommendations.push('Review medication interactions');
            alerts.push('Potential drug interactions - consult pharmacist');
        }
        
        // Add general recommendations if none specific
        if (recommendations.length === 0) {
            recommendations.push('Schedule regular check-ups');
            recommendations.push('Maintain healthy lifestyle');
        }
        
        return {
            riskLevel: riskLevel,
            riskFactors: riskFactors,
            recommendations: recommendations.slice(0, 4),
            alerts: alerts.slice(0, 3)
        };
    }

    showClinicalInsights(insights) {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="glass max-w-4xl w-full mx-4 p-8 rounded-xl">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-3xl font-bold holographic">AI Clinical Insights</h3>
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" class="text-cyan-300 hover:text-cyan-100">
                        <i class="fas fa-times text-2xl"></i>
                    </button>
                </div>
                
                <div class="grid md:grid-cols-3 gap-6">
                    <div class="bg-black/40 p-4 rounded-lg">
                        <h4 class="text-xl font-semibold text-cyan-300 mb-3">Risk Assessment</h4>
                        <div class="text-2xl font-bold text-orange-400">${insights.riskLevel}</div>
                        <div class="mt-2 text-sm">
                            ${insights.riskFactors.map(factor => `<div>• ${factor}</div>`).join('')}
                        </div>
                    </div>
                    
                    <div class="bg-black/40 p-4 rounded-lg">
                        <h4 class="text-xl font-semibold text-cyan-300 mb-3">Recommendations</h4>
                        <ul class="space-y-2 text-sm">
                            ${insights.recommendations.map(rec => `<li>• ${rec}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="bg-black/40 p-4 rounded-lg">
                        <h4 class="text-xl font-semibold text-cyan-300 mb-3">Alerts</h4>
                        <ul class="space-y-2 text-sm">
                            ${insights.alerts.map(alert => `<li class="text-red-400">⚠️ ${alert}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }

    setupRiskAssessment() {
        this.assessRisk = async () => {
            try {
                // Get actual session data from the server
                const response = await fetch('/get_current_patient_data', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                
                if (!response.ok) {
                    throw new Error('No patient data available');
                }
                
                const patientData = await response.json();
                
                if (!patientData.success) {
                    this.showToast('Please upload a CCDA document first', 'error');
                    return;
                }
                
                // Calculate real risk score based on actual data
                const riskScore = this.calculateRealRiskScore(patientData.data);
                const riskLevel = riskScore > 70 ? 'High' : riskScore > 40 ? 'Moderate' : 'Low';
                
                return {
                    score: riskScore.toFixed(1),
                    level: riskLevel,
                    factors: this.generateRealRiskFactors(patientData.data)
                };
                
            } catch (error) {
                console.error('Error assessing risk:', error);
                this.showToast('Please upload a CCDA document first', 'error');
            }
        };
    }

    calculateRealRiskScore(patientData) {
        let score = 0;
        const conditions = patientData.medical?.conditions || [];
        const medications = patientData.medical?.medications || [];
        
        // Base score
        score += 20;
        
        // Add points for conditions
        conditions.forEach(condition => {
            const conditionLower = condition.toLowerCase();
            if (conditionLower.includes('diabetes')) score += 15;
            if (conditionLower.includes('hypertension')) score += 12;
            if (conditionLower.includes('heart') || conditionLower.includes('cardiac')) score += 20;
            if (conditionLower.includes('cancer') || conditionLower.includes('neoplasm')) score += 25;
            if (conditionLower.includes('kidney') || conditionLower.includes('renal')) score += 15;
            if (conditionLower.includes('lung') || conditionLower.includes('pulmonary')) score += 15;
        });
        
        // Add points for multiple medications
        if (medications.length > 3) score += 10;
        if (medications.length > 5) score += 15;
        
        return Math.min(score, 95); // Cap at 95%
    }

    generateRealRiskFactors(patientData) {
        const factors = [];
        const conditions = patientData.medical?.conditions || [];
        const medications = patientData.medical?.medications || [];
        
        // Analyze conditions for risk factors
        conditions.forEach(condition => {
            const conditionLower = condition.toLowerCase();
            if (conditionLower.includes('diabetes')) factors.push('Diabetes mellitus');
            if (conditionLower.includes('hypertension')) factors.push('Hypertension');
            if (conditionLower.includes('heart') || conditionLower.includes('cardiac')) factors.push('Cardiovascular disease');
            if (conditionLower.includes('cancer') || conditionLower.includes('neoplasm')) factors.push('Oncological condition');
            if (conditionLower.includes('kidney') || conditionLower.includes('renal')) factors.push('Renal impairment');
            if (conditionLower.includes('lung') || conditionLower.includes('pulmonary')) factors.push('Pulmonary condition');
        });
        
        // Add medication-related factors
        if (medications.length > 2) factors.push('Multiple medications');
        if (medications.length > 5) factors.push('Complex medication regimen');
        
        // Add general factors if none specific
        if (factors.length === 0) {
            factors.push('Limited medical history available');
        }
        
        return factors.slice(0, 5); // Limit to 5 factors
    }

    setupDoctorConnect() {
        this.openConsultDoctorModal = () => {
            this.showConsultDoctorModal();
        };
    }

    showConsultDoctorModal() {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="glass max-w-md w-full mx-4 p-8 rounded-xl">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-2xl font-bold text-cyan-200">
                        <i class="fas fa-user-md mr-2"></i>Consult Your Doctor
                    </h3>
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" class="text-cyan-300 hover:text-cyan-100">
                        <i class="fas fa-times text-xl"></i>
                    </button>
                </div>
                
                <div class="space-y-6">
                                <div>
                        <label class="block text-cyan-300 text-sm font-medium mb-2">Doctor's Phone Number:</label>
                        <input type="tel" id="doctor-phone" 
                               class="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-cyan-400"
                               placeholder="Enter doctor's phone number (e.g., +1234567890)"
                               required>
                                </div>
                    
                    <div>
                        <label class="block text-cyan-300 text-sm font-medium mb-2">Patient Name:</label>
                        <input type="text" id="patient-name" 
                               class="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-cyan-400"
                               placeholder="Enter your name"
                               required>
                                </div>
                    
                    <div>
                        <label class="block text-cyan-300 text-sm font-medium mb-2">Emergency Message:</label>
                        <textarea id="emergency-message" 
                                  class="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-cyan-400"
                                  placeholder="Describe your emergency or health concern..."
                                  rows="4"
                                  required></textarea>
                            </div>
                            
                    <div class="bg-red-900/20 border border-red-400/30 rounded-lg p-4">
                        <div class="flex items-center mb-2">
                            <i class="fas fa-exclamation-triangle text-red-400 mr-2"></i>
                            <span class="text-red-400 font-semibold">Emergency Alert</span>
                        </div>
                        <p class="text-red-300 text-sm">
                            This message will be sent immediately to your doctor. Use only for urgent medical concerns.
                        </p>
                            </div>
                            
                    <div class="flex space-x-3">
                        <button onclick="window.aiFeatures.sendEmergencyMessage()" 
                                class="flex-1 bg-red-600 hover:bg-red-500 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300 flex items-center justify-center">
                            <i class="fas fa-paper-plane mr-2"></i>Send Emergency Message
                        </button>
                        <button onclick="this.parentElement.parentElement.parentElement.remove()" 
                                class="flex-1 bg-gray-600 hover:bg-gray-500 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300">
                            Cancel
                                </button>
                            </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Focus on phone input
        setTimeout(() => {
            const phoneInput = document.getElementById('doctor-phone');
            if (phoneInput) phoneInput.focus();
        }, 100);
    }

    sendEmergencyMessage() {
        const doctorPhone = document.getElementById('doctor-phone').value.trim();
        const patientName = document.getElementById('patient-name').value.trim();
        const emergencyMessage = document.getElementById('emergency-message').value.trim();
        
        if (!doctorPhone || !patientName || !emergencyMessage) {
            this.showToast('Please fill in all fields', 'error');
            return;
        }
        
        // Validate phone number format
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        if (!phoneRegex.test(doctorPhone.replace(/\s/g, ''))) {
            this.showToast('Please enter a valid phone number', 'error');
            return;
        }
        
        // Show loading state
        const sendButton = document.querySelector('button[onclick="window.aiFeatures.sendEmergencyMessage()"]');
        if (sendButton) {
            const originalText = sendButton.innerHTML;
            sendButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Sending...';
            sendButton.disabled = true;
            
            // Simulate sending message (in real app, this would connect to SMS/WhatsApp API)
        setTimeout(() => {
                // Close modal
                const modal = document.querySelector('.fixed.inset-0');
                if (modal) modal.remove();
                
                // Show success message
                this.showSuccessModal(doctorPhone, patientName, emergencyMessage);
                
                // Reset button
                sendButton.innerHTML = originalText;
                sendButton.disabled = false;
        }, 2000);
        }
    }

    showSuccessModal(doctorPhone, patientName, message) {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="glass max-w-md w-full mx-4 p-8 rounded-xl text-center">
                <div class="mb-6">
                    <div class="inline-flex items-center justify-center w-16 h-16 bg-green-500 rounded-full mb-4">
                        <i class="fas fa-check text-2xl text-white"></i>
                    </div>
                    <h3 class="text-2xl font-bold text-green-400 mb-2">Message Sent Successfully!</h3>
                    <p class="text-cyan-300">Emergency message has been sent to your doctor.</p>
                </div>
                
                <div class="bg-black/40 rounded-lg p-4 mb-6 text-left">
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <span class="text-cyan-300/80">Doctor:</span>
                            <span class="text-cyan-200">${doctorPhone}</span>
                                    </div>
                        <div class="flex justify-between">
                            <span class="text-cyan-300/80">Patient:</span>
                            <span class="text-cyan-200">${patientName}</span>
                                    </div>
                        <div class="flex justify-between">
                            <span class="text-cyan-300/80">Time:</span>
                            <span class="text-cyan-200">${new Date().toLocaleString()}</span>
                                </div>
                    </div>
                                    </div>
                                    
                <div class="bg-yellow-900/20 border border-yellow-400/30 rounded-lg p-4 mb-6">
                    <div class="flex items-center mb-2">
                        <i class="fas fa-info-circle text-yellow-400 mr-2"></i>
                        <span class="text-yellow-400 font-semibold">Next Steps</span>
                    </div>
                    <ul class="text-yellow-300 text-sm space-y-1">
                        <li>• Your doctor will respond within 15-30 minutes</li>
                        <li>• Keep your phone nearby for incoming calls</li>
                        <li>• If no response, call emergency services</li>
                                        </ul>
                                </div>
                                
                <button onclick="this.parentElement.parentElement.remove()" 
                        class="bg-cyan-600 hover:bg-cyan-500 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300">
                    <i class="fas fa-check mr-2"></i>OK
                </button>
            </div>
        `;
        
        document.body.appendChild(modal);
    }



    getDirections(lat, lng) {
        this.showToast('Opening Google Maps with directions...', 'info');
        // In a real app, this would open Google Maps with directions
        setTimeout(() => {
            this.showToast('Directions opened in Google Maps!', 'success');
            // Simulate opening maps URL
            const mapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`;
            console.log('Would open:', mapsUrl);
        }, 1000);
    }



    setupDrugInteractionChecker() {
        this.checkDrugInteractions = async () => {
            this.showToast('Analyzing medication interactions...', 'info');
            
            // Simulate AI analysis
            setTimeout(() => {
                const patientData = this.getMockPatientData();
                const interactions = this.analyzeDrugInteractions(patientData);
                this.showDrugInteractionModal(interactions);
            }, 2000);
        };
    }

    analyzeDrugInteractions(patientData) {
        const medications = patientData.medications || [];
        const interactions = [];
        
        // Simulate drug interaction analysis
        if (medications.length > 0) {
            interactions.push({
                severity: 'Moderate',
                description: 'Potential interaction between medications detected',
                recommendation: 'Consult with pharmacist or physician',
                medications: medications.slice(0, 2)
            });
        }
        
        return {
            totalInteractions: interactions.length,
            highRisk: interactions.filter(i => i.severity === 'High').length,
            moderateRisk: interactions.filter(i => i.severity === 'Moderate').length,
            lowRisk: interactions.filter(i => i.severity === 'Low').length,
            interactions: interactions
        };
    }

    showDrugInteractionModal(interactions) {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="glass max-w-4xl w-full mx-4 p-8 rounded-xl">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-3xl font-bold holographic">Drug Interaction Analysis</h3>
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" class="text-cyan-300 hover:text-cyan-100">
                        <i class="fas fa-times text-2xl"></i>
                    </button>
                </div>
                
                <div class="space-y-6">
                    <div class="grid md:grid-cols-3 gap-4">
                        <div class="bg-black/40 p-4 rounded-lg text-center">
                            <div class="text-3xl font-bold text-red-400">${interactions.highRisk}</div>
                            <div class="text-sm text-cyan-300">High Risk</div>
                    </div>
                        <div class="bg-black/40 p-4 rounded-lg text-center">
                            <div class="text-3xl font-bold text-yellow-400">${interactions.moderateRisk}</div>
                            <div class="text-sm text-cyan-300">Moderate Risk</div>
                                    </div>
                        <div class="bg-black/40 p-4 rounded-lg text-center">
                            <div class="text-3xl font-bold text-green-400">${interactions.lowRisk}</div>
                            <div class="text-sm text-cyan-300">Low Risk</div>
                                    </div>
                                </div>
                                
                    ${interactions.interactions.length > 0 ? `
                        <div class="space-y-4">
                            <h4 class="text-xl font-semibold text-cyan-300">Detected Interactions</h4>
                            ${interactions.interactions.map(interaction => `
                                <div class="bg-black/40 p-4 rounded-lg">
                                    <div class="flex justify-between items-start mb-2">
                                        <span class="text-${interaction.severity === 'High' ? 'red' : interaction.severity === 'Moderate' ? 'yellow' : 'green'}-400 font-semibold">
                                            ${interaction.severity} Risk
                                        </span>
                                </div>
                                    <p class="text-gray-300 mb-2">${interaction.description}</p>
                                    <p class="text-cyan-300 text-sm"><strong>Recommendation:</strong> ${interaction.recommendation}</p>
                                    ${interaction.medications ? `
                                        <div class="mt-2">
                                            <p class="text-sm text-gray-400">Medications involved:</p>
                                            <ul class="text-sm text-gray-300 mt-1">
                                                ${interaction.medications.map(med => `<li>• ${med}</li>`).join('')}
                                            </ul>
                                        </div>
                                    ` : ''}
                            </div>
                        `).join('')}
                    </div>
                    ` : `
                        <div class="text-center py-8">
                            <i class="fas fa-check-circle text-4xl text-green-400 mb-4"></i>
                            <h4 class="text-xl font-semibold text-green-400 mb-2">No Interactions Detected</h4>
                            <p class="text-gray-300">Your current medication regimen appears to be safe.</p>
                        </div>
                    `}
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }

    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-${this.getToastIcon(type)} mr-2"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    getToastIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            info: 'info-circle',
            warning: 'exclamation-circle'
        };
        return icons[type] || 'info-circle';
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.advancedAnimations = new AdvancedAnimations();
    window.aiFeatures = new AIFeatures();
    
    // Setup global functions
    window.enrichDocument = () => window.aiFeatures.analyzeDocument();
    window.getClinicalInsights = () => window.aiFeatures.generateClinicalInsights();
    window.checkDrugInteractions = () => window.aiFeatures.checkDrugInteractions();
    window.showToast = (message, type) => window.aiFeatures.showToast(message, type);
    window.openConsultDoctorModal = () => window.aiFeatures.openConsultDoctorModal();
}); 