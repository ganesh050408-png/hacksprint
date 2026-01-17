# Quick Start Guide

## Installation & Setup

### Step 1: Create Virtual Environment
```bash
python -m venv venv
```

### Step 2: Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Database
```bash
python setup.py
```

This will:
- Create all database tables
- Create sample user accounts for testing
- Create necessary directories

### Step 5: Run the Application
```bash
python run.py
```

The application will be available at: **http://localhost:5000**

---

## Sample Login Credentials

### Student Account
- **Username:** student1
- **Password:** password123

### Teacher Account
- **Username:** teacher1
- **Password:** password123

### Counsellor Account
- **Username:** counsellor1
- **Password:** password123

---

## First Time User Guide

### As a Student:

1. **Login** with your account
2. **Register Your Face:**
   - Go to Dashboard → Register Face (if not done)
   - Upload a clear photo of your face
   - System will process and store your face encoding

3. **Mark Attendance:**
   - Go to Mark Attendance
   - Wait for teacher to display QR code
   - Scan QR code (paste QR data)
   - Upload face image for verification
   - Attendance marked if both verifications pass

4. **Apply for Leave:**
   - Go to Apply Leave
   - Select dates and reason
   - Submit for counsellor approval

5. **View Online Meetings:**
   - Go to Online Meetings
   - Click meeting link to join

---

## File Structure

```
attendance_system/
├── app/                      # Main application package
│   ├── __init__.py          # Flask app factory
│   ├── models/              # Database models
│   ├── routes/              # Route blueprints
│   ├── utils/               # Utility functions
│   ├── face_recognition/    # Face recognition logic
│   ├── templates/           # HTML templates
│   └── static/              # CSS and JS files
├── config.py                # Configuration settings
├── run.py                   # Application entry point
├── setup.py                 # Database setup script
├── requirements.txt         # Python dependencies
├── README.md               # Full documentation
└── QUICKSTART.md          # This file
```

---

## Common Commands

### Database Reset
```bash
python setup.py reset
```

### Create Admin User
```bash
python
>>> from app import create_app
>>> from app.models import db, User, UserRole
>>> from app.utils.auth import hash_password
>>> app = create_app()
>>> with app.app_context():
...     user = User(username='admin', email='admin@example.com',
...                 password=hash_password('admin123'),
...                 full_name='Admin User', role=UserRole.ADMIN)
...     db.session.add(user)
...     db.session.commit()
>>> exit()
```

---

## Features Checklist

- [x] Student Registration with Academic Details
- [x] Face Registration & Recognition
- [x] QR Code Generation & Verification
- [x] Dual Verification (QR + Face)
- [x] Attendance Marking
- [x] Attendance History & Statistics
- [x] Leave Application & Management
- [x] Online Meeting Links
- [x] User Dashboard
- [x] Responsive UI with Bootstrap

---

## Troubleshooting

### Port 5000 Already in Use
Change port in `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module Not Found Error
Reinstall requirements:
```bash
pip install -r requirements.txt --upgrade
```

### Database Errors
Reset and reinitialize:
```bash
python setup.py reset
```

### Face Recognition Issues
- Ensure good lighting
- Use clear, frontal photo
- File format: JPG, PNG, or GIF
- Image quality: High resolution

---

## Production Deployment

1. Update `config.py` for production settings
2. Set `FLASK_ENV=production`
3. Use PostgreSQL instead of SQLite
4. Enable HTTPS/SSL
5. Use Gunicorn or similar WSGI server:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

---

## Support & Help

- Check `README.md` for detailed documentation
- Review code comments for implementation details
- Check browser console for JavaScript errors
- Check application logs for errors

---

**Enjoy using Student Attendance System!** 🎓
