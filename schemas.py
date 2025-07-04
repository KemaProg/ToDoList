from pydantic import BaseModel
from typing import Optional
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


class UserBase(BaseModel): 
    username: str 

class UserCreate(UserBase): 
    username: str
    password: str  # Пароль, который потом будет хэшироваться
    
class UserResponse(UserBase): 
    id: int
    
    class Config:
        orm_mode = True 
    
class ToDoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class ToDoCreate(ToDoBase):
    pass

class ToDoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class ToDoResponse(ToDoBase):
    id: int

    class Config:
        orm_mode = True
