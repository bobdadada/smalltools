# 密码封装
import sys

from hashlib import sha256
from getpass import getpass

_password = b'\xdf \xb2\x0c\x8e\xad\xf42\xa4\xe2y\xb4t\x84<\n\xfbR\xa19\xda\xc5\xc7\x7fRD\xb4\xe6hXv\xed'

for _ in range(5):
    test_password = getpass('请输入密码：').encode('utf-8')
    s = sha256()
    s.update(test_password)
    if s.digest() != _password:
        print('密码错误，请重新输入')
        if _ == 4:
            print('密码错误5次，退出软件')
            sys.exit()
    else:
        print('密码正确，欢迎使用')
        break