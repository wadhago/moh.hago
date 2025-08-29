# 🏥 Hospital Management System - Startup Guide

## Quick Start (Choose Your Method)

### Method 1: Automated Setup (Recommended)
```bash
# Navigate to the project directory
cd /Users/mohammedalmogadum/Desktop/MS

# Run the setup script (this will install everything)
bash setup.sh
```

### Method 2: Manual Step-by-Step
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Initialize the database
python scripts/init_db.py

# 3. Start the server
python start.py
```

### Method 3: Simple Run (Fallback)
```bash
# If other methods fail, use the simple runner
python run_simple.py
```

### Method 4: Verification First
```bash
# Check if everything is set up correctly
python verify_system.py

# Then start the system
python start.py
```

## 🔗 Access the System

Once the server starts successfully, you can access:

- **Main Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs  
- **ReDoc Documentation**: http://localhost:8000/redoc

## 🔐 Default Login Credentials

```
Username: admin
Password: admin123
```

**⚠️ IMPORTANT**: Change these credentials immediately after first login!

## 🚨 Troubleshooting Common Issues

### Issue 1: Python Not Found
**Error**: `command not found: python` or `python3`

**Solutions**:
1. **Install Python 3.8+** from https://python.org/downloads
2. **On macOS**: `brew install python3`
3. **On Ubuntu/Debian**: `sudo apt update && sudo apt install python3 python3-pip`
4. **On Windows**: Download from python.org or use Microsoft Store

### Issue 2: pip Not Found
**Error**: `command not found: pip`

**Solutions**:
1. **Use python -m pip instead**: `python -m pip install -r requirements.txt`
2. **Install pip**: `python -m ensurepip --upgrade`
3. **On Linux**: `sudo apt install python3-pip`

### Issue 3: Dependencies Installation Failed
**Error**: Various import errors

**Solutions**:
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# If specific packages fail, install individually:
pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib jinja2
```

### Issue 4: Database Errors
**Error**: Database connection or table errors

**Solutions**:
```bash
# Reinitialize database
python scripts/init_db.py

# Or use simple database creation
python run_simple.py
```

### Issue 5: Port Already in Use
**Error**: `Port 8000 is already in use`

**Solutions**:
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn main:app --port 8080
```

### Issue 6: Permission Errors
**Error**: Permission denied when creating files

**Solutions**:
```bash
# Make sure you have write permissions
chmod +x setup.sh
chmod +x scripts/init_db.py

# Create directories manually if needed
mkdir -p logs uploads app/static/uploads
```

## 🔧 Configuration Options

### Environment Variables (.env)
```env
# Database Configuration
DATABASE_URL=sqlite:///./hospital.db
# For PostgreSQL: postgresql://user:password@localhost:5432/hospital_db

# Security
SECRET_KEY=change-this-to-a-secure-random-string
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
DEBUG=True
APP_NAME=Hospital Management System
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,ar

# Server Settings
HOST=0.0.0.0
PORT=8000
```

### Database Options
```bash
# SQLite (Default - for development)
DATABASE_URL=sqlite:///./hospital.db

# PostgreSQL (Recommended for production)
DATABASE_URL=postgresql://username:password@localhost:5432/hospital_db

# MySQL (Alternative)
DATABASE_URL=mysql://username:password@localhost:3306/hospital_db
```

## 📱 First Steps After Starting

1. **Open your browser** and go to http://localhost:8000
2. **Login** with admin/admin123
3. **Change the default password** in user settings
4. **Explore the dashboard** and available modules
5. **Add sample data** (patients, doctors) to test the system

## 🌟 Available Features

### ✅ Working Features
- User authentication and management
- Bilingual interface (Arabic/English)
- Patient registration and management
- Doctor registration and profiles
- Dashboard with statistics
- Theme switching (Light/Dark/Medical)
- Role-based access control

### 🚧 Ready to Implement
- Emergency department workflows
- Laboratory test management
- Radiology and imaging
- Pharmacy inventory
- Financial billing
- HR management
- Warehouse tracking
- Report generation

## 🔄 Development Mode

For development with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🐳 Docker Alternative

If you prefer using Docker:
```bash
# Build the image
docker build -t hospital-management-system .

# Run the container
docker run -p 8000:8000 hospital-management-system
```

## 📚 Additional Resources

- **Setup Guide**: SETUP_GUIDE.md - Comprehensive installation guide
- **API Documentation**: http://localhost:8000/docs - Interactive API docs
- **System Requirements**: Python 3.8+, 2GB RAM, 10GB storage

## 🆘 Getting Help

If you're still having issues:

1. **Check the logs** in the `logs/` directory
2. **Run the verification script**: `python verify_system.py`
3. **Try the simple runner**: `python run_simple.py`
4. **Check Python installation**: `python --version`
5. **Verify dependencies**: `pip list`

## 🎯 Success Indicators

You'll know the system is running correctly when you see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Then you can access the web interface and see the Hospital Management System dashboard.

---

**Ready to manage your hospital efficiently! 🏥✨**