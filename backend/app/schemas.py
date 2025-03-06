# pydantic schemas for validation
from pydantic import BaseModel, Field
from datetime import datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username:str | None = None

class TaskCreate(BaseModel):
    title:str 
    description: str | None = None
    end_time:datetime
    status:str = Field("normal", pattern= "^(urgent|normal)$")

class TaskResponse(TaskCreate):
    id:int
    user_id:int

class TaskUpdate(TaskCreate):
    title: str | None = None
    description: str | None = None
    end_time: datetime | None = None
    status: str | None = None


