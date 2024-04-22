from fastapi import FastAPI
import uvicorn
from fastapi_pagination import add_pagination

from config import get_env
from app.api.user_api import user
from app.api.post_api import router
from app.middleware.init_logger import InitLogger
from app.middleware.access_control import AccessControl
from app.middleware.trusted_host import TrustedHostMiddleware

from app.db.connection import db


def start_app():
    
    app = FastAPI(debug=True)
    env = get_env()
    db.init_db(app=app, **env.dict())
    
    app.add_middleware(InitLogger)
    app.add_middleware(AccessControl)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=env.TRUSTED_HOSTS, except_path=["/"])
    
    app.include_router(user, prefix="/users", tags=["Users"])
    app.include_router(router, prefix="/board", tags=["board"])
    
    add_pagination(router)
    
    return app

app = start_app()

if __name__ =="__main__":
    uvicorn.run("main:start_app", host="0.0.0.0", port=8000,  reload=True, factory=True)