
# -*- coding: UTF-8 -*-
import os
import sys
import subprocess
import chardet


def get_avaliable_aps():
    """
    导出当前电脑可连接的所有wifi名称，以元组的形式保存
    """

    # 结果
    ssids = []

    # 获取信息
    messages = subprocess.check_output('netsh wlan show network')
    messages = messages.decode(chardet.detect(messages)['encoding'], errors='ignore')

    for message in messages.split('\r\n'):
        if message.find("SSID ") != -1:
            ssids.append(message[9:].strip())

    return tuple(ssids)

def get_wlan_profiles():
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

if __name__ == '__main__':
    print("正在查询可连接的wifi......")
    # 将查询结果遍历输出
    for name in get_avaliable_aps():
        print("SSID名称：%s"%name)

    print("\n正在查询连接过的wifi......")
    # 将查询结果遍历输出
    for name, passwd in get_wlan_profiles().items():
        print("wifi名称：%s，密码：%s"%(name, passwd))
