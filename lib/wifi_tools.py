"""
简单的网卡联网功能
"""

import time
import pywifi

def get_iface(i=0):
    """
    获取编号为0的网卡，并断开当前连接
    """
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[i]

    return iface

def disconnect(iface):
    iface.disconnect()
    time.sleep(1)
    assert iface.status() in [pywifi.const.IFACE_DISCONNECTED, pywifi.const.IFACE_INACTIVE]
    return iface

def isconnected(iface=None):
    if iface is None:
        iface = get_iface()
    if iface.status() == pywifi.const.IFACE_CONNECTED:
        return True
    else:
        return False

def create_ap_profile(ssid, key=None):
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = pywifi.const.AUTH_ALG_OPEN
    profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
    profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
    profile.key = key
    return profile

def connect_profile_by_iface(iface, profile):
    disconnect(iface)
    iface.connect(profile)
    time.sleep(30)
    assert iface.status() == pywifi.const.IFACE_CONNECTED

def connect_ap(ssid, key=None, force=False):
    iface = get_iface()
    if (not force) and isconnected(iface):
        return True

    try:
        profile = create_ap_profile(ssid, key)
        connect_profile_by_iface(iface, profile)
    except AssertionError:
        return False

    return True
