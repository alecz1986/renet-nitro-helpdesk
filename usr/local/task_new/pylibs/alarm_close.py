#!/usr/local/bin/python
# -*- coding: koi8-r -*-
# $Id: views.py 65 2008-04-02 06:01:19Z zimina_svetlana $

import sys
import sqlalchemy
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import smtplib
import datetime
from task import *
Session = sessionmaker(bind=engine)
dbconn = Session()



em = 'o.boykov@renet.ru'
em1 = 'v.serzhantova@renet.ru'
em2 = 's.zimina@renet.ru'
em3 = 'd.utkin@renet.ru'
em4 = 'n.popov@renet.ru'
em5 = 'a.romanova@renet.ru'

msg = MIMEMultipart()
msg['From'] = 'helpdesk@helpdesk.renet.ru'
msg['To'] = em
msg['Subject'] = '*** REPORT HD ***'
msg.set_charset('utf-8')
msg.set_default_type("text/html")
now = datetime.datetime.now()
delta1 = now + datetime.timedelta(days=-1)
mess = "<b>%s</b><br/>Задачи, закрытые за %s.<br/>" % (now.strftime('%Y-%m-%d %H:%M'), delta1.strftime('%Y-%m-%d'))
mess += """
<br>
<table border='1' cellpadding="0" cellspacing="0" ><tr><td>Исполнитель</td><td>Задачи</td></tr><tr><td colspan='2'>HELPDESK</td></tr>
"""
do = False
for email,  profile_id, fio in dbconn.query(Userprofile.email, Userprofile.id, Userprofile.fio):#.filter(sqlalchemy.or_(Userprofile.system_id == 2, Userprofile.id.in_((54, 29, 30, 31)))):
    threads = [str(r[0]) for r in dbconn.query(Threads.id_global).filter(
                        Threads.closed_by_id == profile_id
                        ).filter(Threads.close_date == delta1.strftime('%Y-%m-%d')
                        ).filter(Threads.id_local==1
                        ).filter(Threads.status == Status.text
                        ).filter(Status.id ==2
                        ).filter(Threads.title_id == Tasktype.id
                        ).filter(Tasktype.system_id == 0
                     )]
    if threads:
        do = True
        mess += """
        <tr><td>%s</td><td>%s</td></tr>
        """ % (fio.encode('utf-8'), ','.join(threads))
mess += "<tr><td colspan='2'>TASKPRODUCTION</td></tr>"
for email,  profile_id, fio in dbconn.query(Userprofile.email, Userprofile.id, Userprofile.fio):#filter(sqlalchemy.or_(Userprofile.system_id == 2, Userprofile.id.in_((54, 29, 30, 31)))):
    threads = [str(r[0]) for r in dbconn.query(Threads.id_global).filter(
                        Threads.closed_by_id == profile_id
                        ).filter(Threads.close_date == delta1.strftime('%Y-%m-%d')
                        ).filter(Threads.id_local==1
                        ).filter(Threads.status == Status.text
                        ).filter(Status.id ==2
                        ).filter(Threads.title_id == Tasktype.id
                        ).filter(Tasktype.system_id == 1 
                     )]
    if threads:
        do = True
        mess += """
        <tr><td>%s</td><td>%s</td></tr>
        """ % (fio.encode('utf-8'), ','.join(threads))
mess += """
</table>
"""
if do:
    msg.attach(MIMEText(mess, 'html', _charset='utf-8'))
    smtp = smtplib.SMTP()
    smtp.connect()
    smtp.sendmail('helpdesk@helpdesk.renet.ru', em, msg.as_string())
    smtp.sendmail('helpdesk@helpdesk.renet.ru', em1, msg.as_string())
    smtp.sendmail('helpdesk@helpdesk.renet.ru', em3, msg.as_string())
    smtp.sendmail('helpdesk@helpdesk.renet.ru', em4, msg.as_string())
    smtp.sendmail('helpdesk@helpdesk.renet.ru', em5, msg.as_string())
    smtp.sendmail('helpdesk@helpdesk.renet.ru', 'oleg@renet.ru', msg.as_string())
    smtp.close()





