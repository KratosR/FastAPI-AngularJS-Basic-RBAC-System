from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models, auth
from app.database import get_db

router = APIRouter(prefix="/instructors", tags=["Instructors"])

@router.post("/", response_model=schemas.Instructor)
def create_instructor(instructor: schemas.InstructorCreate,
                      db: Session = Depends(get_db),
                      current_user: models.User = Depends(auth.get_current_active_user)):
    if not auth.has_permission(db, current_user.role, "admin"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    try:
        return crud.create_instructor(db, instructor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.Instructor])
def read_instructors(skip: int = 0, limit: int = 100,
                     db: Session = Depends(get_db),
                     current_user: models.User = Depends(auth.get_current_active_user)):
    return crud.get_instructors(db, skip=skip, limit=limit)

@router.get("/{instructor_id}", response_model=schemas.Instructor)
def read_instructor(instructor_id: int,
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(auth.get_current_active_user)):
    instructor = crud.get_instructor(db, instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return instructor

@router.get("/by-user/{user_id}", response_model=schemas.Instructor)
def read_instructor_by_user(user_id: int,
                            db: Session = Depends(get_db),
                            current_user: models.User = Depends(auth.get_current_active_user)):
    instructor = crud.get_instructor_by_user(db, user_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor record not found for this user")
    return instructor

@router.patch("/{instructor_id}", response_model=schemas.Instructor)
def update_instructor(instructor_id: int,
                      instructor_update: schemas.InstructorUpdate,
                      db: Session = Depends(get_db),
                      current_user: models.User = Depends(auth.get_current_active_user)):
    # Only admins can update instructor records
    if not auth.has_permission(db, current_user.role, "admin"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    updated_instructor = crud.update_instructor(db, instructor_id, instructor_update)
    if not updated_instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return updated_instructor

@router.delete("/{instructor_id}", response_model=schemas.Instructor)
def delete_instructor(instructor_id: int,
                      db: Session = Depends(get_db),
                      current_user: models.User = Depends(auth.get_current_active_user)):
    if not auth.has_permission(db, current_user.role, "admin"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    deleted_instructor = crud.delete_instructor(db, instructor_id)
    if not deleted_instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return deleted_instructor