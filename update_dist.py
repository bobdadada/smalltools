import sys

from utils.install import install_all

def main(objdir, srcdir=None, quiet=False):
    if srcdir is None:
        srcdir = os.path.join(os.path.dirname(__file__), 'dist')
    install_all(srcdir, objdir, quiet)

if __name__ == '__main__':
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

    sys.exit(0)