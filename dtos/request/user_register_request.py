from typing import Annotated

from pydantic import EmailStr, BaseModel, Field, constr, StringConstraints, validator

from exceptions.invaild_input_exception import InvalidInputException


class UserRegisterRequest(BaseModel):

    name: str
    email: EmailStr
    phone: Annotated[str, StringConstraints(pattern=r'^\+?\d{10,15}$')]
    age: int = Field(...,ge=16)
    password: str

    @validator("age")
    def validate_age(cls, value):
        if value < 16:
            raise InvalidInputException("Age must be 16 or older")
        return value

