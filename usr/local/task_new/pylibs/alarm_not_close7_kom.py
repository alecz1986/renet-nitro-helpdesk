#!/usr/local/bin/python
# -*- coding: utf-8 -*-
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
em1 = 's.zimina@renet.ru'
em2 = 'd.utkin@renet.ru'
em3 = 'n.popov@renet.ru'
em4 = 'a.romanova@renet.ru'

msg = MIMEMultipart()
msg['From'] = 'helpdesk@helpdesk.renet.ru'
msg['To'] = em
msg['Subject'] = '*** REPORT HD ***'
msg.set_charset('utf-8')
msg.set_default_type("text/html")
now = datetime.datetime.now()
delta = now + datetime.timedelta(days=-7)
mess = "<b>%s</b><br/>Задачи не закрыты более недели.<br/>" % (now.strftime('%Y-%m-%d %H:%M'))
mess += """
<br>
<table border='1' cellpadding="0" cellspacing="0" ><tr><td>Исполнитель</td><td>Задачи</td></tr>
"""

do = False
for email,  profile_id, fio in dbconn.query(Userprofile.email, Userprofile.id, Userprofile.fio).filter(Userprofile.system_id == 4):
    threads = [str(r[0]) for r in dbconn.execute("""select id_global 
        from thread
        where id_global in (select id_global
            from thread join tasktype on thread.title_id = tasktype.id
            where id_local=1
                and status!=(select text from status where id=2)
                and creation_date<"%s"
                and system_id=0
                )
         and status=(select text from status where id=1) and performer_id=%s""" % (
        delta.strftime('%Y-%m-%d'), profile_id,
)) ]
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
    smtp.sendmail('helpdesk@helpdesk.renet.ru', 'oleg@renet.ru', msg.as_string())
    smtp.sendmail('helpdesk@helpdesk.renet.ru', em, msg.as_string())
    smtp.sendmail('helpdesk@helpdesk.renet.ru', em2, msg.as_string())
    smtp.sendmail('helpdesk@helpdesk.renet.ru', em3, msg.as_string())
    smtp.sendmail('helpdesk@helpdesk.renet.ru', em4, msg.as_string())
    smtp.close()


