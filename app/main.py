from fastapi import FastAPI,APIRouter,Request,HTTPException,status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes.task import task
from app.routes.user import user
from app.routes.auth import auth
from app.routes.ws import ws
from fastapi.middleware.cors import CORSMiddleware
import os


app=FastAPI()

app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
app.include_router(task)
app.include_router(user)
app.include_router(auth)
app.include_router(ws)

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "frontend")), name="static")

@app.get("/")
def get_home():
    return FileResponse(os.path.join(os.path.dirname(__file__), "frontend", "index.html"))


