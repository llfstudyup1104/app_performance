import subprocess
import sys, os
from loguru import logger

# host = '10.13.2.111'
# output = subprocess.call(f'ping -c2 {host}', shell=True)
# print(f'The output is {output}')

# try:
#     subprocess.check_call('lsd -t', shell=True)
# except subprocess.CalledProcessError as err:
#     print("Command err")


try:
    output = subprocess.check_output('it - l', shell=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as err:
    print(f"Command error: {err}")
