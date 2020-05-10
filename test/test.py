from stat import S_ISDIR, S_ISREG
import paramiko
from loguru import logger

local_file = r'/tmp/llf/1.log'
local_dir = r'/tmp/llf'
host = '10.13.2.111'
user = 'tester'
pwd = 'byton[]\\'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
ssh.connect(hostname=host, username=user, password=pwd)
sftp = ssh.open_sftp()
print(sftp.stat(local_dir).st_mode)

if S_ISDIR(sftp.stat(local_dir).st_mode):
    logger.info("目录")
else:
    logger.warning("Unknown")

ssh.close()
sftp.close()

# print(os.stat(local_file).st_mode)
# print(os.stat(local_dir).st_mode)

# if S_ISDIR(os.stat(local_dir).st_mode):
#     logger.info("目录")
# else:
#     logger.info("Unknown")

# if S_ISREG(os.stat(local_file).st_mode):
#     logger.info("文件")
# else:
#     logger.info("Unknown")
