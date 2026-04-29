#!/usr/bin/env python
"""
Setup script to initialize the Crop Recommendation project
This script verifies all required dependencies are installed
"""

import sys
import subprocess

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = {
        'django': 'Django',
        'pandas': 'pandas',
        'sklearn': 'scikit-learn',
        'joblib': 'joblib',
        'cv2': 'opencv-python',
        'imutils': 'imutils',
        'matplotlib': 'matplotlib',
        'numpy': 'numpy',
        'openpyxl': 'openpyxl'
    }
    
    print("=" * 60)
    print("Checking Project Dependencies...")
    print("=" * 60)
    
    missing = []
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✓ {package} - OK")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print("\n" + "=" * 60)
        print("Installing missing packages...")
        print("=" * 60)
        cmd = [sys.executable, '-m', 'pip', 'install'] + missing
        subprocess.check_call(cmd)
        print("\n✓ All packages installed successfully!")
    else:
        print("\n✓ All dependencies are already installed!")
    
    print("\n" + "=" * 60)
    print("Setup Complete! Ready to run the project.")
    print("=" * 60)

if __name__ == '__main__':
    check_dependencies()
