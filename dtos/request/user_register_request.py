from typing import Annotated

from pydantic import EmailStr, BaseModel, Field, constr, StringConstraints


class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email:EmailStr
    phone: Annotated[str, StringConstraints(pattern=r'^\+?\d{10,15}$')]
    age:int
    password:str = Field(..., min_length=8)

