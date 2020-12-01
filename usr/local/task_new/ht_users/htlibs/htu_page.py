# -*- coding: utf-8 -*-
import httplib
import urllib

from lxml import etree
from lxml.html import fragment_fromstring
import uuid
import os
import re
import sys
import datetime
import cStringIO
import csv
import htu_main
from htu_config import secret_minlength
from task import *
from rrduet.rr_template import E,field
from sphinxapi import *
from htu_base import template_base, form_base, template_html
from rrduet.rr_sessdict import sessdict
import sqlalchemy
from htu_config import htdocs_dir
from htu_host import host_name
import re
from lxml.html import fragment_fromstring
from sqlalchemy import not_
from task_mail import sendemail
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#URL="sendsms.a1agregator.ru"
#PATH="/http/"
#company="RENET"
URL="traffic.smstitan.ru"
PATH="/API:0.9/"
APIKey="c95537060ed22142bbd810635309e6547eb12fd5"
Command="SendOne"
company="RENET"

db_info = 'mysql://spring:abz666@87.238.232.17/spring?charset=utf8&use_unicode=1'
sms_autocopmplit = ['fio']

def get_fio(message):
    check = [u"Фамилия:", u"Имя:", u"Отчество:", u"ФИО:"]
    ret = []
    fields = message.split('$')
    for param in check:
        if param in fields:
            param_index = fields.index(param)
            ret.append(fields[param_index+1].replace('\n', '').replace(' ', ''))
    return ' '.join(ret)


def agregator(sms, phone):
#    dbengine = create_engine(db_info)
#    Session = sessionmaker(bind=dbengine)
#    conn = Session()
#    conn.execute("""insert into agregator_sms (date, msg, phones, company)
#        values ('%s', '%s', '%s', '%s')""" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
#            sms, phone, company))
#    conn.commit()
#    conn.close()
    try:
        accept='text/plain'
        data = {'Number': phone,
                'Sender': 'RENET',
                'Command': Command,
                'Content': sms.encode('utf-8'),
                'Concatenated': 1,
                'APIKey': APIKey
                }
        http_conn = httplib.HTTPSConnection(URL)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": accept}
        http_conn.request('POST', PATH, urllib.urlencode(data), headers)
        resp = http_conn.getresponse().read()
        http_conn.close()
    except:
        resp = 'error during send of sms'
    return str(resp)

def field_minmax(name, minval=0, maxval=None):
    if maxval is None:
        return field(name, minval, lambda x, y=minval: min(y, int(x)), ValueError)
    return field(name, minval, lambda x, y=minval, z=maxval: max(z, min(y, int(x))), ValueError)

class perf(template_html):
    cls__kwds = set(['common'])
    class callback_form(form_base):
        fields = [
            field('id', ''),
            field('perf_id', 0),
        ]
    def E_data(self, state=None):
        form = self.form
        dbconn = self.dbconn
        gr_id = form['id']
        perf_id = int(form['perf_id'])
        opts = []
        for p in dbconn.query(Userprofile).filter(Userprofile.system_id == gr_id).filter(not_(Userprofile.fio.like(u"%увол%"))).filter(not_(Userprofile.fio.like(u"%в отпуске%"))).order_by(Userprofile.weight, Userprofile.fio):
            if perf_id == p.id:
                opts.append(E.option(p.fio+' '+p.post,  value=str(p.id), selected='1'))
            elif not perf_id:
                opts.append(E.option(p.fio+' '+p.post,  value=str(p.id)))
        if not perf_id:
            opts.append(E.option('--',  value='0'))
        res = E.select(*opts, name="performer_id")
        return res

class comment(template_html):
    cls__kwds = set(['common'])
    class callback_form(form_base):
        fields = [
            field('task_id', ''),
            field('thread_id', 0),
        ]
    def E_data(self, state=None):
        form = self.form
        dbconn = self.dbconn
        task_id = form['task_id']
        thread_id = form['thread_id']
        res = []
        mess = []
        tasktype =  dbconn.query(Tasktype).filter(Tasktype.id == task_id).one()
        for r in dbconn.query(Commentfield).filter(Commentfield.field_comment_id == Fields.field_id).filter(Fields.type_id == task_id):
            res.append(r.comment)
        for r in dbconn.query(Taskfield).filter(Taskfield.id == Fields.field_id).filter(Fields.type_id == task_id).order_by(Taskfield.weight.desc()):
            mess.append('$'+r.name+':$')
        mess.append(u"$Примечание"+':$')
        try:
            res.append(dbconn.query(Instruction_glob.instruct).filter(Instruction_glob.type_task_id == task_id).one()[0].replace('. ', '.\n'))
        except:
            pass
        sms = tasktype.sms_text
        if int(thread_id):
            try:
                th_sms = dbconn.query(ThreadSms).filter(Threads.id == thread_id).filter(ThreadSms.id_global == Threads.id_global).one()
            except:
                th_sms = None 
            for i in sms_autocopmplit:
                if i in sms:
                    val = '--'
                    if th_sms is not None:
                        try:
                            if getattr(th_sms, i).replace(' ', ''):
                                val = getattr(th_sms, i)
                        except:
                            if getattr(th_sms, i):
                                val = str(getattr(th_sms, i))
                    sms = sms.replace(i, val)
        for i in sms_autocopmplit:
            sms = sms.replace(i, '--')
        return E.div(
                E.pre('\n'.join(res), id='comment'),
                E.textarea('\n'.join(mess)),
                E.sms(sms),
                E.send(str(tasktype.send)),
                )

class message(template_html):
    cls__kwds = set(['common'])
    class callback_form(form_base):
        fields = [
            field('message', ''),
        ]
    def E_data(self, state=None):
        form = self.form
        message = form['message']
        fields = message.split('$')
        try:
            phone_index = fields.index(u'Тел. сотовый:')
        except:
            phone_index = 0
        if not phone_index:
            try:
                phone_index = fields.index(u'Контактный телефон:')
            except:
                phone_index = 0
        if phone_index:
            phone = fields[phone_index+1].replace('+7', '').replace(' ', '')
        else:
            phone = ''
        return E.div(
                E.phone(phone)
                )

class hd(template_base):
    def E_main(self):
        return E.main(E.bgcolor("#9ACD32"),
                E.menu(E.href('/hd'), E.color(u"blue"), E.name(u"главная")),
                E.menu(E.href('/hd/threads'), E.color(u"blue"), E.name(u"задания")),
                E.menu(E.href('/hd/reports'), E.color(u"blue"), E.name(u"отчеты")),
                E.menu(E.href('/passwd'), E.color(u"blue"), E.name(u"смена пароля")),
                E.menu(E.href('/hd/search'), E.color(u"blue"), E.name(u"поиск")),
                E.menu(E.href('/info'), E.color(u"blue"), E.name(u"справка")),
                E.menu(E.href('/auth'), E.color(u"blue"), E.name(u"выход")),
                E.link(E.href('/'), E.color(u"blue"), E.name(u"TASKPRODUCTION")),
                link='/hd'
                )

class main_page(template_base):
    cls__title = u"Главная"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('form1', '__form1__.xsl'),
        ('body', 'main.xsl'),
    ]
    cls__kwds = set(['common'])
    cls__externals = [
        '/js/main.js',
    ]
    user_id = 0
    inst = ' '
    class callback_form(form_base):
        fields = [
            field('status',  ''),
            field('date',  ''),
            field('title',  ''),
#            field_minmax('limit', minval=10, maxval=100),
#            field_minmax('offset'),
#            field_minmax('user_id'),
            field('limit', 10),
            field('offset', 0),
            field('user_id', 0),
        ]
        labels = {
            'status':u'по статусу',
            'date':u'по дате',
            'title':u'по названию',
            'limit':u'показывать',
        }
        ftypes = {
            'status':'select',
            'date':'date',
            'title':'select',
            'limit':'select',
        }
        def select_status(self, field):
            return E.options(
                     E.option(E.value(u""), u"--"),
                     E.option(E.value(u"открыто_открыто"), u"открыто_открыто"),
                     E.option(E.value(u"открыто_закрыто"), u"открыто_закрыто"),
                     E.option(E.value(u"закрыто_закрыто"), u"закрыто_закрыто"),
                    )
        def select_limit(self, field):
            return E.options(
                E.option(E.value(u"10"), u"10"),
                E.option(E.value(u"20"), u"20"),
                E.option(E.value(u"30"), u"30"),
                E.option(E.value(u"40"), u"40"),
                E.option(E.value(u"70"), u"70"),
                E.option(E.value(u"150"), u"150"),
            )
        def select_title(self, field):
            sess = self.req.environ['rrduet.sess']
            try:
                user_id = sess['id']
            except:
                return  E.options()
            options = []
            options.append(E.option(E.value(u""), u"--"))
            for r in self.template_ref().dbconn.query(Tasktype).filter(Tasktype.system_id == 1).order_by(Tasktype.name):
                options.append(E.option(E.value(str(r.id)), r.name))
            return E.options(*options)
    def user(self):
        sess = self.req.environ['rrduet.sess']
        try:
            self.user_id = sess['id']
        except:
            pass
    def comment(self):
        pass
    def E_data(self):
        self.user()
        self.comment()
        user_id = self.user_id
        dbconn = self.dbconn
        form = self.form
        limit = int(form['limit'])
        offset =  int(form['offset'])
        where = ''
        status = form['status']
        date = form['date']
        title = form['title']
        if status:
            where += ' and status="%s"' % status
        if title:
            where += ' and tasktype.id=%s' % str(title)
        if date:
             where += ' and creation_date = "%s"' % date
        query_perf = list(dbconn.execute("""select sql_calc_found_rows * from (
                select thread.id, id_global, id_local, creation_date, creation_time, fio, tasktype.name, status, importance, info
                    from thread join tasktype on thread.title_id = tasktype.id
                        join userprofile on thread.customer_id = userprofile.id
                    where performer_id=%s and tasktype.system_id =1 %s
                    order by status desc , creation_date desc , creation_time desc
            ) as p limit %d offset %d """ % (str(user_id),where, limit, offset)))
        count_p = list(dbconn.execute("select found_rows()"))[0][0]
        query_cust = list(dbconn.execute("""select sql_calc_found_rows * from (
                select thread.id, id_global, id_local, creation_date, creation_time, fio, tasktype.name, status, importance, info
                    from thread join tasktype on thread.title_id = tasktype.id
                        join userprofile on thread.performer_id = userprofile.id
                    where customer_id = %s and tasktype.system_id =1 %s
                    order by status desc , creation_date desc , creation_time desc
            ) as c limit %d offset %d """ % (str(user_id), where, limit, offset) ))
        count_c = list(dbconn.execute("select found_rows()"))[0][0]
        count  = max(count_p, count_c)
        page_tag = E.pages()
        if count%limit:
            res = count/limit + 1
        else:
            res = count/limit
        if (offset/limit+1) < 10 and res > 10 :
            for i in range(1, 11):
                page_tag.append(E.page(val=str(i), offset=str((i-1)*limit), limit=str(limit), action=str(int(offset/limit == i-1))))
                page_tag.append(E.next(val=u'...'))
        elif (offset/limit+1) <= 10 and res <= 10:
            for i in range(1, res + 1):
                page_tag.append(E.page(val=str(i), offset=str((i-1)*limit), limit=str(limit),  action=str(int(offset/limit == i-1))))
        elif (offset/limit+1) > 10 and (res - offset/limit) < 9:
            start = res + 1 - 10
            if start <= 0:
                start = 1
            page_tag.append(E.prev(val=u'...'))
            for i in range(start, res+1):
                page_tag.append(E.page(val=str(i), offset=str((i-1)*limit), limit=str(limit),  action=str(int(offset/limit == i-1))))
        else:
            page_tag.append(E.prev(val=u'...'))
            page_tag.append(E.next(val=u'...'))
            end  = min (offset/limit+7, res+1)
            for i in range(offset/limit-3, end):
                page_tag.append(E.page(val=str(i), offset=str((i-1)*limit), limit=str(limit),  action=str(int(offset/limit == i-1))))
        colors={u"открыто_открыто":"#B22222", u"закрыто_закрыто":"#27408B", u"открыто_закрыто":"green"}
        return E.data(
                E.inst(self.inst),
                E.form1(),
                E.perf(*[E.th(id=str(r[0]),
                            id_global=str(r[1]),
                            id_local=str(r[2]),
                            creation_date=str(r[3]),
                            creation_time=str(r[4]),
                            fio=r[5],
                            name=r[6],
                            status=r[7],
                            importance=r[8],
                            color = colors[r[7]],
                            css="white",
                            info=r[9]) for r in query_perf]
                            ),
                E.cust(*[E.th(id=str(r[0]),
                            id_global=str(r[1]),
                            id_local=str(r[2]),
                            creation_date=str(r[3]),
                            creation_time=str(r[4]),
                            fio=r[5],
                            name=r[6],
                            status=r[7],
                            importance=r[8],
                            color = colors[r[7]],
                            info=r[9]) for r in query_cust]),
                page_tag,
                status=status,
                date = date,
                title=title,
                limit = str(limit),
                user_id = str(form['user_id'])
                )
class main_page_hd(hd):
    cls__title = u"Главная"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('form1', '__form1__.xsl'),
        ('body', 'main_hd.xsl'),
    ]
    cls__kwds = set(['common'])
#    cls__kwds = set(['helpdesk'])
    cls__externals = [
        '/js/main.js',
    ]
    user_id = 0
    inst = u" "

    class callback_form(form_base):
        fields = [
            field('status',  ''),
            field('date',  ''),
            field('title',  ''),
            field('limit',  10),
            field('offset',  0),
            field('user_id',  0),
        ]
        labels = {
                'status':u'по статусу',
                'date':u'по дате',
                'title':u'по названию',
                'limit':u'показывать',
        }
        ftypes = {
            'status':'select',
            'date':'date',
            'title':'select',
            'limit':'select',
        }
        def select_status(self, field):
            return E.options(
                     E.option(E.value(u""), u"--"),
                     E.option(E.value(u"открыто_открыто"), u"открыто_открыто"),
                     E.option(E.value(u"открыто_закрыто"), u"открыто_закрыто"),
                     E.option(E.value(u"закрыто_закрыто"), u"закрыто_закрыто"),
                    )
        def select_limit(self, field):
            return E.options(
                E.option(E.value(u"10"), u"10"),
                E.option(E.value(u"20"), u"20"),
                E.option(E.value(u"30"), u"30"),
                E.option(E.value(u"40"), u"40"),
                E.option(E.value(u"70"), u"70"),
                E.option(E.value(u"150"), u"150"),
            )
        def select_title(self, field):
            sess = self.req.environ['rrduet.sess']
            try:
                user_id = sess['id']
            except:
                return  E.options()
            options = []
            options.append(E.option(E.value(u""), u"--"))
            for r in self.template_ref().dbconn.query(Tasktype).filter(Tasktype.system_id == 0).order_by(Tasktype.name):
                options.append(E.option(E.value(str(r.id)), r.name))
            return E.options(*options)
    def user(self):
        sess = self.req.environ['rrduet.sess']
        try:
            self.user_id = sess['id']
        except:
            pass
    def comment(self):
        if self.user_id == '30':
            self.inst = u'В конце смены Вы обязаны по всем открытым заданиям (со статусом "открыто_открыто") сформировать задачу "Передать задание о проблеме" и в качестве исполнителя выбрать деж. служба I уровня.'
    def E_data(self):
        self.user()
        self.comment()
        user_id = self.user_id
        dbconn = self.dbconn
        form = self.form
        limit = int(form['limit'])
        offset =  int(form['offset'])
        where = ''
        status = form['status']
        date = form['date']
        title = form['title']
        if status:
            where += ' and status="%s"' % status
        if title:
            where += ' and tasktype.id=%s' % str(title)
        if date:
             where += ' and creation_date = "%s"' % date
        query_perf = list(dbconn.execute("""select sql_calc_found_rows * from (
                select thread.id, id_global, id_local, creation_date, creation_time, fio, tasktype.name, status, importance, info
                    from thread join tasktype on thread.title_id = tasktype.id
                        join userprofile on thread.customer_id = userprofile.id
                    where performer_id=%s and tasktype.system_id =0 %s
                    order by status desc, creation_date desc, creation_time desc
            ) as p limit %d offset %d """ % (str(user_id),where, limit, offset)))
        count_p = list(dbconn.execute("select found_rows()"))[0][0]
        query_cust = list(dbconn.execute("""select sql_calc_found_rows * from (
                select thread.id, id_global, id_local, creation_date, creation_time, fio, tasktype.name, status, importance, info
                    from thread join tasktype on thread.title_id = tasktype.id
                        join userprofile on thread.performer_id = userprofile.id
                    where customer_id = %s and tasktype.system_id =0 %s
                    order by status desc, creation_date desc, creation_time desc
            ) as c limit %d offset %d """ % (str(user_id), where, limit, offset) ))
        count_c = list(dbconn.execute("select found_rows()"))[0][0]
        count  = max(count_p, count_c)
        page_tag = E.pages()
        if count%limit:
            res = count/limit + 1
        else:
            res = count/limit
        if (offset/limit + 1) < 10 and res > 10 :
            for i in range(1, 11):
                page_tag.append(E.page(val=str(i), offset=str((i - 1)*limit), limit=str(limit), action=str(int(offset/limit == i - 1))))
                page_tag.append(E.next(val=u'...'))
        elif (offset/limit + 1) <= 10 and res <= 10:
            for i in range(1, res + 1):
                page_tag.append(E.page(val=str(i), offset=str((i - 1)*limit), limit=str(limit),  action=str(int(offset/limit == i - 1))))
        elif (offset/limit + 1) > 10 and (res - offset/limit) < 9:
            start = res + 1 - 10
            if start <= 0:
                start = 1
            page_tag.append(E.prev(val=u'...'))
            for i in range(start, res + 1):
                page_tag.append(E.page(val=str(i), offset=str((i - 1)*limit), limit=str(limit),  action=str(int(offset/limit == i - 1))))
        else:
            page_tag.append(E.prev(val=u'...'))
            page_tag.append(E.next(val=u'...'))
            end  = min (offset/limit+7, res+1)
            for i in range(offset/limit-3, end):
                page_tag.append(E.page(val=str(i), offset=str((i - 1)*limit), limit=str(limit),  action=str(int(offset/limit == i - 1))))
        colors = {
            u"открыто_открыто":"#B22222",
            u"закрыто_закрыто":"#27408B",
            u"открыто_закрыто":"green",
            u"закрыто_закрыто":"green",
        }
        th = []
        for  r in query_perf:
            css = u"white"
            if r.status == u'открыто_открыто':
                ctm = str(r.creation_time).split(':')
                cdt = r.creation_date
                delta = datetime.datetime.now() - datetime.datetime(cdt.year, cdt.month, cdt.day, int(ctm[0]), int(ctm[1]), int(ctm[2]))
                if delta.days == 0 and delta.seconds > 3600 and delta.seconds < 3*3600 and r.id_local == 1:
                    css = '#FFC0CB'
                elif delta.seconds >= 3*3600 or delta.days > 0:
                    css = '#F5DEB3'
            try:
                th.append(E.th(
                    id=str(r[0]),
                    id_global=str(r[1]),
                    id_local=str(r[2]),
                    creation_date=str(r[3]),
                    creation_time=str(r[4]),
                    fio=r[5],
                    name=r[6],
                    status=r[7],
                    importance=r[8],
                    color=colors[r[7]],
                    info=r[9],
                    css=css,
                ))
            except ValueError:
                import pprint
                pprint.pprint({
                    'id':str(r[0]),
                    'id_global':str(r[1]),
                    'id_local':str(r[2]),
                    'creation_date':str(r[3]),
                    'creation_time':str(r[4]),
                    'fio':r[5],
                    'name':r[6],
                    'status':r[7],
                    'importance':r[8],
                    'color':colors[r[7]],
                    'info':r[9],
                    'css':css,
                })
        if 0:
            for i, d in enumerate(list(dict(
                    id=str(r[0]),
                    id_global=str(r[1]),
                    id_local=str(r[2]),
                    creation_date=str(r[3]),
                    creation_time=str(r[4]),
                    fio=r[5],
                    name=r[6],
                    status=r[7],
                    importance=r[8],
                    color=colors[r[7]],
                    info=r[9],
                ) for r in query_cust)):
                for k, v in d.items():
                    if type(v) not in (unicode, str) or chr(0) in v:
                        print repr((i, k, v, d))


        return E.data(
            E.inst(self.inst),
            E.form1(),
            E.perf(*th),
            E.cust(*[ E.th(
                id=str(r[0]),
                id_global=str(r[1]),
                id_local=str(r[2]),
                creation_date=str(r[3]),
                creation_time=str(r[4]),
                fio=r[5],
                name=r[6],
                status=r[7],
                importance=r[8],
                color=colors[r[7]],
                info=r[9]
            ) for r in query_cust ]),
            page_tag,
            status=status,
            date=date,
            title=title,
            limit=str(limit),
            user_id=str(form['user_id']),
        )
class threads(template_base):
    cls__title = u"Задания"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('form', '__form__.xsl'),
        ('body', 'threads.xsl'),
    ]
    cls__kwds = set(['common'])
    cls__externals = [
        '/js/thread.js',
        '/js/jquery.maskedinput-1.3.min.js',
    ]


    class callback_form(form_base):
#    id_global, id_local, created_by_id, deleted_by_id, creation_time, creation_date, deletion_time, category_id, customer_id, performer_id, finish_date, importance, status, title_id, message, info):
        fields = [
            field('performer', 0),
            field('performer_id', 0),
            field('importance', u"стандартное"),
            field('title_id', 0),
            field('message', ''),
            field('phone', ''),
            field('send', 0),
            field('sms', ''),
            field('action', ''),
        ]
        labels = {
                'performer':u'Исполнитель',
                'performer_id':u'',
                'importance':u'Важность',
                'title_id':u'Задание',
                'message':u"Текст задания",
                'phone': u"Номер абонента для отправки смс",
                'send': u"Отправить смс",
                'sms': u"Текст сообщения",
        }
        ftypes = {
            'performer':'select',
            'performer_id':'select',
            'importance':'select',
            'title_id':'select',
            'message':'textarea',
            'sms':'textarea',
            'send':'checkbox',
        }
        def select_performer(self, field):
            return E.options(
                     E.option(E.value(u""), u"--"),
                     E.option(E.value(u"2"), u"тех. отдел"),
                     E.option(E.value(u"3"), u"абон. отдел"),
                     E.option(E.value(u"4"), u"коммерч. отдел"),
                     E.option(E.value(u"1"), u"прочие"),
                    )
        def select_performer_id(self, field):
            return E.options()
        def select_importance(self, field):
            return E.options(
                     E.option(E.value(u"стандартное"), u"стандартное"),
                     E.option(E.value(u"низкой важности"), u"низкой важности"),
                     E.option(E.value(u"важное"), u"важное"),
                     E.option(E.value(u"особой важности"), u"особой важности"),
                    )
        def select_title_id(self, field):
            sess = self.req.environ['rrduet.sess']
            try:
                user_id = sess['id']
            except:
                return  E.options()
            options = []
            options.append(E.option(E.value(u""), u"--"))
            for r in self.template_ref().dbconn.query(Tasktype).filter(Tasktype.system_id == 1).filter(Tasktype.id == Taskuser.type_id).filter(Taskuser.user_id == user_id).order_by(Tasktype.weight, Tasktype.name):
                options.append(E.option(E.value(str(r.id)), r.name))
            return E.options(*options)
    def logic(self):
        sess = self.req.environ['rrduet.sess']
        try:
            user_id = sess['id']
            fio = sess['fio']
        except:
            return
        form = self.form
        dbconn = self.dbconn
        action = form['action']
        performer_id = form['performer_id']
        phone = form['phone'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        send = form['send']
        sms = form['sms']
        if int(send):
            if len(phone) != 10:
                self.errors.append(u"Формат телефона для отправки смс нарушен.")
                return
            if '--' in sms:
                self.errors.append(u"В сообщении символы -- замените на требуемое описание.")
                return
        try:
            performer_id = int(performer_id)
        except:
            performer_id = 0
        importance = form['importance']
        title_id = form['title_id']
        message = form['message']
        check = message.replace('$', '')
        if not action:
            form['action'] = 'check'
        if action == 'check':
            info = []
            if message:
                fs = list( dbconn.query(Taskfield).filter(Taskfield.id == Fields.field_id).filter(Fields.type_id == title_id).order_by(Taskfield.weight.desc()) )
                for r in fs:
                    if '$'+r.name+':$' not in message:
                        self.errors.append(u"Поле %s было повреждено" % r.name)
                    if r.weight > 0:
                        try:
                            end = check[(check.index(r.name)+len(r.name))+1:].split(':')[0]
                        except:
                            end = ''
                        for k in fs:
                            end = end.replace(k.name, '').replace('\n', '').replace('\r', '')
                        info.append(end)
            if performer_id and importance and title_id and message and not self.errors:
                now = datetime.datetime.now().strftime('%H:%M:%S')
                try:
                    fio_perf,email = dbconn.query(Userprofile.fio, Userprofile.email).filter(Userprofile.id == performer_id).one()
                except  sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    fio_perf = ''
                    email = 's.zimina@renet.ru'
                if int(send):
                    ret = agregator(sms, phone)
                else:
                    ret = ''
                th = Threads(0, 1, user_id, 0, now, datetime.date.today(), '0:0:0', 1, user_id, performer_id, '2050:01:01', importance, u"открыто_открыто", title_id, message.replace('\r', ''), ' '.join(info), fio, fio_perf, sms_text=sms, phone=phone, ret=ret)
                dbconn.add(th)
                try:
                    dbconn.commit()
                    self.results.append(u"Задание создано.")
                    max_id = int(list(dbconn.execute('select max(id_global) from thread'))[0][0])+1
                    ths =  dbconn.query(Threads).filter(Threads.id_global==0)
                    for t in ths:
                        t.id_global = max_id
                        max_id += 1
                    dbconn.commit()
                    fio_ = get_fio(th.message)
                    thread_sms = ThreadSms(th.id_global, phone, fio_)
                    dbconn.add(thread_sms)
                    dbconn.commit()
                    name = dbconn.query(Tasktype.name).filter(Tasktype.id == th.title_id).one()[0]
                    sendemail(email, th.id, th.message, name, link='') 
                except:
                    dbconn.rollback()
                    self.errors.append(u"Задание не создано.")
            else:
                self.errors.append(u"Не все поля были заполнены.")


    def E_data(self):
        sess = self.req.environ['rrduet.sess']
        try:
            user_id = sess['id']
        except:
            return E.data()
        form  = self.form
        dbconn = self.dbconn
        return E.data(*[E.th(
            E.message(t.message.replace('\r', '').replace('\n', '').replace(':$', ': ').replace('$', '\n').replace('*', '')),
            id=str(t.id),
            id_global=str(t.id_global),
            id_local=str(t.id_local),
            name=name,
            status=t.status,
            date=str(t.creation_date),
            time=str(t.creation_time),
            importance=t.importance,
            fio_perf=t.fio_perf,
            fio_cust=t.fio_cust
             ) for t, name in dbconn.query(Threads, Tasktype.name
                ).filter(Threads.id_local == 1
                ).filter(Threads.customer_id == user_id
                ).filter(Threads.status != u"закрыто_закрыто"
                ).filter(Tasktype.id == Threads.title_id
                ).filter(Tasktype.system_id == 1).order_by(Threads.id.desc())
                ],
            perf=str(form['performer_id']))
class threads_hd(hd):
    cls__title = u"Задания"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('form', '__form__.xsl'),
        ('body', 'threads.xsl'),
    ]
    cls__kwds = set(['common'])
    cls__externals = [
        '/js/thread.js',
        '/js/jquery.maskedinput-1.3.min.js',
    ]


    class callback_form(form_base):
        fields = [
            field('performer', 0),
            field('performer_id', 0),
            field('importance', u"стандартное"),
            field('title_id', 0),
            field('message', ''),
            field('phone', ''),
            field('send', 0),
            field('sms', ''),
            field('action', ''),
        ]
        labels = {
                'performer':u'Исполнитель',
                'performer_id':u'',
                'importance':u'Важность',
                'title_id':u'Задание',
                'message':u"Текст задания",
                'phone': u"Номер абонента для отправки смс",
                'send': u"Отправить смс",
                'sms': u"Текст сообщения",
        }
        ftypes = {
            'performer':'select',
            'performer_id':'select',
            'importance':'select',
            'title_id':'select',
            'message':'textarea',
            'sms':'textarea',
            'send':'checkbox',
        }
        def select_performer(self, field):
            return E.options(
                     E.option(E.value(u""), u"--"),
                     E.option(E.value(u"2"), u"тех. отдел"),
                     E.option(E.value(u"3"), u"абон. отдел"),
                     E.option(E.value(u"4"), u"коммерч. отдел"),
                     E.option(E.value(u"1"), u"прочие"),
                    )
        def select_performer_id(self, field):
            return E.options(*[E.option(E.value(str(r.id)), r.fio) for r in self.template_ref().dbconn.query(Userprofile).filter(Userprofile.system_id==1)])
        def select_importance(self, field):
            return E.options(
                     E.option(E.value(u"стандартное"), u"стандартное"),
                     E.option(E.value(u"низкой важности"), u"низкой важности"),
                     E.option(E.value(u"важное"), u"важное"),
                     E.option(E.value(u"особой важности"), u"особой важности"),
                    )
        def select_title_id(self, field):
            sess = self.req.environ['rrduet.sess']
            try:
                user_id = sess['id']
            except:
                return  E.options()
            options = []
            options.append(E.option(E.value(u""), u"--"))
            for r in self.template_ref().dbconn.query(Tasktype).filter(Tasktype.system_id == 0).filter(Tasktype.id == Taskuser.type_id).filter(Taskuser.user_id == user_id).order_by(Tasktype.name):
                options.append(E.option(E.value(str(r.id)), r.name))
            return E.options(*options)
            sess = self.req.environ['rrduet.sess']
            try:
                user_id = sess['id']
            except:
                return  E.options()
            options = []
            options.append(E.option(E.value(u""), u"--"))
            for r in self.template_ref().dbconn.query(Tasktype).filter(Tasktype.system_id == 0).filter(Tasktype.id == Taskuser.type_id).filter(Taskuser.user_id == user_id).order_by(Tasktype.name):
                options.append(E.option(E.value(str(r.id)), r.name))
            return E.options(*options)
    def logic(self):
        sess = self.req.environ['rrduet.sess']
        try:
            user_id = sess['id']
            fio = sess['fio']
        except:
            return
        form = self.form
        dbconn = self.dbconn
        action = form['action']
        performer_id = form['performer_id']
        phone = form['phone'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        send = form['send']
        sms = form['sms']
        if int(send):
            if len(phone) != 10:
                self.errors.append(u"Формат телефона для отправки смс нарушен.")
                return
            if '--' in sms:
                self.errors.append(u"В сообщении символы -- замените на требуемое описание.")
                return
        try:
            performer_id = int(performer_id)
        except:
            performer_id = 0
        importance = form['importance']
        title_id = form['title_id']
        message = form['message']
        check = message.replace('$', '')
        if not action:
            form['action'] = 'check'
            form['performer'] = '1'
            form['performer_id'] = 30
            form['title_id'] = 38


        if action == 'check':
            info = []
            if message:
                fs = list( dbconn.query(Taskfield).filter(Taskfield.id == Fields.field_id).filter(Fields.type_id == title_id).order_by(Taskfield.weight.desc()) )
                for r in fs:
                    if '$'+r.name+':$' not in message:
                        self.errors.append(u"Поле %s было повреждено" % r.name)
                    if r.weight > 0:
                        try:
                            end = check[(check.index(r.name)+len(r.name))+1:].split(':')[0]
                        except:
                            end = ''
                        for k in fs:
                            end = end.replace(k.name, '').replace('\n', '').replace('\r', '')
                        info.append(end)
            if performer_id and importance and title_id and message and not self.errors:
                now = datetime.datetime.now().strftime('%H:%M:%S')
                try:
                    fio_perf, email = dbconn.query(Userprofile.fio, Userprofile.email).filter(Userprofile.id == performer_id).one()
                except  sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    fio_perf = ''
                    email = ''
                th = Threads(0, 1, user_id, 0, now, datetime.date.today(), '0:0:0', 1, user_id, performer_id, '2050:01:01', importance, u"открыто_открыто", title_id, message.replace('\r', ''), ' '.join(info), fio, fio_perf, sms_text=sms, phone=phone, ret=str(send))
                dbconn.add(th)
                try:
                    dbconn.commit()
                    self.results.append(u"Задание создано.")
                    max_id = int(list(dbconn.execute('select max(id_global) from thread'))[0][0])+1
                    ths =  dbconn.query(Threads).filter(Threads.id_global==0)
                    for t in ths:
                        t.id_global = max_id
                        t.sms_text = t.sms_text.replace('HD_GLOB', str(max_id))
                        if int(t.ret):
                            ret = agregator(t.sms_text, t.phone)
                        else:
                            ret = ''
                        t.ret = ret
                        max_id += 1
                    dbconn.commit()
                    fio_ = get_fio(th.message)
                    thread_sms = ThreadSms(th.id_global, phone, fio_)
                    dbconn.add(thread_sms)
                    dbconn.commit()
                    name = dbconn.query(Tasktype.name).filter(Tasktype.id == th.title_id).one()[0]
                    sendemail(email, th.id, th.message, name, link='/hd')
                except:
                    dbconn.rollback()
                    self.errors.append(u"Задание не создано.")
            else:
                self.errors.append(u"Не все поля были заполнены.")


    def E_data(self):
        sess = self.req.environ['rrduet.sess']
        try:
            user_id = sess['id']
        except:
            return E.data()
        form  = self.form
        dbconn = self.dbconn
        ths = dbconn.query(Threads, Tasktype.name).filter(Threads.id_local == 1).filter(Threads.status != u"закрыто_закрыто").filter(Tasktype.id == Threads.title_id).filter(Tasktype.system_id ==0).filter(Threads.customer_id == Userprofile.id)
        if int(user_id) == 29:
            ths = ths.filter(Userprofile.system_id != 4)
        else:
            ths = ths.filter(Threads.customer_id == user_id)
        ths = ths.order_by(Threads.id.desc())
        return E.data(*[E.th(
            E.message(t.message.replace('\r', '').replace('\n', '').replace(':$', ': ').replace('$', '\n').replace('*', '')),
            id=str(t.id),
            id_global=str(t.id_global),
            id_local=str(t.id_local),
            name=name,
            status=t.status,
            date=str(t.creation_date),
            time=str(t.creation_time),
            importance=t.importance,
            fio_perf=t.fio_perf,
            fio_cust=t.fio_cust,
             ) for t, name in ths ],
            perf=str(form['performer_id']))
class thread(template_base):
    cls__title = u"Задание"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('form', '__form__.xsl'),
        ('body', 'thread.xsl'),
    ]
    cls__kwds = set(['common'])
    cls__externals = [
        '/js/thread.js',
        '/js/jquery.maskedinput-1.3.min.js',
    ]


    class callback_form(form_base):
        fields = [
            field('performer', 0),
            field('performer_id', 0),
            field('id', 0),
            field('importance', u"стандартное"),
            field('title_id', 0),
            field('message', ''),
            field('phone', ''),
            field('send', 0),
            field('sms', ''),
            field('action', ''),
        ]
        labels = {
                'performer':u'Исполнитель',
                'performer_id':u'',
                'importance':u'Важность',
                'title_id':u'Задание',
                'message':u"Текст задания",
                'phone': u"Номер абонента для отправки смс",
                'send': u"Отправить смс",
                'sms': u"Текст сообщения",
        }
        ftypes = {
            'performer':'select',
            'performer_id':'select',
            'importance':'select',
            'title_id':'select',
            'message':'textarea',
            'sms':'textarea',
            'send':'checkbox',
        }
        def select_performer(self, field):
            return E.options(
                     E.option(E.value(u""), u"--"),
                     E.option(E.value(u"2"), u"тех. отдел"),
                     E.option(E.value(u"3"), u"абон. отдел"),
                     E.option(E.value(u"4"), u"коммерч. отдел"),
                     E.option(E.value(u"1"), u"прочие"),
                    )
        def select_performer_id(self, field):
            return E.options()
        def select_importance(self, field):
            return E.options(
                     E.option(E.value(u"стандартное"), u"стандартное"),
                     E.option(E.value(u"низкой важности"), u"низкой важности"),
                     E.option(E.value(u"важное"), u"важное"),
                     E.option(E.value(u"особой важности"), u"особой важности"),
                    )
        def select_title_id(self, field):
            sess = self.req.environ['rrduet.sess']
            try:
                user_id = sess['id']
            except:
                return  E.options()
            options = []
            options.append(E.option(E.value(u""), u"--"))
            for r in self.template_ref().dbconn.query(Tasktype).filter(Tasktype.system_id == 1).filter(Tasktype.id == Taskuser.type_id).filter(Taskuser.user_id == user_id).order_by(Tasktype.weight, Tasktype.name):
                options.append(E.option(E.value(str(r.id)), r.name))
            return E.options(*options)
    def logic(self):
        sess = self.req.environ['rrduet.sess']
        try:
            user_id = sess['id']
            fio = sess['fio']
        except:
            return
        form = self.form
        dbconn = self.dbconn
        action = form['action']
        thread_id = form['id']
        try:
            th_sms = dbconn.query(ThreadSms).filter(Threads.id == thread_id).filter(ThreadSms.id_global == Threads.id_global).one()
            if not form['phone']:
                form['phone'] = th_sms.phone
        except:
            pass
        performer_id = form['performer_id']
        try:
            performer_id = int(performer_id)
        except:
            performer_id = 0
        importance = form['importance']
        title_id = form['title_id']
        message = form['message']
        phone = form['phone'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        send = form['send']
        sms = form['sms']
        if not action:
            form['action'] = 'check'
        thread_id = max(self.req.POST.get('id'), self.req.GET.get('id'))
        form['id'] = thread_id
        if int(send):
            if len(phone) != 10:
                self.errors.append(u"Формат телефона для отправки смс нарушен.")
                return
            if '--' in sms:
                self.errors.append(u"В сообщении символы -- замените на требуемое описание.")
                return
        if action == 'check':
            info =[] 
            if message:
                fs = list( dbconn.query(Taskfield).filter(Taskfield.id == Fields.field_id).filter(Fields.type_id == title_id).order_by(Taskfield.weight.desc()) )
                for r in fs:
                    if '$'+r.name+':$' not in message:
                        self.errors.append(u"Поле %s было повреждено" % r.name)
            if performer_id and importance and title_id and message and not self.errors:
                now = datetime.datetime.now().strftime('%H:%M:%S')
                try:
                    fio_perf, email = dbconn.query(Userprofile.fio, Userprofile.email).filter(Userprofile.id == performer_id).one()
                except  sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    fio_perf = ''
                    email = ''
                try:
                   thread = dbconn.query(Threads).filter(Threads.id == thread_id).one()
                   glob = thread.id_global
                   local = thread.id_local+1
                   info = thread.info
                   if not (thread.performer_id == int(user_id) and thread.status == u"открыто_открыто"):
                       self.errors.append(u"Вы не можете отвечать на это задание.")
                       return
                except sqlalchemy.orm.exc.NoResultFound:
                   sys.exc_clear()
                if int(send):
                    ret = agregator(sms, phone)
                else:
                    ret = ''
                th = Threads(glob, local, user_id, 0, now, datetime.date.today(), '0:0:0', 1, user_id, performer_id, '2050:01:01', importance, u"открыто_открыто", title_id, message.replace('\r', ''), info, fio, fio_perf, sms_text=sms, phone=phone, ret=ret)
                dbconn.add(th)
                try:
                    dbconn.commit()
                    dbconn.execute('update thread set status="%s" where id_global=%s and id_local<%s' % (u"открыто_закрыто", str(glob), str(local)))
                    self.results.append(u"Задание создано.")
                    name = dbconn.query(Tasktype.name).filter(Tasktype.id == th.title_id).one()[0]
                    sendemail(email, th.id, th.message, name, link='')
                except:
                    dbconn.rollback()
                    self.errors.append(u"Задание не создано.")
            else:
                self.errors.append(u"Не все поля были заполнены.")


    def E_data(self):
        sess = self.req.environ['rrduet.sess']
        try:
            user_id = sess['id']
        except:
            return E.data()
        form  = self.form
        dbconn = self.dbconn
        thread_id = form['id']
        do = 0
        glob = 0
        inst = ''
        try:
           thread = dbconn.query(Threads).filter(Threads.id == thread_id).one()
           glob = thread.id_global
           do = 1
           inst =  dbconn.query(Instruction.instruct).filter(Threads.id == thread_id).filter(Threads.title_id == Instruction.type_task_id).one()[0]
        except sqlalchemy.orm.exc.NoResultFound:
           sys.exc_clear()
        if do:
            if not (thread.performer_id == int(user_id) and thread.status == u"открыто_открыто"):
                do = 0
        data = E.data(*[E.th(
            E.message(t.message.replace('\r', '').replace('\n', '').replace(':$', ': ').replace('$', '\n').replace('*', '')),
            E.sms(t.sms_text),
            E.phone(t.phone),
            E.ret(t.ret),
            id=str(t.id),
            id_global=str(t.id_global),
            id_local=str(t.id_local),
            name=name,
            status=t.status,
            date=str(t.creation_date),
            time=str(t.creation_time),
            importance=t.importance,
            fio_perf=t.fio_perf,
            fio_cust=t.fio_cust,
             ) for t, name in dbconn.query(Threads, Tasktype.name
                ).filter(Threads.id_global == glob
                ).filter(Tasktype.id == Threads.title_id).order_by(Threads.id)
                ],
            do = str(do),
            glob = str(glob),
            thread_id = str(thread_id),
            perf=str(form['performer_id']))
        data.append( E.inst(inst))
        return data

class thread_hd(hd):
    cls__title = u"Задание"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('form', '__form__.xsl'),
        ('body', 'thread.xsl'),
    ]
    cls__kwds = set(['common'])
    cls__externals = [
        '/js/thread.js',
        '/js/jquery.maskedinput-1.3.min.js',
    ]


    class callback_form(form_base):
        fields = [
            field('performer', 0),
            field('performer_id', 0),
            field('id', 0),
            field('importance', u"стандартное"),
            field('title_id', 0),
            field('message', ''),
            field('phone', ''),
            field('send', 0),
            field('sms', ''),
            field('action', ''),
        ]
        labels = {
                'performer':u'Исполнитель',
                'performer_id':u'',
                'importance':u'Важность',
                'title_id':u'Задание',
                'message':u"Текст задания",
                'phone': u"Номер абонента для отправки смс",
                'send': u"Отправить смс",
                'sms': u"Текст сообщения",
        }
        ftypes = {
            'performer':'select',
            'performer_id':'select',
            'importance':'select',
            'title_id':'select',
            'message':'textarea',
            'sms':'textarea',
            'send':'checkbox',
        }
        def select_performer(self, field):
            return E.options(
                     E.option(E.value(u""), u"--"),
                     E.option(E.value(u"2"), u"тех. отдел"),
                     E.option(E.value(u"3"), u"абон. отдел"),
                     E.option(E.value(u"4"), u"коммерч. отдел"),
                     E.option(E.value(u"1"), u"прочие"),
                    )
        def select_performer_id(self, field):
            return E.options()
        def select_importance(self, field):
            return E.options(
                     E.option(E.value(u"стандартное"), u"стандартное"),
                     E.option(E.value(u"низкой важности"), u"низкой важности"),
                     E.option(E.value(u"важное"), u"важное"),
                     E.option(E.value(u"особой важности"), u"особой важности"),
                    )
        def select_title_id(self, field):
            sess = self.req.environ['rrduet.sess']
            try:
                user_id = sess['id']
            except:
                return  E.options()
            options = []
            options.append(E.option(E.value(u""), u"--"))
            for r in self.template_ref().dbconn.query(Tasktype).filter(Tasktype.system_id == 0).filter(Tasktype.id == Taskuser.type_id).filter(Taskuser.user_id == user_id).order_by(Tasktype.name):
                options.append(E.option(E.value(str(r.id)), r.name))
            return E.options(*options)
    def logic(self):
        sess = self.req.environ['rrduet.sess']
        try:
            user_id = sess['id']
            fio = sess['fio']
        except:
            return
        form = self.form
        dbconn = self.dbconn
        action = form['action']
        thread_id = form['id']
        try:
            th_sms = dbconn.query(ThreadSms).filter(Threads.id == thread_id).filter(ThreadSms.id_global == Threads.id_global).one()
            if not form['phone']:
                form['phone'] = th_sms.phone
        except:
            pass
        performer_id = form['performer_id']
        phone = form['phone'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        send = form['send']
        sms = form['sms']
        try:
            performer_id = int(performer_id)
        except:
            performer_id = 0
        importance = form['importance']
        title_id = form['title_id']
        message = form['message']
        if not action:
            form['action'] = 'check'
        thread_id = max(self.req.POST.get('id'), self.req.GET.get('id'))
        form['id'] = thread_id
        if int(send):
            if len(phone) != 10:
                self.errors.append(u"Формат телефона для отправки смс нарушен.")
                return
            if '--' in sms:
                self.errors.append(u"В сообщении символы -- замените на требуемое описание.")
                return
        if action == 'check':
            info =[] 
            if message:
                fs = list( dbconn.query(Taskfield).filter(Taskfield.id == Fields.field_id).filter(Fields.type_id == title_id).order_by(Taskfield.weight.desc()) )
                for r in fs:
                    if '$'+r.name+':$' not in message:
                        self.errors.append(u"Поле %s было повреждено" % r.name)
            if performer_id and importance and title_id and message and not self.errors:
                now = datetime.datetime.now().strftime('%H:%M:%S')
                try:
                    fio_perf, email = dbconn.query(Userprofile.fio, Userprofile.email).filter(Userprofile.id == performer_id).one()
                except  sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    fio_perf = ''
                    email = ''
                try:
                   thread = dbconn.query(Threads).filter(Threads.id == thread_id).one()
                   glob = thread.id_global
                   local = thread.id_local+1
                   info = thread.info
                   if not (thread.performer_id == int(user_id) and thread.status == u"открыто_открыто"):
                       self.errors.append(u"Вы не можете отвечать на это задание.")
                       return
                except sqlalchemy.orm.exc.NoResultFound:
                   sys.exc_clear()
                if int(send):
                    ret = agregator(sms, phone)
                else:
                    ret = ''
                th = Threads(glob, local, user_id, 0, now, datetime.date.today(), '0:0:0', 1, user_id, performer_id, '2050:01:01', importance, u"открыто_открыто", title_id, message.replace('\r', ''), info, fio, fio_perf, sms_text=sms, phone=phone, ret=ret)
                dbconn.add(th)
                try:
                    dbconn.commit()
                    dbconn.execute('update thread set status="%s" where id_global=%s and id_local<%s' % (u"открыто_закрыто", str(glob), str(local)))
                    self.results.append(u"Задание создано.")
                    answer_time = datetime.datetime.now().strftime('%H:%M:%S')
                    answer_date = datetime.datetime.now().strftime('%Y-%m-%d')
                    dbconn.execute('update expired_task set answer_time="%s", answer_date="%s" '
                                   'where id_task=%s' % (answer_time, answer_date, thread_id))
                    name = dbconn.query(Tasktype.name).filter(Tasktype.id == th.title_id).one()[0]
                    sendemail(email, th.id, th.message, name, link='/hd')
                except:
                    dbconn.rollback()
                    self.errors.append(u"Задание не создано.")
            else:
                self.errors.append(u"Не все поля были заполнены.")


    def E_data(self):
        sess = self.req.environ['rrduet.sess']
        try:
            user_id = sess['id']
        except:
            return E.data()
        form  = self.form
        dbconn = self.dbconn
        thread_id = form['id']
        do = 0
        glob = 0
        inst = ''
        try:
           thread = dbconn.query(Threads).filter(Threads.id == thread_id).one()
           glob = thread.id_global
           do = 1
           inst =  dbconn.query(Instruction.instruct).filter(Threads.id == thread_id).filter(Threads.title_id == Instruction.type_task_id).one()[0]
        except sqlalchemy.orm.exc.NoResultFound:
           sys.exc_clear()
        if do:
            if not (thread.performer_id == int(user_id) and thread.status == u"открыто_открыто"):
                do = 0
        data = E.data(*[E.th(
            E.message(t.message.replace('\r', '').replace('\n', '').replace(':$', ': ').replace('$', '\n').replace('*', '')),
            E.sms(t.sms_text),
            E.phone(t.phone),
            E.ret(t.ret),
            id=str(t.id),
            id_global=str(t.id_global),
            id_local=str(t.id_local),
            name=name,
            status=t.status,
            date=str(t.creation_date),
            time=str(t.creation_time),
            importance=t.importance,
            fio_perf=t.fio_perf,
            fio_cust=t.fio_cust,
             ) for t, name in dbconn.query(Threads, Tasktype.name
                ).filter(Threads.id_global == glob
                ).filter(Tasktype.id == Threads.title_id).order_by(Threads.id)
                ],
            do = str(do),
            glob = str(glob),
            thread_id = str(thread_id),
            perf=str(form['performer_id']))
        data.append( E.inst(inst))
        return data
class close(template_base):
    cls__xsllist = [
        ('', '__root__.xsl'),
    ]
    cls__kwds = set(['common'])

    class callback_form(form_base):
        fields = [
            field('path',  ''),
            field('id',  0),
            ]
    def logic(self):
        form = self.form
        glob = form['id']
        path = form['path']
        sess = self.req.environ['rrduet.sess']
        try:
            user_id = sess['id']
            fio = sess['fio']
        except:
            user_id = 0
        dbconn = self.dbconn
        do = False
        try:
            thread = dbconn.query(Threads).filter(Threads.id_global == int(glob)).filter(Threads.id_local == 1).one()
            if int(user_id) in[thread.customer_id , 29 , 77] and thread.status != u'закрыто_закрыто':
                do = True
        except  sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
        if do:
            threads =  dbconn.query(Threads).filter(Threads.id_global == int(glob))
            for t in threads:
                t.status = u"закрыто_закрыто"
                t.message += '\n'+u"$Задание было закрыто:$"+fio+' '+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                t.closed_by_id = user_id
                t.close_time = datetime.datetime.now().strftime('%H:%M:%S')
                t.close_date = datetime.datetime.now().strftime('%Y-%m-%d')
            dbconn.commit()
            answer_time = datetime.datetime.now().strftime('%H:%M:%S')
            answer_date = datetime.datetime.now().strftime('%Y-%m-%d')
            dbconn.execute('update expired_task set answer_time="%s", answer_date="%s" '
                           'where id_global=%s and answer_date is null' % (answer_time, answer_date, glob))
        self.resp.location = path
        self.resp.status_int = 302
        self.resp.body = ''
class glob(template_base):
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'thread.xsl'),
    ]
    cls__kwds = set(['common'])
    cls__externals = [
        '/js/thread.js',
        '/js/jquery.maskedinput-1.3.min.js',
    ]


    class callback_form(form_base):
        fields = [
            field('id', 0),
        ]
    def logic(self):
        self.title = u"Задания %s" % str(self.form['id'])
    def E_data(self):
        form  = self.form
        dbconn = self.dbconn
        glob = form['id']
        data = E.data(*[E.th(
            E.message(t.message.replace('\r', '').replace('\n', '').replace(':$', ': ').replace('$', '\n').replace('*', '')),
            E.sms(t.sms_text),
            E.phone(t.phone),
            E.ret(t.ret),
            id=str(t.id),
            id_global=str(t.id_global),
            id_local=str(t.id_local),
            name=name,
            status=t.status,
            date=str(t.creation_date),
            time=str(t.creation_time),
            importance=t.importance,
            fio_perf=t.fio_perf,
            fio_cust=t.fio_cust,
             ) for t, name in dbconn.query(Threads, Tasktype.name
                ).filter(Threads.id_global == glob
                ).filter(Tasktype.id == Threads.title_id).order_by(Threads.id)
                ],
            glob = str(glob),
            thread_id = str(glob))
        return data
class glob_hd(hd):
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'thread.xsl'),
    ]
    cls__kwds = set(['common'])
    cls__externals = [
        '/js/thread.js',
        '/js/jquery.maskedinput-1.3.min.js',
    ]


    class callback_form(form_base):
        fields = [
            field('id', 0),
        ]
    def logic(self):
        self.title = u"Задания %s" % str(self.form['id'])
    def E_data(self):
        form  = self.form
        dbconn = self.dbconn
        glob = form['id']
        data = E.data(*[E.th(
            E.message(t.message.replace('\r', '').replace('\n', '').replace(':$', ': ').replace('$', '\n').replace('*', '')),
            E.sms(t.sms_text),
            E.phone(t.phone),
            E.ret(t.ret),
            id=str(t.id),
            id_global=str(t.id_global),
            id_local=str(t.id_local),
            name=name,
            status=t.status,
            date=str(t.creation_date),
            time=str(t.creation_time),
            importance=t.importance,
            fio_perf=t.fio_perf,
            fio_cust=t.fio_cust,
             ) for t, name in dbconn.query(Threads, Tasktype.name
                ).filter(Threads.id_global == glob
                ).filter(Tasktype.id == Threads.title_id).order_by(Threads.id)
                ],
            glob = str(glob),
            thread_id = str(glob))
        return data
class passwd(template_base):
    cls__kwds = set([ 'common' ])
    cls__title = u"Изменение пароля пользователя"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', '__form__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('secret_old', ''),
            field('secret_new', ''),
            field('secret_repeat', ''),
            field('action', ''),
        ]
        labels = {
            'secret_old': u"Старый пароль",
            'secret_new': u"Новый пароль",
            'secret_repeat': u"Повтор пароля",
        }
        ftypes = {
            'secret_old': 'password',
            'secret_new': 'password',
            'secret_repeat': 'password',
        }
    def logic(self):
        form = self.form
        action = form['action']
        form['action'] = 'update'

        secret_old = form['secret_old']
        secret_new = form['secret_new']
        secret_repeat = form['secret_repeat']
        form['secret_old'] = form['secret_new'] = form['secret_repeat'] = ''

        if action == '':
            return

        if secret_new == '':
            self.errors.append(u"Пароль не может быть нулевым")
        elif len(secret_new) < 6:
            self.errors.append(u"Пароль не может быть короче %d символов" % (hta_config.secret_minlength,))
        if secret_new != secret_repeat:
            self.errors.append(u"Неправильное подтверждение пароля")

        if self.errors:
            return

        sess = self.environ['rrduet.sess']
        user_id = sess.get('id')
        if user_id is None:
            self.errors.append(u"Ошибка данных в струкутре сессии")
            return
        dbconn = self.dbconn
        try:
            user = dbconn.query(Userprofile).filter(Userprofile.id == user_id).one()
        except sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
            self.errors.append(u"Данные в сессии устарели, необходимо перерегестрироваться")
            return
        if user.password != secret_old:
            self.errors.append(u"Предоставленный пароль не совпадает с заданным в базе данных")
            return
        user.password = secret_new
        dbconn.commit()
        self.results.append(u"Пароль был успешно изменен")

class info(template_base):
    cls__kwds = set([ 'common' ])
    cls__title = u"Справка"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'info.xsl'),
    ]

class search(template_base):
    cls__kwds = set([ 'common' ])
    cls__title = u"Поиск"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('form1', '__form1__.xsl'),
        ('body', 'search.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('message',  ''),
            field('title',  ''),
            field('field',  ''),
            field('date',  ''),
            field('glob', 0, int, (ValueError,)),
            field('offset', 0, int, (ValueError,)),
        ]
        labels = {
            'message':u'по тексту',
            'date':u'по дате',
            'title':u'по типу',
            'field':u'по полю',
            'glob':u"по номеру",
        }
        ftypes = {
            'field':'select',
            'date':'date',
            'title':'select',
        }
        def select_title(self, field):
            options = []
            options.append(E.option(E.value(u""), u"--"))
            for r in self.template_ref().dbconn.query(Tasktype).filter(Tasktype.system_id == 1).filter(Tasktype.id.in_(ts)):
                options.append(E.option(E.value(str(r.id)), r.name))
            return E.options(*options)
        def select_field(self, field):
            options = []
            options.append(E.option(E.value(u""), u"--"))
            for r in self.template_ref().dbconn.query(Taskfield).filter(~ Taskfield.id.in_(fs)):
                options.append(E.option(E.value(str(r.id)), r.name))
            return E.options(*options)
    def query_(self):
        form = self.form
        dbconn = self.dbconn
        message = form['message'].strip().replace('/', '_').replace(u'ё', u'е').replace(u'Ё', u'е')
        title = form['title']
        field = form['field']
        date = form['date'].replace('-', '_')
        glob = form['glob']
        offset = form['offset']
        query = None
        try:
            offset = int(offset)
        except:
            offset = 0
        limit = 50
        count = 0
        try:
            glob = int(glob)
        except:
            glob = 0
        if glob:
            query = dbconn.query(Threads, Tasktype.name).filter(
                    Threads.id_global == glob).filter(
                    Tasktype.id == Threads.title_id).filter(
                    Tasktype.system_id == 1).order_by(Threads.id)
        elif date or title or field or message:
            fulltext = ''
            if date:
                fulltext += ' @dt %s' % (date,)
            if title:
                fulltext += ' @task ^%s$' % (title,)
            if field:
                fulltext += ' @tag%s ' % (field,)
            if message:
                message = message.replace(' ', '*')
                if field:
                    fulltext += ' *%s* ' % (message,)
                else:
                    fulltext += '@* *%s* ' % (message,)
            mode = SPH_MATCH_EXTENDED2
            cl = SphinxClient()
            cl._limit = 100000
            cl.SetLimits ( 0, 100000, max(100000,1000) )
            host = 'localhost'
            port = 9312
            cl.SetServer ( host, port )
            cl.SetWeights ( [1000, 1] )
            cl.SetMatchMode ( mode )
            rs = []
            res = cl.Query('@sys ^1$ ' + fulltext)
            #print fulltext
            if res is not None and res.has_key('matches'):
                for match in res['matches']:
                    rs.append(match['id'])
            rs.sort()
            rs = [ r for r in rs ]
            ths = []
            if rs:
                count = len(rs)
                query = dbconn.query(Threads, Tasktype.name).filter(
                    Threads.id.in_(rs)
                ).filter(
                    Tasktype.id == Threads.title_id
                ).filter(
                    Tasktype.system_id == 1
                ).order_by(Threads.id.desc()).limit(limit).offset(offset)
            else:
                query = []
        d = {
            'message': form['message'],
            'title': str(form['title']),
            'field': str(form['field']),
            'date': form['date']
        }
        return (query, count, limit, d)
    def E_data(self):
        offset = self.form['offset']
        try:
            offset = int(offset)
        except:
            offset = 0
        page_tag = E.pages()
        query, count, limit, d = self.query_()
        ths = []
        if query is not None:
            ths = [
                E.th(
                    E.message(
                        t.message.replace('\r', '').replace('\n', '').replace(':$', ': ').replace('$', '\n').replace('*', '')
                    ),
                    id=str(t.id),
                    id_global=str(t.id_global),
                    id_local=str(t.id_local),
                    name=name,
                    status=t.status,
                    date=str(t.creation_date),
                    time=str(t.creation_time),
                    importance=t.importance,
                    fio_perf=t.fio_perf,
                    fio_cust=t.fio_cust,
                ) for t, name in query ]
        if count%limit:
            res = count/limit + 1
        else:
            res = count/limit
        if (offset/limit+1) < 10 and res > 10 :
            for i in range(1, 11):
                page_tag.append(E.page(val=str(i), offset=str((i-1)*limit), limit=str(limit), action=str(int(offset/limit == i-1))))
                page_tag.append(E.next(val=u'...'))
        elif (offset/limit+1) <= 10 and res <= 10:
            for i in range(1, res + 1):
                page_tag.append(E.page(val=str(i), offset=str((i-1)*limit), limit=str(limit),  action=str(int(offset/limit == i-1))))
        elif (offset/limit+1) > 10 and (res - offset/limit) < 9:
            start = res + 1 - 10
            if start <= 0:
                start = 1
            page_tag.append(E.prev(val=u'...'))
            for i in range(start, res+1):
                page_tag.append(E.page(val=str(i), offset=str((i-1)*limit), limit=str(limit),  action=str(int(offset/limit == i-1))))
        else:
            page_tag.append(E.prev(val=u'...'))
            page_tag.append(E.next(val=u'...'))
            end  = min (offset/limit+7, res+1)
            for i in range(offset/limit-3, end):
                page_tag.append(E.page(val=str(i), offset=str((i-1)*limit), limit=str(limit),  action=str(int(offset/limit == i-1))))
        data = E.data(*ths, offset=str(self.form['offset']))
        for k in d:
            data.set(k, d[k])
        data.append(E.form1())
        data.append(page_tag)
        return data
class search_hd(hd):
    cls__kwds = set([ 'common' ])
    cls__title = u"Поиск"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('form1', '__form1__.xsl'),
        ('body', 'search.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('message',  ''),
            field('title',  ''),
            field('field',  ''),
            field('date',  ''),
            field('glob',  0),
            field('offset',  0),
        ]
        labels = {
                'message':u'по тексту',
                'date':u'по дате',
                'title':u'по типу',
                'field':u'по полю',
                'glob':u"по номеру",
        }
        ftypes = {
            'field':'select',
            'date':'date',
            'title':'select',
        }
        def select_title(self, field):
            options = []
            options.append(E.option(E.value(u""), u"--"))
            for r in self.template_ref().dbconn.query(Tasktype).filter(Tasktype.system_id == 0).filter(Tasktype.id.in_(ts)):
                options.append(E.option(E.value(str(r.id)), r.name))
            return E.options(*options)
        def select_field(self, field):
            options = []
            options.append(E.option(E.value(u""), u"--"))
            for r in self.template_ref().dbconn.query(Taskfield).filter(~ Taskfield.id.in_(fs)):
                options.append(E.option(E.value(str(r.id)), r.name))
            return E.options(*options)
    def query_(self):
        form = self.form
        dbconn = self.dbconn
        message = form['message'].strip().replace('/', '_').replace(u'ё', u'е').replace(u'Ё', u'е')
        title = form['title']
        field = form['field']
        date = form['date'].replace('-', '_')
        glob = form['glob']
        offset = form['offset']
        query = None
        try:
            offset = int(offset)
        except:
            offset = 0
        limit = 50
        count = 0
        try:
            glob = int(glob)
        except:
            glob = 0
        if glob:
            query = dbconn.query(Threads, Tasktype.name).filter(
                    Threads.id_global == glob).filter(
                    Tasktype.id == Threads.title_id).filter(
                    Tasktype.system_id == 0).order_by(Threads.id)
        elif date or title or field or message:
            query = ''

            if date:
                query += ' @dt %s' % (date,)
            if title:
                query += ' @task ^%s$' % (title,)
            if field:
                query += ' @tag%s ' % (field,)
            if message:
                if field:
                    query += ' *%s* ' % (message,)
                else:
                    query += '@* *%s* ' % (message,)
            mode = SPH_MATCH_EXTENDED2
            cl = SphinxClient()
            cl._limit = 100000
            cl.SetLimits ( 0, 100000, max(100000,1000) )
            host = 'localhost'
            port = 9312
            cl.SetServer ( host, port )
            cl.SetWeights ( [1000, 1] )
            cl.SetMatchMode ( mode )
            rs = []
            res = cl.Query('@sys ^0$ '+query)
            if res is not None and res.has_key('matches'):
                for match in res['matches']:
                    rs.append(match['id'])
            rs.sort()
            rs = [r for r in rs]
            ths = []
            query = []
            if rs:
                count = len(rs)
                query = dbconn.query(Threads, Tasktype.name).filter(
                        Threads.id.in_(rs)).filter(
                        Tasktype.id == Threads.title_id).filter(
                        Tasktype.system_id == 0).order_by(Threads.id.desc()).limit(limit).offset(offset)
        d = {'message':form['message'], 'title':str(form['title']), 'field': str(form['field']), 'date':form['date']}
        return (query, count, limit, d)
    def E_data(self):
        offset = self.form['offset']
        try:
            offset = int(offset)
        except:
            offset = 0
        page_tag = E.pages()
        query, count, limit, d = self.query_()
        ths = []
        if query is not None:
            ths = [E.th(
                E.message(t.message.replace('\r', '').replace('\n', '').replace(':$', ': ').replace('$', '\n').replace('*', '')),
                id=str(t.id),
                id_global=str(t.id_global),
                id_local=str(t.id_local),
                name=name,
                status=t.status,
                date=str(t.creation_date),
                time=str(t.creation_time),
                importance=t.importance,
                fio_perf=t.fio_perf,
                fio_cust=t.fio_cust,
                ) for t, name in query]
        if count%limit:
            res = count/limit + 1
        else:
            res = count/limit
        if (offset/limit+1) < 10 and res > 10 :
            for i in range(1, 11):
                page_tag.append(E.page(val=str(i), offset=str((i-1)*limit), limit=str(limit), action=str(int(offset/limit == i-1))))
                page_tag.append(E.next(val=u'...'))
        elif (offset/limit+1) <= 10 and res <= 10:
            for i in range(1, res + 1):
                page_tag.append(E.page(val=str(i), offset=str((i-1)*limit), limit=str(limit),  action=str(int(offset/limit == i-1))))
        elif (offset/limit+1) > 10 and (res - offset/limit) < 9:
            start = res + 1 - 10
            if start <= 0:
                start = 1
            page_tag.append(E.prev(val=u'...'))
            for i in range(start, res+1):
                page_tag.append(E.page(val=str(i), offset=str((i-1)*limit), limit=str(limit),  action=str(int(offset/limit == i-1))))
        else:
            page_tag.append(E.prev(val=u'...'))
            page_tag.append(E.next(val=u'...'))
            end  = min (offset/limit+7, res+1)
            for i in range(offset/limit-3, end):
                page_tag.append(E.page(val=str(i), offset=str((i-1)*limit), limit=str(limit),  action=str(int(offset/limit == i-1))))
        data = E.data(*ths, offset=str(self.form['offset']))
        for k in d:
            data.set(k, d[k])
        data.append(E.form1())
        data.append(page_tag)
        return data
class reports(template_base):
    cls__kwds = set([ 'reports' ])
    cls__title = u"Отчеты"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'reports.xsl'),
    ]
    def E_data(self):
        sess = self.req.environ['rrduet.sess']
        try:
            user_id = sess['id']
        except:
            return  E.data()
        return E.data(*[
            E.report(name=r.name, link=r.link) for r in self.dbconn.query(Report).filter(
                Admin_operkw.group_kw.like('%'+Report.link+'%')).filter(
                Admin_operkw.oper_id ==user_id).filter(
                Admin_operkw.group_include == '1').order_by(Report.name)
            ])
class reports_hd(hd):
    cls__kwds = set([ 'reports' ])
    cls__title = u"Отчеты"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'reports.xsl'),
    ]
    def E_data(self):
        sess = self.req.environ['rrduet.sess']
        try:
            user_id = sess['id']
        except:
            return  E.data()
        return E.data(*[
            E.report(name=r.name, link=r.link) for r in self.dbconn.query(Report).filter(
                Admin_operkw.group_kw.like('%'+Report.link+'%')).filter(
                Admin_operkw.oper_id ==user_id).filter(
                Admin_operkw.group_include == '1').order_by(Report.name)
            ])
class users(template_base):
    cls__kwds =  set([ 'rep_users'])
    cls__title = u"Отчет по пользователям"
    cls__xsllist = [
            ('', '__root__.xsl'),
            ('body', 'users.xsl'),
        ]

    def E_data(self):
        return E.data(*[
            E.user(fio=r.fio, user_id=str(r.id)) for r in self.dbconn.query(Userprofile).order_by(Userprofile.system_id, Userprofile.fio)
            ])
class users_hd(hd):
    cls__kwds =  set([ 'rep_users'])
    cls__title = u"Отчет по пользователям"
    cls__xsllist = [
            ('', '__root__.xsl'),
            ('body', 'users.xsl'),
        ]

    def E_data(self):
        return E.data(*[
            E.user(fio=r.fio, user_id=str(r.id)) for r in self.dbconn.query(Userprofile).order_by(Userprofile.system_id, Userprofile.fio)
            ])
class rep_users(main_page):
    cls__kwds =  set([ 'rep_users'])
    cls__title = u""
    def user(self):
        self.user_id = max(self.req.POST.get('user_id'), self.req.GET.get('user_id'))
    def comment(self):
        try:
            fio = self.dbconn.query(Userprofile.fio).filter(Userprofile.id == int(self.user_id)).one()
        except:
            fio = u""
        self.inst = u"Отчет по сотруднику %s" % fio

class rep_users_hd(main_page_hd):
    cls__kwds =  set([ 'rep_users'])
    cls__title = u""
    def user(self):
        self.user_id = max(self.req.POST.get('user_id'), self.req.GET.get('user_id'))
    def comment(self):
        try:
            fio = self.dbconn.query(Userprofile.fio).filter(Userprofile.id == int(self.user_id)).one()
        except:
            fio = u""
        self.inst = u"Отчет по сотруднику %s" % fio
        self.title = self.inst
class rep_date(search):
    cls__kwds =  set([ 'rep_date' ])
    cls__title = u"отчет по дате"
    class callback_form(form_base):
        fields = [
            field('date',  ''),
            field('offset',  0),
        ]
        labels = {
                'date':u'Введите дату',
        }
        ftypes = {
            'date':'date',
        }
    def query_(self):
        form = self.form
        dbconn = self.dbconn
        date = form['date']
        offset = form['offset']
        query = None
        try:
            offset = int(offset)
        except:
            offset = 0
        limit = 10
        count = 0
        if date:
            query = dbconn.query(Threads, Tasktype.name).filter(
                    Threads.creation_date == date).filter(
                    Tasktype.id == Threads.title_id).filter(
                    Threads.id_local == 1).filter(
                    Tasktype.system_id == 1).order_by(Threads.id.desc()).limit(limit).offset(offset)
            try:
                count = list(dbconn.execute("select count(*) from thread join tasktype on thread.title_id = tasktype.id where creation_date = '%s' and id_local =1 and tasktype.system_id=1" % (date)))[0][0]
            except:
                pass
        d = { 'date':form['date']}
        return (query, count, limit, d)
class rep_date_hd(search_hd):
    cls__kwds =  set([ 'rep_date' ])
    cls__title = u"отчет по дате"
    class callback_form(form_base):
        fields = [
            field('date',  ''),
            field('offset',  0),
        ]
        labels = {
                'date':u'Введите дату',
        }
        ftypes = {
            'date':'date',
        }
    def query_(self):
        form = self.form
        dbconn = self.dbconn
        date = form['date']
        offset = form['offset']
        query = None
        try:
            offset = int(offset)
        except:
            offset = 0
        limit = 10
        count = 0
        if date:
            query = dbconn.query(Threads, Tasktype.name).filter(
                    Threads.creation_date == date).filter(
                    Tasktype.id == Threads.title_id).filter(
                    Threads.id_local == 1).filter(
                    Tasktype.system_id == 0).order_by(Threads.id.desc()).limit(limit).offset(offset)
            try:
                count = list(dbconn.execute("select count(*) from thread join tasktype on thread.title_id = tasktype.id where creation_date = '%s' and id_local =1 and tasktype.system_id=0" % (date)))[0][0]
            except:
                pass
        d = { 'date':form['date']}
        return (query, count, limit, d)
class rep_stat(search):
    cls__kwds =  set([ 'rep_stat' ])
    cls__title = u"Статистика выполненных заданий"
    class callback_form(form_base):
        fields = [
            field('field',  0),
            field('date',  0),
            field('offset',  0),
        ]
        labels = {
                'date':u'Введите количество дней',
                'field':u'Выбирете сотрудника',
        }
        ftypes = {
            'field':'select',
        }
        def select_field(self, field):
            sess = self.req.environ['rrduet.sess']
            try:
                user_id = sess['id']
            except:
                return  E.options()
            options = []
            options.append(E.option(E.value(u"0"), u"--"))
            for r in self.template_ref().dbconn.query(Userprofile).order_by(Userprofile.fio):
                options.append(E.option(E.value(str(r.id)), r.fio))
            return E.options(*options)
    def query_(self):
        form = self.form
        dbconn = self.dbconn
        date = form['date']
        field = form['field']
        offset = form['offset']
        query = None
        try:
            offset = int(offset)
        except:
            offset = 0
        limit = 10
        count = 0
        try:
            date = int(date)
        except:
            date = 0
        try:
            field = int(field)
        except:
            field = 0
        if date or field:
            query = dbconn.query(Threads, Tasktype.name).filter(Tasktype.id == Threads.title_id).filter(Tasktype.system_id == 1).filter(Threads.status == u'открыто_открыто')
            dt = fd =''
            if date:
                check = datetime.date.today() - datetime.timedelta(int(date))
                query = query.filter(Threads.creation_date > check)
                dt = "creation_date> '%s' and" % check.strftime('%Y-%m-%d')
            if field:
                query = query.filter(Threads.performer_id == field)
                fd = 'performer_id=%s and ' % str(field)
            query = query.order_by(Threads.id.desc()).limit(limit).offset(offset)
            try:
                count = list(dbconn.execute("select count(*) from thread join tasktype on thread.title_id = tasktype.id where %s %s status='%s' and tasktype.system_id=1" % (dt, fd, u"открыто_открыто"), ))[0][0]
            except:
                pass
        d = { 'date':str(form['date']), 'field':str(form['field'])}
        return (query, count, limit, d)
class rep_stat_hd(search_hd):
    cls__kwds =  set([ 'rep_stat' ])
    cls__title = u"Статистика выполненных заданий"
    class callback_form(form_base):
        fields = [
            field('field',  0),
            field('date',  0),
            field('offset',  0),
        ]
        labels = {
                'date':u'Введите количество дней',
                'field':u'Выбирете сотрудника',
        }
        ftypes = {
            'field':'select',
        }
        def select_field(self, field):
            sess = self.req.environ['rrduet.sess']
            try:
                user_id = sess['id']
            except:
                return  E.options()
            options = []
            options.append(E.option(E.value(u"0"), u"--"))
            for r in self.template_ref().dbconn.query(Userprofile).order_by(Userprofile.fio):
                options.append(E.option(E.value(str(r.id)), r.fio))
            return E.options(*options)
    def query_(self):
        form = self.form
        dbconn = self.dbconn
        date = form['date']
        field = form['field']
        offset = form['offset']
        query = None
        try:
            offset = int(offset)
        except:
            offset = 0
        limit = 10
        count = 0
        try:
            date = int(date)
        except:
            date = 0
        try:
            field = int(field)
        except:
            field = 0
        if date or field:
            query = dbconn.query(Threads, Tasktype.name).filter(Tasktype.id == Threads.title_id).filter(Tasktype.system_id == 0).filter(Threads.status == u'открыто_открыто')
            dt = fd =''
            if date:
                check = datetime.date.today() - datetime.timedelta(int(date))
                query = query.filter(Threads.creation_date > check)
                dt = "creation_date> '%s' and" % check.strftime('%Y-%m-%d')
            if field:
                query = query.filter(Threads.performer_id == field)
                fd = 'performer_id=%s and ' % str(field)
            query = query.order_by(Threads.id.desc()).limit(limit).offset(offset)
            try:
                count = list(dbconn.execute("select count(*) from thread join tasktype on thread.title_id = tasktype.id where %s %s status='%s' and tasktype.system_id=0" % (dt, fd, u"открыто_открыто"), ))[0][0]
            except:
                pass
        d = { 'date':str(form['date']), 'field':str(form['field'])}
        return (query, count, limit, d)
class rep_names(search):
    cls__kwds =  set([ 'rep_names' ])
    cls__title = u"Отчет по юр. и физ. лицам."
    class callback_form(form_base):
        fields = [
            field('message',  ''),
            field('offset',  0),
        ]
        labels = {
                'message':u'Введите наименование',
        }
    def query_(self):
        form = self.form
        dbconn = self.dbconn
        message = form['message']
        offset = form['offset']
        query = None
        try:
            offset = int(offset)
        except:
            offset = 0
        limit = 10
        count = 0
        if message:
            query = dbconn.query(Threads, Tasktype.name).filter(Tasktype.id == Threads.title_id).filter(Tasktype.system_id == 1).filter(Threads.message.like('%'+message+'%'))
            query = query.order_by(Threads.id.desc()).limit(limit).offset(offset)
            if 1:
                count = list(dbconn.execute("select count(*) from thread join tasktype on thread.title_id = tasktype.id where thread.message like '%s' and tasktype.system_id=1" % ('%'+message+'%')))[0][0]
#            except:
#                pass
        d = { 'message':form['message']}
        return (query, count, limit, d)
class rep_names_hd(search_hd):
    cls__kwds =  set([ 'rep_names' ])
    cls__title = u"Отчет по юр. и физ. лицам."
    class callback_form(form_base):
        fields = [
            field('message',  ''),
            field('offset',  0),
        ]
        labels = {
                'message':u'Введите наименование',
        }
    def query_(self):
        form = self.form
        dbconn = self.dbconn
        message = form['message']
        offset = form['offset']
        query = None
        try:
            offset = int(offset)
        except:
            offset = 0
        limit = 10
        count = 0
        if message:
            query = dbconn.query(Threads, Tasktype.name).filter(Tasktype.id == Threads.title_id).filter(Tasktype.system_id == 0).filter(Threads.message.like('%'+message+'%'))
            query = query.order_by(Threads.id.desc()).limit(limit).offset(offset)
            if 1:
                count = list(dbconn.execute("select count(*) from thread join tasktype on thread.title_id = tasktype.id where thread.message like '%s' and tasktype.system_id=0" % ('%'+message+'%')))[0][0]
#            except:
#                pass
        d = { 'message':form['message']}
        return (query, count, limit, d)
