from time import sleep
import pytest

@pytest.mark.parametrize('n', list(range(5)))
def test_no_fixture(login, n):
    sleep(1)
    print("执行头条用例，====头条没有__init__，进入头条", login)