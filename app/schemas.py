from pydantic import BaseModel

class ToDoBase(BaseModel):
    title: str
    completed: bool = False

class ToDoCreate(ToDoBase):
    pass

class ToDo(ToDoBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
