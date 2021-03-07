#! python3

import sys
import re
from datetime import datetime
import time
import random
import urllib

import requests
from bs4 import BeautifulSoup

from coolutils.json_plus import load_json
from coolutils.email_tools import notify_self
from coolutils.regexp import date as date_reg


REPORT_TEMPLATE = {
    "now_address": 1,  # 内地
    "gps_now_address": "",
    "now_province": 340000,  # 安徽省
    "gps_province": "",
    "now_city": 340100,  # 合肥市
    "gps_city": "",
    "now_detail": "",
    "is_inschool": 2,  # 在校
    "body_condition": 1,  # 正常
    "body_condition_detail": "",
    "now_status": 1,  # 正常在校园中
    "now_status_detail": "",
    "has_fever": 0,  # 不发热
    "last_touch_sars": 0,  # 没接触过感染者
    "last_touch_sars_date": "",
    "last_touch_sars_detail": "",
    "other_detail": ""
}

def main(username, password, data_file, sleep=True, start_delaym=2, interval_delaym=1, email_addr=None, email_passwd=None):
    print('每日健康上报！')

    if (not isinstance(username, str)) or (not isinstance(username, str)):
        raise Exception('[!]请输入正确的学号和密码')

    if sleep:
        time.sleep(random.random()*start_delaym*60)

    start_url = "https://weixine.ustc.edu.cn/2020"

    User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'

    with requests.Session() as session:
        session.headers.update({'User-Agent': User_Agent})

        # 登录
        print('[+]学号登入')
        service = start_url+'/caslogin'

        login_url = 'https://passport.ustc.edu.cn/login'
        session.get(login_url+'?service=%s'%urllib.parse.quote_plus(service))  # 获取 JSESSIONID cookie
        session.cookies.update({'lang':'zh'})

        data = {'model': 'uplogin.jsp', 'service': service, 'warn': '', 'showCode': '', 'username': username, 'password': password, 'button': ''}
        r_login = session.post(login_url, data=data)
        try:
            r_login.raise_for_status()
            html_login = BeautifulSoup(r_login.text, features='html.parser')
            _token = html_login.findChild('input', {'name':'_token'}).attrs['value']
        except:
            raise Exception('[!]登录失败')
        print('[-]登录成功')

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
        try:
            data = load_json(data_file, js_comments=True)
        except:
            raise Exception('[!]导入个人报告信息失败，请参考\n'+str(REPORT_TEMPLATE))
        data.update({'_token': _token})

        # 上报
        print('[+]健康上报')
        r_report = session.post(start_url+'/daliy_report', data)
        try:
            r_report.raise_for_status()
        except:
            raise Exception('[!]上报失败')
        print('[*]上报成功')

        print('[*]完成每日健康上报！')

    if isinstance(email_addr, str) and isinstance(email_passwd, str):
        print('[+]发送提醒邮件')
        try:
            notify_self(('mail.ustc.edu.cn', 25), email_addr, email_passwd,
                "%s 完成每日健康上报！"%(datetime.now().date()), subject="每日健康上报")
            print('[-]发送提醒邮件成功')
        except:
            print('[!]发送提醒邮件失败')

def __main__():
    import time
    import argparse

    parser = argparse.ArgumentParser(description='中科大健康上报')
    parser.add_argument('username', type=str, help='学号')
    parser.add_argument('password', type=str, help='密码')
    parser.add_argument('file', type=str, help='记录当前信息的JSON文件')
    parser.add_argument('--sleep', action='store_true', help='服务器短暂的延迟')
    parser.add_argument('--sdelay', nargs=1, type=int, default=2, help='开始延迟分钟数')
    parser.add_argument('--idelay', nargs=1, type=int, default=1, help='中间延迟分钟数')
    parser.add_argument('--email_addr', type=str, help='中科大邮箱地址，用于发送邮件提醒')
    parser.add_argument('--email_passwd', type=str, help='中科大邮箱密码，用于发送邮件提醒')
    args = parser.parse_args()

    try:
        main(username=args.username, password=args.password, data_file=args.file, sleep=args.sleep, start_delaym=args.sdelay, 
            interval_delaym=args.idelay, email_addr=args.email_addr, email_passwd=args.email_passwd)
    except Exception as e:
        print(e)
        raise
    finally:
        print("\n程序运行完成，10s后自动关闭\n")
        time.sleep(10)

    sys.exit(0)

if __name__ == '__main__':
    __main__()
