# -*- coding: utf-8 -*-

from bxypyutils.email_tools import send_email

def __main__():
    import argparse

    parser = argparse.ArgumentParser(description="发送邮件小程序")
    parser.add_argument('server', type=str, help="服务器地址。例如mail.ustc.edu.cn:465:1表示建立TLS/SSL连接。")
    parser.add_argument('emailbox', type=str, help="邮箱账户和密码。例如address:passwrod。")
    parser.add_argument('msg', type=str, help="简单的邮件文本")
    parser.add_argument('--subject', type=str, help="邮件的主题")
    parser.add_argument('--toaddr', nargs="+", type=str, help="接受的邮箱地址。若无，则发送给自己")
    args = parser.parse_args()

    server = args.server.split(':')
    if len(server) == 3:
        server[2] = int(server[2])

    emailbox = args.emailbox.split(':')
    msg = args.msg

    subject = args.subject

    if not args.toaddr:
        toaddrs = [emailbox[0]]
    else:
        toaddrs = args.toaddr

    print('[+]正在发送邮件...')
    try:
        send_email(server, emailbox, toaddrs, msg, subject=subject)
        print('[-]邮件发送完成')
    except Exception as e:
        print(e)
        print('[!]邮件发送失败')

if __name__ == '__main__':
    __main__()
