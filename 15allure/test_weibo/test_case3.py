import pytest
from time import sleep


@pytest.mark.parametrize('n', list(range(5)))
class TestWeibo(object):
    def test_case3_01(self, open_weibo, n):
        sleep(1)
        print("执行微博用例01，查看微博热搜", n)
    @pytest.mark.flaky(reruns=2, reruns_delay=2)
    def test_case3_02(self, open_weibo, n):
        sleep(1)
        print("执行微博用例02，查看范冰冰", n)