"""
全角字符unicode编码从65281~65374 （十六进制 0xFF01 ~ 0xFF5E）
半角字符unicode编码从33~126 （十六进制 0x21~ 0x7E）
空格比较特殊,全角为 12288（0x3000）,半角为 32 （0x20）
而且除空格外,全角/半角按unicode编码排序在顺序上是对应的
所以可以直接通过用+-法来处理非空格数据,对空格单独处理

url: https://www.jb51.net/article/53903.htm
"""

def full2half(ins):
    """把字符串全角转半角"""
    outs = ""
    for c in ins:
        code = ord(c)
        if code == 0x3000:  # 转换空格
            code = 0x0020
        else:
            code -= 0xFEE0

        if code < 0x0020 or code > 0x007E:  # 对不在半角字符范围内的，返回原来字符
            outs += c
        else:
            outs += chr(code)

    return outs

def half2full(ins):
    """把字符串半角转全角"""
    outs = ""
    for c in ins:
        code = ord(c)
        if code < 0x0020 or code > 0x007E:
            outs += c
        else:
            if code == 0x0020:
                code += 0x3000
            else:
                code += 0xFEE0
            outs += chr(code)

    return outs

