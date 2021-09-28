"""
window连接wifi功能
"""
import sys
from pprint import pprint

from wifi_tools import connect, search_network_profile_by_ssid, isconnected, get_store_wifi_table, get_scan_ssids_pywifi


def main():
    print('连接可用WIFI服务!')

    if not isconnected():
        print('[+]开始连接wifi')
        
        assids = get_scan_ssids_pywifi()

        if assids:
            print('[*]当前位置可用的wifi为')
            pprint(assids)

            wifi_table = get_store_wifi_table()

            for assid in assids:
                if assid in wifi_table:
                    print('[+]尝试连接 %s' % assid)
                    aprofile = search_network_profile_by_ssid(assid)
                    aprofile.key = wifi_table[assid]
                    if connect(aprofile):
                        print('[-]成功连接 %s' % assid)
                        break
                    else:
                        print('[!]无法连接 %s' % assid)
        else:
            print('[!]当前位置无可用的wifi')
            return

    else:
        print('[*]wifi已连接')

    # 判断两次，保证网卡服务正常
    if not isconnected():
        raise Exception('[!]网卡连接失败')

    print('[*]完成连接WIFI!')


def __main__():
    import time
    import argparse

    parser = argparse.ArgumentParser(description='自动选择可用的WIFI并连接')
    args = parser.parse_args()

    try:
        main()
    except Exception as e:
        print(e)
        raise
    finally:
        print("\n程序运行完成，10s后自动关闭\n")
        time.sleep(10)

    sys.exit(0)


if __name__ == '__main__':
    __main__()
