#! /usr/bin/python3

import sys

from bxypyutils import zhchar


def main_interface():
    print('交互式人名币大写转换工具，使用CTRL+C退出程序')
    try:
        while True:
            num = input(">>请输入阿拉伯数字：")
            try:
                float(num)
                cnum = zhchar.num_to_cnum(num)
                print("[*]中文大写数字：%s" % cnum)
            except ValueError:
                print("[!]请输入正确的阿拉伯数字")
    except KeyboardInterrupt:
        pass


def main(num):
    cnum = zhchar.num_to_cnum(num)
    print("阿拉伯数字：%s" % num)
    print("中文大写数字：%s" % cnum)
    return cnum


def __main__():
    import argparse

    if len(sys.argv) == 1:
        main_interface()
    else:
        parser = argparse.ArgumentParser(
            description="人民币大写转换工具。不带参数运行程序时，以交互式运行。")
        parser.add_argument('num', type=str, help='输入的阿拉伯数字')
        args = parser.parse_args()

        main(args.num)

    sys.exit(0)


if __name__ == '__main__':
    __main__()
