#coding=utf-8
import smtplib
from email.mime.text import MIMEText
import random
import string
from email.header import Header
from email.utils import formataddr
def sendmail(address):
    msg_from='290162965@qq.com'
    passwd='gxxroimxjcclcaaa'
    msg_to=address
    subject="邮箱验证码"
    content=str(random.randrange(1000,10000))
    msg=MIMEText("验证码:"+content)
    msg['Subject']=subject
    msg['From']=formataddr(["小题训练", "290162965@qq.com"])
    msg['To']=msg_to
    try:
    	s=smtplib.SMTP_SSL("smtp.qq.com",465) 	
    	s.login(msg_from,passwd)
    	s.sendmail(msg_from,msg_to,msg.as_string())
    	return content
    except Exception as e:
        print(e)
    	return "failed"
    finally:
    	s.quit()


