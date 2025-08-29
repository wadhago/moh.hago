# Hospital Management System - Quick Run Instructions

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database
```bash
python scripts/init_db.py
```

### Step 3: Start Server
```bash
python start.py
```

## 🔗 Access the System

- **Web Interface**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔐 Default Login

- **Username**: admin
- **Password**: admin123

**⚠️ Change password after first login!**

## 🌟 Features Available

### ✅ Implemented & Working
- User authentication and authorization
- Bilingual interface (Arabic/English)
- Theme switching (Light/Dark/Medical)
- Patient registration and management
- Doctor registration and management
- Department management
- Dashboard with real-time stats
- Role-based access control
- Comprehensive database models

### 🚧 Ready for Implementation
- Emergency department workflows
- Laboratory test management
- Radiology imaging workflows
- Pharmacy inventory and sales
- Financial billing and payments
- HR employee management
- Warehouse inventory tracking
- Medical reports generation

## 📱 Interface Features

### Language Support
- Click the language switcher in the top-right (🇺🇸 English / 🇸🇦 العربية)
- Full RTL support for Arabic
- All text translates automatically

### Theme Support
- Click theme switcher in top-right
- Light theme (☀️)
- Dark theme (🌙)
- Medical theme (🏥)

### Navigation
- Responsive sidebar navigation
- Mobile-friendly interface
- Quick actions dashboard
- Real-time statistics

## 🏥 Module Access

Based on your role, you'll have access to different modules:

### Admin Users
- All modules and full permissions
- User management
- System configuration

### Doctor Users
- Patient records (read/write)
- Medical records
- Prescriptions
- Laboratory/Radiology orders

### Nurse Users
- Patient vital signs
- Basic patient information
- Emergency department

### Receptionist Users
- Patient registration
- Appointment scheduling
- Basic patient information

## 🔧 Configuration

### Environment Variables (.env)
```env
# Database (SQLite for development)
DATABASE_URL=sqlite:///./hospital.db

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
DEFAULT_LANGUAGE=en
```

### Database Options

**Development (SQLite)**:
```env
DATABASE_URL=sqlite:///./hospital.db
```

**Production (PostgreSQL)**:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/hospital_db
```

## 📊 Sample Data

The initialization script creates:
- 1 Admin user (admin/admin123)
- Hospital departments (Emergency, Cardiology, etc.)
- 2 Sample doctors
- 2 Sample patients

## 🚨 Troubleshooting

### Common Issues

**1. Module Import Errors**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**2. Database Errors**
```bash
# Solution: Reinitialize database
python scripts/init_db.py
```

**3. Permission Errors**
```bash
# Solution: Check .env file permissions and database file access
```

**4. Port Already in Use**
```bash
# Solution: Change port in start.py or kill process on port 8000
```

## 🔄 Development Workflow

### Making Changes
1. Edit code files
2. Server auto-reloads (if started with --reload)
3. Check browser for changes

### Adding New Features
1. Create/modify models in `app/models/`
2. Add API endpoints in `app/api/`
3. Update templates in `app/templates/`
4. Add styles in `app/static/css/`

### Database Changes
1. Modify models
2. Run: `python scripts/init_db.py` (recreates tables)
3. Or implement proper migrations for production

## 📚 API Usage Examples

### Authentication
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Get Patients
```bash
curl -X GET "http://localhost:8000/api/patients" \
  -H "Authorization: Bearer <your-token>"
```

### Create Patient
```bash
curl -X POST "http://localhost:8000/api/patients" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Ahmed",
    "last_name": "Al-Rashid", 
    "date_of_birth": "1990-01-01",
    "gender": "male",
    "phone": "+966501234567"
  }'
```

## 🎯 Next Steps

1. **Customize for your hospital**:
   - Update hospital name and branding
   - Configure departments and specializations
   - Set up user roles and permissions

2. **Implement additional modules**:
   - Complete the emergency department workflow
   - Add laboratory test management
   - Implement pharmacy inventory
   - Set up financial billing

3. **Production deployment**:
   - Configure PostgreSQL database
   - Set up proper security measures
   - Configure backup procedures
   - Set up monitoring and logging

## 🆘 Support

If you encounter issues:
1. Check the console output for error messages
2. Review the SETUP_GUIDE.md for detailed information
3. Check the API documentation at http://localhost:8000/docs
4. Verify your .env configuration

---

**Ready to revolutionize your hospital's management system! 🏥✨**