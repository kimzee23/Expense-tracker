from pydantic import BaseModel,EmailStr
from typing import Optional

class UserRegisterResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    age: int
    token: Optional[str] = None