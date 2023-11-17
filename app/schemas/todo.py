from pydantic import BaseModel
from datetime import datetime
from .user import UserOut

# from pydantic.types import conint

class TodoBase(BaseModel):
    content: str
    completed: bool = False


class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class TodoOut(BaseModel):
    todo: Todo

    class Config:
        orm_mode = True