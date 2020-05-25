import pytest

@pytest.fixture(scope='function')
def open_weibo(login):
    name, token = login
    print('\n' + f"&&& 微博的conftest, fixture name=open_weibo，scope=function, \
用户{name} 返回微博首页 &&&")
    # yield name, token
    # print('\n' + "微博模块的case执行完毕，退出微博模块conftest")