#!/usr/bin/env python3
"""
Simple run script for Hospital Management System
Handles database creation and server startup
"""

import os
import sys
import sqlite3
from datetime import date
import hashlib

def create_simple_database():
    """Create a simple SQLite database if it doesn't exist"""
    db_path = "hospital.db"
    
    if os.path.exists(db_path):
        print(f"✅ Database already exists: {db_path}")
        return True
    
    print(f"🗄️  Creating database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'receptionist',
            permissions TEXT,
            is_active BOOLEAN DEFAULT 1,
            is_verified BOOLEAN DEFAULT 0,
            preferred_language TEXT DEFAULT 'en',
            preferred_theme TEXT DEFAULT 'light',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create departments table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            name_ar TEXT,
            code TEXT UNIQUE NOT NULL,
            description TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create patients table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id TEXT PRIMARY KEY,
            patient_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            first_name_ar TEXT,
            last_name_ar TEXT,
            date_of_birth DATE NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT,
            national_id TEXT UNIQUE,
            nationality TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Insert admin user
        admin_password = hashlib.sha256("admin123".encode()).hexdigest()  # Simple hash for demo
        cursor.execute('''
        INSERT OR IGNORE INTO users 
        (id, username, email, full_name, phone, hashed_password, role, is_active, is_verified)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'admin-001',
            'admin', 
            'admin@hospital.com',
            'System Administrator',
            '+966123456789',
            admin_password,
            'admin',
            1,
            1
        ))
        
        # Insert sample departments
        departments = [
            ('dept-001', 'Emergency Department', 'قسم الطوارئ', 'EMER'),
            ('dept-002', 'Cardiology', 'أمراض القلب', 'CARD'),
            ('dept-003', 'Pediatrics', 'طب الأطفال', 'PEDI'),
        ]
        
        for dept_id, name, name_ar, code in departments:
            cursor.execute('''
            INSERT OR IGNORE INTO departments (id, name, name_ar, code)
            VALUES (?, ?, ?, ?)
            ''', (dept_id, name, name_ar, code))
        
        conn.commit()
        conn.close()
        
        print("✅ Database created successfully!")
        print("📊 Created tables: users, departments, patients")
        print("👤 Admin user created: admin / admin123")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Hospital Management System server...")
    
    try:
        # Try to import and start uvicorn
        import uvicorn
        from main import app
        
        print("✅ FastAPI application loaded successfully")
        print("🌐 Starting server at http://localhost:8000")
        print("📚 API docs will be at http://localhost:8000/docs")
        print("🔐 Login with: admin / admin123")
        print("\n" + "=" * 50)
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,  # Set to False to avoid file watching issues
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try installing dependencies: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def main():
    """Main function"""
    print("🏥 Hospital Management System - Quick Start")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ main.py not found. Please run from the project directory.")
        return False
    
    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        print("📝 Creating .env file...")
        with open(".env", "w") as f:
            f.write("""DATABASE_URL=sqlite:///./hospital.db
SECRET_KEY=hospital-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
APP_NAME=Hospital Management System
DEFAULT_LANGUAGE=en
""")
        print("✅ .env file created")
    
    # Create necessary directories
    dirs = ["logs", "uploads", "app/static/uploads"]
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
    
    # Create database
    if not create_simple_database():
        return False
    
    # Start server
    start_server()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)