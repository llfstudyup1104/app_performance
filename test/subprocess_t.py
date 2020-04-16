import subprocess
import sys, os
from loguru import logger

def ping_check(host):
    ret = None
    cmd = f'ping -c 1 -t 1 -s 1 {host}'
    # response = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                    # shell=True).communicate(timeout=30)[0].decode(sys.getdefaultencoding(), errors='replace').encode().decode('utf-8', errors='replace')
    response = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, shell=True).communicate()[0].decode(sys.getdefaultencoding(), errors='replace').encode().decode('utf-8', errors='replace')

    if 'ttl=' in response.lower():
        logger.debug("ping succeeded for {0}".format(host))
        ret = True

def ping_check2(host):
    ret = None
    cmd = f'ping -c 1 -t 1 -s 1 {host}'
    res = os.popen(cmd)
    if res:
        for line in res.readlines():
            if 'ttl' in line:
                logger.info("Ping check success")
ping_check2('10.13.2.111')
