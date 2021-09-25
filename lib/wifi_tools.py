# -*- coding: UTF-8 -*-
"""
简单的网卡联网功能
"""
import os
import subprocess
import time

import chardet
import pywifi

__all__ = [
    'get_iface', 'disconnect', 'isconnected', 'create_profile', 'search_network_profile_by_ssid',
    'connect', 'connect_ap', 'get_scan_ssids_netsh', 'get_scan_ssids_pywifi', 'get_saved_wifi_table'
]


def get_iface(i=0):
    """
    获取对应编号的网卡
    """
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[i]

    return iface


def disconnect(iface=None):
    if iface is None:
        iface = get_iface()
    iface.disconnect()
    time.sleep(1)
    return iface.status() in [
        pywifi.const.IFACE_DISCONNECTED, pywifi.const.IFACE_INACTIVE]


def isconnected(iface=None):
    if iface is None:
        iface = get_iface()
    return iface.status() == pywifi.const.IFACE_CONNECTED


def create_profile(ssid, key=None, auth=pywifi.const.AUTH_ALG_OPEN, cipher=pywifi.const.CIPHER_TYPE_CCMP,
                   akm=pywifi.const.AKM_TYPE_WPA2PSK):
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = auth
    profile.cipher = cipher
    profile.key = key
    profile.akm.append(akm)
    return profile


def search_network_profile_by_ssid(ssid, iface=None):
    if iface is None:
        iface = get_iface()

    for profile in iface.network_profiles():
        if profile.ssid == ssid:
            return profile


def connect(profile, iface=None):
    if iface is None:
        iface = get_iface()

    disconnect(iface)
    iface.connect(profile)
    time.sleep(5)
    return iface.status() == pywifi.const.IFACE_CONNECTED


def connect_ap(ssid, key=None, auth=pywifi.const.AUTH_ALG_OPEN, cipher=pywifi.const.CIPHER_TYPE_CCMP,
               akm=pywifi.const.AKM_TYPE_WPA2PSK, force=False):
    if (not force) and isconnected():
        return True

    profile = create_profile(ssid, key, auth=auth, cipher=cipher, akm=akm)
    return connect(profile)


def get_scan_ssids_netsh():
    """
    使用netsh查看当前位置处电脑可见的wifi名称，以元组的形式保存
    """

    # 结果
    ssids = []

    # 获取信息
    messages = subprocess.check_output('netsh wlan show network')
    messages = messages.decode(chardet.detect(
        messages)['encoding'], errors='ignore')

    for message in messages.split('\r\n'):
        if message.find("SSID ") != -1:
            ssids.append(message[9:].strip())

    return tuple(ssids)


def get_scan_ssids_pywifi():
    """
    使用pywifi查看当前位置处电脑可见的wifi名称，以元组的形式保存
    """

    iface = get_iface()
    iface.scan()
    time.sleep(5)

    return tuple([profile.ssid for profile in iface.scan_results()])


def get_saved_wifi_table():
    """
    获取电脑连接过的所有wifi名称和密码，以wifi名称-密码的键值对形式存储结构。空密码的值未None。
    """

    # 结果字典
    wifi_table = {}

    # 查询所有的wifi名称
    messages = os.popen('netsh wlan show profiles').readlines()
    # print(messages)

    # 获取的结果是一个列表list，需要进行遍历
    for message in messages:

        message = message.strip()
        # print(message)

        # 检查每一个结果中是否含有指定关键字
        if message.find(u"所有用户配置文件 : ") != -1:

            # 从位置11开始截取wifi名称
            wifiname = message[11:].strip()

            # 如果找到关键字，就截取指定位置的字符串，即wifi名称，再拼接成cmd命令
            # netsh wlan show profiles name="Xiaomi_216E" key=clear
            command = 'netsh wlan show profiles name="' + wifiname + '" key=clear'

            # 执行拼接好的命令，获取含有密码的结果
            wifiinfo = os.popen(command).readlines()
            # print(wifiinfo)

            # 获取的结果是一个列表list，需要进行遍历
            for info in wifiinfo:

                info = info.strip()
                # print(info)

                # 检查关键字
                if info.find(u"安全密钥               :") != -1:
                    # 判断是否存在密钥
                    if info[21:].strip() == '不存在':
                        # 不存在密钥时，使用None为值
                        wifi_table[wifiname] = None
                        break
                elif info.find(u"关键内容            :") != -1:
                    # 获取字符串指定位置的内容并判断是否为空
                    if info[18:] != '':
                        # 保存密码
                        wifi_table[wifiname] = info[18:].strip()

                        # print("wifi名称:" + wifiname)
                        # print("wifi密码:" + wifi_table[wifiname])
                        # print("")

    return wifi_table
