from typing import Annotated

from pydantic import EmailStr, BaseModel, Field, constr, StringConstraints


class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    phone: Annotated[str, StringConstraints(pattern=r'^\+?\d{10,15}$')]
    age: int
    password: str


