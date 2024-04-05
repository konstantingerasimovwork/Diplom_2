from pydantic import BaseModel


class PostOkSchema(BaseModel):

    success: bool
    accessToken: str
    refreshToken: str
    user: dict


class UserData(BaseModel):
    
    email: str
    name: str


class PostErrorSchema(BaseModel):

    success: bool
    message: str
