import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas, crud

def seed_all():
    db = SessionLocal()
    try:
        # ----- 1. ROLES (idempotent) -----
        admin_role = crud.get_role_by_name(db, "admin")
        if not admin_role:
            admin_role = crud.create_role(db, schemas.RoleCreate(role_name="admin", parent_id=None))
        
        instructor_role = crud.get_role_by_name(db, "instructor")
        if not instructor_role:
            instructor_role = crud.create_role(db, schemas.RoleCreate(role_name="instructor", parent_id=admin_role.id))
        
        student_role = crud.get_role_by_name(db, "student")
        if not student_role:
            student_role = crud.create_role(db, schemas.RoleCreate(role_name="student", parent_id=instructor_role.id))

        # ----- 2. USERS -----
        # --- Admin (1) ---
        admin_user = crud.get_user_by_username(db, "admin")
        if not admin_user:
            admin_user = crud.create_user(db, schemas.UserCreate(
                username="admin",
                email="admin@example.com",
                password="admin123",
                role_id=admin_role.id,
                status=models.UserStatus.ACTIVE
            ))

        # --- Instructors (5 total) ---
        instructor_data = [
            ("prof_smith", "smith@example.com", "password"),
            ("prof_jones", "jones@example.com", "password"),
            ("prof_taylor", "taylor@example.com", "password"),
            ("prof_brown", "brown@example.com", "password"),
            ("prof_wilson", "wilson@example.com", "password"),
        ]

        instructor_users = []
        for username, email, password in instructor_data:
            user = crud.get_user_by_username(db, username)
            if not user:
                user = crud.create_user(db, schemas.UserCreate(
                    username=username,
                    email=email,
                    password=password,
                    role_id=instructor_role.id,
                    status=models.UserStatus.ACTIVE
                ))
            instructor_users.append(user)

        # --- Students (10 total) ---
        student_data = [
            ("john_doe", "john@example.com", "password"),
            ("jane_smith", "jane.smith@example.com", "password"),
            ("bob_johnson", "bob.johnson@example.com", "password"),
            ("alice_williams", "alice.williams@example.com", "password"),
            ("charlie_brown", "charlie.brown@example.com", "password"),
            ("diana_prince", "diana.prince@example.com", "password"),
            ("peter_parker", "peter.parker@example.com", "password"),
            ("bruce_wayne", "bruce.wayne@example.com", "password"),
            ("clark_kent", "clark.kent@example.com", "password"),
            ("tony_stark", "tony.stark@example.com", "password"),
        ]

        student_users = []
        for username, email, password in student_data:
            user = crud.get_user_by_username(db, username)
            if not user:
                user = crud.create_user(db, schemas.UserCreate(
                    username=username,
                    email=email,
                    password=password,
                    role_id=student_role.id,
                    status=models.UserStatus.ACTIVE
                ))
            student_users.append(user)

        # ----- 3. INSTRUCTOR DETAILS (one per instructor user) -----
        instructor_details = [
            ("prof_smith", "Computer Science", "PhD"),
            ("prof_jones", "Mathematics", "PhD"),
            ("prof_taylor", "Physics", "MSc"),
            ("prof_brown", "Chemistry", "PhD"),
            ("prof_wilson", "Biology", "MSc"),
        ]

        for username, dept, qual in instructor_details:
            user = crud.get_user_by_username(db, username)
            if user and not crud.get_instructor_by_user(db, user.id):
                crud.create_instructor(db, schemas.InstructorCreate(
                    user_id=user.id,
                    department=dept,
                    qualification=qual
                ))

        # ----- 4. STUDENT DETAILS (one per student user) -----
        student_details = [
            ("john_doe", "S12345", "BSc CS", 2),
            ("jane_smith", "S12346", "BSc Maths", 1),
            ("bob_johnson", "S12347", "BSc Physics", 3),
            ("alice_williams", "S12348", "BSc Chemistry", 2),
            ("charlie_brown", "S12349", "BA English", 4),
            ("diana_prince", "S12350", "BA History", 2),
            ("peter_parker", "S12351", "BSc Biology", 1),
            ("bruce_wayne", "S12352", "BBA", 3),
            ("clark_kent", "S12353", "BJMC", 2),
            ("tony_stark", "S12354", "BEng", 4),
        ]

        for username, enroll, course, year in student_details:
            user = crud.get_user_by_username(db, username)
            if user and not crud.get_student_by_user(db, user.id):
                crud.create_student(db, schemas.StudentCreate(
                    user_id=user.id,
                    enrollment_no=enroll,
                    course=course,
                    year=year
                ))

        print("✅ Sample data seeded successfully.")
        print(f"   - Roles: admin, instructor, student")
        print(f"   - Users: 1 admin, {len(instructor_users)} instructors, {len(student_users)} students")
        print(f"   - Details: {len(instructor_details)} instructor profiles, {len(student_details)} student profiles")
        print(f"   - Role:Admin : username: admin : password: admin123")
        print(f"   - Role:Instructor : username: prof_smith : password: password")
        print(f"   - Role:Student : username: tony_stark : password: password")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        raise
    finally:
        db.close()