import time
import math
import random

from pywifi import const  # 引用一些定义

__all__ = [
    'get_aps', 'classify_aps', 'try_connect', 'sample_passwords'
]


def get_aps(iface, count=None, filtered_ssids=None):
    """
    获取信号强度靠前的count个信号的ssid
    """
    if filtered_ssids is None:
        filtered_ssids = []

    iface.scan()
    time.sleep(8)
    profiles = iface.scan_results()

    filtered_profiles = list(
        filter(lambda profile: profile.ssid not in filtered_ssids, profiles))
    filtered_profiles.sort(key=lambda p: p.signal, reverse=True)

    if count:
        return filtered_profiles[:count]
    else:
        return filtered_profiles


def classify_aps(profiles):
    """
    将热点分为需要密码和不需要密码两类
    """
    needpwd, notneedpwd = [], []

    for profile in profiles:
        if const.AKM_TYPE_NONE in profile.akm:
            notneedpwd.append(profile)
        else:
            needpwd.append(profile)

    return needpwd, notneedpwd


def try_connect(iface, profile):
    """
    使用profile连接iface，如果连接失败，则清除profile
    """
    iface.disconnect()  # 断开无限网卡连接
    time.sleep(1)

    # 网卡断开链接后开始连接测试
    if iface.status() == const.IFACE_DISCONNECTED:
        iface.add_network_profile(profile)
        iface.connect(profile)

        # wifi连接时间
        time.sleep(2)
        if iface.status() != const.IFACE_CONNECTED:

            # 清理network_profiles
            network_profiles = iface.network_profiles()
            for network_profile in network_profiles:
                if all(getattr(profile, attr) != getattr(network_profile, attr) for attr in ('ssid', 'key')):
                    iface.remove_network_profile(network_profile)

            return False
        else:
            return True
    else:
        return None


def sample_passwords(passwords, stype):
    """
    密码本采样类型：
    0: 完全复制密码本
    1: 提取前200个密码
    2: 随机采取sqrt(length)个密码
    3: 提取前200个密码+随机采取sqrt(remaining_length)个密码
    """
    if stype == 1:
        if len(passwords) < 200:
            return passwords.copy()
        else:
            return passwords[:200]
    elif stype == 2:
        return random.sample(passwords, int(math.sqrt(len(passwords))))
    elif stype == 3:
        if len(passwords) < 200:  # 起始的200个被认为是具有较高可能性的密码
            p_passwords = passwords
            r_passwords = []
        else:
            p_passwords = passwords[:200]
            r_passwords = passwords[200:]
        return p_passwords + \
            random.sample(r_passwords, int(math.sqrt(len(r_passwords))))
    else:
        return passwords.copy()
