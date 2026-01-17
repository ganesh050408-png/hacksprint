# Database Schema Documentation - Enhanced Version

## Overview
The Student Attendance System now includes 9 database models with comprehensive relationships for managing students, face recognition, achievements, attendance, leaves, and online meetings.

---

## Database Models

### 1. User (Base Authentication Model)
**Purpose:** Core user authentication and role management

**Fields:**
```
id (Integer) - Primary Key
username (String, Unique) - Login username
email (String, Unique) - User email
password (String) - Hashed password (PBKDF2)
role (Enum) - STUDENT | TEACHER | COUNSELLOR | ADMIN
full_name (String) - User's full name
created_at (DateTime) - Account creation timestamp
```

**Relationships:**
- `student` (One-to-One) → Student profile
- `teacher` (One-to-One) → Teacher profile
- `counsellor` (One-to-One) → Counsellor profile

**Enums:**
```python
class UserRole(enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    COUNSELLOR = "counsellor"
    ADMIN = "admin"
```

---

### 2. Student
**Purpose:** Student-specific information and face registration tracking

**Fields:**
```
id (Integer) - Primary Key
user_id (Integer, Foreign Key) - References User
roll_number (String, Unique) - Student roll number
registration_number (String, Unique) - Registration ID
course (String) - Course/Program name
semester (Integer) - Current semester
branch (String) - Branch/Department
phone (String) - Contact number
face_registered (Boolean) - Face encoding stored?
face_data_path (String) - Path to face image (if uploaded)
created_at (DateTime) - Profile creation timestamp
```

**Relationships:**
- `user` (One-to-One) ← User authentication
- `attendance_records` (One-to-Many) → Attendance
- `leave_applications` (One-to-Many) → LeaveApplication
- `qr_registrations` (One-to-Many) → QRCodeRegistration
- `achievements` (One-to-Many) → Achievement (NEW)

**Indexes:**
- `roll_number` (Unique)
- `registration_number` (Unique)
- `user_id` (Foreign Key)

---

### 3. Teacher
**Purpose:** Teacher/Instructor profile management

**Fields:**
```
id (Integer) - Primary Key
user_id (Integer, Foreign Key) - References User
employee_id (String, Unique) - Employee ID
department (String) - Department name
phone (String) - Contact number
created_at (DateTime) - Profile creation timestamp
```

**Relationships:**
- `user` (One-to-One) ← User authentication
- `lectures` (One-to-Many) → Lecture

---

### 4. Counsellor
**Purpose:** Counsellor/Advisor profile for leave approvals

**Fields:**
```
id (Integer) - Primary Key
user_id (Integer, Foreign Key) - References User
employee_id (String, Unique) - Employee ID
department (String) - Department name
phone (String) - Contact number
created_at (DateTime) - Profile creation timestamp
```

**Relationships:**
- `user` (One-to-One) ← User authentication
- `leave_applications` (One-to-Many) → LeaveApplication

---

### 5. Lecture (Active Session)
**Purpose:** Course lecture information and QR code management

**Fields:**
```
id (Integer) - Primary Key
teacher_id (Integer, Foreign Key) - References Teacher
course_code (String) - Course code (e.g., CS101)
course_name (String) - Full course name
date (Date) - Lecture date
start_time (Time) - Lecture start time
end_time (Time) - Lecture end time
is_active (Boolean) - Lecture currently active?
qr_code_data (String) - JSON QR code payload
created_at (DateTime) - Record creation timestamp
```

**QR Code Data Format:**
```json
{
    "type": "lecture_attendance",
    "lecture_id": 123,
    "teacher_id": 45,
    "course_code": "CS101"
}
```

**Relationships:**
- `teacher` (Many-to-One) ← Teacher
- `attendance_records` (One-to-Many) → Attendance
- `online_meetings` (One-to-Many) → OnlineMeeting

---

### 6. Attendance (Dual Verification)
**Purpose:** Track student attendance with QR code and face verification

**Fields:**
```
id (Integer) - Primary Key
student_id (Integer, Foreign Key) - References Student
lecture_id (Integer, Foreign Key) - References Lecture
qr_verified (Boolean) - QR code matched?
face_verified (Boolean) - Face matched?
marked_at (DateTime) - Attendance marking timestamp
face_match_score (Float) - Face match confidence (0.0-1.0)
status (String) - present | absent | cancelled
created_at (DateTime) - Record creation timestamp
```

**Status Values:**
- `present` - Both QR and face verified ✓
- `absent` - QR or face verification failed ✗
- `cancelled` - Lecture cancelled

**Relationships:**
- `student` (Many-to-One) ← Student
- `lecture` (Many-to-One) ← Lecture

**Indexes:**
- `student_id, lecture_id` (Unique constraint - one record per student per lecture)
- `created_at` (For sorting)

---

### 7. LeaveApplication
**Purpose:** Leave request management with counsellor approval

**Fields:**
```
id (Integer) - Primary Key
student_id (Integer, Foreign Key) - References Student
counsellor_id (Integer, Foreign Key) - References Counsellor (nullable)
start_date (Date) - Leave start date
end_date (Date) - Leave end date
reason (Text) - Reason for leave
status (String) - pending | approved | rejected
remarks (Text) - Counsellor remarks (nullable)
created_at (DateTime) - Application submission timestamp
updated_at (DateTime) - Last update timestamp
```

**Status Values:**
- `pending` - Awaiting counsellor approval
- `approved` - Counsellor approved ✓
- `rejected` - Counsellor rejected ✗

**Relationships:**
- `student` (Many-to-One) ← Student
- `counsellor` (Many-to-One) ← Counsellor (nullable)

---

### 8. OnlineMeeting
**Purpose:** Online meeting links for lectures

**Fields:**
```
id (Integer) - Primary Key
lecture_id (Integer, Foreign Key) - References Lecture
meeting_link (String) - URL to meeting room
meeting_password (String) - Meeting password (nullable)
platform (String) - zoom | teams | meet | jitsi
scheduled_time (DateTime) - Meeting scheduled time
created_at (DateTime) - Record creation timestamp
```

**Supported Platforms:**
- `zoom` - Zoom meetings
- `teams` - Microsoft Teams
- `meet` - Google Meet
- `jitsi` - Jitsi Meet
- `other` - Other platforms

**Relationships:**
- `lecture` (Many-to-One) ← Lecture

---

### 9. Achievement (NEW) ⭐
**Purpose:** Student certificate and achievement management

**Fields:**
```
id (Integer) - Primary Key
student_id (Integer, Foreign Key) - References Student
title (String, 200 chars) - Certificate title
organization (String, 200 chars) - Issuing organization
year (Integer) - Year obtained
description (Text) - Additional details (optional)
file_name (String, 255 chars) - Original filename
file_path (String, 500 chars) - Relative path to file
file_type (String, 50 chars) - pdf | jpg | png | jpeg
file_size (Integer) - Size in bytes
is_verified (Boolean) - Admin verification status
created_at (DateTime) - Upload timestamp
updated_at (DateTime) - Last update timestamp
```

**File Type Values:**
- `pdf` - PDF document
- `jpg` - JPEG image
- `png` - PNG image
- `jpeg` - Alternative JPEG format

**File Organization:**
```
static/certificates/
├── <roll_number_1>/
│   ├── Python_Certification_2024_<timestamp>.pdf
│   ├── Google_Award_2024_<timestamp>.jpg
│   └── ...
├── <roll_number_2>/
│   ├── Course_Certificate_<timestamp>.pdf
│   └── ...
```

**Relationships:**
- `student` (Many-to-One) ← Student
- Cascade delete with Student (if student deleted, achievements deleted)

**Indexes:**
- `student_id` (For filtering by student)
- `created_at` (For sorting by date)
- `is_verified` (For filtering by status)

---

## Database Diagram

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ username        │
│ email           │
│ password        │
│ role            │
│ full_name       │
│ created_at      │
└────────┬────────┘
         │
    ┌────┴─────┬──────────┬──────────┐
    │           │          │          │
    v           v          v          v
┌──────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐
│ Student  │ │Teacher │ │Counsellor│ │  Admin   │
└──────────┘ └────────┘ └──────────┘ └──────────┘
    │             │                        
    │             │                        
    ├─────────────┼──────────────┐         
    │             │              │         
    v             v              v         
┌──────────────┐ ┌─────────┐ ┌──────────┐
│ Attendance   │ │ Lecture │ │OnlineMeeting
└──────────────┘ └─────────┘ └──────────┘
    │             │                        
    └─────────────┘                        
                                         
    ├────────────┬──────────────┐        
    │            │              │        
    v            v              v        
┌──────────┐ ┌──────────┐ ┌────────────┐
│ Achievement │Leave│QRCode│
└──────────┘ └──────────┘ └────────────┘
```

---

## Key Features

### Relationships
- **One-to-One:** User ↔ Student, User ↔ Teacher, User ↔ Counsellor
- **One-to-Many:** Student → Attendance, Lecture → Attendance, etc.
- **Cascade Delete:** Student → Achievements (delete student = delete achievements)

### Unique Constraints
- `User.username` - Each username unique
- `User.email` - Each email unique
- `Student.roll_number` - Each roll number unique
- `Student.registration_number` - Each registration number unique
- `Attendance.(student_id, lecture_id)` - One record per student per lecture

### Indexes
- All Foreign Keys automatically indexed
- `created_at` indexed for sorting
- `student_id` indexed for filtering
- Unique constraints create indexes automatically

---

## Migration Path

### From Previous Version:
1. Add `Achievement` table
2. Add `achievements` relationship to Student
3. Create `static/certificates/` directory
4. Initialize student-specific subdirectories during first upload

### No Breaking Changes:
- All existing tables preserved
- All existing fields preserved
- Only additions (new model and relationships)

---

## Data Integrity

### Constraints:
1. **NOT NULL:** id, user_id, roll_number, registration_number, etc.
2. **UNIQUE:** username, email, roll_number, registration_number
3. **FOREIGN KEY:** All ForeignKey fields enforce referential integrity
4. **CHECK:** year >= 1900 AND year <= current_year (application-level)
5. **ENUM:** role must be valid UserRole value

### Validation:
- **Application-Level:** Python validation in routes
- **Database-Level:** Constraints enforced by SQLAlchemy/SQLite

---

## Database Size Estimation

### Record Counts (Example):
- Users: 500 (10 teachers, 10 counsellors, 480 students)
- Students: 480
- Lectures: 100
- Attendance: 48,000 (480 students × 100 lectures)
- Achievements: 1,000 (avg 2 per student)
- Leaves: 500
- Online Meetings: 100

### Storage Estimate:
- Database file: ~10-50 MB
- Face encodings: ~1 MB (480 students × ~2 KB each)
- Certificates: ~2-5 GB (avg 5 MB per student × 480 × 2 certificates)
- **Total: ~2-5 GB**

---

**Document Version:** 2.0 (Enhanced)  
**Last Updated:** January 2026  
**Status:** Production Ready  
