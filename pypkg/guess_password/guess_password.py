#! /usr/bin/python3

"""
密码封装小程序
"""

import sys

from hashlib import sha256
from getpass import getpass


def main_interface():
    print('密码猜测程序，可以拓展为其他程序的启动程序，用CTRL+C退出程序')
    _password = getpass('>>请输入所要猜的密码：').encode('utf-8')

    s = sha256()
    s.update(_password)
    encode_password = s.digest()

    try:
        while True:
            test_password = input('>>请输入猜测的密码：').encode('utf-8')
            s = sha256()
            s.update(test_password)
            if s.digest() != encode_password:
                print('[!]密码错误，请重新输入')
            else:
                print('[*]密码正确，欢迎使用')
                break

    except KeyboardInterrupt:
        pass


def __main__():
    import argparse

    if len(sys.argv) == 1:
        main_interface()
    else:
        parser = argparse.ArgumentParser(description="密码猜测程序，可以拓展为其他程序的启动程序。")
        parser.print_help()

    sys.exit()


if __name__ == '__main__':
    __main__()
