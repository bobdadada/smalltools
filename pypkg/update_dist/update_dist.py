import sys
import os

from bxypyutils.installer import install, install_all

__description__ = """
更新文件或文件夹的工具
"""


def main_interface():
    print(__description__)
    print('使用CTRL+C退出程序')

    try:
        run_flag = True
        while run_flag:

            while True:
                src = input('>>请输入源文件或文件夹的路径：')
                if os.path.exists(src):
                    break
                else:
                    print('[!]源文件或源文件夹不存在')

            while True:
                obj = input('>>请输入目标文件夹的路径：')
                if not os.path.exists(obj):
                    os.makedirs(obj)
                    break
                else:
                    if not os.path.isdir(obj):
                        print('[!]目标路径存在同名的文件')
                    else:
                        break

            all_flag = True
            if os.path.isdir(src):
                while True:
                    reply = input(">>是否在目标文件中创建同名源文件夹[y|n](默认为n)？")
                    if reply not in ['y', 'n', '']:
                        print('[!]请输入y或n，或者使用默认')
                    else:
                        if reply == 'y':
                            all_flag = False
                        break

            if all_flag:
                install_all(src, obj, quiet=False, exception_ok=True)
            else:
                install(src, obj, quiet=False, exception_ok=True)

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
        pass


def main(src=None, obj=None, all_flag=True, quiet=False):
    if not os.path.exists(src):
        raise Exception('[!]请输入正确的源文件或文件夹路径')

    if obj is None:
        raise Exception('[!]请输入正确的目标文件夹路径')

    if not os.path.exists(obj):
        os.makedirs(obj)
    elif not os.path.isdir(obj):
        raise Exception('[!]%s不是文件夹路径' % obj)

    if all_flag:
        install_all(src, obj, quiet=quiet, exception_ok=True)
    else:
        install(src, obj, quiet=quiet, exception_ok=True)


def __main__():
    import time
    import argparse

    if len(sys.argv) == 1:
        main_interface()
    else:
        parser = argparse.ArgumentParser(description=__description__)
        parser.add_argument('-a', '--all', action='store_true',
                            help='将源文件夹内所有文件拷贝到目标目录中，不在目标目录下创建与源文件夹同名的文件夹')
        parser.add_argument('src', nargs='+',
                            type=str, help='需要更新的文件/文件夹')
        parser.add_argument('-o', '--obj', type=str,
                            default='dist', help='更新后文件/文件夹所在的目标文件夹路径，默认为./dist')
        parser.add_argument('-q', '--quiet', action='store_true', help='不打印输出')
        args = parser.parse_args()

        try:
            for s in args.src:
                main(s, args.obj, all_flag=args.all, quiet=args.quiet)
        except Exception as e:
            print(e)
            raise
        finally:
            # 等待一定时间，以供查看输出
            print("\n程序运行完成，10s后自动关闭\n")
            time.sleep(10)

    sys.exit(0)


if __name__ == '__main__':
    __main__()
