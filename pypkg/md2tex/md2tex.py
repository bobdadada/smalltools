import os
from concurrent.futures import ThreadPoolExecutor

def md2tex(filename):
    newname = '.'.join(filename.split('.')[:-1]+['tex'])
    os.system('pandoc {} -o {}'.format(filename,newname))

md_filenames = []
for filename in os.listdir('.'):
    if filename.endswith('.md'):
        md_filenames.append(filename)

with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(md2tex, md_filenames)

