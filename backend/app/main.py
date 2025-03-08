from schemas import LoginRequest, Token, TaskCreate, TaskResponse, TaskUpdate
from auth import create_access_token, authenticate_user, hash_password, get_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import models, database
from sqlalchemy.orm import Session
from models import User, Task
import logging

logging.basicConfig(level=logging.INFO)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins = ["http://localhost:3000"],
                   allow_credentials = True, 
                   allow_methods = ["*"],
                   allow_headers = ["*"])

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
    existing_user = db.query(User).filter(User.username == user.username).first()
    if(existing_user):
        raise HTTPException(status_code=401, detail="The user already exists")
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
                          user_id = current_user.id,
                          status = task.status
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
def delete_task(task_id:int,db:Annotated[Session, Depends(database.get_db)], current_user:Annotated[User, Depends(get_current_user)]):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    #check if the task exist
    if not db_task:
        logging.info(f"Task{task_id} not found")
        raise HTTPException(status_code=404, detail="The task does not exist")
    # ensure task belongs to current user
    if(db_task.user_id != current_user.id):
        logging.info(f"User {current_user.id} unauhtorized to delete task")
        raise HTTPException(status_code=403, detail="Unauthorized to delete task")
    # Deleting task
    db.delete(db_task)
    db.commit()
    db.flush()
    db.expire_all()
    logging.info(f"Task{task_id} deleted successfully")
    return {"message": f"Task {task_id} deleted successfully"}


# update tasks
@app.patch("/tasks/{task_id}")
def update_task(task: Annotated[TaskUpdate, Body()],db:Annotated[Session, Depends(database.get_db)], current_user:Annotated[User, Depends(get_current_user)], task_id:int):
    db_task =db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
       raise HTTPException(status_code=404, detail="task not found")
    if(db_task.user_id != current_user.id):
        raise HTTPException(status_code=403, detail= "Unauthorized to update this task!")
    # update the task fields (only the provided fields)
    if task.title is not None:
        db_task.title = task.title
    if task.description is not None:
        db_task.description = task.description
    if task.status is not None:
        db_task.status = task.status
    if task.end_time is not None:
        db_task.end_time = task.end_time
    # commit the changes to the database
    db.commit()
    db.refresh(db_task)
    return({"task":db_task, "message":"Task updated successfully"})
    
