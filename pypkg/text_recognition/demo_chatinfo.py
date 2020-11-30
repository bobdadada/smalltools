# -*- coding: utf-8 -*-

from PIL import Image
from imagebreak import pytesseract, parse_raw, get_pattern
import matplotlib.pyplot as plt
from pprint import pprint

# 解决中文显示问题
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

# 导入图片
img_path = 'images/chatinfo_1.png'
img = Image.open(img_path)

# 识别
text = pytesseract.image_to_string(img, lang = 'chi_sim').replace(' ', '')

# 解析
doc = parse_raw(text, get_pattern('baiduyunpan'))
pprint(doc)

plt.subplot(2, 1, 1)
plt.imshow(img)
plt.axis('off')
plt.subplot(2, 1, 2)
plt.text(0, 0, str(doc))
plt.axis('off')
plt.show()
