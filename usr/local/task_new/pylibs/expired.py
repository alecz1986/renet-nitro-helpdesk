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

"""
Дежурная служба 1 уровня                                                        Оперативные дежурные
+---------------------------------------+---------+-----------------------+     +-----------------------------+---------+----------------------+
| fio                                   | user_id | email                 |     | fio                         | user_id | email                |
+---------------------------------------+---------+-----------------------+     +-----------------------------+---------+----------------------+
| деж. служба I уровня                  |      30 |                       |     | опер. дежурный              |      29 | oper@renet.ru        |
| Баландин Вячеслав                     |      81 | v.balandin@renet.ru   |     | Зубков Алексей              |      41 | a.zubkov@renet.ru    |
| Болотов Максим                        |      83 | m.bolotov@renet.ru    |     | Чубарых Михаил              |      34 | m.chubarykh@renet.ru |
| Нугаев Руслан                         |      88 | r.nugaev@renet.ru     |     | Брагин Тимофей              |      51 | t.bragin@renet.ru    |
| Слюсарь Галина                        |      96 | g.slyusar@renet.ru    |     +-----------------------------+---------+----------------------+
| Марченко Булат                        |     102 | b.marchenko@renet.ru  |
| Мельников Никита                      |     105 | n.melnikov@renet.ru   |
| Пальнов Александр                     |     107 | palnov@renet.ru       |
| Кудрявцев Александр                   |     108 | a.kudryavcev@renet.ru |
+---------------------------------------+---------+-----------------------+

Дежурная служба 2 уровня                                                        Руководители
+--------------------------------------+---------+------------------------+     +-----------------------------+---------+------------------------+
| fio                                  | user_id | email                  |     | fio                         | user_id | email                  |
+--------------------------------------+---------+------------------------+     +-----------------------------+---------+------------------------+
| деж. служба II уровня                |      31 | des2@renet.ru          |     | Осадчий Олег                |       4 | oleg@renet.ru          |
| Айкашев Денис                        |      32 | d.aikashev@renet.ru    |     | Бойков Олег                 |       3 | o.boykov@renet.ru      |
| Демагин Александр                    |      36 | a.demagin@renet.ru     |     | Сартаков Алексей            |      18 | a.sartakov@renet.ru    |
| Токовенко Андрей                     |      68 | a.tokovenko@renet.ru   |     | Сержантова Вероника         |      84 | v.serzhantova@renet.ru |
+--------------------------------------+---------+------------------------+     +-----------------------------+---------+------------------------+
"""

check_list = (
    # (Report name, list of emails, ids profiles)        

    #  Отчет по сотрудникам службы 1 уровня
    ('Дежурная служба I уровня', ['m.bolotov@renet.ru', 'r.nugaev@renet.ru', 'g.slyusar@renet.ru',
              'n.melnikov@renet.ru', 'a.lapshov@renet.ru', 'a.kudryavcev@renet.ru','g.grishin@renet.ru','i.skripkarev@renet.ru','s.spiryushin@renet.ru',
              'v.serzhantova@renet.ru', 'a.zubkov@renet.ru', 'm.chubarykh@renet.ru', 't.bragin@renet.ru',
              'o.boykov@renet.ru', 'oleg@renet.ru', 'a.sartakov@renet.ru'],
     [30, 81, 83, 88, 96, 102, 105, 107, 108]),
    #  Отчет по сотрудникам службы 2 уровня
    ('Дежурная служба II уровня', ['d.aikashev@renet.ru', 'a.demagin@renet.ru', 'd.karev@renet.ru',
              'a.zubkov@renet.ru', 'm.chubarykh@renet.ru', 't.bragin@renet.ru',
              'o.boykov@renet.ru', 'oleg@renet.ru', 'a.sartakov@renet.ru'],
     [31, 32, 36, 68]),
    # Отчет по оперативным дежурным 
    ('Оперативные дежурные', ['a.zubkov@renet.ru', 'm.chubarykh@renet.ru', 't.bragin@renet.ru',
              'o.boykov@renet.ru', 'oleg@renet.ru', 'a.sartakov@renet.ru'],
     [29, 41, 34, 51])
)

Session = sessionmaker(bind=engine)
dbconn = Session()



em = 's.zimina@renet.ru'
now = datetime.datetime.now()
delta = now + datetime.timedelta(hours=-24)
# select threads that have been already marked as expired
ids_expire = dbconn.execute("select id_task from expired_task").fetchall()


for (title, emails, user_ids) in check_list:
    msg = MIMEMultipart()
    msg['From'] = 'helpdesk@helpdesk.renet.ru'
    msg['To'] = ",".join(emails)
    msg.set_charset('utf-8')
    msg.set_default_type("text/html")
    msg['Subject'] = '*** Нет активности по задачам более суток  (%s) ***' % (title,)

    mess = "<b>%s</b><br/>На аварийные задачи нет реации более суток.<br/>" % (now.strftime('%Y-%m-%d %H:%M'))
    mess += """
    <br>
    <table border='1' cellpadding="0" cellspacing="0" ><tr><td>Исполнитель</td><td>Задачи</td></tr>
    """

    do = False
    ids = {}

    for user_id in user_ids:
        threads = [(th.id, th.id_global, th.creation_time, th.creation_date, th.fio_perf)
                    for th in dbconn.query(Threads).filter(Threads.performer_id == user_id
                                                  ).filter(Threads.status == Status.text
                                                  ).filter(Status.id ==1
                                                  ).filter(Threads.title_id == Tasktype.id
                                                  ).filter(Tasktype.system_id == 0 
                                                  ).filter(sqlalchemy.or_(Threads.creation_date < delta.strftime('%Y-%m-%d'),
                                                           sqlalchemy.and_(Threads.creation_date == delta.strftime('%Y-%m-%d'),
                                                                           Threads.creation_time < delta.strftime('%H:%M:%S')))
                 )]
        if threads:
            do = True

            for (id, glob, cr_time, cr_dt, fio) in threads:
                if (id,) not in ids_expire:
                    dbconn.execute("insert into expired_task (id_task, id_global, creation_time, creation_date, fio_perf) values "
                                   "(%s, %s, '%s', '%s', '%s')" % (id, glob, cr_time, cr_dt, fio))
                link = "<a href='http://helpdesk.renet.ru/hd/thread?id=%s'>%s</a>" % (id, glob)
                if fio in ids:
                    ids[fio].append(link)
                else:
                    ids[fio] = [link]

    if do:
        for fio, task_ids in ids.items():
            mess += """
                    <tr><td>%s</td><td>%s</td></tr>
                    """ % (fio.encode('utf-8'), ', '.join(task_ids))
        mess += """</table>"""
        msg.attach(MIMEText(mess, 'html', _charset='utf-8'))
        smtp = smtplib.SMTP()
        smtp.connect()
        smtp.sendmail('helpdesk@helpdesk.renet.ru', emails, msg.as_string())
        smtp.close()
