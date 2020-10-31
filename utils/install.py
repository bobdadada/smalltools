"""
移动可执行文件到目标文件夹
"""

import os
import shutil

def install_all(srcdir, objdir, quiet=False):
    for filename in os.listdir(srcdir):
        install(os.path.join(srcdir, filename), objdir, quiet)

def install(src, objdir, quiet=False):
    _, filename = os.path.split(src)
    if not quiet:
        print("[+]更新软件%s"%filename)

    if filename in os.listdir(objdir):
        pst = os.stat(os.path.join(objdir, filename))
        cst = os.stat(src)

        if pst.st_mtime < cst.st_mtime:
            shutil.copy(src, objdir)
    else:
        shutil.copy(src, objdir)
    
    if not quiet:
        print("[-]更新软件%s成功"%filename)
