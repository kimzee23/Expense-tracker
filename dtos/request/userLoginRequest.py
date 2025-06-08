from pydantic import  BaseModel, EmaulStr

class UserLoginRequest(BaseModel):
    email: str
    password: str