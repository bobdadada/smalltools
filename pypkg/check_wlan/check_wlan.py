import sys

from tabulate import tabulate

from wifi_tools import get_scan_ssids_pywifi, get_store_wifi_table


def main(mode, **kwargs):
    if mode & 0b01:
        print("[+]正在查询连接过的wlan......")
        store_wifi_table = get_store_wifi_table()
        if 'store_ssid' in kwargs:
            ssid = kwargs['store_ssid']
            if ssid in store_wifi_table:
                print("[*]wlan名称：%s，密码：%s" %
                      (ssid, store_wifi_table[ssid]))
            else:
                print("[!]wlan: %s 不在电脑中" % (kwargs['store_ssid']))
        else:
            print(tabulate(get_store_wifi_table().items(), headers=('名称', '密码')))
        print("[-]查询完成")

    if mode & 0b10:
        print("[+]正在查询当前位置可连接的wlan......")
        scan_ssids = set(get_scan_ssids_pywifi())  # deduplication
        print("[*]当前位置可连接的wlan名称：")
        print(tabulate(zip(scan_ssids), headers=('名称',)))
        print("[-]查询完成")


def __main__():
    import argparse
    import time

    parser = argparse.ArgumentParser(description="打印可用的WLAN信息")
    parser.add_argument('--show_all', action='store_true', help='打印所有信息')
    parser.add_argument('--store', nargs='?', const=True,
                        metavar="SSID", help='打印电脑中存储过的WLAN')
    parser.add_argument('--scan', action='store_true',
                        help='打印当前位置扫描出的WLAN')
    args = parser.parse_args()

    mode, kwargs = 0, {}
    if args.show_all:
        mode |= 0b11
    if args.store:
        mode |= 0b01
        if isinstance(args.store, str):
            kwargs['store_ssid'] = args.store
    if args.scan:
        mode |= 0b10

    try:
        main(mode, **kwargs)
    except Exception as e:
        print(e)
        raise
    finally:
        print("\n程序运行完成，10s后自动关闭\n")
        time.sleep(10)

    sys.exit(0)

if __name__ == '__main__':
    __main__()
