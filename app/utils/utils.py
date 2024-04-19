from datetime import datetime, timezone
from loguru import logger
import pendulum


def get_current_utc_time():
    return datetime.now(timezone.utc)

def now_date():
    """ 현재 날짜 반환 """
    now = pendulum.now('Asia/Seoul')
    day = now.strftime('%Y%m%d')
    logger.debug(now.strftime("%Y-%m-%d %H:%M:%S"))
    return day

def now_time():
    """ 현재 날짜 및 시간 반환 """
    now = pendulum.now('Asia/Seoul')
    now_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return now_time