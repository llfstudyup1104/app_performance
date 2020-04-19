import paramiko
from loguru import logger

HOST = '10.13.2.111'
USER = 'tester'
PWD = 'byton[]\\'
PORT = 22
file_key = '/Users/longfei.li/.ssh/id_rsa'
file_local = r'/Users/longfei.li/1.txt'
file_remote = r'/tmp/1.txt'
p_key = paramiko.RSAKey.from_private_key_file(file_key)


def connect_linux_ssh(HOST, PORT, USER, PWD):
    """测试链接linux函数"""
    Client = paramiko.SSHClient()
    try:
        Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        Client.connect(HOST, PORT, USER, PWD)
    except Exception as e:
        print(e)
    return Client


def connect_linux_pkey(HOST, PORT, USER, PKEY):
    """测试通过ssh公钥链接server"""
    Client = paramiko.SSHClient()
    try:
        Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        Client.connect(HOST, PORT, USER, PKEY)
    except Exception as e:
        print(e)
    return Client


def connect_linux_transport(HOST, PORT, USER, PWD):
    """测试通过Transport()实例链接linux server"""
    transport = paramiko.Transport((HOST, PORT))
    try:
        transport.connect(username=USER, password=PWD)
    except Exception as e:
        print(e)
    return transport


def cmd_linux(client, cmd):
    """将远程执行的Linux命令结果返回：stdin, stdout, stderr"""
    """stdout通过decode方法返回"""
    stdin, stdout, stderr = client.exec_command(cmd)
    res, err = stdout.read(), stderr.read()
    result = res if res else err
    print(result.decode())
    return result


def put_linux_sftp(client, localfile, rtfile):
    try:
        sftp = client.open_sftp()
        sftp.put(localfile, rtfile)
        sftp.close()
        return True
    except Exception as e:
        print(e)


def get_linux_sftp(client, rtfile, localfile):
    try:
        sftp = client.open_sftp()
        sftp.get(rtfile, localfile)
        sftp.close()
        return True
    except Exception as e:
        print(e)


def put_linux_transport(transport, localfile, remotefile):
    try:
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(localfile, remotefile)
        transport.close()
        return True
    except Exception as e:
        print(e)


def get_linux_transport(transport, remotefile, localfile):
    try:
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remotefile, localfile)
        transport.close()
        return True
    except Exception as e:
        print(e)


def main_ssh():
    """设置远程执行linux操作命令输入"""
    client = connect_linux_ssh(HOST, PORT, USER, PWD)
    while True:
        cmd = input("请您输入需要执行的命令(空为退出): ").strip()
        if cmd == "":
            return False
        else:
            cmd_linux(client, cmd)


def main_pky():
    """设置远程执行linux操作命令输入"""
    client = connect_linux_pkey(HOST, PORT, USER, p_key)
    while True:
        cmd = input("请您输入需要执行的命令(空为退出): ").strip()
        if cmd == "":
            return False
        else:
            cmd_linux(client, cmd)


def main_put():
    Client = connect_linux_ssh(HOST, PORT, USER, PWD)
    if put_linux_sftp(Client, file_local, file_remote):
        logger.info("恭喜你，文件上传成功")
    else:
        logger.inf("对不起，文件上传失败，请重试")
        return False


def main_get():
    Client = connect_linux_ssh(HOST, PORT, USER, PWD)
    if get_linux_sftp(Client, file_remote, file_local):
        logger.info("恭喜你，文件下载成功")
    else:
        logger.info("对不起，文件下载失败，请重试")
        return False


def main_put_transport():
    Client = connect_linux_transport(HOST, PORT, USER, PWD)
    if put_linux_transport(Client, file_local, file_remote):
        logger.info("恭喜你，文件上传成功")
    else:
        logger.info("对不起，文件上传失败，请重试")
        return False


def main_get_transport():
    Client = connect_linux_transport(HOST, PORT, USER, PWD)
    if get_linux_transport(Client, file_remote, file_local):
        logger.info("恭喜你，文件下载成功")
    else:
        logger.info("对不起，文件下载失败，请重试")
        return False


if __name__ == "__main__":
    main_ssh()
    