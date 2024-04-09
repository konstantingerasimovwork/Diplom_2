from pydantic import BaseModel


class PostOkSchema(BaseModel):
    success: bool
    orders: list
    total: int
    totalToday: int


class PostErrorSchema(BaseModel):

    success: bool
    message: str
