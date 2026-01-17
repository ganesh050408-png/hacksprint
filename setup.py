#!/usr/bin/env python
"""
Setup script for Student Attendance System
Run this script to initialize the database and create admin users
"""

import os
import sys
from datetime import datetime

def setup_database():
    """Initialize the database"""
    print("=" * 60)
    print("Setting up Student Attendance System Database")
    print("=" * 60)
    
    try:
        from app import create_app
        from app.models import db, User, Student, Teacher, Counsellor, UserRole
        from app.utils.auth import hash_password
        
        app = create_app('development')
        
        with app.app_context():
            print("\n[1/3] Creating database tables...")
            db.create_all()
            print("✓ Database tables created successfully!")
            
            print("\n[2/3] Creating sample data...")
            
            # Check if sample data already exists
            if User.query.filter_by(username='student1').first():
                print("⚠ Sample data already exists. Skipping...")
            else:
                # Create sample student
                student_user = User(
                    username='student1',
                    email='student1@example.com',
                    password=hash_password('password123'),
                    full_name='John Doe',
                    role=UserRole.STUDENT
                )
                db.session.add(student_user)
                db.session.flush()
                
                student = Student(
                    user_id=student_user.id,
                    roll_number='STU001',
                    registration_number='REG001',
                    course='B.Tech',
                    semester=1,
                    branch='CSE',
                    phone='9876543210',
                    face_registered=False
                )
                db.session.add(student)
                
                # Create sample teacher
                teacher_user = User(
                    username='teacher1',
                    email='teacher1@example.com',
                    password=hash_password('password123'),
                    full_name='Dr. Jane Smith',
                    role=UserRole.TEACHER
                )
                db.session.add(teacher_user)
                db.session.flush()
                
                teacher = Teacher(
                    user_id=teacher_user.id,
                    employee_id='EMP001',
                    department='Computer Science',
                    phone='9876543210'
                )
                db.session.add(teacher)
                
                # Create sample counsellor
                counsellor_user = User(
                    username='counsellor1',
                    email='counsellor1@example.com',
                    password=hash_password('password123'),
                    full_name='Mr. Robert Brown',
                    role=UserRole.COUNSELLOR
                )
                db.session.add(counsellor_user)
                db.session.flush()
                
                counsellor = Counsellor(
                    user_id=counsellor_user.id,
                    employee_id='EMP002',
                    department='Student Affairs',
                    phone='9876543210'
                )
                db.session.add(counsellor)
                
                db.session.commit()
                print("✓ Sample data created successfully!")
            
            print("\n[3/3] Creating required directories...")
            os.makedirs('uploads', exist_ok=True)
            os.makedirs('student_faces', exist_ok=True)
            print("✓ Directories created successfully!")
            
            print("\n" + "=" * 60)
            print("Database setup completed successfully!")
            print("=" * 60)
            print("\nSample Credentials:")
            print("-" * 60)
            print("Student:")
            print("  Username: student1")
            print("  Password: password123")
            print("-" * 60)
            print("Teacher:")
            print("  Username: teacher1")
            print("  Password: password123")
            print("-" * 60)
            print("Counsellor:")
            print("  Username: counsellor1")
            print("  Password: password123")
            print("=" * 60)
            print("\nYou can now run the application with: python run.py")
            
    except Exception as e:
        print(f"\n✗ Error during setup: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def reset_database():
    """Reset the database (WARNING: This will delete all data)"""
    print("=" * 60)
    print("WARNING: This will delete all data from the database!")
    print("=" * 60)
    
    response = input("\nAre you sure you want to reset the database? (yes/no): ").strip().lower()
    
    if response == 'yes':
        try:
            from app import create_app
            from app.models import db
            
            app = create_app('development')
            
            with app.app_context():
                print("\nResetting database...")
                db.drop_all()
                db.create_all()
                print("✓ Database reset successfully!")
                
                # Recreate sample data
                setup_database()
        
        except Exception as e:
            print(f"✗ Error resetting database: {str(e)}")
            sys.exit(1)
    else:
        print("Reset cancelled.")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        reset_database()
    else:
        setup_database()
