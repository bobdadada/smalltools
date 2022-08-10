#! /usr/bin/python3

import sys
from datetime import datetime
import time
import random
import urllib
import pprint
import traceback


import requests
from bs4 import BeautifulSoup

from bxypyutils.email_tools import notify_self

VERSION = '1.1'

REPORT_TEMPLATE = {
    "juzhudi": "",
    "city_area": "",
    "jutiwz": "",
    "body_condition": "1",  # 正常
    "body_condition_detail": "",
    "has_fever": "0",  # 不发热
    "last_touch_sars": "0",  # 没接触过感染者
    "last_touch_sars_date": "",
    "last_touch_sars_detail": "",
    "is_danger": "0",  # 当前居住地是否为疫情中高风险地区
    "is_goto_danger": "0",  # 14天内是否有疫情中高风险地区旅居史
    "jinji_lxr": "",  # 紧急联系人
    "jinji_guanxi": "",  # 与本人关系
    "jiji_mobile": "",  # 联系人电话，此处原网站代码有问题，应为jinji_mobile更加合理
    "other_detail": ""
}


def main(username, password, sleep=True, start_delaym=2, interval_delaym=1, email=None):
    print('[+]每日健康上报！')

    if sleep:
        time.sleep(random.random()*start_delaym*60)

    start_url = "https://weixine.ustc.edu.cn/2020"  # 健康上报起始url

    User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'

    with requests.Session() as session:
        session.headers.update({'User-Agent': User_Agent})

        # 登录
        print('[+]学号登入')
        try:
            service = start_url+'/caslogin'  # 健康上报用户登录所用的服务器地址
            login_url = 'https://passport.ustc.edu.cn/login'  # 科大统一用户登录所用的服务器地址

            # 获取JSESSIONID保存在cookie中，并在返回的html中提取CAS_LT字段
            r_caslt = session.get(login_url+'?service=%s' %
                                  urllib.parse.quote_plus(service))
            session.cookies.update({'lang': 'zh'})

            r_caslt.raise_for_status()
            html_caslt = BeautifulSoup(r_caslt.text, features='html.parser')
            caslt = html_caslt.findChild(
                'input', {'name': 'CAS_LT'}).attrs['value']

            # 登录健康上报网站
            login_data = {'model': 'uplogin.jsp', 'service': service, 'CAS_LT': caslt,
                          'warn': '', 'showCode': '', 'username': username, 'password': password, 'button': ''}
            r_login = session.post(login_url, data=login_data)
            r_login.raise_for_status()
            html_login = BeautifulSoup(r_login.text, features='html.parser')
        except:
            raise Exception('[!]登录失败')
        print('[-]登录成功')

        if sleep:
            time.sleep(random.random()*interval_delaym*60)

        # 获取网上的当前健康状况，并进行评估
        body_condition = '1'  # 正常
        try:
            for e in html_login.findChild('select', {'name': 'body_condition'}).findChildren('option'):
                if 'selected' in e.attrs:
                    body_condition = e.attrs['value']
        except:
            pass
        if body_condition != '1':
            print('[*]健康状况不正常，请手动上报')
            return

        # 判断人是否在内地，若不在内地，需要手动上报
        now_address = '1'  # 国内
        try:
            for e in html_login.findChild('input', {'name': 'now_address'}):
                if 'checked' in e.attrs:
                    now_address = e.attrs['now_address']
        except:
            pass
        if now_address != '1':
            print('[*]上报人不在内地，请手动上报')
            return

        try:
            data = {"_token": html_login.findChild(
                'input', {'name': '_token'}).attrs['value']}
        except:
            raise Exception('[!]无法从登录网站上获取获取_token')

        # 制造每日健康上报的表单
        data.update(REPORT_TEMPLATE)

        print('[+]从网站上更新部分个人报告信息')
        try:

            # 获取当前所在地的地址信息
            for key in ('juzhudi', 'jutiwz'):
                data.update({key: html_login.findChild(
                    'input', {'name': key}).attrs['value']})
            for key in ('city_area',):
                for e in html_login.findChild('select', {'name': key}).findChildren('option'):
                    if 'selected' in e.attrs:
                        data.update({key: e.attrs['value']})

            for key in ("has_fever", "last_touch_sars", "is_danger", "is_goto_danger"):
                for e in html_login.findChild('input', {'name': key}):
                    if 'checked' in e.attrs:
                        data.update({key: e.attrs['value']})

            # 从网上获取家庭紧急联系人信息
            for key in ("jinji_lxr", "jinji_guanxi", "jiji_mobile"):
                data.update({key: html_login.findChild(
                    'input', {'type': 'text', 'name': key}).attrs['value']})

        except:
            raise Exception('[!]无法从网站上更新部分个人报告信息')
        print('[-]更新部分个人报告信息成功')

        # 健康上报
        print('[+]健康上报')
        print('[!]个人上报信息')
        pprint.pprint(data)
        r_report = session.post(start_url+'/daliy_report', data)
        try:
            r_report.raise_for_status()

            # 是否上报成功
            html_report = BeautifulSoup(r_report.text, features='html.parser')
            i = html_report.text.find('上报成功')
            if i >= 0:
                print('[-]上报成功')
            else:
                raise Exception('[!]上报失败')
        except:
            raise Exception('[!]上报失败')

        print('[-]完成每日健康上报！')

    # 如有必要，可以发送邮件提醒
    if email:
        print('[+]发送提醒邮件')
        try:
            notify_self(('mail.ustc.edu.cn', 465, True), (email[0], email[1]),
                        "%s 完成每日健康上报！" % (datetime.now().date()), subject="每日健康上报")
            print('[-]发送提醒邮件成功')
        except:
            raise Exception('[!]发送提醒邮件失败')


def __main__():
    import time
    import argparse

    parser = argparse.ArgumentParser(
        description='中科大每日健康上报软件（版本号：%s）' % VERSION)

    parser.add_argument('-v', '--version', action='store_true', help='版本号')
    for v in ('-v', '--version'):
        if v in sys.argv[1:]:
            print("版本号: %s"%VERSION)
            sys.exit(0)

    parser.add_argument('username', type=str, help='学号')
    parser.add_argument('password', type=str, help='密码')
    parser.add_argument('-s', '--sleep', action='store_true', help='是否使用软件延迟')
    parser.add_argument('--sdelay', nargs=1, type=int,
                        default=2, help='登录延迟的分钟数')
    parser.add_argument('--idelay', nargs=1, type=int,
                        default=1, help='上报延迟的分钟数')
    parser.add_argument('--email', nargs=2, metavar=('ADDRESS',
                        'PASSWORD'), type=str, help='中科大邮箱，用于发送邮件提醒')

    args = parser.parse_args()

    try:
        main(username=args.username, password=args.password, sleep=args.sleep, start_delaym=args.sdelay,
             interval_delaym=args.idelay, email=args.email)
    except Exception as e:
        sys.exit(traceback.format_exc())
    
    print("\n程序运行完成，10s后自动关闭\n")
    time.sleep(10)
    sys.exit(0)


if __name__ == '__main__':
    __main__()
