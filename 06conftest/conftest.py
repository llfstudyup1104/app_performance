import pytest

@pytest.fixture(scope='session')
def login():
    print('\n'+"最外层conftest, fixture name=login, scope=session, \
初始化读取name和token")
    name = 'test'
    token = '123'
    yield name, token
    print('\n'+"退出最外层的conftest文件")

@pytest.fixture(autouse=True)
def get_info(login):
    name, token = login
    print('\n'+f"最外层conftest，fixture name: get_info, autouse=True, \
每个用例都会调用最外层的fixture，token={token}")