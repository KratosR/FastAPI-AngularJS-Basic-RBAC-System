from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models, auth
from app.database import get_db

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(auth.get_current_active_user)):
    if not auth.has_permission(db, current_user.role, "instructor"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    try:
        return crud.create_student(db, student)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 100,
                  db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_active_user)):
    if not auth.has_permission(db, current_user.role, "instructor"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.get_students(db, skip=skip, limit=limit)

@router.get("/{student_id}", response_model=schemas.Student)
def read_student(student_id: int,
                 db: Session = Depends(get_db),
                 current_user: models.User = Depends(auth.get_current_active_user)):
    if not auth.has_permission(db, current_user.role, "instructor"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/by-user/{user_id}", response_model=schemas.Student)
def read_student_by_user(user_id: int,
                         db: Session = Depends(get_db),
                         current_user: models.User = Depends(auth.get_current_active_user)):
    if not auth.has_permission(db, current_user.role, "instructor"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    student = crud.get_student_by_user(db, user_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student record not found for this user")
    return student

@router.patch("/{student_id}", response_model=schemas.Student)
def update_student(student_id: int,
                   student_update: schemas.StudentUpdate,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(auth.get_current_active_user)):
    # Instructors and admins can update students
    if not auth.has_permission(db, current_user.role, "instructor"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    updated_student = crud.update_student(db, student_id, student_update)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

@router.delete("/{student_id}", response_model=schemas.Student)
def delete_student(student_id: int,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(auth.get_current_active_user)):
    # Only admins can delete students – instructors cannot.
    if not auth.has_permission(db, current_user.role, "admin"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    deleted_student = crud.delete_student(db, student_id)
    if not deleted_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return deleted_student