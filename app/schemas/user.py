from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = True
    is_superuser: bool = False
    full_name: str | None = None

class UserCreate(UserBase):
    email: EmailStr
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True