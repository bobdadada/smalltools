import sys
import os

from coolutils.install_tools import install_all

def main(objdir, srcdir=None, quiet=False):
    if not os.path.exists(objdir):
        os.makedirs(objdir)
    elif not os.path.isdir(objdir):
        raise Exception(objdir + ' is not a directory.')
    if srcdir is None:
        srcdir = os.path.join(os.path.dirname(__file__), 'dist')
    install_all(srcdir, objdir, quiet=quiet, exception_ok=True)

def __main__():
    import time
    import argparse
    
    parser = argparse.ArgumentParser('安装可执行文件的工具')
    parser.add_argument('srcdir', type=str, help='可执行文件本地路径')
    parser.add_argument('objdir', type=str, help='可执行文件安装路径')
    parser.add_argument('--quiet', '-q', action='store_true', help='安静地运行')
    arg = parser.parse_args()

    try:
        main(srcdir=arg.srcdir, objdir=arg.objdir, quiet=arg.quiet)
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