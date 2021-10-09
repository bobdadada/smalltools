#! /usr/bin/python3

import sys

from web_tools import is_ext_network_connectable
from connect_wlt import connect_wlt

__description__ = """
中科大网络通登录联网服务
"""


def main_interface():
    print(__description__)
    print('使用CTRL+C退出程序')

    try:
        run_flag = True
        while run_flag:

            force = False
            if is_ext_network_connectable():
                print('[*]外网已经可以连接')
                while True:
                    reply = input('>>是否强制改变登录的用户[y|n](默认为n)？')
                    if reply not in ['y', 'n', '']:
                        print('[!]请输入y或n，或者使用默认')
                    else:
                        if reply == 'y':
                            force = True
                        else:
                            force = False
                        break

                if not force:
                    return

            while True:
                username = input('>>请输入网络通账号名称：')
                if username == '':
                    print('[!]请输入正确的网络通账号名称')
                else:
                    break

            while True:
                password = input('>>请输入网络通账号密码：')
                if password == '':
                    print('[!]请输入正确的网络通账号密码')
                else:
                    break

            type_ = input('>>请输入通道类型0~7之间的整数(默认为7)：')
            type_ = type_ if type_ else '7'

            exp = input('>>请输入联网时间（秒），0代表无限时间(默认为0)：')
            exp = exp if exp else '0'

            try:
                connect_wlt(username, password, type_,
                            exp, force=force, verbose=True)
                run_flag = False
            except Exception as e:
                print(e)
                while True:
                    reply = input('>>是否重新运行程序[y|n](默认为n)？')
                    if reply not in ['y', 'n', '']:
                        print('[!]请输入y或n，或者使用默认')
                    else:
                        if reply == 'y':
                            run_flag = True
                        else:
                            run_flag = False
                        break

    except KeyboardInterrupt:
        return


def __main__():
    import time
    import argparse

    if len(sys.argv) == 1:
        main_interface()
    else:

        parser = argparse.ArgumentParser(description=__description__)
        parser.add_argument('username', type=str, help='账号名称')
        parser.add_argument('password', type=str, help='账号密码')
        parser.add_argument('-t', '--type', type=int,
                            default=7, help='通道类型，0~7之间的整数')
        parser.add_argument('-e', '--exp', type=int,
                            default=0, help='联网时间（秒），0代表无限时间')
        parser.add_argument(
            '-f', '--force', action='store_true', help='强制登陆所用的账号')
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
