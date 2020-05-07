import os
import io


parent_path = os.path.dirname(__file__)
file_name = os.path.join(parent_path,'cookie.txt')
print(file_name)

fo = open(file_name, 'rb')
str = fo.read(10)
print(f'Reading Strs are: {str}')

position = fo.tell()
print(f'Current position: {position}')

str = fo.seek(0, io.SEEK_END)
position = fo.tell()
print(f'Current position: {position}')

str = fo.seek(-1, io.SEEK_END)
position = fo.tell()
print(f'Current position: {position}')
fo.close()