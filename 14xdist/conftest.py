import pytest
from filelock import FileLock

@pytest.fixture(scope='session')
def login():
    print('\n'+"最外层conftest, fixture name=login, scope=session, \
初始化读取name和token")
    with FileLock("session.lock"):
        name = 'testyy'
        token = '123123'
        # web ui自动化
        # 声明一个driver，再返回

        # 接口自动化
        # 发起一个登录请求，将token返回都可以这样写

    yield name, token
    print('\n'+"退出最外层的conftest文件")