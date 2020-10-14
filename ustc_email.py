import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

ustc_smtp = ('mail.ustc.edu.cn', 25)

def notify_self(addr, password, msg, subject=None):

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header(formataddr(('我', addr)), 'utf-8')   # 发送者
    message['To'] =  Header(formataddr(('我', addr)), 'utf-8')    # 接收者
    message['Subject'] = Header(str(subject), 'utf-8')
    
    with smtplib.SMTP() as smtpObj:
        smtpObj.connect(*ustc_smtp)
        smtpObj.login(addr, password)
        smtpObj.sendmail(addr, [addr], message.as_string())
