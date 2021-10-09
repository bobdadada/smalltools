import sys

__description__ = """
处理密码本文件，只提取长度大于或等于8的密码
"""

def main_interface():
    print(__description__)
    print('使用CTRL+C退出程序')
    try:
        while True:
            main(input('>>密码本文件名：'))
            
    except KeyboardInterrupt:
        return

def main(filename):
    lines = []
    with open(filename, 'r', encoding='utf-8') as f:
        for l in f:
            l = l.strip('\n')
            if len(l) >= 8:
                lines.append(l)

    with open(filename, 'w', encoding='utf-8') as f:
        for l in lines:
            f.write(l+'\n')

    print('[*]修改密码本%s成功' % filename)

def __main__():
    import argparse

    if len(sys.argv) == 1:
        main_interface()
    else:
        parser = argparse.ArgumentParser(description=__description__)
        parser.add_argument('file', type=str, help='密码本文件名')
        args = parser.parse_args()

        main(args.file)

    sys.exit(0)

if __name__ == '__main__':
    __main__()