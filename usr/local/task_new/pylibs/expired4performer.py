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
common_perf = {"Deg1": 30,
               "Deg2": 31,
               "Oper": 29}
titles = {"Deg1": "Дежурная служба I уровня",
          "Deg2": "Дежурная служба II уровня",
          "Oper": "Оперативные дежурные"
          }

check_list = (
    # (Report name, ids profiles)        

    #  Отчет по сотрудникам службы 1 уровня
    ('Deg1', [81, 83, 88, 96, 102, 105, 107, 108]),
    #  Отчет по сотрудникам службы 2 уровня
    ('Deg2', [32, 36, 68]),
    # Отчет по оперативным дежурным 
    ('Oper', [41, 34, 51])
)

Session = sessionmaker(bind=engine)
dbconn = Session()



now = datetime.datetime.now()
delta = now + datetime.timedelta(hours=-24)


for (title, user_ids) in check_list:
    for user_id in user_ids:
        msg = MIMEMultipart()
        msg['From'] = 'helpdesk@helpdesk.renet.ru'
        email = 'sshturm@mirantis.com'
        email = dbconn.query(Userprofile.email).filter(Userprofile.id == user_id).one()[0]
        msg['To'] = email
        msg.set_charset('utf-8')
        msg.set_default_type("text/html")
        msg['Subject'] = '*** ОБНОВЛЕНИЕ СТАТУСА ЗАДАЧИ (%s) ***' % (titles[title],)

        mess = "<b>%s</b><br/>Задачи без движения более суток. Необходимо отписаться по следущим из них:<br/>" % (now.strftime('%Y-%m-%d %H:%M'))
        mess += """
        <br>
        <table border='1' cellpadding="0" cellspacing="0" ><tr><td>исполнитель</td><td>задачи</td></tr>
        """
        ids = {}
        threads = [(th.id, th.fio_perf, th.id_global)
                    for th in dbconn.query(Threads).filter(Threads.performer_id.in_([user_id, common_perf[title]])
                                                  ).filter(Threads.status == Status.text
                                                  ).filter(Status.id ==1
                                                  ).filter(Threads.title_id == Tasktype.id
                                                  ).filter(Tasktype.system_id == 0 
                                                  ).filter(sqlalchemy.or_(Threads.creation_date < delta.strftime('%Y-%m-%d'),
                                                           sqlalchemy.and_(Threads.creation_date == delta.strftime('%Y-%m-%d'),
                                                                           Threads.creation_time < delta.strftime('%H:%M:%S')))
                 )]
        if threads:
            for (id, fio, glob) in threads:
                link = "<a href='http://helpdesk.renet.ru/hd/thread?id=%s'>%s</a>" % (id, glob)
                if fio in ids:
                    ids[fio].append(link)
                else:
                    ids[fio] = [link]

            for fio, task_ids in ids.items():
                mess += """
                        <tr><td>%s</td><td>%s</td></tr>
                        """ % (fio.encode('utf-8'), ', '.join(task_ids))
            mess += """</table>"""
            msg.attach(MIMEText(mess, 'html', _charset='utf-8'))
            smtp = smtplib.SMTP()
            smtp.connect()
            smtp.sendmail('helpdesk@helpdesk.renet.ru', email, msg.as_string())
            smtp.close()
