"""
windows系统连接wifi功能，并连接中科大网络通
"""
import requests

from check_wifi import check_wifi
from wifi_tools import connect_ap, isconnected
from wlt import main as wlt

def ext_network_connectable():
    try:
        r = requests.get(r"https://www.baidu.com")
        r.raise_for_status()
        if not len(r.text)>1000:
            raise Exception('联网失败')
        return True
    except:
        return False


def main(name, password):
    print('连接WIFI且登入中科大网络通!')

    # 联网
    if not isconnected():
        print('[!]wifi未连接')
        for ssid, key in check_wifi().items():
            print('[+]尝试连接 %s'%ssid)
            if connect_ap(ssid, key):
                print('[-]成功连接 %s'%ssid)
                break
            else:
                print('[!]无法连接 %s'%ssid)

    # 判断两次，保证网卡服务正常
    if not isconnected():
        raise Exception('[!]网卡连接失败')

    if not ext_network_connectable():
        # 登录网络通
        wlt(name, password)
    
    print('[*]完成连接WIFI且登入中科大网络通!')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('连接WIFI且登入中科大网络通')
    parser.add_argument('--name', type=str, help='账号名称')
    parser.add_argument('--password', type=str, help='账号密码')
    arg = parser.parse_args()

    try:
        main(arg.name, arg.password)
    except Exception as e:
        print(e)
        raise

    exit(0)

