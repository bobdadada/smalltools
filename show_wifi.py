import os
import time

import pywifi

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]

ssids = []
iface.scan()
time.sleep(5)
for profile in iface.scan_results():
    ssids.append(profile.ssid)
print('当前所有wifi的ssid:\n'+''.join('{}\n'.format(ssid) for ssid in ssids if ssid.strip()), flush=True)

while True:
    op = input('是否需要查看wifi信息?(y|n):')
    if op in ('y', 'yes'):
        name = input('请输入wifi名称:')
        if name:
            os.system('netsh wlan show profiles name={} key=clear'.format(name))
        else:
            print('输入名称无效')
    elif op in ('n', 'no'):
        break
    else:
        continue

