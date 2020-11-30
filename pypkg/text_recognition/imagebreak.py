# -*- coding: utf-8 -*-

"""
图片文字识别
"""

import pytesseract

# 命令所在地址
pytesseract.pytesseract.tesseract_cmd = r'D:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

# 解析键值对
def parse_keyvalue(text):
    doc = {}
    for para in text.split('\n'):
        para = para.replace(' ', '')
        if para == '':
            continue
        else:
            index = para.find(':')
            doc[para[:index]] = para[index+1:]
    return doc

import re

# 一些有用的正则匹配样式
_patterns={
        'baiduyunpan':r'链接[:|：](https?://?[a-zA-Z0-9\.\?/=&\s]*)密码[:|：]([a-zA-Z0-9\s]+)',
        }

def display_patterns():
    import pprint
    pprint.pprint(_patterns)
    
def get_pattern(name):
    return _patterns[name]

def set_pattern(pattern):
    if isinstance(pattern, dict):
        _patterns.update(pattern)
        print('Update pattern dict successfully.')
    else:
        raise TypeError('The argument is dict-like object.')

# 解析文本
def parse_raw(text, pattern=get_pattern('baiduyunpan')):
    text = text.replace('\n', '')
    iters = re.finditer(pattern, text)
    doc = {}
    ind = 1
    for item in iters:
        doc[ind] = (item.group(1), item.group(2))
        ind += 1
    return doc
    