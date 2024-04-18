from fastapi import FastAPI
import uvicorn

from config import get_env


def start_app():
    app = FastAPI(debug=True)
    env = get_env
    
    
    
    return app

app = start_app()

if __name__ =="__main__":
    uvicorn.run("main:start_app", host="0.0.0.0", port=8000,  reload=True, factory=True)