from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional
from enum import Enum


class Priority(str,Enum):
    low="low"
    medium = "medium"
    high = "high"

class Task(BaseModel):
    task:str
    description: str | None = None
    completed: bool = False
    priority: Priority = Priority.medium

class TaskUpdate(BaseModel):
    task: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[Priority] = None

    model_config = ConfigDict(extra='forbid')

class User(BaseModel):
    email : EmailStr
    password:str
    role: str = "user"

class UserOut(BaseModel):
    user_id: str
    email : EmailStr
    tasks_list : list

class Logincreds(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    type:str

class TokenData(BaseModel):
    email:Optional[EmailStr]= None
