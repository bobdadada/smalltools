#! python3
# -*- coding: utf-8 -*-

import sys
import time
import re

import requests

from web_tools import HEADERS as headers
from web_tools import is_ext_network_connectable
from connect_wlt import connect_wlt

def __main__():
    import time
    import argparse

    parser = argparse.ArgumentParser('中科大网络通登录联网服务')
    parser.add_argument('username', type=str, help='账号名称')
    parser.add_argument('password', type=str, help='账号密码')
    parser.add_argument('-t', '--type', type=int, default=7, help='通道类型,0~7之间的整数')
    parser.add_argument('-e', '--exp', type=int, default=0, help='联网时间(秒),0代表无限时间')
    parser.add_argument('-f', '--force', action='store_true', help='强制登陆所给账号')
    arg = parser.parse_args()

    try:
        connect_wlt(arg.username, arg.password, arg.type,
                    arg.exp, force=arg.force, verbose=True)
    except Exception as e:
        print(e)
        raise
    finally:
        print("\n程序运行完成，10s后自动关闭\n")
        time.sleep(10)

    sys.exit(0)

if __name__ == '__main__':
    __main__()
