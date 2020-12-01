#! /usr/local/bin/python
# -*- coding: utf-8 -*-


import smtplib
from email.MIMEText import MIMEText
from htu_host import host_name
task_email = 'helpdesk@helpdesk.renet.ru'
#shop_email1 = 'peshka@sarbc.ru'


def sendemail(email, id, mess, title, link=''):
    if link == '':
        mark= 'TP'
    else:
        mark = 'HD'
#    email = 'vys@renet.ru' 
    rcpt = email
    body ="""
    Вам поступило задание <a href="helpdesk.renet.ru%s/thread?id=%s">%s</a>
    <br/>
    <pre>
    %s
    </pre>
    """ % (link, str(id), title.encode('utf-8'), mess.encode('utf-8').replace(':$', ':').replace('$', '\n'))
    msg = MIMEText(body,  'html', _charset='utf-8')
    msg['Subject'] = u"Задание %s" % mark
    msg['Content-Type'] = "text/html"
    msg['From'] = task_email
    msg['To']   = rcpt
    msg.set_default_type("text/html")
    s = smtplib.SMTP()
    s.connect()
    s.sendmail(task_email, [rcpt], msg.as_string())

