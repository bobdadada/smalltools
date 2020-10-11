#! python3
# -*- coding: utf-8 -*-

import requests
import re
import time

def main(name, password):
    print('启动中科大网络通登录联网服务！')

    url = 'http://wlt.ustc.edu.cn/cgi-bin/ip'

    # 修改name和password为对应的账户和密码就可以
    parm1 = {'cmd':'login', 'name': name, 'password': password}
    # type为对应的通道，从0开始；exp为使用时间，以秒为单位，0代表无穷。可以上网查看。
    parm2 = {'cmd':'set', 'type':7, 'exp':0}

    try:
        r1 = requests.get(url, params=parm1)
        r1.raise_for_status()
        r1.encoding = 'GB2312'
        print(r1.text)
        if re.search('用户名不存在',r1.text) or re.search('请重新登录', r1.text):
            raise Exception('登入失败')
        else:
            print('[*]登陆成功', flush=True)
            r2 = requests.get(url, params=parm2, cookies=r1.cookies)
            r2.raise_for_status()
            print('[*]设置成功', flush=True)
            r3 = requests.get('http://www.baidu.com')
            if len(r3.text)>1000:
                print('[*]联网成功', flush=True)
            else:
                raise Exception('联网失败')
            time.sleep(3)
        exit(0)
    except Exception as e:
        print('[!]connect network failed', flush=True)
        print('[!]'+str(e))
        exit(-1)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('中科大网络通登录联网服务')
    parser.add_argument('--name', type=str, help='账号名称')
    parser.add_argument('--password', type=str, help='账号密码')
    arg = parser.parse_args()

    main(arg.name, arg.password)
