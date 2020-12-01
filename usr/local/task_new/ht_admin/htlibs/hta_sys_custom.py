#
# -*- coding: utf-8 -*-

import sys
import re
from rrduet.rr_template import field, E
import hta_config
from hta_base import check_action
from hta_page import form_base, template_base
from fullshopapi import User
import sqlalchemy
import sqlalchemy.orm

class change_secret(template_base):
    cls__title = u"Изменение пароля пользователя"
    cls__kwds = set([ 'custom' ])
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', '__simpleedit__.xsl'),
        ('menu', '__menu__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('user_id', 0, int, ValueError),
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
        user_id = form['user_id']
        secret_old = form['secret_old']
        secret_new = form['secret_new']
        secret_repeat = form['secret_repeat']
        form['secret_old'] = form['secret_new'] = form['secret_repeat'] = ''

        if action == '':
            return None

        if secret_new == '':
            self.errors.append(u"Пароль не может быть нулевым")
        elif len(secret_new) < hta_config.secret_minlength:
            self.errors.append(u"Пароль не может быть короче %d символов" % (hta_config.secret_minlength,))
        if secret_new != secret_repeat:
            self.errors.append(u"Неправильное подтверждение пароля")

        if self.errors:
            return None

        dbconn = self.dbconn
        try:
            user = dbconn.query(User).filter(User.user_id == user_id).one()
        except sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
            self.errors.append(u"Пользователя не существует")
            return None
        if user.password != secret_old:
            self.errors.append(u"Предоставленный пароль не совпадает с заданным в базе данных")
            return None
        user.password = secret_new
        dbconn.commit()
        self.results.append(u"Пароль был успешно изменен")

class manage_custom(template_base):
    cls__title = u"Покупатели"
    cls__kwds = set([ 'custom' ])
    cls__xsllist = [
        ('', '__root__.xsl'),
    ]
    cls__externals = [
        '/css/main.css',
        '/extjs/resources/css/ext-all.css',
        '/extjs/resources/css/dd.css',
        '/extjs/adapter/ext/ext-base.js',
        '/extjs/ext-all-debug.js',
        #'/extjs/ext-all.js',
        '/js/private/custom.js',
    ]
     
class custom_ajax(template_base):
    cls__kwds = set([ 'custom' ])
    cls__application = 'ajax'
    class callback_form(form_base):
        fields = [
            field('user_id', 0,int, ValueError),
            field('login',''),
            field('username',''),
            field('sername',''),
            field('patronymic', ''),
            field('email',''),
            field('address',''),
            field('phones',''),
            field('sale_type',''),
            field('send2email',''),
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
        users = dbconn.query(User).all()
        ajax = []
        for r in users:
            ajax.append(E.user(
                user_id = str(r.user_id),
                name = r.username,
                login = r.login,
                sername = r.sername,
                patronymic = r.patronymic,
                email = r.email,
                address = r.address,
                phones = r.phones,
                sale_type = r.sale_type,
                send2email = r.send2email,
                ))
        return E.ajax(*ajax)


    def config(self, dbconn):
        form = self.form
        action = form['action']
        user_id = form['user_id']
        login = form['login']
        username = form['username']
        sername = form['sername']
        patronymic = form['patronymic']
        email = form['email']
        address = form['address']
        phones = form['phones']
        sale_type = form['sale_type']
        send2email = form['send2email']
        if user_id == 0 and login and username and sername and patronymic and email and address and phones and sale_type and send2email:
            user = User(login, '1234567', username, sername,patronymic, address, phones, email, sale_type=None, send2email=None)
            dbconn.add(user)
            try:
                dbconn.commit()
            except:
                pass
        elif user_id  and login and username and sername and patronymic and email and address and phones and sale_type and send2email:
            try:
                user = dbconn.query(User).filter(User.user_id == user_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return E.ajax()
            form.store_to_orm(user)
            dbconn.commit()
            try:
                dbconn.commit()
            except:
                dbconn.rollback()
            finally:
                dbconn.close()
        return E.ajax() 
