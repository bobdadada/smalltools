import time

from pywifi import const  # 引用一些定义

__all__ = [
    'get_aps', 'classify_aps', 'crack_ap'
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

    # 网卡断开链接后开始连接测试
    if iface.status() == const.IFACE_DISCONNECTED:

        iface.add_network_profile(profile)
        iface.connect(profile)

        # wifi连接时间
        time.sleep(2)
        flag = iface.status() == const.IFACE_CONNECTED

        # 清理痕迹
        iface.remove_network_profile(profile)

        return flag

    else:
        return None
