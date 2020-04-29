import shutil, os
from pathlib import Path

ori_path = '/tmp/test1'
path = Path(ori_path)
filename = ori_path.rpartition('/')[-1]
print(filename)
new_path = Path.joinpath(path.parent, 'test2')
new_path02 = Path.joinpath(new_path, 'test.log')
print(new_path02)

# shutil.move(ori_path, new_path)


# shutil.copytree(ori_path, new_path)
shutil.make_archive(new_path02, 'tar', ori_path)
