import smtplib
from email.mime.text import  MIMEText
from email.mime.multipart import MIMEMultipart
sender="suhu201606@163.com"
receiver="510920092@qq.com"
host="smtp.163.com"
password="shayang2012"
smtp=smtplib.SMTP_SSL(host,465)
