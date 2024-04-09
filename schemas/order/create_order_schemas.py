from pydantic import BaseModel


class PostOkSchema(BaseModel):
    success: bool
    name: str
    order: dict

class PostErrorSchema(BaseModel):

    success: bool
    message: str


