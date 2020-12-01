#
# -*- coding: utf-8 -*-

import sys
import os
import sqlalchemy

import htu_main

from task import *
from rrduet.rr_sesscookie import cookie_auth
from rrduet.rr_template import nodefault, field, form, template, E
from htu_config import base_dir, htroot_dir, templates_dir, sessions_dir
from htu_config import sessions_dir, dbi_info
from htu_host import host_name
import regerror
import re
import datetime
from lxml import etree
from lxml.html import fragment_fromstring



class form_base(form):
    fields = ()
    tagging_map = {
        'default': "P/ok G/wrong",
    }
    keyenc = None
    keyenc_list = [ u"ru:Ё" ]
    keyenc_charsets = [ 'utf-8', 'koi8-r', 'cp1251', 'cp866' ]
    @classmethod
    def meta_init(cls, cvars):
        if not ('keyenc_list' in cvars or 'keyenc_charsets' in cvars):
            return
        cls.keyenc = keyenc = u','.join(cls.keyenc_list)
        cls.keyenc_mapper = keyenc_mapper = {}
        for k in cls.keyenc_list:
            k_latin1 = k.encode('latin1', 'ignore')
            for cs in cls.keyenc_charsets:
                k_cs = k.encode(cs, 'ignore')
                if k_cs == '' or k_cs == k_latin1:
                    continue
                keyenc_mapper[k_cs] = cs
    @classmethod
    def meta_fields_userlevel(cls):
        fields = [
            field('ie', cls.keyenc, setup='charset_detect'),
        ]
        fields.extend(cls.fields)
        cls.fields = fields
    def charset_detect(self, field):
        cs = None
        vals = self.req.str_params.getall(field.name)
        if vals:
            ie = vals[0]
            for tok in ie.split(','):
                cs = self.keyenc_mapper.get(tok)
                if cs is not None:
                    self.req.charset = cs
                    break
            else:
                cs = 'utf-8'
        else:
            cs = 'utf-8'
        if self.req.charset is None:
            self.req.charset = cs
        return self.__class__.keyenc





class template_base(template, regerror.errtemplate):
    debug = False 
    cls__template_path = templates_dir
    callback_form = form_base
    cls__pathprefix = '/'
    cls__kwds = set(['common'])
    dbconn_cache = None
    kwds = None
    def __init__(self, *args, **kw):
        regerror.errtemplate.__init__(self, '/usr/local/task_new/var/log/error.log')
        template.__init__(self, *args, **kw)
    def E_main(self):
        return E.main(E.bgcolor("darkgray"),
                E.menu(E.href('/'), E.color(u"white"), E.name(u"главная")),
                E.menu(E.href('/threads'), E.color(u"white"), E.name(u"задания")),
                E.menu(E.href('/reports'), E.color(u"white"), E.name(u"отчеты")),
                E.menu(E.href('/passwd'), E.color(u"white"), E.name(u"смена пароля")),
                E.menu(E.href('/search'), E.color(u"white"), E.name(u"поиск")),
                E.menu(E.href('/info'), E.color(u"white"), E.name(u"справка")),
                E.menu(E.href('/auth'), E.color(u"white"), E.name(u"выход")),
                E.link(E.href('/hd'), E.color(u"blue"), E.name(u"HELPDESK")),
                )
    def E_page(self):
        sess = self.resp.environ.get('rrduet.sess')
        form = self.form
        path_encode = unicode(self.req.path_info) 
        return E.page(
            E.title(self.title),
            E.path(path_encode),
            self.E_main(),
            E.serv(name=host_name),
        )
    @classmethod
    def rrduet_callback(cls, url_path, url_label):
        dbconn = htu_main.dbhandler()
        try:
            if cls.kwds is None:
                cls.kwds = {}
            try:
                setkw = set()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                setkw = set()
            if cls.cls__kwds is not None:
                setkw.update(cls.cls__kwds)
            cls.kwds[url_path, url_label] = setkw
        finally:
            dbconn.close()
    def rr_checkperm(self):
        if self.kwds is None:
            return
        kwds_page = self.kwds.get((self.path_info, self.environ['rrduet.exact']), set())
        kwds_req = self.environ['rrduet.sess']['kwds']
        if not (kwds_page & kwds_req):
            self.cls__externals = []
            self.apps = 'access_denied'
            self.title += u" [Не хватает прав доступа]"
            self.errors.append(u"Доступ запрещен")
        self.kwds_page = kwds_page
        self.kwds_req = kwds_req
    @property
    def dbconn(self):
        if self.dbconn_cache is None:
            self.dbconn_cache = htu_main.dbhandler()
        return self.dbconn_cache
    def xmlresult(self):
        self.list_exc = []
        if hasattr(self, 'logic'):
            return self.logic()
    def rr_cleanup(self,exc_info=None):
        self.dump()
        if self.dbconn_cache is not None:
            self.dbconn_cache.close()
            del self.dbconn_cache
    def E_user(self):
        sess = self.req.environ['rrduet.sess']
        try:
            user_id = sess['id']
        except KeyError:
            sys.exc_clear()
            user_id = None
        if user_id is None:
            return E.needlogin()
        return E.user(*[ getattr(E, k)(v) for k, v in sess['sign'] ])
    def access_denied(self):
        xml = E.R(
            self.E_page(),
            self.E_user(),
            self.E_product(),
            # Должны выполнятся позже всех.
            self.E_results(),
            self.E_errors(),
        )
        self.resp.status_int = 500 # FIXME
        self.xsl_exec('', '__root__.xsl', xml)
        self.xsl_fillbind()

class template_html(template_base):
    cls__application = 'ajax'
    def ajax(self):
        self.resp.content_type = 'text/html'
        self.xmlroot = self.E_data()



class authorize(template_base):
    class callback_form(form_base):
        fields = (
            field('auth_tries', 0, int, ValueError),
            field('auth_name', ''),
            field('auth_key', ''),
        )
        labels = {
            'auth_name': u"Имя пользователя",
            'auth_key': u"Пароль",
        }
    cls__title = u"Авторизация"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', '__auth__.xsl'),
    ]
    def E_ivars(self):
        ivars = []
        for k, v in self.req.params.items():
            if k.startswith('auth_'):
                continue
            ivars.append(E.ivar(E.name(k), E.value(v)))
        return E.ivars(*ivars)
    def logic(self):
        form = self.form
        auth_tries = form['auth_tries']
        auth_name = form['auth_name']
        auth_key = form['auth_key']
        form['auth_tries'] += 1
        if auth_tries:
            dbconn = self.dbconn
            d = {}
            d_sign = []
            try:
                user = dbconn.query(Userprofile).filter(Userprofile.login == auth_name).one()
                if user.password == auth_key:
                    d['login'] = user.login
                    d['fio'] = user.fio
                    d['email'] = user.email
                    d['id'] = str(user.id)
                    d_sign.append(('login', user.login))
                    d_sign.append(('fio', user.fio))
                    d_sign.append(('id', str(user.id)))

                    kwds = set(( kw.group_kw for kw in dbconn.query(Admin_groupkw).filter(
                        Admin_groupkw.group_id == user.group_id
                    ) ))
                    for kw in dbconn.query(Admin_operkw).filter(Admin_operkw.oper_id == user.id):
                        if int(kw.group_include):
                            kwds.add(kw.group_kw)
                        else:
                            kwds.discard(kw.group_kw)
                    kwds.add('common')
                    d['kwds'] = kwds
                    d['sign'] = d_sign

            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                self.errors.append(u"Неправильно набран пароль или имя пользователя")
                if form['auth_tries'] > 1:
                    self.results.append(u"Неудачная попытка входа No%d" % (form['auth_tries'],))
            self.resp.environ['rrduet.sess'].update(d)


class public_cookie_auth(cookie_auth):
    sidname = 'sid_public'
    autharea = '/'
    authpath = '/'
    cookie_dir = sessions_dir
    def anonymous(self, resp):
        if resp.request.path_info.endswith('/ajax'):
            resp.status_int = 404
            resp.content_type = 'application/xml'
            resp.body = "<ajax failed='need-login'/>"
            return resp
        return cookie_auth.anonymous(self, resp)
    def authorize(self, resp):
        return authorize(resp)
