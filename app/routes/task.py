from fastapi import FastAPI,APIRouter,Request,HTTPException,status, Depends
from app.schema.schema import Task,User,TaskUpdate
from app.Oauth2 import get_current_user
from app.db.db import db,tasks,users
from datetime import datetime
from bson import ObjectId
from app.SocketManager import manager
from pymongo import ReturnDocument
import json

task=APIRouter(tags=['Tasks'])


@task.get("/alltasks")
async def get_tasks(current_user: str = Depends(get_current_user)):
    task_list=await tasks.find({"email": current_user["email"]}).to_list()
    for t in task_list:
        t["_id"] = str(t["_id"])
    return{"messge":"hi","tasks":task_list}
    
@task.post("/task")
async def add_tasks(task:Task, current_user: str = Depends(get_current_user)):
    task_dict=task.model_dump()
    task_dict["email"]=current_user["email"]
    task_dict["Created_at"] = datetime.now()
    result =await  tasks.insert_one(task_dict)
    task_dict["Created_at"]=str(task_dict["Created_at"])
    task_dict["_id"]=str(result.inserted_id)
    await manager.broadcast(email=current_user["email"], message = json.dumps({"action" : "new_task", "task" : task_dict}))
    return {"Message":"done","id":str(result.inserted_id)}

@task.put("/tasks/{id}")
async def update_task(task:TaskUpdate,id:str, current_user : str = Depends(get_current_user)):
    obj_id = ObjectId(id)

    result =await  tasks.find_one_and_update(
        {"_id" : obj_id, "email" : current_user["email"]},
        {'$set': task.model_dump(exclude_none=True)}, 
        return_document=ReturnDocument.AFTER
    )
    if result:
        result["_id"]=str(result["_id"])
        result["Created_at"]=str(result["Created_at"])
        await manager.broadcast(email=result["email"], message=json.dumps({"action" : "Updated_task", "task" : result}))
        return result

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found, try again")


@task.delete("/tasks/{id}")
async def delete_task(id : str, current_user : str = Depends(get_current_user)):
    obj_id=ObjectId(id)

    result=await tasks.find_one_and_delete({"_id" : obj_id, "email" : current_user["email"]})

    if result:
        result["_id"]=str(result["_id"])
        result["Created_at"]=str(result["Created_at"])
        await manager.broadcast(email=result["email"], message=json.dumps({"action" : "Deleted_task", "task" : result}))
        return {"Message":"Deleted", "Task: ": result}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found, try again")


