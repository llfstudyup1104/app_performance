import importlib

imp_module = 'test_import_class'
imp_class = 'ClassA'
ip_module = importlib.import_module('.', imp_module)
ip_module_cls = getattr(ip_module, imp_class)
cls_obj = ip_module_cls()

if 'int_value' in dir(cls_obj):
    print(cls_obj.int_value)
    cls_obj.int_value = 10
    print(cls_obj.int_value)

# reload()重新加载，一般用于原模块有变化等特殊情况。
# reload()之前该模块必须已经使用import导入模块。
# 重新加载模块，但原来已经使用的实例还是会使用旧的模块，而新生产的实例会使用新的模块，reload后还是用原来的内存地址。
ip_module = importlib.reload(ip_module)
print(getattr(ip_module, imp_class).int_value)
