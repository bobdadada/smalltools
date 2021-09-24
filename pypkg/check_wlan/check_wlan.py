print("正在查询可连接的wifi......")
# 将查询结果遍历输出
for name in get_avaliable_aps():
    print("SSID名称：%s"%name)

print("\n正在查询连接过的wifi......")
# 将查询结果遍历输出
for name, passwd in get_wlan_profiles().items():
    print("wifi名称：%s，密码：%s"%(name, passwd))
