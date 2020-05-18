class Protected(object):
    _protected = "受保护变量"
    name = "test"

    def test(self):
        print("实例属性：", self._protected)
        print("类属性：", Protected._protected)

    @classmethod
    def class_m(cls):
        print("类方法中类属性：", cls._protected)

    def _test(self):
        print("受保护的方法")


class Protectedson(Protected):

    def __init__(self):
        self._protected = "子类的受保护实例变量"
        print("子类实例属性：", self._protected)
        print("子类类属性：", Protectedson._protected)


if __name__ == "__main__":
    p1 = Protectedson()
    p1.test()
    print("子类实例对象调用类属性", p1._protected)
    Protectedson.class_m()
    print("类对象调用类属性", Protectedson._protected)
    p1._test()