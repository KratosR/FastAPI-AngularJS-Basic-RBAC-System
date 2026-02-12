from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models, auth
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, 
                db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_active_user)):
    if not auth.has_permission(db, current_user.role, "admin"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        return crud.create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, 
               db: Session = Depends(get_db),
               current_user: models.User = Depends(auth.get_current_active_user)):
    return crud.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=schemas.UserWithRelations)
def read_user(user_id: int, 
              db: Session = Depends(get_db),
              current_user: models.User = Depends(auth.get_current_active_user)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, 
                user_update: schemas.UserUpdate, 
                db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_active_user)):
    if current_user.id != user_id and not auth.has_permission(db, current_user.role, "admin"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    updated_user = crud.update_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: int,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_active_user)):
    if not auth.has_permission(db, current_user.role, "admin"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    deleted_user = crud.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user