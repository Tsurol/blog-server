# coding:utf-8

import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from rest_framework import status

# sender_email = '2656155887@qq.com'
# sender_passwd = 'uqmcpadgribcebib'
sender_email = 'zzlzzl1243@163.com'
sender_passwd = 'ITKQBFDPRGLBLSZH'
# 发信服务器,端口号
# smtp_server = 'smtp.qq.com'
smtp_server = 'smtp.163.com'
port = 465
PROJECT_NAME = "zzl Blog"


def send_email(to_email: str, verify_code: str):
    """
    :param to_email: 收件邮箱
    :param verify_code: 验证码
    :return:
    """
    # 邮件主题
    subject = "[周梓凌的个人网站】请查收您的短信登录验证码"
    mail_msg = MIMEMultipart()
    content = '您的邮箱验证码为：{} \n Please don`t report this email \n ---  {}  ---'.format(verify_code, PROJECT_NAME)
    mail_msg.attach(MIMEText(content, 'plain', 'utf-8'))
    mail_msg['From'] = sender_email
    mail_msg['Subject'] = Header(subject, 'utf-8')
    mail_msg['To'] = to_email
    try:
        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server, port)
        # 登录发信邮箱
        server.login(sender_email, sender_passwd)
        # 发送邮件
        server.sendmail(sender_email, to_email, mail_msg.as_string())
        # 关闭服务器
        server.quit()
    except smtplib.SMTPException as e:
        print(e)
        return {}
    return status.HTTP_201_CREATED


def start_send_mail(message):
    mail_msg = MIMEMultipart()
    mail_msg['Subject'] = Header('尊敬的周梓凌，请注意查收用户的反馈', 'utf-8')
    mail_msg['From'] = sender_email
    toaddrs = ['zzlzzl996@126.com']
    mail_msg['To'] = ','.join(toaddrs)
    mail_msg.attach(MIMEText(message, 'plain', 'utf-8'))
    try:
        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server, port)
        # 登录发信邮箱
        server.login(sender_email, sender_passwd)
        # 发送邮件
        server.sendmail(sender_email, mail_msg['To'], mail_msg.as_string())
        # 关闭服务器
        server.quit()
    except Exception as e:
        print(e)
        print("Error: unable to send email")


if __name__ == '__main__':
    # Test代码
    start = time.time()
    send_email(to_email='zzlzzl996@126.com', verify_code='5555')
    print(time.time()-start)
    # start_send_mail(message='312312')
    print('ok')
