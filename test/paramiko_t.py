import paramiko

pic = '192.168.111.10'

client = paramiko.SSHClient()
# client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname='10.13.2.111',
               port=22,
               username='tester',
               password='byton[]\\',
               timeout=10,
               banner_timeout=10)
print(f'SSH Client is {client}')
stdin, stdout, stderr = client.exec_command('ls -l')
print(stdout.read().decode())
# 关闭连接
print('Successful connection')

if client is not None:
    client.close()
    del client, stdin, stdout, stderr
