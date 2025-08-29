# Hospital Management System - Setup Guide

## Overview

This is a comprehensive Hospital Management System (HMS) built with Python FastAPI, featuring bilingual support (Arabic/English) and a modern web interface. The system includes modules for patient management, doctor registration, emergency care, laboratory, radiology, pharmacy, financial management, human resources, and warehouse management.

## Features

### Core Features
- ✅ **Bilingual Interface**: Full Arabic and English support with RTL layout
- ✅ **Role-Based Access Control**: Comprehensive user permissions system
- ✅ **Patient Management**: Complete patient registration and medical records
- ✅ **Doctor Management**: Doctor profiles with specializations and schedules
- ✅ **Authentication**: JWT-based secure login system
- ✅ **Dashboard**: Real-time statistics and quick actions
- ✅ **Theme Support**: Light, dark, and medical themes

### Hospital Modules
- 🏥 **Emergency Department**: Patient triage and emergency care
- 👥 **User Management**: Staff accounts and permissions
- 📅 **Appointments**: Scheduling and management
- 🧪 **Laboratory**: Test orders, results, and reports
- 📸 **Radiology**: Imaging orders and DICOM support
- 💊 **Pharmacy**: Medication inventory and dispensing
- 💰 **Financial Management**: Billing and payments
- 👨‍💼 **Human Resources**: Staff management and payroll
- 📦 **Warehouse**: Medical supplies and equipment
- 📋 **Reports**: Medical and administrative reports

## System Requirements

### Minimum Requirements
- **Python**: 3.11 or higher
- **Database**: PostgreSQL 13+ (recommended) or SQLite for development
- **Memory**: 2GB RAM minimum, 4GB recommended
- **Storage**: 10GB free space
- **OS**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)

### Optional Requirements
- **Redis**: For caching and background tasks
- **Docker**: For containerized deployment
- **Nginx**: For production reverse proxy

## Installation

### Method 1: Automated Setup (Recommended)

1. **Clone/Download the project**
   ```bash
   # If you have git
   git clone <repository-url>
   cd MS
   
   # Or extract the ZIP file and navigate to the folder
   ```

2. **Run the automated setup script**
   ```bash
   # On Linux/macOS
   chmod +x setup.sh
   ./setup.sh
   
   # On Windows (use Git Bash or WSL)
   bash setup.sh
   ```

   The script will:
   - Install Python dependencies
   - Create environment configuration
   - Initialize the database
   - Create sample data
   - Optionally start the server

### Method 2: Manual Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   # Copy the environment template
   cp .env.example .env
   
   # Edit the .env file with your settings
   nano .env  # or use your preferred editor
   ```

3. **Database Setup**
   ```bash
   # Initialize the database
   python scripts/init_db.py
   ```

4. **Start the Server**
   ```bash
   python start.py
   # or
   uvicorn main:app --reload
   ```

## Configuration

### Database Configuration

Edit the `.env` file to configure your database:

```env
# For PostgreSQL (Production)
DATABASE_URL=postgresql://username:password@localhost:5432/hospital_db

# For SQLite (Development)
DATABASE_URL=sqlite:///./hospital.db
```

### Key Settings

```env
# Security
SECRET_KEY=your-very-secure-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME="Hospital Management System"
DEBUG=True
ENVIRONMENT=development

# Language
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,ar
```

## Usage

### Accessing the System

1. **Web Interface**: http://localhost:8000
2. **API Documentation**: http://localhost:8000/docs
3. **Alternative API Docs**: http://localhost:8000/redoc

### Default Login Credentials

**⚠️ IMPORTANT: Change these credentials immediately after first login!**

- **Username**: `admin`
- **Password**: `admin123`
- **Role**: Administrator

### First Steps

1. **Login** with the default admin credentials
2. **Change the default password** in user settings
3. **Create departments** and customize them for your hospital
4. **Add doctors** and assign them to departments
5. **Configure user roles** and permissions
6. **Start registering patients** and using the system

## Module Guide

### User Management
- Create and manage user accounts
- Assign roles and permissions
- Control access to different modules
- Track user activity and sessions

### Patient Registration
- Complete patient demographics
- Medical history and allergies
- Insurance information
- Emergency contacts
- Generate unique patient IDs

### Doctor Management
- Professional credentials and licenses
- Specializations and departments
- Working schedules and availability
- Consultation fees and settings

### Emergency Department
- Patient triage and priority levels
- Vital signs tracking
- Treatment protocols
- Discharge planning

### Laboratory Module
- Predefined test catalog
- Test orders and sample tracking
- Results entry and verification
- Report generation

### Radiology Module
- Imaging exam types (X-Ray, CT, MRI, Ultrasound)
- DICOM image management
- Radiologist reporting
- Integration with PACS systems

### Pharmacy Module
- Medication inventory management
- Prescription processing
- Sales tracking and billing
- Controlled substance monitoring

### Financial Management
- Patient billing and invoices
- Insurance claims processing
- Payment tracking
- Financial reporting

## Security Features

### Authentication
- JWT-based token authentication
- Secure password hashing (bcrypt)
- Session management and tracking
- Multi-factor authentication support

### Authorization
- Role-Based Access Control (RBAC)
- Granular permissions system
- Resource-level access control
- Audit trail logging

### Data Protection
- Input validation and sanitization
- SQL injection protection
- XSS prevention
- CSRF protection
- Data encryption at rest

## API Documentation

The system provides a RESTful API with automatic documentation:

### Key Endpoints
- `POST /api/auth/login` - User authentication
- `GET /api/patients` - List patients
- `POST /api/patients` - Create new patient
- `GET /api/doctors` - List doctors
- `GET /api/dashboard/stats` - Dashboard statistics

### Authentication
All API endpoints (except login) require authentication:

```javascript
// Include JWT token in requests
Authorization: Bearer <your-jwt-token>
```

## Deployment

### Development
```bash
python start.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker Deployment
```bash
# Build image
docker build -t hospital-management-system .

# Run container
docker run -p 8000:8000 hospital-management-system
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check your database credentials in `.env`
   - Ensure PostgreSQL is running
   - Verify network connectivity

2. **Permission Denied Errors**
   - Check user roles and permissions
   - Verify JWT token is valid
   - Ensure user account is active

3. **Language/RTL Issues**
   - Clear browser cache
   - Check language setting in user preferences
   - Verify Arabic fonts are loading

4. **Import/Module Errors**
   - Ensure all dependencies are installed
   - Check Python path and virtual environment
   - Verify file permissions

### Getting Help

1. Check the error logs in the `logs/` directory
2. Review the API documentation at `/docs`
3. Verify your configuration in `.env`
4. Check database connectivity and permissions

## Development

### Project Structure
```
MS/
├── app/
│   ├── api/          # API endpoints
│   ├── auth/         # Authentication
│   ├── core/         # Configuration
│   ├── database/     # Database connection
│   ├── models/       # SQLAlchemy models
│   ├── services/     # Business logic
│   ├── static/       # CSS, JS, images
│   ├── templates/    # HTML templates
│   └── utils/        # Utility functions
├── scripts/          # Database and setup scripts
├── tests/           # Unit and integration tests
└── requirements.txt # Python dependencies
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For technical support and questions:
- Review this documentation
- Check the API documentation at `/docs`
- Review error logs in the `logs/` directory

---

**Hospital Management System v1.0.0**  
*Comprehensive Healthcare Solution*