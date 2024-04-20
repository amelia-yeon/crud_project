from fastapi import FastAPI
import uvicorn

from config import get_env
from app.api.user_api import user
from app.middleware.init_logger import InitLogger
from app.middleware.access_control import AccessControl

from app.db.connection import db


def start_app():
    
    app = FastAPI(debug=True)
    env = get_env()
    
    app.add_middleware(InitLogger)
    app.add_middleware(AccessControl)
    
    app.include_router(user, prefix="/users", tags=["Users"])
    
    return app

app = start_app()

if __name__ =="__main__":
    uvicorn.run("main:start_app", host="0.0.0.0", port=8000,  reload=True, factory=True)