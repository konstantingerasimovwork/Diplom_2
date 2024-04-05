from pydantic import BaseModel


class PostOkSchema(BaseModel):

    success: bool
    user: dict


class UserData(BaseModel):

    email: str
    name: str


class PostErrorSchema(BaseModel):

    success: bool
    message: str
