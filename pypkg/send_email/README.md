# 说明

使用Python内置的`smtplib`和`email`模块完成邮件发送，其中`email`负责构造邮件，`smtplib`负责发送邮件。常见邮箱的IMAP/POP3/SMTP设置可以参考资料[[2]](2)。

我们采用的科大的邮箱系统，即Coremail(盈世)，以下为相关信息，具体可以参看资料[[3]](3)。
SMTP(发信认证)/POP3/IMAP服务器: 
  mail.ustc.edu.cn(建议国内使用) 或 mail3.ustc.edu.cn(建议国外使用)
登录名/帐户名: (注意要完整的email地址)
  username@ustc.edu.cn(教工) 或 username@mail.ustc.edu.cn(学生)
教育网入口: http://email.ustc.edu.cn/
电信网入口: http://email2.ustc.edu.cn/
科技网入口: http://email3.ustc.edu.cn/

|服务端口|POP|IMAP|SMTP|
|:--|:--|:--|:--|
|不加密端口|110|143|25|
|SSL加密端口|995|993|465|


# 参考资料

[1]:https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432005226355aadb8d4b2f3f42f6b1d6f2c5bd8d5263000	"SMTP发送邮件"
[2]:https://www.cnblogs.com/shangdawei/p/4305989.html  "常见邮箱的IMAP/POP3/SMTP设置"
[3]:http://mail.ustc.edu.cn/coremail/help/index_zh_CN.jsp  "科大邮箱系统"

# 文件说明

|名称|描述|
|:--|:--|
|pysmtp.py|运行smtp主要的Python脚本|
|smaple.py|示例脚本|
|.rc|存储了邮箱地址的脚本文件|