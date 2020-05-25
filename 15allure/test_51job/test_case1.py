from time import sleep
import pytest

@pytest.mark.parametrize('n', list(range(5)))
def test_case2_01(open_51, n):
    sleep(1)
    print('\n' + "执行51job用例01, 列出所有的职位", n)

@pytest.mark.parametrize('n', list(range(5)))
def test_case2_02(open_51, n):
    sleep(1)
    print('\n' + "执行51job用例02, 列出所有的python职位", n)