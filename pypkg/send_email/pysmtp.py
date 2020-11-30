# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.utils import parseaddr, formataddr
import smtplib
import os

def read_rc(path):
    with open(os.path.join(os.getcwd(), path), encoding='utf-8') as f:
        details = f.readlines()
        data = [detail.split('#')[0].strip() for detail 
                             in details if detail.strip()!='']
        data.remove('')
        # 存储服务器相关信息
        smtp_info = {}
        for i in data:
            if i.startswith('['):
                server = i[1:-1].strip()
                smtp_info[server] = {}
                continue
            key,value = i.split('=')
            smtp_info[server][key.strip()] = value.strip()
        return smtp_info

def _format_addr(s):
    # 注意不能简单地传入name <addr@example.com>，因为如果包含中文，
    # 需要通过Header对象进行编码
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

if __name__ == '__main__':

    rc_path =  r'.rc'
    smtp_info = read_rc(rc_path)
    print(smtp_info)
    
    # 设置服务器为中科大，并使用加密模式
    smtp = smtp_info['中科大']
    smtp_server = smtp['smtp_server']
    port = int(smtp['port'].split(',')[1])
    if port == 25:
        server = smtplib.SMTP(smtp_server, port)
    elif port == 465:
        server = smtplib.SMTP_SSL(smtp_server, port)
        server.starttls()
    server.set_debuglevel(1)
    
    # 编辑邮件
    from_addr = smtp['from_addr']
    to_addr = [addr.strip() for addr in smtp['to_addr'].split(',') if addr.strip()!='']
    password = smtp['password']
    
    msg = MIMEMultipart('alternative')
    msg['From'] = _format_addr('服务器 <%s>' % from_addr)
    msg['To'] = ','.join([_format_addr('使用者 <%s>' % addr) for addr in to_addr])
    msg['Subject'] = Header('服务器读取的信息', 'utf-8').encode()
    
    msg.attach(MIMEText('hello', 'plain', 'utf-8'))
    msg.attach(MIMEText('<html><body><h1>Hello</h1></body></html>', 'html', 'utf-8'))
    
    # 传输邮件
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()  