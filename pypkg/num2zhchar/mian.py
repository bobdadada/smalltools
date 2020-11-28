pt = cnumber()

while True:
    num = str(input('请输入转换金额：'))
    if not num:
        break
    else:
        print(pt.cwchange(num))
