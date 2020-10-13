#! python3

import re
from datetime import datetime
import time
import random
import urllib
import requests
from bs4 import BeautifulSoup

from regexp import date as date_reg

def main(usrname, password, sleep=True, start_delaym=2, interval_delaym=1):
    print('每日健康上报！')

    if (not isinstance(usrname, str)) or (not isinstance(usrname, str)):
        raise Exception('[!]请输入正确的学号和密码')

    start_url = "https://weixine.ustc.edu.cn/2020"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.79 Safari/537.36'
    }

    if sleep:
        time.sleep(random.random()*start_delaym*60)

    # 登录
    print('[+]学号登入')
    params = {'username': usrname, 'password': password}
    service = urllib.parse.quote_plus(start_url+'/caslogin')
    r_login = requests.post('https://passport.ustc.edu.cn/login?service=%s'%(service),
                    data=params, headers=headers)
    try:
        r_login.raise_for_status()
    except:
        raise Exception('[!]登录失败')
    print('[-]登录成功')

    html_login = BeautifulSoup(r_login.text, features='html.parser')

    try:
        # 获取上次上报的时间
        i = html_login.text.find('上次上报时间')
        if i >= 0:
            past_date = re.match('(.*)'+date_reg, html_login.text[i:]).group(2)
            if datetime.now().date() == datetime.strptime(past_date, '%Y-%m-%d').date():
                print('[*]今天已经做过每日健康上报!')
                return
    except:
        pass

    if sleep:
        time.sleep(random.random()*interval_delaym*60)

    # 制造表单
    data = {
        '_token': html_login.findChild('input', {'name':'_token'}).attrs['value'],
        'now_address': 1,  # 内地
        'gps_now_address': '',
        'now_province': 340000,  # 安徽省
        'gps_province': '',
        'now_city': 340100,  # 合肥市
        'gps_city': '',
        'now_detail': '',
        'is_inschool': 2,  # 东区
        'body_condition': 1,  # 正常
        'body_condition_detail': '',
        'now_status': 1,  # 正常在校园中
        'now_status_detail': '',
        'has_fever': 0,  # 无
        'last_touch_sars': 0,  # 无
        'last_touch_sars_date': '',
        'last_touch_sars_detail': '',
        'other_detail': ''
    }
    
    # 上报
    print('[+]健康上报')
    r_report = requests.post(start_url+'/daliy_report', data,
                             cookies=r_login.cookies, headers=headers)
    try:
        r_report.raise_for_status()
    except:
        raise Exception('[!]上报失败')
    print('[*]上报成功')

    print('[*]完成每日健康上报！')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='中科大健康上报')
    parser.add_argument('--usrname', type=str, help='用户名称')
    parser.add_argument('--password', type=str, help='用户密码')
    parser.add_argument('--nosleep', action='store_false', help='快速响应服务器请求')
    parser.add_argument('--sdelay', nargs=1, type=int, default=2, help='开始延迟分钟数')
    parser.add_argument('--idelay', nargs=1, type=int, default=1, help='中间延迟分钟数')
    args = parser.parse_args()

    try:
        main(args.usrname, args.password, sleep=args.nosleep, start_delaym=args.sdelay, 
            interval_delaym=args.idelay)
    except Exception as e:
        print(e)
        raise
    
    exit(0)
