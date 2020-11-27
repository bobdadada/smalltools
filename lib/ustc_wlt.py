#! python3
# -*- coding: utf-8 -*-

import sys
import time
import re

import requests

from coolutils.web_tools import HEADERS as headers
from coolutils.web_tools import is_ext_network_connectable

def connect_wlt(name, password, force=False, verbose=False):
    if verbose:
        print('中科大网络通登录联网服务！')

    if not force:
        if is_ext_network_connectable():
            if verbose:
                print('[*]已经可以连接外网！')
            return

    if (not isinstance(name, str)) or (not isinstance(password, str)):
        raise Exception('[!]请输入正确的网络通用户名和密码')

    url = 'http://wlt.ustc.edu.cn/cgi-bin/ip'

    # 修改name和password为对应的账户和密码就可以
    parm1 = {'cmd':'login', 'name': name, 'password': password}
    # type为对应的通道，从0开始；exp为使用时间，以秒为单位，0代表无穷。可以上网查看。
    parm2 = {'cmd':'set', 'type':7, 'exp':0}

    if verbose:
        print('[+]登入网络通')

    r1 = requests.get(url, params=parm1, headers=headers)
    r1.raise_for_status()
    r1.encoding = 'GB2312'
    if re.search('用户名不存在',r1.text) or re.search('请重新登录', r1.text):
        raise Exception('[!]登入失败')
    
    if verbose:
        print('[-]登陆成功')
        print('[+]连接外网')

    r2 = requests.get(url, params=parm2, cookies=r1.cookies, headers=headers)
    r2.raise_for_status()
    if is_ext_network_connectable():
        if verbose:
            print('[-]联网成功')
    else:
        raise Exception('[!]联网失败')

    if verbose:
        print('[*]完成中科大网络通登录联网服务！')
