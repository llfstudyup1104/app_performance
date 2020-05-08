import paramiko
import os
from loguru import logger
from stat import S_ISDIR as isdir


class SSH(object):
    def __init__(self, hostname, username):
        self.host = hostname
        self.user = username
        self.ssh_obj = None
    
    def connect_ssh_pwd(self, pwd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        try:
            ssh.connect(hostname=self.host,
                        username=self.user,
                        password=pwd)
            logger.debug(
                    f"connected to remote host({self.host}"
            )
        except Exception as err:
            logger.info(f"Failed to connect remote server: {self.host} by {err}")
        else:
            self.ssh_obj = ssh
    
    def connect_ssh_pkey(self, _pkey):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh.connect(hostname=self.host, username=self.user, pkey=_pkey)
        except Exception as err:
            logger.info(f"Connection failed with err: {err}")
        else:
            self.ssh_obj = ssh

    def send_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh_obj.exec_command(cmd)
        res, err = stdout.read(), stderr.read()
        result = res if res else err
        return result.decode()
    
    def close(self):
        if not self.ssh_obj:
            self.ssh_obj.close()
    
    def get_file(self, remote_file, local_file):
        sftp = self.ssh_obj.open_sftp()
        sftp.get(remote_file, local_file)

    def put_file(self, local_file, remote_file):
        sftp = self.ssh_obj.open_sftp()
        sftp.put(local_file, remote_file)


def main():
    host = '10.13.2.111'
    user = 'tester'
    pwd = 'byton[]\\'
    file_key = '/Users/longfei.li/.ssh/id_rsa'
    pkey = paramiko.RSAKey.from_private_key_file(file_key)
    choices = ['p', 'r']
    remote_dir = '/home/tester/llf_temp/1.log'
    local_dir = '/tmp/llf/1.log'
    
    client = SSH(host, user)
    choice = input("Please select your SSH ways(password/rsa): ")
    if choice not in choices:
        logger.warning("Please input your correct choice again!")
    elif choice == 'p':
        client.connect_ssh_pwd(pwd)
        logger.info("Logon remote server with PWD success!")
    else:
        client.connect_ssh_pkey(pkey)
        logger.info("Logon remote server with RSA success!")
    print(client.send_cmd('pwd'))
    client.put_file(local_dir, remote_dir)
    client.close()


if __name__ == '__main__':
    main()
