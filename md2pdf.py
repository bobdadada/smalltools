import os

files = [file for file in os.listdir('.') if file.endswith('.md')]

sfiles = ' '.join(files)

os.system('pandoc -s -o wrap.pdf --latex-engine=xelatex '+sfiles)
