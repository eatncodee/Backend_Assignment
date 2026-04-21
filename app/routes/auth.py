from fastapi import APIRouter, Depends, status, HTTPException,Response
from app.db.db import db,tasks,users
from app.utils.hash import verify
from pydantic import EmailStr
from app.schema.schema import Logincreds
from app import Oauth2
from app.redis_dependency import login_rate_limiter

auth=APIRouter(tags=['Authentication'])


@auth.post("/login", dependencies=[Depends(login_rate_limiter)])
async def login(creds:Logincreds):
    user=await users.find_one({"email":creds.email})

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not verify(creds.password,user["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")    

    token=Oauth2.create_access_token(data={"email" : user["email"]})

    return {"access_token": token, "token_type":"bearer"}


