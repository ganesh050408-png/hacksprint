# Student Attendance System - User Guide

## 📋 Table of Contents
1. System Overview
2. User Roles & Features
3. Step-by-Step Workflows
4. Technical Details
5. Troubleshooting

---

## 🎯 System Overview

The Student Attendance System is an automated attendance management solution that uses:
- **Face Recognition** to identify students
- **QR Code Verification** for lecture authentication
- **Dual Verification** for secure attendance marking
- **Leave Management** with counsellor approval

### Key Components
```
┌─────────────────────────────────────────┐
│        Student Attendance System        │
├─────────────────────────────────────────┤
│  ✓ Web-Based Interface (Flask)          │
│  ✓ Face Recognition Engine (OpenCV)     │
│  ✓ QR Code System                       │
│  ✓ Database (SQLAlchemy)                │
│  ✓ User Management & Roles              │
│  ✓ Leave Workflow                       │
│  ✓ Online Meeting Integration           │
└─────────────────────────────────────────┘
```

---

## 👥 User Roles & Features

### 👨‍🎓 Student
**Features:**
- Register with academic details
- Register face for identification
- Mark attendance via QR + Face verification
- View attendance history and statistics
- Apply for leave
- Access online meetings
- Track leave applications

**Access Points:**
- Dashboard: `/student/dashboard`
- Mark Attendance: `/student/mark-attendance`
- Apply Leave: `/student/apply-leave`
- View Leaves: `/student/leaves`
- Online Meetings: `/student/online-meetings`
- Attendance History: `/student/attendance-history`

### 👨‍🏫 Teacher
**Features:**
- Create lectures
- Generate QR codes
- Monitor student attendance
- View attendance reports

**Access Points:**
- Dashboard: `/teacher/dashboard`
- Create Lecture: `/teacher/lectures/create`
- QR Display: `/teacher/lectures/<id>/qr`
- Attendance View: `/teacher/attendance`

### 👨‍💼 Counsellor
**Features:**
- Review leave applications
- Approve/reject leaves
- Add remarks to applications
- Generate leave reports

**Access Points:**
- Dashboard: `/counsellor/dashboard`
- Leave Requests: `/counsellor/leaves`
- Approve Leave: `/counsellor/leaves/<id>/approve`

### 👨‍💻 Admin
**Features:**
- User management
- System configuration
- Generate reports
- System maintenance

---

## 📖 Step-by-Step Workflows

### Workflow 1: Student Registration & First Login

```
Step 1: Register Account
├─ Go to http://localhost:5000
├─ Click "Register"
├─ Fill Personal Details
│  ├─ Full Name
│  ├─ Email
│  ├─ Phone
│  └─ Password
├─ Fill Academic Details
│  ├─ Roll Number
│  ├─ Registration Number
│  ├─ Course
│  ├─ Semester
│  └─ Branch
└─ Submit Registration

Step 2: First Login
├─ Click "Login"
├─ Enter Credentials
│  ├─ Username/Email
│  └─ Password
└─ Click "Login"

Step 3: Face Registration
├─ Dashboard shows "Register Face"
├─ Click "Register Face"
├─ Upload Clear Face Photo
│  ├─ Format: JPG, PNG
│  ├─ Quality: High resolution
│  └─ Visibility: Full face visible
├─ Click "Register Face"
└─ ✅ Face Registered!
```

### Workflow 2: Marking Attendance

```
During Lecture:

Step 1: Teacher Setup
├─ Teacher Creates Lecture
├─ Lecture becomes Active
└─ Teacher displays QR Code

Step 2: Student Marks Attendance
├─ Student goes to "Mark Attendance"
├─ Scan/Copy QR Code Data
├─ Submit QR Code
├─ Upload Face Image
│  ├─ Clear lighting
│  ├─ Front-facing
│  └─ Similar to registration
└─ Submit for Verification

Step 3: Verification Process
├─ System verifies QR Code
│  └─ ✓ Must be valid lecture QR
├─ System verifies Face
│  ├─ ✓ Must match registered face
│  └─ ✓ Confidence > 60%
└─ If both verified:
   ✅ Attendance MARKED as PRESENT
   If not verified:
   ❌ Attendance MARKED as ABSENT

Step 4: Confirmation
├─ Student sees attendance status
├─ Match confidence score displayed
└─ Can view in "Attendance History"
```

### Workflow 3: Applying for Leave

```
Step 1: Initiate Leave Request
├─ Go to "Apply Leave"
├─ Select Start Date
├─ Select End Date
│  └─ Must be after start date
├─ Write Reason (detailed)
│  ├─ Medical emergency
│  ├─ Family event
│  └─ Personal reasons
└─ Click "Submit"

Step 2: Submission Confirmation
├─ Application Status: PENDING
├─ Notification sent to Counsellor
└─ Can view in "My Leaves"

Step 3: Counsellor Reviews
├─ Counsellor receives notification
├─ Reviews application
├─ Approves or Rejects
│  └─ May add remarks
└─ Student receives update

Step 4: Student Sees Result
├─ Status updates to:
│  ├─ APPROVED ✓
│  ├─ REJECTED ✗
│  └─ With remarks from counsellor
└─ Attendance not counted during leave period
```

### Workflow 4: Accessing Online Meetings

```
Step 1: View Available Meetings
├─ Go to "Online Meetings"
├─ See all scheduled meetings
│  ├─ Platform (Zoom, Teams, Google Meet)
│  ├─ Scheduled time
│  └─ Meeting password (if any)
└─ Click "Join Meeting"

Step 2: Join Meeting
├─ Redirected to meeting platform
├─ Enter password if required
├─ Attend lecture
└─ Meeting attendance tracked
```

---

## 🔐 Technical Details

### Face Recognition System

**How It Works:**
```
1. Registration Phase:
   └─ Photo → Face Detection → Encoding (128-D Vector) → Storage

2. Recognition Phase:
   └─ Photo → Face Detection → Encoding (128-D Vector) → Comparison

3. Matching:
   └─ Distance Calculation → Confidence Score → Pass/Fail
      └─ Distance < 0.4 → MATCH ✓
      └─ Distance ≥ 0.4 → NO MATCH ✗
```

**Accuracy:** 99.38% on standard datasets

### QR Code System

**QR Code Contains:**
```json
{
  "type": "lecture_attendance",
  "lecture_id": 123,
  "teacher_id": 456,
  "course_code": "CS101"
}
```

**Verification:**
- QR decoded → Data extracted → Lecture matched → Status validated

### Dual Verification Logic

```
┌──────────────────────┐
│ Mark Attendance Form │
└──────────────────────┘
           ↓
    ┌──────────────┐
    │ Verify QR    │
    │ Verify Face  │
    └──────────────┘
           ↓
   ┌──────────────────┐
   │ QR Valid?        │ ──→ NO → Attendance ABSENT
   └──────────────────┘
           ↓ YES
   ┌──────────────────┐
   │ Face Match?      │ ──→ NO → Attendance ABSENT
   │ Confidence > 60% │
   └──────────────────┘
           ↓ YES
   ┌──────────────────┐
   │ ✅ ATTENDANCE    │
   │    MARKED        │
   └──────────────────┘
```

### Database Relationships

```
User
├── Student
│   ├── Attendance
│   ├── LeaveApplication
│   └── QRCodeRegistration
├── Teacher
│   └── Lecture
│       ├── Attendance
│       ├── QRCodeRegistration
│       └── OnlineMeeting
└── Counsellor
    └── LeaveApplication
```

---

## 🆘 Troubleshooting

### Issue 1: Face Not Recognized

**Symptoms:**
- "No match found" error
- Low confidence score (< 60%)

**Solutions:**
```
Try:
1. ✓ Use better lighting
2. ✓ Take centered, clear photo
3. ✓ Remove sunglasses/hat
4. ✓ Match original registration photo style
5. ✓ Re-register face with better quality
```

### Issue 2: QR Code Error

**Symptoms:**
- "Invalid QR code" error
- QR not accepted

**Solutions:**
```
Try:
1. ✓ Scan QR code again
2. ✓ Verify QR data is complete
3. ✓ Check lecture is active
4. ✓ Ensure QR is from current lecture
5. ✓ Ask teacher for new QR code
```

### Issue 3: Cannot Login

**Symptoms:**
- "Invalid username/email or password"

**Solutions:**
```
Try:
1. ✓ Check caps lock is off
2. ✓ Verify username/email spelling
3. ✓ Reset password (contact admin)
4. ✓ Try with email instead of username
```

### Issue 4: Face Registration Failed

**Symptoms:**
- "No face detected" error
- "Multiple faces detected" error

**Solutions:**
```
For "No face detected":
1. ✓ Ensure face is clearly visible
2. ✓ Check lighting is adequate
3. ✓ Take photo from straight angle

For "Multiple faces detected":
1. ✓ Remove other people from photo
2. ✓ Ensure only your face visible
3. ✓ Take photo alone
```

### Issue 5: Page Not Loading

**Symptoms:**
- 404 error
- Blank page

**Solutions:**
```
Try:
1. ✓ Refresh page (F5)
2. ✓ Clear browser cache
3. ✓ Check URL is correct
4. ✓ Log out and log in again
5. ✓ Restart application
```

---

## 📊 Dashboard Overview

### Student Dashboard Shows:
```
┌─────────────────────────────────────┐
│   Student Dashboard                 │
├─────────────────────────────────────┤
│                                     │
│  Total Lectures:        [  25  ]    │
│  Present:               [  23  ]    │
│  Attendance %:          [ 92.0% ]   │
│  Face Registration:     [ ✓ Done ]  │
│                                     │
│  Quick Actions:                     │
│  [Mark Attendance] [Apply Leave]    │
│  [Online Meetings] [Register Face]  │
│                                     │
│  Recent Attendance:                 │
│  ├─ CS101 - Present ✓               │
│  ├─ CS102 - Absent ✗                │
│  └─ CS103 - Present ✓               │
│                                     │
│  Pending Leaves:                    │
│  ├─ 5-7 Jan 2024 - PENDING          │
│  └─ 10-12 Jan 2024 - APPROVED       │
│                                     │
└─────────────────────────────────────┘
```

---

## 🚀 Getting Started

1. **Installation**: See QUICKSTART.md
2. **First Login**: Use sample credentials
3. **Register Face**: Complete within 24 hours
4. **Check Schedule**: Know lecture times
5. **Mark Attendance**: During each lecture

---

## 💾 Important Information

### Face Registration
- ✓ Required for attendance marking
- ✓ One-time setup (can re-register if needed)
- ✓ Face stored securely as encoding
- ✓ Original photo deleted after processing

### Attendance Rules
- ✓ Both QR and Face must be verified
- ✓ Can only mark during lecture time
- ✓ Each lecture marked only once
- ✓ Cannot retroactively mark attendance

### Leave Policy
- ✓ Submit before absence
- ✓ Requires reason details
- ✓ Needs counsellor approval
- ✓ Can track status in real-time

---

## 📞 Support

For issues:
1. Check Troubleshooting section
2. Review documentation in README.md
3. Check browser console for errors
4. Contact system administrator

---

**Student Attendance System v1.0**
**Documentation Last Updated: January 11, 2026**
