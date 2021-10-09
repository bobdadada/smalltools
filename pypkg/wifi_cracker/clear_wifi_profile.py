import sys

__description__ = """
清理网卡中存储的热点信息
"""

import pywifi


def main(ssid, iface_name=None):

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

    print('[+]开始清理(SSID:%S)的热点' % ssid)
    network_profiles = iface.network_profiles()
    for network_profile in network_profiles:
        if ssid == network_profile.ssid:
            iface.remove_network_profile(network_profile)
    print('[-]清理(SSID:%S)的热点完成' % ssid)


def __main__():
    import argparse

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('ssid', type=str, help='所要清理的SSID名称')
    parser.add_argument('-i', '--iface_name', type=str,
                        help='无限网卡名称，window系统可以通过设备管理器查看，' +
                        'linux系统可在/var/run/wpa_supplicant/中查看。' +
                        '默认为第一个网卡设备。')
    args = parser.parse_args()

    main(args.ssid, iface_name=args.iface_name)

    sys.exit(0)


if __name__ == '__main__':
    __main__()
