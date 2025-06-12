from pydantic import BaseModel, EmailStr
from typing import Optional

class userLoginResponse(BaseModel):
    id: str
    email: EmailStr
    phone: str
    age: int
    token: Optional[str] = None
