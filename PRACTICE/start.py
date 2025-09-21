#!/usr/bin/env python3
"""
Startup Script for MediChain AI - Blockchain-Secured AI Healthcare System
This script initializes and starts the enhanced healthcare platform.
"""

import os
import sys
import time
import subprocess
from datetime import datetime

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking system dependencies...")
    
    required_packages = [
        'flask',
        'cryptography',
        'numpy',
        'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package} - Available")
        except ImportError:
            print(f"  ❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Please install missing dependencies:")
        print("pip install -r requirements.txt")
        return False
    
    print("  ✅ All dependencies available\n")
    return True

def check_files():
    """Check if required files exist"""
    print("📁 Checking system files...")
    
    required_files = [
        'app.py',
        'blockchain.py',
        'ccda_parser.py',
        'templates/index.html',
        'static/css/futuristic.css',
        'static/js/futuristic.js'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✓ {file_path} - Found")
        else:
            print(f"  ❌ {file_path} - Missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Missing files: {', '.join(missing_files)}")
        print("Please ensure all system files are present")
        return False
    
    print("  ✅ All required files found\n")
    return True

def initialize_system():
    """Initialize the MediChain AI system"""
    print("🚀 Initializing MediChain AI System...")
    
    try:
        # Import and initialize blockchain
        from blockchain import get_enhanced_blockchain
        blockchain = get_enhanced_blockchain()
        
        print(f"  ✓ Blockchain initialized with {len(blockchain.chain)} blocks")
        print(f"  ✓ Security level: {blockchain.security_level}")
        print(f"  ✓ Encryption: {'Enabled' if blockchain.encryption_enabled else 'Disabled'}")
        
        # Import CCDA parser
        from ccda_parser import parse_ccda_for_display
        print("  ✓ CCDA parser loaded")
        
        # Import Flask app
        from app import app
        print("  ✓ Flask application loaded")
        
        print("  ✅ System initialization completed\n")
        return True
        
    except Exception as e:
        print(f"  ❌ System initialization failed: {e}")
        return False

def start_web_server():
    """Start the web server"""
    print("🌐 Starting Web Server...")
    
    try:
        # Check if port 5000 is available
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5000))
        sock.close()
        
        if result == 0:
            print("  ⚠️ Port 5000 is already in use")
            print("  Please stop any existing services on port 5000")
            return False
        
        print("  ✓ Port 5000 available")
        
        # Start the Flask application
        print("  ✓ Starting Flask development server...")
        print("  ✓ Server will be available at: http://localhost:5000")
        print("  ✓ Press Ctrl+C to stop the server")
        print("\n" + "="*60)
        print("🚀 MediChain AI is starting up...")
        print("="*60)
        
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"  ❌ Failed to start web server: {e}")
        return False

def show_system_info():
    """Display system information"""
    print("🏥 MediChain AI - Blockchain-Secured AI Healthcare System")
    print("=" * 60)
    print(f"Version: 2.0.0")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print(f"Platform: {sys.platform}")
    print("=" * 60)
    print()

def show_features():
    """Display system features"""
    print("✨ System Features:")
    print("  🔒 Enhanced Blockchain Security")
    print("    - Proof of Work consensus")
    print("    - AES-256 encryption")
    print("    - Digital signatures")
    print("    - Audit trail")
    print()
    print("  🤖 AI-Powered Healthcare Intelligence")
    print("    - Disease prediction algorithms")
    print("    - Medicine recommendation system")
    print("    - Clinical risk assessment")
    print("    - Treatment planning")
    print()
    print("  📄 Advanced Medical Data Processing")
    print("    - CCDA/XML document parsing")
    print("    - Patient data extraction")
    print("    - Lab result analysis")
    print("    - Vital signs monitoring")
    print()
    print("  🎨 Futuristic User Interface")
    print("    - Modern responsive design")
    print("    - Advanced animations")
    print("    - Real-time data visualization")
    print("    - Interactive medical assistant")
    print()

def main():
    """Main startup function"""
    show_system_info()
    show_features()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Please install missing packages.")
        return False
    
    # Check files
    if not check_files():
        print("❌ File check failed. Please ensure all system files are present.")
        return False
    
    # Initialize system
    if not initialize_system():
        print("❌ System initialization failed.")
        return False
    
    # Start web server
    print("🎯 Ready to start web server...")
    time.sleep(2)
    
    return start_web_server()

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ System startup failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Startup interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error during startup: {e}")
        sys.exit(1) 