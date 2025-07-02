from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str

class User(UserBase):
    class Config:
        from_attributes = True
