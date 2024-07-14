import time
import logging
import pendulum
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp, Scope, Receive, Send
import logging.config

class CustomFormatter(logging.Formatter):
    """Override logging.Formatter to use an aware datetime object and custom name"""

    @staticmethod
    def converter(timestamp):
        dt = pendulum.from_timestamp(timestamp, tz='UTC').in_tz('Asia/Seoul')
        return dt

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        s = dt.to_rfc3339_string()
        return s

    def format(self, record):
        # Set custom name for uvicorn.error to uvicorn if level is INFO
        if record.name == "uvicorn.error" and record.levelname == "INFO":
            record.name = "uvicorn"
        return super().format(record)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": CustomFormatter,
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "exception": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "exception_logger": {
            "handlers": ["exception"],
            "level": "ERROR",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.asgi": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.protocols": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        }
    },
}

    
    
class InitLogger(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.configure_logging()
        self.logger =  logging.getLogger("API.Logging")
        
    @staticmethod
    def configure_logging():
        logging.config.dictConfig(LOGGING_CONFIG)

    async def dispatch(self, request: Request, call_next) -> Response:
        ip = request.client.host
        request.state.ip = ip.split(",")[0] if "," in ip else ip

        start_time = time.time()

        try:
            response = await call_next(request)
        except HTTPException as e:
            return JSONResponse({"message": e.detail}, status_code=e.status_code)
        except Exception as e:
            logging.getLogger("uvicorn.error").error(f"{request.method} {request.url} >> {e}")
            return JSONResponse({"message": "Internal Server Error"}, status_code=500)

        end_time = time.time()
        self.logger.info(
            f"{request.client.host} | {request.method} | {request.url} | {response.status_code} | {end_time - start_time:.3f}s"
        )

        return response
