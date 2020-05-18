from loguru import logger
import time

log_path = r'/tmp/logs'
t = time.strftime('%Y_%m_%d')

class Loggings(object):
    
    logger.add(f"{log_path}/interface_log_{t}.log", rotation="500MB", encoding="utf-8", enqueue=True,
               retention="10 days")

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def info(self, msg):
        return logger.info(msg)

    def debug(self, msg):
        return logger.debug(msg)

    def warning(self, msg):
        return logger.warning(msg)

    def error(self, msg):
        return logger.error(msg)


loggings = Loggings()
