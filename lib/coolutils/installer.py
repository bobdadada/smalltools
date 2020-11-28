"""
移动可执行文件到目标文件夹
"""

import os
import shutil

def install_all(srcdir, objdir, quiet=False, exception_ok=False):
    except_filenames = []
    for filename in os.listdir(srcdir):
        try:
            install(os.path.join(srcdir, filename), objdir, quiet, exception_ok)
        except:
            except_filenames.append(filename)
    if except_filenames:
        raise Exception('[!]更新软件%s失败'%(','.join(except_filenames)))


def install(src, objdir, quiet=False, exception_ok=False):
    _, filename = os.path.split(src)

    update_flag = False

    if filename in os.listdir(objdir):
        # 时间戳比较
        pst = os.stat(os.path.join(objdir, filename))
        cst = os.stat(src)
        if pst.st_mtime < cst.st_mtime:
            update_flag = True
    else:
        update_flag = True

    if update_flag:
        if not quiet:
            print("[+]更新软件%s"%filename)

        try:
            shutil.copy(src, objdir)
        except:
            if not quiet:
                print("[!]更新软件%s失败"%filename)
            if not exception_ok:
                raise

        if not quiet:
            print("[-]更新软件%s成功"%filename)
    else:
        print("[*]软件%s不需要更新"%filename)
