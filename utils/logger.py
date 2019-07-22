# -*- coding: utf-8 -*-
__version__ = '0.0.1'
__author__ = 'Cavin Rui cavin.rui@byton.com'


import logging
import time
import os

logging.getLogger("paramiko").setLevel(logging.ERROR)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
rq = time.strftime('%Y%m%d', time.localtime(time.time()))
logPath = os.path.dirname(__file__)
logPath = os.path.join(logPath, '../../Logs')
if not os.path.exists(logPath):
    os.mkdir(logPath)
logFile = os.path.join(logPath, rq + '.log' )
    
handler = logging.FileHandler(logFile, mode='a')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logger.addHandler(console)
    


