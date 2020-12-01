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


em = 'tech@renet.ru'
em1 = 's.zimina@renet.ru'
msg = MIMEMultipart()
msg['From'] = 'helpdesk@helpdesk.renet.ru'
msg['To'] = em
msg['Subject'] = '*** REPORT HD ***'
msg.set_charset('utf-8')
msg.set_default_type("text/html")
now = datetime.datetime.now()
delta = now + datetime.timedelta(hours=-3)
mess = "<b>%s</b><br/>Нет реакции на задачу более 3 часов.<br/>" % (now.strftime('%Y-%m-%d %H:%M'))
mess += """
<br>
<table border='1' cellpadding="0" cellspacing="0" ><tr><td>PERFORMER</td><td>THREADS</td></tr>
"""

do = False
for email,  profile_id, fio in dbconn.query(Userprofile.email, Userprofile.id, Userprofile.fio).filter(sqlalchemy.or_(Userprofile.system_id == 2, Userprofile.id.in_((54, 29, 30, 31)))):
    threads = [str(r[0]) for r in dbconn.query(Threads.id_global).filter(
                        Threads.performer_id == profile_id
                        ).filter(Threads.id_local != 1
                        ).filter(Threads.status == Status.text
                        ).filter(Status.id ==1
                        ).filter(Threads.title_id == Tasktype.id
                        ).filter(Tasktype.system_id == 0
#                        ).filter(sqlalchemy.or_(Threads.creation_date < now.strftime('%Y-%m-%d'), sqlalchemy.and_(Threads.creation_date == now.strftime('%Y-%m-%d'), Threads.creation_time < delta.strftime('%H:%M:%S')))
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
    smtp.sendmail('helpdesk@helpdesk.renet.ru', 'oleg@renet.ru', msg.as_string())
    smtp.close()
