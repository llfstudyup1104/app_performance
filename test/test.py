from stat import S_ISDIR as isdir
import paramiko

local_dir = r'/tmp/llf/1.log'
host = '10.13.2.111'
user = 'tester'
pwd = 'byton[]\\'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
ssh.connect(hostname=host, username=user, password=pwd)
sftp = ssh.open_sftp()
status = sftp.stat(local_dir)
print(status.st_mode)
ssh.close()
sftp.close()
