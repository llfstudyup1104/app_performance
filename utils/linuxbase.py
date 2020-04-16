import paramiko
import re
import traceback
import subprocess
import os, sys
from loguru import logger


class LinuxDevNetConnection(object):
    def __init__(self, host, user, password, port=22):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ssh_obj = None

    def __del__(self):
        self.close()

    def _connect_ssh(self, timeout=10, banner_timeout=None):
        ret = None
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        for _ in range(0, 3):
            try:
                ssh.connect(hostname=self.host,
                            username=self.user,
                            password=self.password,
                            timeout=timeout,
                            banner_timeout=banner_timeout)
                tr = ssh.get_transport()
                tr.set_keepalive(1)
                logger.debug(
                    f"connected to remote host({self.user}:{self.password}@{self.host}:{self.port})"
                )
            except Exception as err:
                logger.info(
                    "connect remote host({0}:{1}@{2}:{3}) err by {4}.".format(
                        self.user, self.password, self.host, self.port, err))
            else:
                ret = ssh
                break
        return ret

    def connect(self, timeout=10, banner_timeout=None):
        if not self.ssh_obj:
            self.ssh_obj = self._connect_ssh()

    def reconnect(self):
        if not self.ssh_obj:
            self.close()
            self.connect()

    def close(self):
        if self.ssh_obj:
            self.ssh_obj.close()
            # del self.ssh_obj, stdin, stdout, stderr
            self.ssh_obj = None
            logger.debug(
                f"disconnected to remote host({self.host}:{self.port})")

    def send_command(self, command, timeout=20):
        try:
            stdin, stdout, stderr = self.ssh_obj.exec_command(command,
                                                              timeout=timeout)
            ret = stdout.read().decode() + stderr.read().decode()
            logger.debug('execute command({0}), return: {1}'.format(
                command, ret))
        except Exception as err:
            logger.info('exexcution command({0}) err by {1}\n{2}'.format(
                command, traceback.format_exc(), err))
            ret = None
        return ret

    def check_ssh(self):
        res = self.send_command('echo hello!')
        if res:
            ret = True if 'hello' in res else False
            logger.info("SSH connection is successful!")
        else:
            ret = None
        if not ret:
            logger.info("ssh failed: cannot connect to device {0}".format(
                self.host))
        return ret

    def check_connection(self):
        ret = None
        cmd = f'ping -c 1 -t 1 -s 1 {self.host}'
        response = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            shell=True).communicate(timeout=30)[0].decode(
                sys.getdefaultencoding(),
                errors='replace').encode().decode('utf-8', errors='replace')
        # print("=====" + response + "=====")
        # print(type(response))
        # print(len(response))
        if 'ttl=' in response.lower():
            logger.debug("ping succeeded for {0}".format(self.host))
            ret = True
        else:
            logger.info("ping failed: cannot connect to device {0}".format(
                self.host))
            ret = False
        return ret

    def check_connection02(self):
        ret = None
        cmd = f'ping -c1 -t1 -s1 {self.host}'
        response = os.popen(cmd).readlines()
        for line in response:
            if 'ttl' in line:
                # logger.debug("ping succeeded for {0}".format(self.host))
                ret = True
                break
            else:
                # logger.info("ping failed: cannot connect to device {0}".format(self.host))
                ret = False
                continue
        return ret


if __name__ == '__main__':
    tk = LinuxDevNetConnection(host='10.13.2.111',
                               user='tester',
                               password='byton[]\\')
