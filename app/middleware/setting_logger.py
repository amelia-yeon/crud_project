import os, sys
from app.utils.utils import *


class BaseConfig(object):
    TYPE = ""
    LOGURU_CONFIG = {}


class DevelopConfig(BaseConfig):
    """ 개발기 로그 설정 """
    LOGURU_SETTINGS = {
        "handler": [
            dict(sink=sys.stderr, format="{extra[datetime]:%Y-%m-%d %H:%M:%S} | {level.name} | {message}"),
            dict(sink=f"./log/dev.log", format="{extra[datetime]:%Y-%m-%d %H:%M:%S} | {level.name} | {message}",rotation="09:00", enqueue=True, serialize=False  , backtrace=True),
        ],
        "levels": []
    }
    

class ProductionConfig(BaseConfig):
    """ 운영기 로그 설정 """
    LOGURU_SETTINGS = {
        "handler": [
            dict(sink=sys.stderr, format="{extra[datetime]:%Y-%m-%d %H:%M:%S} | {level.name} | {message}"),
            dict(sink=f"./log/{now_date()}_prd.log", format="{extra[datetime]:%Y-%m-%d %H:%M:%S} | {level.name} | {message}", enqueue=True, serialize=False),
        ],
        "levels": []
    }