from pydantic import BaseModel, EmailStr, constr, ConfigDict
from typing import List, Optional


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: constr(min_length=1)  # type: ignore
    name: str
    is_active: bool
    role: str

    model_config = ConfigDict(from_attributes=True)


class RoleUpdate(BaseModel):
    role: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class TokenData(BaseModel):
    sub: str
    exp: int
    role: str
    scopes: List[str]
    id: Optional[int] = None
