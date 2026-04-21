from jose import JWTError,jwt
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from datetime import timedelta,timezone
from app.db.db import users
from app.schema.schema import TokenData


oauth_scheme=OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90



def create_access_token(data: dict):
    to_encode=data.copy()

    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp" : expire})

    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return token


async def verify_access_token(token:str , Credentials_exception):

    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email : str = payload.get("email")
        if email is None:
            raise Credentials_exception
        token_data = TokenData(email=email)
        return token_data

    except JWTError:
        raise Credentials_exception 

async def get_current_user(token: str = Depends(oauth_scheme)):
    Credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not verify credentials",
        headers={"WWW-AUTHENTICATE":"BEARER"}
        )

    token_data= await verify_access_token(token, Credentials_exception)
    email=token_data.email
    result = await users.find_one({"email":email})
    if result:
        return result
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid")
        
