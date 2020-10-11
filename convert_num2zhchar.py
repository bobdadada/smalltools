#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#算法说明：要求字符串输入，现将字符串差费为整数部分和小数部分生成list[整数部分,小数部分]
#将整数部分拆分为：[亿，万，仟]三组字符串组成的List:['0000','0000','0000']（根据实际输入生成阶梯List）
#例如：600190000010.70整数部分拆分为：['600','1900','0010']
#然后对list中每个字符串分组进行大写化再合并
#最后处理小数部分的大写化
'''


class cnumber:
    cdict = {}
    gdict = {}
    xdict = {}

    def __init__(self):
        self.cdict = {1: '', 2: '拾', 3: '佰', 4: '仟'}
        self.xdict = {1: '元', 2: '万', 3: '亿', 4: '兆'}  # 数字标识符
        self.gdict = {0: '零', 1: '壹', 2: '贰', 3: '叁', 4: '肆', 5: '伍', 6: '陆', 7: '柒', 8: '捌', 9: '玖'}

    def csplit(self, cdata):  # 拆分函数，将整数字符串拆分成[亿，万，仟]的list
        g = len(cdata) % 4
        csdata = []
        lx = len(cdata) - 1
        if g > 0:
            csdata.append(cdata[0:g])
        k = g
        while k <= lx:
            csdata.append(cdata[k:k + 4])
            k += 4
        return csdata

    def cschange(self, cki):  # 对[亿，万，仟]的list中每个字符串分组进行大写化再合并
        lenki = len(cki)
        i = 0
        lk = lenki
        chk = ''
        for i in range(lenki):
            if int(cki[i]) == 0:
                if i < lenki - 1:
                    if int(cki[i + 1]) != 0:
                        chk = chk + self.gdict[int(cki[i])]
            else:
                chk = chk + self.gdict[int(cki[i])] + self.cdict[lk]
            lk -= 1
        return chk

    def cwchange(self, data):
        cdata = str(data).split('.')
        cki = cdata[0]
        if len(cdata) == 1:
            i = 0
            chk = ''
            cski = self.csplit(cki)  # 分解字符数组[亿，万，仟]三组List:['0000','0000','0000']
            ikl = len(cski)  # 获取拆分后的List长度
            # 大写合并
            for i in range(ikl):
                if self.cschange(cski[i]) == '':  # 有可能一个字符串全是0的情况
                    chk = chk + self.cschange(cski[i])  # 此时不需要将数字标识符引入
                else:
                    chk = chk + self.cschange(cski[i]) + self.xdict[ikl - i]  # 合并：前字符串大写+当前字符串大写+标识符
            chk = chk + '整'
        else:
            i = 0
            chk = u''
            cski = self.csplit(cki)  # 分解字符数组[亿，万，仟]三组List:['0000','0000','0000']
            ikl = len(cski)  # 获取拆分后的List长度
            # 大写合并
            for i in range(ikl):
                if self.cschange(cski[i]) == '':  # 有可能一个字符串全是0的情况
                    chk = chk + self.cschange(cski[i])  # 此时不需要将数字标识符引入
                else:
                    chk = chk + self.cschange(cski[i]) + self.xdict[ikl - i]  # 合并：前字符串大写+当前字符串大写+标识符
            # 处理小数部分
            ckj = cdata[1]
            lenkj = len(ckj)
            if lenkj == 1:  # 若小数只有1位
                if int(ckj[0]) == 0:
                    chk = chk + '整'
                else:
                    chk = chk + self.gdict[int(ckj[0])] + '角整'
            else:  # 若小数有两位的四种情况
                if int(ckj[0]) == 0 and int(ckj[1]) != 0:
                    chk = chk + '零' + self.gdict[int(ckj[1])] + '分'
                elif int(ckj[0]) == 0 and int(ckj[1]) == 0:
                    chk = chk + '整'
                elif int(ckj[0]) != 0 and int(ckj[1]) != 0:
                    chk = chk + self.gdict[int(ckj[0])] + '角' + self.gdict[int(ckj[1])] + '分'
                else:
                    chk = chk + self.gdict[int(ckj[0])] + '角整'
        return chk


if __name__ == '__main__':

    pt = cnumber()

    while True:
        num = str(input('请输入转换金额：'))
        if not num:
            break
        else:
            print(pt.cwchange(num))
