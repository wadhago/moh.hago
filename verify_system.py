#!/usr/bin/env python3
"""
System verification script for Hospital Management System
This script checks if all requirements are met before running the system
"""

import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {sys.version}")
        return False
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'jose',
        'passlib',
        'jinja2'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
            print(f"❌ {package} - Not installed")
        else:
            print(f"✅ {package} - Installed")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def check_database():
    """Check database configuration"""
    print("\n🗄️  Checking database configuration...")
    
    env_file = ".env"
    if not os.path.exists(env_file):
        print("❌ .env file not found")
        print("   Run: cp .env.example .env")
        return False
    else:
        print("✅ .env file exists")
    
    # Check if database file exists for SQLite
    db_file = "hospital.db"
    if os.path.exists(db_file):
        print("✅ Database file exists")
    else:
        print("⚠️  Database file not found")
        print("   Run: python scripts/init_db.py")
    
    return True

def check_directories():
    """Check if required directories exist"""
    print("\n📁 Checking directories...")
    
    required_dirs = [
        'app',
        'app/static',
        'app/templates',
        'scripts',
        'logs',
        'uploads'
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ - Missing")
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"   ✅ Created {directory}/")
            except Exception as e:
                print(f"   ❌ Failed to create {directory}/: {e}")
                return False
    
    return True

def main():
    """Main verification function"""
    print("🏥 Hospital Management System - System Verification")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Database", check_database),
        ("Directories", check_directories)
    ]
    
    all_passed = True
    
    for check_name, check_function in checks:
        try:
            if not check_function():
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name} check failed: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✅ All checks passed! System is ready to run.")
        print("\n🚀 To start the system:")
        print("   python start.py")
        print("\n🔗 Then visit: http://localhost:8000")
        print("🔐 Default login: admin / admin123")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\n📚 For help, see:")
        print("   - SETUP_GUIDE.md")
        print("   - RUN_INSTRUCTIONS.md")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)