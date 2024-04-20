import pendulum
from loguru import logger
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.middleware.base import BaseHTTPMiddleware

from config import get_env
from app.middleware import setting_logger as setting


class InitLogger(BaseHTTPMiddleware): 
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.configure_logger()  
        
    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        await self.app(scope, receive, send)  

    def configure_logger(self):
        """로그 형식 및 파일 위치 설정"""
        def set_datetime(record):
            record["extra"]["datetime"] = pendulum.now('Asia/Seoul')
        
        if get_env()  == 'dev':
            logger.configure(
            patcher=set_datetime,
            handlers=setting.DevelopConfig.LOGURU_SETTINGS['handler'],
            levels=setting.DevelopConfig.LOGURU_SETTINGS['levels']
        )
        elif get_env() == 'prd':
            logger.configure(
                patcher=set_datetime,
                handlers=setting.ProductionConfig.LOGURU_SETTINGS['handler'],
                levels=setting.ProductionConfig.LOGURU_SETTINGS['levels']
            )