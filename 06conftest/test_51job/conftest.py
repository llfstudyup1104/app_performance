import pytest

@pytest.fixture(scope='module')
def open_51(login):
    name, token = login
    print('\n'+f"51job模块的conftest, fixture name=open_51, scope=module, \
读取全局name: {name}, token: {token}")
    yield name, token
    print('\n' + "51job模块的case执行完毕，退出51job模块conftest")