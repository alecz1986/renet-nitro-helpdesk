#! /usr/local/bin/python
# -*- coding: utf-8 -*-


from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine, Numeric, DateTime, Text, Date, Time
from sqlalchemy import Index, UniqueConstraint, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.databases.mysql import MSEnum, MSInteger, MSSmallInteger
from sqlalchemy.orm import mapper, relation
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import ColumnDefault
from sqlalchemy import and_
import datetime


from regerror import regerror

err = regerror('/usr/local/fshop/var/log/task.log')
metadata = MetaData()




"""
Награды и выговоры
"""
aw_table = Table('aw', metadata,
    Column('id', Integer, primary_key=True),
    Column('th_id', Integer, nullable=False, default=0),
    Column('cr_by_id', Integer, nullable=False, default=0),
    Column('cr_to_id', Integer, nullable=False, default=0),
    Column('status', String(200), nullable=False, default=''),
    Column('com', Text, nullable=False, default=''),
    Column('cr_date',  DateTime(14), nullable=False),
)
class Aw(object):
    def __init__(self, th_id, cr_by_id, cr_to_id, status, com,cr_date):
        self.th_id = th_id
        slef.cr_by_id = cr_by_id
        self.cr_to_id = cr_to_id
        self.status = status 
        self.com = com
        self.cr_date = cr_date
mapper(Aw, aw_table)

awarsuser_table = Table('awarsuser', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id_id', Integer, nullable=False, default=0),
)
class Awarsuser(object):
    def __init__(self, user_id_id):
        self. user_id_id = user_id_id
mapper(Awarsuser, awarsuser_table)
"""
Комментарий к полю задания.
"""

commentfield_table = Table('commentfield', metadata,
    Column('id', Integer, primary_key=True),
    Column('field_comment_id', Integer, nullable=False, default=0),
    Column('comment', Text, nullable=False, default=''),
)
class Commentfield(object):
    def __init__(self, field_comment_id, comment):
        self.field_comment_id = field_comment_id
        self.comment = comment
mapper(Commentfield, commentfield_table)
deg1_table = Table('deg1', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id_id', Integer, nullable=False, default=0),
)
class Deg1(object):
    def __init__(self, user_id_id):
        self.user_id_id = user_id_id
mapper(Deg1, deg1_table)
fields_table = Table('fields', metadata,
    Column('id', Integer, primary_key=True),
    Column('type_id', Integer, nullable=False, default=0),
    Column('field_id', Integer, nullable=False, default=0),
)
class Fields(object):
    def __init__(self, type_id, field_id):
        self.type_id = type_id
        self.field_id = field_id
mapper(Fields, fields_table)
instruction_table = Table('instruction', metadata,
    Column('id', Integer, primary_key=True),
    Column('type_task_id', Integer, nullable=False, default=0),
    Column('instruct', Text, nullable=False, default=''),
)
class Instruction(object):
    def __init__(self, type_task_id, instruct):
        self.type_task_id = type_task_id
        self.instruct = instruct
mapper(Instruction, instruction_table)
report_table = Table('report', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(200), nullable=False, default=''),
    Column('link', String(200), nullable=False, default=''),
)
class Report(object):
    def __init__(self, name, link):
        self.name = name
        self.link = link
mapper(Report, report_table)
reportsuser_table = Table('reportsuser', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_report_id', Integer, nullable=False, default=0),
    Column('report_id', Integer, nullable=False, default=0),
)
class Reportsuser(object):
    def __init__(self, user_report_id, report_id):
        self.user_report_id = user_report_id
        self.report_id = report_id
mapper(Reportsuser, reportsuser_table)
taskfield_table = Table('taskfield', metadata,
    Column('id', Integer, primary_key=True),
    Column('weight', Integer, nullable=False, default=0),
    Column('name', String(200), nullable=False, default=''),
)
class Taskfield(object):
    def __init__(self, weight, name):
        self. weight = weight
        self.name = name
mapper(Taskfield, taskfield_table)
"""
тип задания.
system_id:
    0 - hd
    1 - tp
"""
tasktype_table = Table('tasktype', metadata,
    Column('id', Integer, primary_key=True),
    Column('system_id', Integer, nullable=False, default=0),
    Column('name', String(200), nullable=False, default=''),
)
class Tasktype(object):
    def __init__(self, name, system_id):
        self.name = name
        self.system_id = system_id
mapper(Tasktype, tasktype_table)
taskuser_table = Table('taskuser', metadata,
    Column('id', Integer, primary_key=True),
    Column('type_id', Integer, nullable=False, default=0),
    Column('user_id', Integer, nullable=False, default=0),
)
class Taskuser(object):
    def __init__(self, type_id, user_id):
        self.type_id = type_id
        self.user_id = user_id
mapper(Taskuser, taskuser_table)
thread_table = Table('thread', metadata,
    Column('id', Integer, primary_key=True),
    Column('id_global', Integer,  nullable=False, default=0),
    Column('id_local', Integer,  nullable=False, default=0),
    Column('created_by_id', Integer,  nullable=False, default=0),
    Column('deleted_by_id', Integer,  nullable=False, default=0),
    Column('creation_time', Time,  nullable=False, default=0),
    Column('creation_date', Date,  nullable=False, default=0),
    Column('deletion_time',  DateTime(14),  nullable=False, default=0),
    Column('category_id', Integer,  nullable=False, default=0),
    Column('customer_id', Integer,  nullable=False, default=0),
    Column('performer_id', Integer,  nullable=False, default=0),
    Column('finish_date',  DateTime(14),  nullable=False, default=0),
    Column('importance',  String(200), nullable=False, default=0),
    Column('status', String(200), nullable=False, default=''),
    Column('title_id', Integer,  nullable=False, default=0),
    Column('message',  Text, nullable=False),
    Column('info',  Text, nullable=False),
)
class Threads(object):
    def __init__(self, id_global, id_local, created_by_id, deleted_by_id, creation_time, creation_date, deletion_time, category_id, customer_id, performer_id, finish_date, importance, status, title_id, message, info):
        self.id_global = id_global
        self.id_local = id_local
        self.created_by_id = created_by_id
        self.deleted_by_id = deleted_by_id
        self.creation_time = creation_time
        self.creation_date = creation_date
        self.deletion_time = deletion_time
        self.category_id = category_id
        self.customer_id = customer_id
        self.performer_id = performer_id
        self.finish_date = finish_date
        self.importance = importance
        self.status = status
        self.title_id = title_id
        self.message = message
        self.info = info
mapper(Threads, thread_table)

"""
system_id
    1 other
    2 teh
    3 abon
    4 kom
"""
userprofile_table = Table('userprofile', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, nullable=False, default=0),
    Column('group_id', Integer, nullable=False, default=0),
    Column('fio', String(200), nullable=False, default=''),
    Column('office', String(200), nullable=False, default=''),
    Column('post', String(200), nullable=False, default=''),
    Column('telephone_sot', String(200), nullable=False, default=''),
    Column('telephone_work', String(200), nullable=False, default=''),
    Column('telephone_home', String(200), nullable=False, default=''),
    Column('system_id', Integer, nullable=False, default=0),
    Column('login', String(200), nullable=False, default=''),
    Column('email', String(200), nullable=False, default=''),
    Column('password', String(200), nullable=False, default=''),
)
class Userprofile(object):
    def __init__(self, user_id, group_id, fio, office, post, telephone_sot, telephone_work, telephone_home, system_id, login, email, password):
        self.user_id = user_id
        self.group_id = group_id
        self.fio = fio
        self.office = office
        self,post = post
        self.telephone_sot = telephone_sot
        self.telephone_work = telephone_work
        self.telephone_home = telephone_home
        self.system_id = system_id
        self.login = login
        self.email = email
        self.password = password
mapper(Userprofile, userprofile_table)
visitedthreads_table = Table('visitedthreads', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, nullable=False, default=0),
    Column('thread_id', Integer, nullable=False, default=0),
    Column('visited_on', DateTime(14), nullable=False, default=0),
)
class Visitedthreads(object):
    def __init__(self, user_id, thread_id, visited_on):
        self.user_id = user_id
        self.thread_id = thread_id
        self.visited_on = visited_on
mapper(Visitedthreads, visitedthreads_table)

"""
Группы операторов
"""
admin_group_table = Table('admin_group', metadata,
    Column('group_id', Integer, primary_key=True),
    Column('group_info', String(64), nullable=False, default=''),
    Column('group_help', String(1000), nullable=False, default=''),
)
class Admin_group(object):
    def __init__(self, group_info, group_help):
        self.group_info = group_info
        self.group_help = group_help
mapper(Admin_group, admin_group_table)

"""
Операторы
"""
oper_table = Table('distrib_oper', metadata,
    Column('oper_id', Integer, nullable=False),
    Column('group_id', Integer, nullable=False),
    Column('auth_name', String(20), nullable=False, unique=True),
    Column('auth_key', String(20), nullable=False),
    Column('lastname', String(30), nullable=False),
    Column('firstname', String(30), nullable=False),
    Column('middlename', String(30), nullable=False),
    Column('email', String(200), nullable=False),
    Column('phones', String(200), nullable=False),
    Column('info', String(200), nullable=False),
    PrimaryKeyConstraint('oper_id'),
)
class Oper(object):
    def __init__(self, group_id=None, auth_name=None, auth_key=None,
            lastname='', firstname='', middlename='', email='', phones='', info=''):
        self.group_id = group_id
        self.auth_name = auth_name
        self.auth_key = auth_key
        self.lastname = lastname
        self.firstname = firstname
        self.middlename = middlename
        self.email = email
        self.phones = phones
        self.info = info
mapper(Oper, oper_table)

user_table = Table('user', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('login', String(100), nullable=False, unique=True),
    Column('password', String(200), nullable=False),
    Column('username', String(200), nullable=False),
    Column('sername', String(200), nullable=False),
    Column('patronymic', String(200), nullable=False),
    Column('address', String(400), nullable=False),
    Column('phones', String(200), nullable=False),
    Column('email', String(200), nullable=False, unique=True),
#тип пользвателя юр и физ лицо
    Column('sale_type', MSEnum('"org"', '"org_vat"','"pp"'), nullable=False, default="pp"),
#подписка на рассылку новостей
    Column('send2email', MSEnum('"yes"', '"no"'), default='yes'),
    Column('comp_name', String(200), nullable=True),
    Column('inn_kpp', String(200), nullable=True),
    Column('bank', String(400), nullable=True),
    Column('opt', MSEnum('"yes"', '"no"'), default='yes')
)
class User(object):
    def __init__(self,login, password, username, sername,patronymic, address, phones, email, sale_type=None, send2email=None, comp_name=None, inn_kpp=None, bank=None, opt='no'):
        self.login = login
        self.password = password
        self.username = username
        self.sername = sername
        self.patronymic = patronymic
        self.address = address
        self.phones = phones
        self.email = email
        self.sale_type = sale_type
        self.send2email = send2email
        self.comp_name = comp_name
        self.inn_kpp = inn_kpp
        self.bank = bank
        self.opt = opt
mapper(User, user_table)


"""
Кейворды в группе
"""
admin_groupkw_table = Table('admin_groupkw', metadata,
    Column('group_id', Integer, nullable=False, autoincrement=False),
    Column('group_kw', String(32), nullable=False, default=''),
    PrimaryKeyConstraint('group_id', 'group_kw'),
)
class Admin_groupkw(object):
    def __init__(self, group_id, group_kw):
        self.group_id = group_id
        self.group_kw = group_kw
mapper(Admin_groupkw, admin_groupkw_table)

"""
Кейворды по урл (не используются)
"""
urlmapkw_info_table = Table('urlmapkw_info', metadata,
    Column('url_kw', String(32), nullable=False, default=''),
    Column('kw_info', String(64), nullable=False, default=''),
    Column('kw_help', String(1000), nullable=False, default=''),
    PrimaryKeyConstraint('url_kw'),
)
class Urlmapkw_info(object):
    def __init__(self, url_kw='', kw_info='', kw_help=''):
        self.url_kw = url_kw
        self.kw_info = kw_info
        self.kw_help = kw_help
mapper(Urlmapkw_info, urlmapkw_info_table)

"""
Расширение/Удаление кейворда оператора по отношению к группе, к которой он относится
"""
admin_operkw_table = Table('admin_operkw', metadata,
    Column('oper_id', Integer, nullable=False, autoincrement=False),
    Column('group_kw', String(32), nullable=False, default=''),
    Column('group_include', MSEnum("'0'", "'1'"), nullable=False, default="1"),
    PrimaryKeyConstraint('oper_id', 'group_kw'),
)
class Admin_operkw(object):
    def __init__(self, oper_id=None, group_kw=None, group_include=None):
        self.oper_id = oper_id
        self.group_kw = group_kw
        self.group_include = group_include
mapper(Admin_operkw, admin_operkw_table)

"""
Метка урл
"""
urllabel_table = Table('urllabel', metadata,
    Column('url_label', String(64), nullable=False, default=''),
    Column('url_prefix', String(64), nullable=False, default=''),
    Column('comment', String(500), nullable=False, default=''),
    PrimaryKeyConstraint('url_label'),
)
class Urllabel(object):
    def __init__(self, url_label, url_prefix, comment=''):
        self.url_label = url_label
        self.url_prefix = url_prefix
        self.comment = comment
mapper(Urllabel, urllabel_table)
"""
Привязка обработки модулями к конкретным урл
"""
urlmap_table = Table('urlmap', metadata,
    Column('url_path', String(64), nullable=False, default=''),
    Column('url_label', String(64), nullable=False, default=''),
    Column('resporator', String(128), nullable=False, default=''),
    PrimaryKeyConstraint('url_label', 'url_path'),
)
class Urlmap(object):
    def __init__(self, url_path=None, url_label=None, resporator=None):
        self.url_path = url_path
        self.url_label = url_label
        self.resporator = resporator
mapper(Urlmap, urlmap_table)



urlmapkw_table = Table('urlmapkw', metadata,
    Column('url_path', String(64), nullable=False, default=''),
    Column('url_label', String(64), nullable=False, default=''),
    Column('url_kw', String(32), nullable=False, default=''),
    PrimaryKeyConstraint('url_path', 'url_label', 'url_kw'),
)
class Urlmapkw(object):
    def __init__(self, url_path, url_label, url_kw):
        self.url_path = url_path
        self.url_label = url_label
        self.url_kw = url_kw

mapper(Urlmapkw, urlmapkw_table)



engine = create_engine('mysql://admintask:rom724Kz@localhost/tasks_new?charset=utf8&use_unicode=1')
metadata.bind = engine
#metadata.create_all(engine)
if 1 and __name__ == '__main__':

    Session = sessionmaker(bind=engine)
    dbconn = Session()
    for i in dbconn.query(UserProfile).all():
        print UserProfile.id
    
if 0:
    Session = sessionmaker(bind=engine)
    dbconn = Session()
    names = [r[0] for r in list(dbconn.query(Taskfield.name).filter(Taskfield.weight == 1))]
    ids = [r[0] for r in list(dbconn.query(Fields.type_id).filter(Fields.field_id == Taskfield.id).filter(Taskfield.weight == 1).group_by(Fields.type_id))]
    thr =  dbconn.query(Threads).order_by(Threads.id).filter(Threads.title_id.in_(ids)).filter(Threads.id > 210740)
    print len(list(thr))
    thr = []
    for t in thr:
        print t.id
        info = []
        mess = t.message.split('$')[1:]
        for i in mess:
            if i.replace(':', '') in names:
                info.append(mess[mess.index(i)+1])
        if info:
            t.info = ' '.join(info).replace('*', '')
            dbconn.commit()
