#! python3
# -*- coding: utf-8 -*-

import requests
import re
import time

def main(name, password):
    print('中科大网络通登录联网服务！')
    if (not isinstance(name, str)) or (not isinstance(password, str)):
        raise Exception('[!]请输入正常的名称和密码')

    url = 'http://wlt.ustc.edu.cn/cgi-bin/ip'

    # 修改name和password为对应的账户和密码就可以
    parm1 = {'cmd':'login', 'name': name, 'password': password}
    # type为对应的通道，从0开始；exp为使用时间，以秒为单位，0代表无穷。可以上网查看。
    parm2 = {'cmd':'set', 'type':7, 'exp':0}

    print('[+]登入网络通')
    r1 = requests.get(url, params=parm1)
    r1.raise_for_status()
    r1.encoding = 'GB2312'
    if re.search('用户名不存在',r1.text) or re.search('请重新登录', r1.text):
        raise Exception('[!]登入失败')
    else:
        print('[-]登陆成功')
        print('[+]连接外网')
        r2 = requests.get(url, params=parm2, cookies=r1.cookies)
        r2.raise_for_status()
        r3 = requests.get('http://www.baidu.com')
        if len(r3.text)>1000:
            print('[-]联网成功')
        else:
            raise Exception('[!]联网失败')
        time.sleep(3)
    
    print('[*]完成中科大网络通登录联网服务！')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('中科大网络通登录联网服务')
    parser.add_argument('--name', type=str, help='账号名称')
    parser.add_argument('--password', type=str, help='账号密码')
    arg = parser.parse_args()

    try:
        main(arg.name, arg.password)
    except Exception as e:
        print(e)
        exit(-1)
    
    exit(0)
