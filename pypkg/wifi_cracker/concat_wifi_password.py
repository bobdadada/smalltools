import sys
from collections import OrderedDict

__description__ = """
处理密码本文件，合并多个密码本文件
"""


def main(*filenames, cfilename='concat_password.txt'):

    def generator():
        for filename in filenames:
            with open(filename, 'r', encoding='utf-8') as f:
                for l in f:
                    l = l.strip('\n')
                    if (len(l) >= 8) and (len(l) <= 16):
                        yield l
            print('[*]导入密码本%s成功' % filename)

    print('[+]开始合并密码')

    # 若OrderedDict()内部是以生成器形式出现的，可能会出现文件重写的bug
    # 使用外层list()保证所有资料都写入内存
    lines = list(OrderedDict().fromkeys(generator()).keys())

    with open(cfilename, 'w', encoding='utf-8') as f:
        for l in lines:
            f.write(l+'\n')

    print('[-]合并密码成功')


def __main__():
    import argparse

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('file', nargs='+', type=str, help='密码本文件名')
    parser.add_argument('-o', '--output_file',
                        default='concat_password.txt', type=str, help='合并后的密码本文件名，默认为concat_password.txt')
    args = parser.parse_args()

    main(*args.file, cfilename=args.output_file)

    sys.exit(0)


if __name__ == '__main__':
    __main__()
