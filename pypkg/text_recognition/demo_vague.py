# -*- coding: utf-8 -*-

from PIL import Image
from imagebreak import pytesseract
import matplotlib.pyplot as plt
from pprint import pprint

# 解决中文显示问题
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

# 导入图片
img_path = 'images/vague_1.jpg'
img = Image.open(img_path)

# 识别
text = pytesseract.image_to_string(img, ).replace(' ', '')
print(text)
