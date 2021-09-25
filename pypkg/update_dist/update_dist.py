import sys
import os

from bxypyutils.installer import install, install_all


def main(src=None, obj=None, all_flag=True, quiet=False):
    if obj is None:
        raise Exception('[!]Please enter a correct destination folder.')

    if not os.path.exists(src):
        raise Exception('[!]Please enter a correct source path.')

    if not os.path.exists(obj):
        os.makedirs(obj)
    elif not os.path.isdir(obj):
        raise Exception('[!]%s is not a directory.' % obj)

    if all_flag:
        install_all(src, obj, quiet=quiet, exception_ok=True)
    else:
        install(src, obj, quiet=quiet, exception_ok=True)


def __main__():
    import time
    import argparse

    parser = argparse.ArgumentParser('更新文件/文件夹的工具')
    parser.add_argument('-a', '--all', action='store_true',
                        help='将源文件夹内所有文件拷贝到目标目录中，不在目标目录下创建与源文件夹同名的文件夹')
    parser.add_argument('-s', '--src', nargs='+',
                        type=str, help='需要更新的文件/文件夹')
    parser.add_argument('-o', '--obj', type=str, help='更新后文件/文件夹所在的目标文件夹路径')
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
