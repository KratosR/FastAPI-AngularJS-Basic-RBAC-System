from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models, auth
from app.database import get_db

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, 
                db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_active_user)):
    if not auth.has_permission(db, current_user.role, "admin"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if crud.get_role_by_name(db, role.role_name):
        raise HTTPException(status_code=400, detail="Role already exists")
    try:
        return crud.create_role(db, role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.Role])
def read_roles(skip: int = 0, limit: int = 100, 
               db: Session = Depends(get_db),
               current_user: models.User = Depends(auth.get_current_active_user)):
    return crud.get_roles(db, skip=skip, limit=limit)

@router.get("/{role_id}", response_model=schemas.Role)
def read_role(role_id: int, 
              db: Session = Depends(get_db),
              current_user: models.User = Depends(auth.get_current_active_user)):
    role = crud.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.delete("/{role_id}", response_model=schemas.Role)
def delete_role(role_id: int,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_active_user)):
    if not auth.has_permission(db, current_user.role, "admin"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    try:
        deleted_role = crud.delete_role(db, role_id)
        if not deleted_role:
            raise HTTPException(status_code=404, detail="Role not found")
        return deleted_role
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))