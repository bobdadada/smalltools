# -*- coding: utf-8 -*-

import paramiko

# 获取配置信息，代码文本使用utf-8编码
def read_rc(path):
    with open(path, 'r', encoding='utf-8') as f:
        details = f.readlines()
        data = [detail.split('#')[0].strip() for detail 
                             in details if detail.strip()!='']
        # 获取信息，并保持在字典中
        info = {}
        for i in range(len(data)):
            if data[i].strip() == '':
                continue
            key,value = data[i].split('=')
            info[key.strip()] = value.strip()
    return info

# 获取代码，代码文本使用utf-8编码
def read_code(path):
    with open(path, 'r', encoding='utf-8') as f:
        details = f.readlines()
        codes = [detail.split('#')[0].strip() for detail 
                             in details if detail.strip()!='']
        try:
            codes.remove('')
        except:
            # 当使用txt编辑器时，文件头会出现多余的'\ufeff'。建议不要使用txt编辑器。
            codes.remove('\ufeff')
    return codes

# --------------------- 
# 作者：orientlu 
# 来源：CSDN 
# 原文：https://blog.csdn.net/qq_18150497/article/details/80787733 
# 版权声明：本文为博主原创文章，转载请附上博文链接！
class SSHClient():

    def __init__(self, hostname=None,port=22, username=None, password=None, pkey_path=None, timeout=10, **kwargs):
        self.client = paramiko.SSHClient()
        """
        使用xshell登录机器，对于第一次登录的机器会提示允许将陌生主机加入host_allow列表
        需要connect 前调用，否则可能有异常。
        """
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if password != None:
            self.client.connect(hostname=hostname,port=int(port), username=username, password=password, timeout=timeout)
        elif  pkey_path != None:
            """使用秘钥登录"""
            self.pkey = paramiko.RSAKey.from_private_key_file(pkey_path)
            self.client.connect(hostname=hostname,port=port,pkey=self.pkey, timeout=timeout)

        self.sftp = self.client.open_sftp()

    def run_cmd(self, cmd):
        _in, _out, _error = self.client.exec_command(cmd)
        return _out.read().decode(),_error.read().decode()

    def put_file(self, local, remote):
        return self.sftp.put(localpath=local, remotepath=remote)

    def get_file(self, local, remote):
        return self.sftp.get(localpath=local, remotepath=remote)

    def __del__(self):
        self.client.close()
        self.sftp.close()


if __name__ == '__main__':
    
    # 存储了配置资料的路径
    rc_path = r'.rc'
    # 存储了Bash代码的路径，所有代码都在txt文件中添加
    codes_path = r'codes.txt'
    # 获取配置信息，保存在字典中
    info = read_rc(rc_path)
    # 获取代码信息，保存在列表中
    codes = read_code(codes_path)
    
    # 连接到服务器
    client = SSHClient(**info)
    for code in codes:
        out, error = client.run_cmd(code)
        print('out', out)
