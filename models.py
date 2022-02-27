from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str    