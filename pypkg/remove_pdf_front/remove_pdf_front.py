# -*- coding: utf-8 -*-

import os
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import re
import traceback

filepath = input('请输入文件所在位置:')
if not os.path.isfile(filepath):
    raise Exception('不存在文件')
filepath = os.path.abspath(filepath)
wrappertimes = len(re.findall("_wrapper", filepath))
downpath = filepath[:filepath.find('_wrapper')]+ '_new' + '.pdf'
temppath = filepath

url = 'http://www.pdfdo.com/pdf-remove-page.aspx'

try:
    for _ in range(wrappertimes):
        print('开始处理')
        option = webdriver.ChromeOptions()
        # option.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=option)
        browser.get(url)
        time.sleep(2)
        browser.find_element_by_xpath("//input[@name='File']").send_keys(temppath)
        time.sleep(5)
        browser.find_element_by_xpath("//input[@name='ctl00$content$cmdSaveAttachment']").click()
        time.sleep(15)
        html_text = browser.page_source
        browser.quit()
        soup = BeautifulSoup(html_text, 'html.parser')
        href = soup.findChild(attrs = {'id': 'ctl00_content_lblNew'}).findChildren('a')[1]['href']
        if not href.startswith('http'):
            href = 'http://' + href
        print('下载href:', href)
        r = requests.get(href)
        r.raise_for_status()
        with open(downpath, 'wb') as f:
            f.write(r.content)
        temppath = downpath
    print('处理成功,', '文件所在位置为:' + downpath)
    time.sleep(5)
except:
    traceback.print_exc()
