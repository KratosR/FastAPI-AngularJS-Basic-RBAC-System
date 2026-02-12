from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_password_hash

# ----- Roles -----
def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()

def get_role_by_name(db: Session, role_name: str):
    return db.query(models.Role).filter(models.Role.role_name == role_name).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()

def create_role(db: Session, role: schemas.RoleCreate):
    if role.parent_id is not None:
        parent = get_role(db, role.parent_id)
        if not parent:
            raise ValueError(f"Parent role with id {role.parent_id} does not exist")
    db_role = models.Role(**role.model_dump())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int):
    role = get_role(db, role_id)
    if not role:
        return None
    if role.children:
        raise ValueError("Cannot delete role with sub-roles")
    if role.users:
        raise ValueError("Cannot delete role assigned to users")
    db.delete(role)
    db.commit()
    return role

# ----- Users -----
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    role = get_role(db, user.role_id)
    if not role:
        raise ValueError(f"Role with id {user.role_id} does not exist")
    hashed_pw = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_pw,
        role_id=user.role_id,
        status=user.status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user

# ----- Students -----
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_student_by_user(db: Session, user_id: int):
    return db.query(models.Student).filter(models.Student.user_id == user_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: schemas.StudentCreate):
    user = get_user(db, student.user_id)
    if not user:
        raise ValueError(f"User with id {student.user_id} does not exist")
    if get_student_by_user(db, student.user_id):
        raise ValueError(f"User {student.user_id} already has a student record")
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, student_update: schemas.StudentUpdate):
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    update_data = student_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    student = get_student(db, student_id)
    if not student:
        return None
    db.delete(student)
    db.commit()
    return student

# ----- Instructors -----
def get_instructor(db: Session, instructor_id: int):
    return db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()

def get_instructor_by_user(db: Session, user_id: int):
    return db.query(models.Instructor).filter(models.Instructor.user_id == user_id).first()

def get_instructors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Instructor).offset(skip).limit(limit).all()

def create_instructor(db: Session, instructor: schemas.InstructorCreate):
    user = get_user(db, instructor.user_id)
    if not user:
        raise ValueError(f"User with id {instructor.user_id} does not exist")
    if get_instructor_by_user(db, instructor.user_id):
        raise ValueError(f"User {instructor.user_id} already has an instructor record")
    db_instructor = models.Instructor(**instructor.model_dump())
    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor

def update_instructor(db: Session, instructor_id: int, instructor_update: schemas.InstructorUpdate):
    db_instructor = get_instructor(db, instructor_id)
    if not db_instructor:
        return None
    update_data = instructor_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_instructor, field, value)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor

def delete_instructor(db: Session, instructor_id: int):
    instructor = get_instructor(db, instructor_id)
    if not instructor:
        return None
    db.delete(instructor)
    db.commit()
    return instructor