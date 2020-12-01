#
# -*- coding: utf-8 -*-

import sys
import re
from rrduet.rr_template import field, E
import hta_config
from hta_base import check_action
from hta_page import form_base, template_base
from fullshopapi import Distrib_oper
from fullshopapi import Urlmapkw_info
from fullshopapi import Admin_group
from fullshopapi import Admin_groupkw
from fullshopapi import Admin_operkw
from fullshopapi import Distributor
from fullshopapi import Category
from fullshopapi import Supplier
import sqlalchemy
import sqlalchemy.orm

class change_secret(template_base):
    cls__kwds = set([ 'user' ])
    cls__title = u"Изменение пароля пользователя"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', '__simpleedit__.xsl'),
        ('menu', '__menu__.xsl'),
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
        elif len(secret_new) < hta_config.secret_minlength:
            self.errors.append(u"Пароль не может быть короче %d символов" % (hta_config.secret_minlength,))
        if secret_new != secret_repeat:
            self.errors.append(u"Неправильное подтверждение пароля")

        if self.errors:
            return

        sess = self.environ['rrduet.sess']
        oper_id = sess.get('oper_id')
        if oper_id is None:
            self.errors.append(u"Ошибка данных в стукутре сессии")
            return
        dbconn = self.dbconn
        try:
            oper = dbconn.query(Distrib_oper).filter(Distrib_oper.oper_id == oper_id).one()
        except sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
            self.errors.append(u"Данные в сессии устарели, необходимо перерегестрироваться")
            return
        if oper.auth_key != secret_old:
            self.errors.append(u"Предоставленный пароль не совпадает с заданным в базе данных")
            return
        oper.auth_key = secret_new
        dbconn.commit()
        self.results.append(u"Пароль был успешно изменен")

class manage_user(template_base):
    cls__kwds = set([ 'user' ])
    cls__title = u"Управление учетными записями пользователей"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', '__simpleedit__.xsl'),
        ('menu', '__menu__.xsl'),
    ]
    cls__externals = [
        '/css/main.css',
        '/extjs/resources/css/ext-all.css',
        '/extjs/resources/css/dd.css',
        '/extjs/adapter/ext/ext-base.js',
        '/extjs/ext-all.js',
        '/js/private/manage_user.js',
        '/js/private/manage_userlist.js',
    ]
    class callback_form(form_base):
        fields = [
            field('oper_id', autoincrement=True),
            field('auth_name', ''),
            field('distrib_id', 0, int, ValueError),
            field('group_id', 0, int, ValueError),
            field('secret_new', ''),
            field('secret_repeat', ''),
            field('lastname', ''),
            field('firstname', ''),
            field('middlename', ''),
            field('email', ''),
            field('phones', ''),
            field('info', ''),
            field('action', '', check_action),
        ]
        labels = {
            'auth_name': u"Учетная запись",
            'group_id': u"Группа",
            'distrib_id': u"Дистрибъюция",
            'secret_new': u"Назначить пароль",
            'secret_repeat': u"Повторить пароль",
            'lastname': u"Фамилия",
            'firstname': u"Имя",
            'middlename': u"Отчество",
            'email': u"E-Mail",
            'phones': u"Телефоны",
            'info': u"Дополнительная информация",
        }
        ftypes = {
            'group_id': 'select',
            'distrib_id': 'select',
            'secret_new': 'password',
            'secret_repeat': 'password',
            'info': 'textarea',
        }
        def select_group_id(self, field):
            options = []
            group_id = self['group_id']
            for r in self.template_ref().dbconn.query(Admin_group).order_by(Admin_group.group_info):
                options.append(E.option(E.value(str(r.group_id)), "%s [ %s ]" % (r.group_info, r.group_help)))
            return E.options(*options)
        def select_distrib_id(self, field):
            options = []
            for r in self.template_ref().dbconn.query(Distributor):
                options.append(E.option(E.value(str(r.distrib_id)), "%s" % (r.discription)))
            options.append(E.option(E.value('0'),u'все'))
            return E.options(*options)
    def logic(self):
        form = self.form

        action = form['action']
        form['action'] = 'new'

        secret_new = form['secret_new']
        secret_repeat = form['secret_repeat']
        form['secret_new'] = form['secret_repeat'] = ''
        if form['distrib_id'] == 0:
            form['distrib_id'] = None

        dbconn = self.dbconn

        if form['oper_id']:
            # Зачитаем данные по идентификатору.
            try:
                row = dbconn.query(Distrib_oper).filter(Distrib_oper.oper_id == form['oper_id']).one()
                if row.distrib_id is None:
                    row.distrib_id = 0
                self.ormloaded = True
                form['action'] = 'edit'
            except sqlalchemy.orm.exc.NoResultFound:
                self.errors.append(u"Идентификатор %d не найден" % (form['oper_id'],))
                form['oper_id'] = None
                sys.exc_clear()

        if action == 'delete':
            if self.ormloaded:
                dbconn.delete(row)
            return
        elif action == '':
            if self.ormloaded:
                form.load_from_orm(row)
            return

        if not form['auth_name']:
            self.errors.append(u"Имя пользователя должно быть определено")
        if re.match(r"^[a-z]+[0-9a-z]*(?:\.[0-9a-z]+)?$", form['auth_name']) is None:
            self.errors.append(u"Имя пользователя должно быть набрано латинскими буквами")

        if not self.ormloaded or secret_new or secret_repeat:
            if secret_new == '':
                self.errors.append(u"Пароль не может быть нулевым")
            elif len(secret_new) < hta_config.secret_minlength:
                self.errors.append(u"Пароль не может быть короче %d символов" % (hta_config.secret_minlength,))
            if secret_new != secret_repeat:
                self.errors.append(u"Неправильное подтверждение пароля")

        if self.errors:
            return

        if not self.ormloaded:
            row = Distrib_oper()
            row.auth_key = secret_new
            dbconn.add(row)
        elif secret_new:
            row.auth_key = secret_new
        form.store_to_orm(row)
        self.changes_commit(row)


class manage_user_ajax(template_base):
    cls__kwds = set([ 'user' ])
    cls__application = 'ajax'
    class callback_form(form_base):
        fields = [
            field('group_id', 0, int, ValueError),
            field('oper_id', 0, int, ValueError),
            field('group_include', 'default'),
            field('group_kw', ''),
            field('action', ''),
        ]
    def ajax(self):
        self.resp.content_type = 'application/xml'

        form = self.form
        action = form['action']

        dbconn = self.dbconn
        if action == '':
            self.xmlroot = self.data(dbconn)
        elif action == 'config':
            self.xmlroot = self.config(dbconn)
    def data(self, dbconn):
        form = self.form
        group_kwds = dict(( (r.group_kw, '1') for r in dbconn.query(Admin_groupkw).filter(Admin_groupkw.group_id == form['group_id']) ))
        oper_kwds = dict(( (r.group_kw, r.group_include) for r in dbconn.query(Admin_operkw).filter(Admin_operkw.oper_id == form['oper_id']) ))
        ajax = []
        for kw, kw_info, kw_help in dbconn.query(
            Urlmapkw_info.url_kw,
            Urlmapkw_info.kw_info,
            Urlmapkw_info.kw_help,
        ).order_by(Urlmapkw_info.url_kw):
            ajax.append(E.kw(
                E.info(kw_info),
                E.comment(kw_help),
                E.group(group_kwds.pop(kw, '0')),
                E.oper(oper_kwds.pop(kw, 'default')),
                name=kw))
        return E.ajax(*ajax)
    def config(self, dbconn):
        self.xmlroot = E.ajax()
        form = self.form
        try:
            dbconn.query(Urlmapkw_info).filter(Urlmapkw_info.url_kw == form['group_kw']).one()
        except sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
            return E.ajax(code='not found')
        try:
            row = dbconn.query(Admin_operkw).filter(sqlalchemy.and_(
                Admin_operkw.oper_id == form['oper_id'],
                Admin_operkw.group_kw == form['group_kw']
            )).one()
            self.ormloaded = True
        except sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
            row = Admin_operkw()
        if form['group_include'] in '01':
            form.store_to_orm(row)
            dbconn.add(row)
        else:
            if self.ormloaded:
                dbconn.delete(row)
        dbconn.commit()
        return E.ajax(code='ok')

class manage_userlist_ajax(template_base):
    cls__kwds = set([ 'user' ])
    cls__application = 'ajax'
    def ajax(self):
        self.resp.content_type = 'application/xml'
        dbconn = self.dbconn
        self.xmlroot = self.data(dbconn)
    def data(self, dbconn):
        form = self.form
        ajax = [ E.oper(
            E.group(group_info, id=str(r.group_id)),
            E.auth_name(r.auth_name),
            E.lastname(r.lastname),
            E.firstname(r.firstname),
            E.middlename(r.middlename),
            E.email(r.email),
            E.phones(r.phones),
            E.info(r.info),
            id=str(r.oper_id)) for r, group_info in dbconn.query(Distrib_oper, Admin_group.group_info).filter(Distrib_oper.group_id ==  Admin_group.group_id) ]
        return E.ajax(*ajax)

class distrib(template_base):
    cls__kwds = set([ 'user' ])
    cls__title = u"Дистрибьюция"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'distrib.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    cls__externals = [
        '/css/main.css',
        '/extjs/resources/css/ext-all.css',
        '/extjs/resources/css/dd.css',
        '/extjs/adapter/ext/ext-base.js',
        '/extjs/ext-all-debug.js',
        #'/extjs/ext-all.js',
        '/js/private/show_category.js',
    ]
    class callback_form(form_base):
        fields = [
            field('distrib_id', 0, int, ValueError),
            field('category_id',0, int, ValueError),
            field('weight',50),
            field('discription',''),
            field('send_sms',''),
            field('zip_visible',''),
            field('phone',None),
            field('rate',0),
            field('supplier_id',0),
            field('action',''),
            ]
        labels = {'category_id':u'Выберите категорию',
                  'discription':u'Описание',
                  'send_sms':u'Отправка сообщений при заказе',
                  'phone':u'Телефоны для смс (в формате 7ХХХХХХХХХХ) через запятую',
                  'zip_visible':u'Делать невидимыми продукты при изменении из csv',
                  'rate':'%',
                  'supplier_id':u'Поставщик',
                  }
        ftypes = {'category_id': 'select',
                  'send_sms': 'select',
                  'zip_visible': 'select',
                  'supplier_id': 'select',
                 }

        def select_category_id(self, field):
            options = []
            for r in self.template_ref().dbconn.query(Category).all():
                options.append(E.option(E.value(str(r.category_id)), r.name))
            return E.options(*options)
        def select_supplier_id(self, field):
            options = []
            options.append(E.option(E.value('0'), u'нет'))
            for r in self.template_ref().dbconn.query(Supplier).all():
                options.append(E.option(E.value(str(r.supplier_id)), r.name))
            return E.options(*options)
        def select_send_sms(self, field):
            options = []
            options.append(E.option(E.value(u'no'), u'нет'))
            options.append(E.option(E.value(u'yes'), u'да'))
            return E.options(*options)
        def select_zip_visible(self, field):
            options = []
            options.append(E.option(E.value(u'no'), u'нет'))
            options.append(E.option(E.value(u'yes'), u'да'))
            return E.options(*options)

    def logic(self):
        action = self.form['action']
        distrib_id = self.form['distrib_id']
        category_id = self.form['category_id']
        discription = self.form['discription']
        send_sms = self.form['send_sms']
        zip_visible = self.form['zip_visible']
        phone = self.form['phone']
        if phone == '':
            phone = None
        rate = self.form['rate']
        supplier_id = self.form['supplier_id']
        try:
            rate = float(rate)
        except:
            rate = 0
        weight = self.form['weight']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if distrib_id==0 and category_id and discription:
                distributor = Distributor(category_id, weight, discription, send_sms, zip_visible, phone, rate, supplier_id)
                dbconn.add(distributor)
                try:
                    dbconn.commit()
                    self.results.append(u'Запись успешно длбавлена')
                except:
                    self.errors.append(u'Конфликт имен')
            elif distrib_id and category_id and discription:
                try:
                    distributor = dbconn.query(Distributor).filter(Distributor.distrib_id == distrib_id).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    self.errors.append(u'Дистрибьюция не найдена')
                    return
                distributor.category_id = category_id
                distributor.discription = discription
                distributor.send_sms = send_sms
                distributor.phone = phone
                distributor.zip_visible = zip_visible
                distributor.rate = rate
                distributor.supplier_id = supplier_id
                try:
                    dbconn.commit()
                    self.results.append(u'Изменения сохранены')
                except:
                    self.errors.append(u'Изменения не сохранены')
            else:
                self.errors.append(u'не все поля были заполнены')
        elif action == 'delete':
            try:
                distributor = dbconn.query(Distributor).filter(Distributor.distrib_id == distrib_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                self.errors.append(u'Дистрибьюция не найдена')
                sys.exc_clear()
                return
            dbconn.delete(distributor)
            dbconn.commit()
            self.results.append(u'Запись удалена')
        if not distrib_id:
            self.form['distrib_id'] = 0
        else:
            try:
                distributor = dbconn.query(Distributor).filter(Distributor.distrib_id == distrib_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                self.errors.append(u'Дистрибьюция не найдена')
                return
            self.form['category_id'] = distributor.category_id
            self.form['weight'] = distributor.weight
            self.form['discription'] = distributor.discription
            self.form['send_sms'] = distributor.send_sms
            self.form['phone'] = distributor.phone
            self.form['rate'] = distributor.rate
            self.form['zip_visible'] = distributor.zip_visible
            self.form['supplier_id'] = distributor.supplier_id


    def E_data(self):
        dbconn = self.dbconn
        distributor = dbconn.query(Distributor, Category).filter(Distributor.category_id == Category.category_id)
        data = E.data()
        data_tag = data.xpath('//data')[0]
        for p in distributor:
            data_tag.append(E.distributor(distrib_id=str(p[0].distrib_id), category_name=p[1].name, category_id=str(p[1].category_id), discription=p[0].discription, rate='%10.2f'% (p[0].rate)))
        return data
