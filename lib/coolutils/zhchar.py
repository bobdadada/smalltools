"""
全角字符unicode编码从65281~65374 （十六进制 0xFF01 ~ 0xFF5E）
半角字符unicode编码从33~126 （十六进制 0x21~ 0x7E）
空格比较特殊,全角为 12288（0x3000）,半角为 32 （0x20）
而且除空格外,全角/半角按unicode编码排序在顺序上是对应的
所以可以直接通过用+-法来处理非空格数据,对空格单独处理

url: https://www.jb51.net/article/53903.htm
"""

def full_to_half(ins):
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

def half_to_full(ins):
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

'''
#算法说明：要求字符串输入，现将字符串差费为整数部分和小数部分生成list[整数部分,小数部分]
#将整数部分拆分为：[亿，万，仟]三组字符串组成的List:['0000','0000','0000']（根据实际输入生成阶梯List）
#例如：600190000010.70整数部分拆分为：['600','1900','0010']
#然后对list中每个字符串分组进行大写化再合并
#最后处理小数部分的大写化
'''

C4DIGIT_D = {1:u'',2:u'拾',3:u'佰',4:u'仟'}
CSDIGIT_D = {1:u'',2:u'万',3:u'亿',4:u'兆'} # 4位分割标志
CNUM_D = {0:u'零',1:u'壹',2:u'贰',3:u'叁',4:u'肆',5:u'伍',6:u'陆',7:u'柒',8:u'捌',9:u'玖'}

def _split_int(integer):
    """拆分函数，将整数字符串拆分成由4位数字组成的list"""
    integer = str(integer)

    int_lst = []
    # 以4为单位划分
    idx = len(integer) % 4
    if idx > 0:
        int_lst.append(integer[0:idx])
    while idx < len(integer):
        int_lst.append(integer[idx:idx+4])
        idx += 4
    return int_lst
              
def _num_to_cnum_int_4(num):
    """将4位数字转换成中文大写数字"""
    cnum = u''

    n = len(num)
    for i in range(n):
        if int(num[i])==0:
            if i < n-1 and int(num[i+1]) != 0:
                cnum += CNUM_D[0]                   
        else:
            cnum += CNUM_D[int(num[i])] + C4DIGIT_D[n-i]
    
    return cnum

def _num_to_cnum_dec(num):
    cnum = u''

    n = len(num)
    if n == 1: #若小数只有1位
        if int(num[0])==0:
            pass
        else:
            cnum += CNUM_D[int(num[0])] + u'角整'
    else: #若小数有两位的四种情况
        if int(num[0])==0 and int(num[1])==0:
            pass
        elif int(num[0])!=0 and int(num[1])==0:
            cnum += CNUM_D[int(num[0])]+u'角整'
        elif int(num[0])==0 and int(num[1])!=0:
           cnum += CNUM_D[int(num[1])]+u'分'
        else:
            cnum += CNUM_D[int(num[0])]+u'角'+CNUM_D[int(num[1])]+u'分'

    return cnum


def num_to_cnum(num):
    temp = str(num).split('.')
    if len(temp) == 2:
        integer, decimal = temp
    else:
        integer, decimal = temp[0], ''

    # 中文大小数字
    cnum = u''

    if integer:  # 处理整数部分
        int_lst = _split_int(integer) #分解字符数组[亿，万，仟]三组List:['0000','0000','0000']
        n = len(int_lst) #获取拆分后的List长度
        #大写合并
        for i in range(n):
            cnum_part = _num_to_cnum_int_4(int_lst[i])
            if cnum_part:  # 合并：前字符串大写+当前字符串大写+标识符
                cnum += cnum_part + CSDIGIT_D[n-i]
        
        if cnum:
            cnum += u'元'
        else:
            cnum = CNUM_D[0] + u'元'

        if not decimal:
            cnum += u'整'
    
    if decimal:
        #处理小数部分
        cnum += _num_to_cnum_dec(decimal)

    return cnum

def test_num_to_cnum():
    assert num_to_cnum(100) == '壹佰元整'
    assert num_to_cnum(10000) == '壹万元整'
    assert num_to_cnum(10100) == '壹万零壹佰元整'
    assert num_to_cnum(10100) == '壹万零壹佰元整'
    assert num_to_cnum(1010010) == '壹佰零壹万零壹拾元整'
    assert num_to_cnum(100.01) == '壹佰元壹分'
    assert num_to_cnum(0) == '零元整'
    assert num_to_cnum(0.00) == '零元'
    assert num_to_cnum(0.01) == '零元壹分'
