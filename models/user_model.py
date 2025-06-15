from dataclasses import dataclass
from typing import Optional


@dataclass
class UserModel:
    id: Optional[str]
    name: str
    email: str
    phone: str
    age:int
    password:str