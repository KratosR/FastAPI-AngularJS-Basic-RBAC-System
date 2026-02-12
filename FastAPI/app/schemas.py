from __future__ import annotations
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.models import UserStatus

# ----- Role Schemas -----
class RoleBase(BaseModel):
    role_name: str
    parent_id: Optional[int] = None

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# ----- User Schemas -----
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role_id: int
    status: UserStatus = UserStatus.ACTIVE

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    status: Optional[UserStatus] = None
    role_id: Optional[int] = None

class User(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# ----- Student Schemas -----
class StudentBase(BaseModel):
    enrollment_no: str
    course: str
    year: int

class StudentCreate(StudentBase):
    user_id: int

class Student(StudentBase):
    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class StudentUpdate(BaseModel):
    enrollment_no: Optional[str] = None
    course: Optional[str] = None
    year: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

# ----- Instructor Schemas -----
class InstructorBase(BaseModel):
    department: str
    qualification: str

class InstructorCreate(InstructorBase):
    user_id: int

class Instructor(InstructorBase):
    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class InstructorUpdate(BaseModel):
    department: Optional[str] = None
    qualification: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# ----- User With Relations (using string forward references) -----
class UserWithRelations(User):
    role: Optional[Role] = None
    student_detail: Optional[Student] = None
    instructor_detail: Optional[Instructor] = None
    model_config = ConfigDict(from_attributes=True)

# ----- Auth Schemas -----
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str