from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,unique=True, index=True)
    password = Column(String)

class Task(Base):
    __tablename__ = "tasks"
    id =  Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    end_time = Column(DateTime, nullable = False)
    status = Column(Enum("urgent", "normal", name="task_status"), default="normal")
    user_id = Column(Integer, ForeignKey("users.id"))



