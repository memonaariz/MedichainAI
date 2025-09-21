// Futuristic Healthcare Platform JavaScript
class MediChainAI {
    constructor() {
        this.init();
        this.setupParticleSystem();
        this.setupAnimations();
        this.setupAI();
    }

    init() {
        // Initialize GSAP
        gsap.registerPlugin(ScrollTrigger);
        
        // Setup smooth scrolling
        this.setupSmoothScrolling();
        
        // Initialize particle system
        this.createParticles();
        
        // Setup AI brain animation
        this.setupAIBrain();
        
        // Setup DNA helix animation
        this.setupDNAHelix();
        
        // Setup medical cross animations
        this.setupMedicalCross();
        
        // Setup data stream effects
        this.setupDataStream();
        
        // Initialize toast system
        this.setupToastSystem();
        
        // Setup 3D card effects
        this.setup3DCards();
        
        // Setup glitch effects
        this.setupGlitchEffects();
        
        // Setup holographic text
        this.setupHolographicText();
        
        // Setup heartbeat animations
        this.setupHeartbeatAnimations();
        
        // Setup floating elements
        this.setupFloatingElements();
        
        // Setup cyber background
        this.setupCyberBackground();
        
        // Initialize AI chat system
        this.setupAIChat();
        
        // Setup document enrichment
        this.setupDocumentEnrichment();
        
        // Setup clinical insights
        this.setupClinicalInsights();
        
        // Setup hash retrieval
        this.setupHashRetrieval();
        
        // Setup file verification
        this.setupFileVerification();
        
        // Setup real-time monitoring
        this.setupRealTimeMonitoring();
    }

    setupSmoothScrolling() {
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    gsap.to(window, {
                        duration: 1,
                        scrollTo: { y: target, offsetY: 100 },
                        ease: "power2.inOut"
                    });
                }
            });
        });
    }

    createParticles() {
        const particleContainer = document.querySelector('.particles');
        if (!particleContainer) return;

        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 15 + 's';
            particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
            particleContainer.appendChild(particle);
        }
    }

    setupParticleSystem() {
        // Create floating particles
        const particles = [];
        const particleCount = 30;

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 15 + 's';
            document.body.appendChild(particle);
            particles.push(particle);
        }

        // Animate particles with GSAP
        particles.forEach((particle, index) => {
            gsap.to(particle, {
                y: -window.innerHeight - 100,
                x: Math.random() * 200 - 100,
                duration: 15 + Math.random() * 10,
                repeat: -1,
                delay: index * 0.5,
                ease: "none"
            });
        });
    }

    setupAnimations() {
        // Animate elements on scroll
        gsap.utils.toArray('.glass').forEach(element => {
            gsap.from(element, {
                scrollTrigger: {
                    trigger: element,
                    start: "top 80%",
                    end: "bottom 20%",
                    toggleActions: "play none none reverse"
                },
                y: 50,
                opacity: 0,
                duration: 1,
                ease: "power2.out"
            });
        });

        // Animate cyber buttons
        gsap.utils.toArray('.cyber-btn').forEach(button => {
            button.addEventListener('mouseenter', () => {
                gsap.to(button, {
                    scale: 1.05,
                    duration: 0.3,
                    ease: "power2.out"
                });
            });

            button.addEventListener('mouseleave', () => {
                gsap.to(button, {
                    scale: 1,
                    duration: 0.3,
                    ease: "power2.out"
                });
            });
        });
    }

    setupAIBrain() {
        const aiBrain = document.querySelector('.ai-brain');
        if (!aiBrain) return;

        // Create pulsing circles
        const circles = [];
        for (let i = 0; i < 3; i++) {
            const circle = document.createElement('div');
            circle.className = 'ai-brain-circle';
            circle.style.position = 'absolute';
            circle.style.border = '2px solid var(--primary-cyan)';
            circle.style.borderRadius = '50%';
            circle.style.left = '50%';
            circle.style.top = '50%';
            circle.style.transform = 'translate(-50%, -50%)';
            circle.style.width = (60 - i * 10) + 'px';
            circle.style.height = (60 - i * 10) + 'px';
            aiBrain.appendChild(circle);
            circles.push(circle);
        }

        // Animate circles
        circles.forEach((circle, index) => {
            gsap.to(circle, {
                scale: 1.2,
                opacity: 0.5,
                duration: 2,
                repeat: -1,
                yoyo: true,
                delay: index * 0.5,
                ease: "power2.inOut"
            });
        });
    }

    setupDNAHelix() {
        const dnaElements = document.querySelectorAll('.dna-helix');
        dnaElements.forEach(dna => {
            gsap.to(dna, {
                rotationY: 360,
                duration: 3,
                repeat: -1,
                ease: "none"
            });
        });
    }

    setupMedicalCross() {
        const crosses = document.querySelectorAll('.medical-cross');
        crosses.forEach(cross => {
            gsap.to(cross, {
                scale: 1.1,
                duration: 2,
                repeat: -1,
                yoyo: true,
                ease: "power2.inOut"
            });
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
        gsap.fromTo(toast, 
            { x: 100, opacity: 0 },
            { x: 0, opacity: 1, duration: 0.3, ease: "power2.out" }
        );
        
        // Animate out
        setTimeout(() => {
            gsap.to(toast, {
                x: 100,
                opacity: 0,
                duration: 0.3,
                ease: "power2.in",
                onComplete: () => toast.remove()
            });
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
                
                gsap.to(card, {
                    rotationX: rotateX,
                    rotationY: rotateY,
                    duration: 0.3,
                    ease: "power2.out"
                });
            });
            
            card.addEventListener('mouseleave', () => {
                gsap.to(card, {
                    rotationX: 0,
                    rotationY: 0,
                    duration: 0.3,
                    ease: "power2.out"
                });
            });
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

    setupHolographicText() {
        const holographicElements = document.querySelectorAll('.holographic');
        holographicElements.forEach(element => {
            gsap.to(element, {
                backgroundPosition: '100% 50%',
                duration: 3,
                repeat: -1,
                yoyo: true,
                ease: "power2.inOut"
            });
        });
    }

    setupHeartbeatAnimations() {
        const heartbeats = document.querySelectorAll('.heartbeat');
        heartbeats.forEach(heart => {
            gsap.to(heart, {
                scale: 1.1,
                duration: 0.75,
                repeat: -1,
                yoyo: true,
                ease: "power2.inOut"
            });
        });
    }

    setupFloatingElements() {
        const floatingElements = document.querySelectorAll('.float');
        floatingElements.forEach(element => {
            gsap.to(element, {
                y: -20,
                duration: 3,
                repeat: -1,
                yoyo: true,
                ease: "power2.inOut"
            });
        });
    }

    setupCyberBackground() {
        const cyberBg = document.querySelector('.cyber-bg');
        if (cyberBg) {
            gsap.to(cyberBg, {
                opacity: 0.6,
                duration: 4,
                repeat: -1,
                yoyo: true,
                ease: "power2.inOut"
            });
        }
    }

    setupAI() {
        // AI Chat System
        this.setupAIChat();
        
        // AI Document Analysis
        this.setupDocumentAnalysis();
        
        // AI Clinical Insights
        this.setupClinicalInsights();
        
        // AI Risk Assessment
        this.setupRiskAssessment();
        
        // AI Treatment Recommendations
        this.setupTreatmentRecommendations();
    }

    setupAIChat() {
        const chatContainer = document.getElementById('chat-container');
        if (!chatContainer) return;

        // Initialize chat with AI responses
        this.aiResponses = {
            'patient': 'I can help you with patient information. What would you like to know?',
            'medication': 'Let me analyze the medication data for you.',
            'diagnosis': 'I\'ll review the diagnostic information.',
            'lab': 'I can help you understand the lab results.',
            'treatment': 'Based on the data, here are my treatment recommendations.'
        };

        // Add typing animation
        this.addTypingAnimation = () => {
            const typingDiv = document.createElement('div');
            typingDiv.className = 'typing-indicator';
            typingDiv.innerHTML = `
                <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 bg-cyan-400 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                    <div class="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                </div>
            `;
            chatContainer.appendChild(typingDiv);
            return typingDiv;
        };
    }

    setupDocumentAnalysis() {
        // Enhanced document analysis with AI
        this.analyzeDocument = async (file) => {
            this.showToast('Analyzing document with AI...', 'info');
            
            // Simulate AI analysis
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            const analysis = {
                confidence: Math.random() * 0.3 + 0.7,
                extractedData: {
                    patientInfo: 'John Doe',
                    medications: ['Aspirin', 'Metformin'],
                    conditions: ['Diabetes', 'Hypertension'],
                    labResults: ['Blood glucose: 120 mg/dL']
                },
                recommendations: [
                    'Monitor blood glucose regularly',
                    'Continue current medication regimen',
                    'Schedule follow-up appointment'
                ]
            };
            
            this.showAnalysisResults(analysis);
        };
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
        // AI-powered clinical insights
        this.generateClinicalInsights = async () => {
            this.showToast('Generating clinical insights...', 'info');
            
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            const insights = {
                riskLevel: 'Moderate',
                riskFactors: ['Age > 65', 'Multiple medications', 'Chronic conditions'],
                recommendations: [
                    'Increase monitoring frequency',
                    'Consider medication review',
                    'Implement preventive measures'
                ],
                alerts: [
                    'Potential drug interactions detected',
                    'Blood pressure monitoring recommended'
                ]
            };
            
            this.showClinicalInsights(insights);
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
        // AI risk assessment system
        this.assessRisk = async (patientData) => {
            // Simulate AI risk assessment
            const riskScore = Math.random() * 100;
            const riskLevel = riskScore > 70 ? 'High' : riskScore > 40 ? 'Moderate' : 'Low';
            
            return {
                score: riskScore.toFixed(1),
                level: riskLevel,
                factors: this.generateRiskFactors(riskScore)
            };
        };
    }

    generateRiskFactors(score) {
        const factors = [
            'Age-related risk factors',
            'Medication interactions',
            'Chronic conditions',
            'Lifestyle factors',
            'Family history'
        ];
        
        return factors.slice(0, Math.floor(score / 20) + 1);
    }

    setupTreatmentRecommendations() {
        // AI treatment recommendation system
        this.generateTreatmentPlan = async (diagnosis) => {
            const treatments = {
                'diabetes': [
                    'Blood glucose monitoring',
                    'Dietary modifications',
                    'Exercise regimen',
                    'Medication management'
                ],
                'hypertension': [
                    'Blood pressure monitoring',
                    'Sodium restriction',
                    'Stress management',
                    'Medication compliance'
                ],
                'default': [
                    'Regular check-ups',
                    'Lifestyle modifications',
                    'Medication adherence',
                    'Preventive care'
                ]
            };
            
            return treatments[diagnosis.toLowerCase()] || treatments.default;
        };
    }

    setupDocumentEnrichment() {
        // Enhanced document enrichment with AI
        this.enrichDocument = async () => {
            this.showToast('Enriching document with AI...', 'info');
            
            await new Promise(resolve => setTimeout(resolve, 2500));
            
            const enrichedData = {
                extractedFields: {
                    patientName: 'John Doe',
                    dateOfBirth: '1985-03-15',
                    medications: ['Aspirin', 'Metformin', 'Lisinopril'],
                    conditions: ['Diabetes Type 2', 'Hypertension'],
                    labResults: ['HbA1c: 7.2%', 'Blood Pressure: 140/90'],
                    vitalSigns: ['Heart Rate: 72 bpm', 'Temperature: 98.6°F']
                },
                confidence: 0.94,
                processingTime: '2.3 seconds',
                aiInsights: [
                    'Potential drug interaction detected',
                    'Blood pressure above normal range',
                    'HbA1c indicates suboptimal control'
                ]
            };
            
            this.showEnrichmentResults(enrichedData);
        };
    }

    showEnrichmentResults(data) {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="glass max-w-5xl w-full mx-4 p-8 rounded-xl">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-3xl font-bold holographic">AI Document Enrichment</h3>
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" class="text-cyan-300 hover:text-cyan-100">
                        <i class="fas fa-times text-2xl"></i>
                    </button>
                </div>
                
                <div class="grid md:grid-cols-2 gap-6">
                    <div class="space-y-4">
                        <div class="bg-black/40 p-4 rounded-lg">
                            <h4 class="text-xl font-semibold text-cyan-300 mb-3">Extracted Data</h4>
                            <div class="space-y-2 text-sm">
                                <div><strong>Patient:</strong> ${data.extractedFields.patientName}</div>
                                <div><strong>DOB:</strong> ${data.extractedFields.dateOfBirth}</div>
                                <div><strong>Medications:</strong> ${data.extractedFields.medications.join(', ')}</div>
                                <div><strong>Conditions:</strong> ${data.extractedFields.conditions.join(', ')}</div>
                            </div>
                        </div>
                        
                        <div class="bg-black/40 p-4 rounded-lg">
                            <h4 class="text-xl font-semibold text-cyan-300 mb-3">AI Insights</h4>
                            <ul class="space-y-2 text-sm">
                                ${data.aiInsights.map(insight => `<li class="text-yellow-400">🔍 ${insight}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                    
                    <div class="space-y-4">
                        <div class="bg-black/40 p-4 rounded-lg">
                            <h4 class="text-xl font-semibold text-cyan-300 mb-3">Processing Stats</h4>
                            <div class="space-y-2 text-sm">
                                <div><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(1)}%</div>
                                <div><strong>Processing Time:</strong> ${data.processingTime}</div>
                                <div><strong>Fields Extracted:</strong> ${Object.keys(data.extractedFields).length}</div>
                            </div>
                        </div>
                        
                        <div class="bg-black/40 p-4 rounded-lg">
                            <h4 class="text-xl font-semibold text-cyan-300 mb-3">Vital Signs & Labs</h4>
                            <div class="space-y-2 text-sm">
                                ${data.extractedFields.labResults.map(result => `<div>🔬 ${result}</div>`).join('')}
                                ${data.extractedFields.vitalSigns.map(vital => `<div>❤️ ${vital}</div>`).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }

    setupHashRetrieval() {
        // Enhanced hash-based data retrieval
        this.retrieveByHash = async (hash) => {
            this.showToast('Retrieving data from blockchain...', 'info');
            
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            const retrievedData = {
                patientInfo: {
                    name: 'John Doe',
                    dob: '1985-03-15',
                    gender: 'Male',
                    mrn: 'MRN123456'
                },
                medicalData: {
                    medications: ['Aspirin', 'Metformin', 'Lisinopril'],
                    conditions: ['Diabetes Type 2', 'Hypertension'],
                    allergies: ['Penicillin'],
                    labResults: ['HbA1c: 7.2%', 'Creatinine: 1.1 mg/dL']
                },
                blockchainInfo: {
                    blockIndex: 1234,
                    timestamp: '2024-01-15 14:30:22',
                    hash: hash,
                    verified: true
                }
            };
            
            this.showRetrievedData(retrievedData);
        };
    }

    showRetrievedData(data) {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="glass max-w-5xl w-full mx-4 p-8 rounded-xl">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-3xl font-bold holographic">Blockchain Data Retrieved</h3>
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" class="text-cyan-300 hover:text-cyan-100">
                        <i class="fas fa-times text-2xl"></i>
                    </button>
                </div>
                
                <div class="grid md:grid-cols-3 gap-6">
                    <div class="bg-black/40 p-4 rounded-lg">
                        <h4 class="text-xl font-semibold text-cyan-300 mb-3">Patient Information</h4>
                        <div class="space-y-2 text-sm">
                            <div><strong>Name:</strong> ${data.patientInfo.name}</div>
                            <div><strong>DOB:</strong> ${data.patientInfo.dob}</div>
                            <div><strong>Gender:</strong> ${data.patientInfo.gender}</div>
                            <div><strong>MRN:</strong> ${data.patientInfo.mrn}</div>
                        </div>
                    </div>
                    
                    <div class="bg-black/40 p-4 rounded-lg">
                        <h4 class="text-xl font-semibold text-cyan-300 mb-3">Medical Data</h4>
                        <div class="space-y-2 text-sm">
                            <div><strong>Medications:</strong> ${data.medicalData.medications.join(', ')}</div>
                            <div><strong>Conditions:</strong> ${data.medicalData.conditions.join(', ')}</div>
                            <div><strong>Allergies:</strong> ${data.medicalData.allergies.join(', ')}</div>
                        </div>
                    </div>
                    
                    <div class="bg-black/40 p-4 rounded-lg">
                        <h4 class="text-xl font-semibold text-cyan-300 mb-3">Blockchain Info</h4>
                        <div class="space-y-2 text-sm">
                            <div><strong>Block:</strong> #${data.blockchainInfo.blockIndex}</div>
                            <div><strong>Timestamp:</strong> ${data.blockchainInfo.timestamp}</div>
                            <div><strong>Verified:</strong> <span class="text-green-400">✓ Yes</span></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }

    setupFileVerification() {
        // Enhanced file verification with blockchain
        this.verifyFile = async (file) => {
            this.showToast('Verifying file integrity...', 'info');
            
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            const verification = {
                integrity: true,
                blockchainVerified: true,
                timestamp: new Date().toISOString(),
                hash: this.generateHash(file.name),
                details: {
                    fileSize: '2.4 MB',
                    uploadTime: '2024-01-15 14:30:22',
                    lastModified: '2024-01-15 14:25:10',
                    checksum: 'SHA-256 verified'
                }
            };
            
            this.showVerificationResults(verification);
        };
    }

    generateHash(text) {
        // Simple hash generation for demo
        let hash = 0;
        for (let i = 0; i < text.length; i++) {
            const char = text.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash).toString(16);
    }

    showVerificationResults(verification) {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="glass max-w-2xl w-full mx-4 p-8 rounded-xl">
                <div class="text-center">
                    <div class="mb-6">
                        ${verification.integrity ? 
                            '<i class="fas fa-shield-check text-6xl text-green-400 mb-4"></i>' :
                            '<i class="fas fa-exclamation-triangle text-6xl text-red-400 mb-4"></i>'
                        }
                        <h3 class="text-3xl font-bold ${verification.integrity ? 'text-green-400' : 'text-red-400'}">
                            ${verification.integrity ? 'File Integrity Verified' : 'Integrity Check Failed'}
                        </h3>
                    </div>
                    
                    <div class="space-y-4 text-left">
                        <div class="bg-black/40 p-4 rounded-lg">
                            <h4 class="text-xl font-semibold text-cyan-300 mb-3">Verification Details</h4>
                            <div class="space-y-2 text-sm">
                                <div><strong>Blockchain Verified:</strong> <span class="text-green-400">✓ Yes</span></div>
                                <div><strong>File Size:</strong> ${verification.details.fileSize}</div>
                                <div><strong>Upload Time:</strong> ${verification.details.uploadTime}</div>
                                <div><strong>Checksum:</strong> ${verification.details.checksum}</div>
                                <div><strong>Hash:</strong> <code class="text-xs">${verification.hash}</code></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }

    setupRealTimeMonitoring() {
        // Real-time system monitoring
        this.startMonitoring = () => {
            setInterval(() => {
                this.updateSystemStatus();
            }, 5000);
        };
        
        this.updateSystemStatus = () => {
            const statusElements = document.querySelectorAll('.system-status');
            statusElements.forEach(element => {
                const status = Math.random() > 0.1 ? 'Online' : 'Warning';
                const color = status === 'Online' ? 'text-green-400' : 'text-yellow-400';
                element.className = `system-status ${color}`;
                element.textContent = status;
            });
        };
    }
}

// Initialize the futuristic healthcare platform
document.addEventListener('DOMContentLoaded', () => {
    window.mediChainAI = new MediChainAI();
    
    // Start real-time monitoring
    window.mediChainAI.startMonitoring();
    
    // Setup global functions for HTML buttons
    window.enrichDocument = () => window.mediChainAI.enrichDocument();
    window.getClinicalInsights = () => window.mediChainAI.generateClinicalInsights();
    window.retrieveByHash = (hash) => window.mediChainAI.retrieveByHash(hash);
    window.verifyFile = (file) => window.mediChainAI.verifyFile(file);
    window.analyzeDocument = (file) => window.mediChainAI.analyzeDocument(file);
}); 