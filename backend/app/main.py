from schemas import LoginRequest, Token, TaskCreate, TaskResponse
from auth import create_access_token, authenticate_user, hash_password, get_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, Body
from typing import Annotated
import models, database
from sqlalchemy.orm import Session
from models import User, Task


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# to get the token while logging in. Send username and password 
@app.post("/token", response_model=Token)
def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db:Annotated[Session, Depends(database.get_db)]):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password", headers={"WWW-Authenticate":"Bearer"})
    token = create_access_token({"sub":user.username})
    return Token(access_token=token, token_type="bearer")

# register the user sending username and password
@app.post("/register")
def register_user(user:LoginRequest, db: Annotated[Session, Depends(database.get_db)]):
    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message":"User created Successfully"}

# Create Tasks
@app.post("/tasks", response_model=TaskResponse)
def create_task(task:Annotated[TaskCreate, Body()], current_user: Annotated[User, Depends(get_current_user)], db:Session = Depends(database.get_db)):
    db_task = models.Task(title=task.title,
                          description=task.description,
                          end_time = task.end_time,
                          user_id = current_user.id
                          )
    # add the task 
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Read tasks
@app.get("/get_tasks")
def get_tasks(db:Annotated[Session, Depends(database.get_db)], current_user:Annotated[User, Depends(get_current_user)]):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks

# delete tasks
@app.delete("/tasks/{task_id}")
def delete_task(db:Annotated[Session, Depends(database.get_db)], current_user:Annotated[User, Depends(get_current_user)], task_id:int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    #check if the task exist
    if not db_task:
        raise HTTPException(status_code=401, detail="The task does not exist")

    # ensure task belongs to current user
    if(db_task.user_id != current_user.id):
        raise HTTPException(status_code=401, detail="Unauthorized to delete task")
    # Deleting task
    db.delete(db_task)
    db.commit()
    return{"message":"Task deleted successfully"}

