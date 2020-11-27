#! python3
# -*- coding: utf-8 -*-

import sys
import time
import re

import requests

from coolutils.web_tools import HEADERS as headers
from coolutils.web_tools import is_ext_network_connectable
from ustc_wlt import connect_wlt

def __main__():
    import time
    import argparse

    parser = argparse.ArgumentParser('中科大网络通登录联网服务')
    parser.add_argument('name', type=str, help='账号名称')
    parser.add_argument('password', type=str, help='账号密码')
    parser.add_argument('-f', '--force', action='store_true', help='强制登陆所给账号')
    arg = parser.parse_args()

    try:
        connect_wlt(arg.name, arg.password, force=arg.force, verbose=True)
    except Exception as e:
        print(e)
        raise
    finally:
        print("\n程序运行完成，10s后自动关闭\n")
        time.sleep(10)

    sys.exit(0)

if __name__ == '__main__':
    __main__()
