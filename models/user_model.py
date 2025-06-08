from dataclasses import dataclass
@dataclass
class UserModel:
    id:str
    name: str
    email: str
    phone: str
    age:int
    password:str