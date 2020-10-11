import os
import shutil
import glob

# 目标文件夹地址
objpath = './temp'

files = []  # 所需要复制的当前位置文件名称
dirs = []  # 所需要复制的文件夹名称
ignorefile = '.ignore'  # 忽略文件，作用与.gitignore类似

# 忽略目标文件夹中的文件名称
def ignore(*args):
    dirname, names = args
    if ignorefile in names:
        names.remove(ignorefile)
        with open(os.path.join(dirname, ignorefile)) as f:
            for line in f:
                matchnames = glob.glob(os.path.join(dirname, line.strip()))
                for matchname in matchnames:
                    try:
                        names.remove(os.path.split(matchname)[-1])
                    except ValueError:
                        pass
    return dirname, names

for file in files:
    shutil.copyfile(file, os.path.join(objpath, file))
for _dir in dirs:
    odir = os.path.join(objpath, _dir)
    if os.path.isdir(odir):
        shutil.rmtree(odir)
    shutil.copytree(_dir, odir, ignore=ignore)

