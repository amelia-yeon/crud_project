import time 
import pendulum
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from loguru import logger

from app.utils.utils import *
from app import models
from app.db.connection import db
from app.exception.exceptions import *
from app.utils.auth_utils import decode_token
from config import *



class AccessControl(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request.state.user = None
        request.state.access_token = request.headers.get("Authorization")
        if request.state.access_token:
            request.state.access_token = request.headers.get("Authorization").replace("Bearer ", "")
            session = next(db.session())
            user = decode_token(request.state.access_token)
            if user:
                request.state.user = models.Users.get(session, user.get("id"))
        #  ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
        ip = request.client.host
        
        request.state.ip = ip.split(",")[0] if "," in ip else ip
        start_time, start =  time.time(), now_time()
        try:
            response = await call_next(request)
        except Exception as e:
            if not isinstance(e, BaseException):
                logger.error(f"{request.method} {request.url} >> {e}")
                return JSONResponse({"message": "Internal Server Error"}, status_code=500)
            else:
                return JSONResponse({"message": e.msg}, status_code=e.status_code)
        end_time , end = time.time(), now_time()
        logger.info(f"{request.client.host} | {request.method} | {request.url} | {response.status_code} | {start} | {end} | {end_time - start_time:.3f}")
        
        return response


