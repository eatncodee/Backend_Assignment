from fastapi import FastAPI,APIRouter,Request,HTTPException,status,Depends
import typing 
from app.Oauth2 import get_current_user
from bson import ObjectId
from app.utils.hash import hash,verify
from app.schema.schema import Task,User,UserOut
from app.db.db import db,tasks,users

user=APIRouter(tags=['User'])



@user.post("/user")
async def create(user:User):
    existing_user = await db.users.find_one({"email": user.email})
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please log in."
        )
    hashed_pass=hash(user.password)
    user.password=hashed_pass
    result=await users.insert_one(user.model_dump())
    return {"message":f"user created with id :{result.inserted_id}"}

@user.get("/me", response_model=UserOut)
async def info(current_user : str = Depends(get_current_user)):    
        current_user["_id"] = str(current_user["_id"]) 
        task_cursor = tasks.find({"email" : current_user["email"]}, {"_id": 0})
        task_list=await task_cursor.to_list()
        return {"user_id": current_user["_id"], "email": current_user["email"], "tasks_list": task_list}        