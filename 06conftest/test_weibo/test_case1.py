import pytest

@pytest.mark.weibo
class TestWeibo(object):
    def test_case3_01(self, open_weibo):
        print("执行微博用例01，查看微博热搜")
    
    def test_case3_02(self, open_weibo):
        print("执行微博用例02，查看范冰冰")