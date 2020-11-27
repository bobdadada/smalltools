"""
windows系统连接wifi功能，并连接中科大网络通
"""
import sys

import requests

from coolutils.check_wlan import get_wlan_profiles, get_avaliable_aps
from coolutils.wifi_tools import connect_ap, isconnected
from coolutils.web_tools import is_ext_network_connectable
from ustc_wlt import connect_wlt

def main(name, password):
    print('连接WIFI且登入中科大网络通!')

    # 联网
    if not isconnected():
        print('[!]wifi未连接')
        aps = get_avaliable_aps()
        if len(aps) == 0:
            filter = lambda ssid: True
        else:
            filter = lambda ssid: True if ssid in aps else False
        for ssid, key in get_wlan_profiles().items():
            if not filter(ssid):
                continue
            print('[+]尝试连接 %s'%ssid)
            if connect_ap(ssid, key):
                print('[-]成功连接 %s'%ssid)
                break
            else:
                print('[!]无法连接 %s'%ssid)

    # 判断两次，保证网卡服务正常
    if not isconnected():
        raise Exception('[!]网卡连接失败')

    if not is_ext_network_connectable():
        # 登录网络通
        connect_wlt(name, password)

    print('[*]完成连接WIFI且登入中科大网络通!')

def __main__():
    import time
    import argparse

    parser = argparse.ArgumentParser('连接WIFI且登入中科大网络通')
    parser.add_argument('name', type=str, help='账号名称')
    parser.add_argument('password', type=str, help='账号密码')
    arg = parser.parse_args()

    try:
        main(arg.name, arg.password)
    except Exception as e:
        print(e)
        raise
    finally:
        print("\n程序运行完成，10s后自动关闭\n")
        time.sleep(10)

    sys.exit(0)

if __name__ == '__main__':
    __main__()
