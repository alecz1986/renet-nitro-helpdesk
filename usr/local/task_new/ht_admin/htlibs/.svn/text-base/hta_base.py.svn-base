#
# -*- coding: utf-8 -*-

import sys

from hta_config import base_dir, htroot_dir, templates_dir, sessions_dir, product
from hta_main import dbhandler, keywords
from fullshopapi import Distrib_oper, Admin_group, Admin_groupkw, Admin_operkw, Urlmap, Urlmapkw, Urlmapkw_info
import regerror
import sqlalchemy
from rrduet.rr_sesscookie import cookie_auth
from rrduet.rr_template import field, form, template, E

__all__ = [
    'form_base',
    'template_base',
    'private_cookie_auth',
    'form_order',
]

def check_action(x):
    if x in ('new', 'edit', 'delete'):
        return x
    return ''

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
        cls.fields.insert(0, field('ie', cls.keyenc, setup='charset_detect'))
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
class form_order(form_base):
    @classmethod
    def meta_fields_userlevel(cls):
        fields = [
            field('ie', cls.keyenc, setup='charset_detect'),
            field('date_b', ''),
            field('date_e', ''),
            field('date_distr', ''),
            field('order_id', 0, int, ValueError),
            field('status', 0, int, ValueError),
            field('limit', 20, int, ValueError),
            field('offset', 0,  int, ValueError),
        ]
        fields.extend(cls.fields)
        cls.fields = fields
#        cls.fields.insert(0, field('ie', cls.keyenc, setup='charset_detect'))

class template_base(template, regerror.errtemplate):
    callback_form = form_base
    cls__product = product
    cls__template_path = templates_dir
    cls__pathprefix = '/private/'
    cls__kwds = set([ 'common' ])
    cls__externals = [ '/css/main.css' ]
    ormloaded = False
    dbconn_cache = None
    kwds = None
    def __init__(self, *args, **kw):
        self.err = regerror.regerror('/usr/local/fshop/var/log/admin.log')
        self.admin_actions = []
        regerror.errtemplate.__init__(self, '/usr/local/fshop/var/log/error.log')
        template.__init__(self, *args, **kw)
    @classmethod
    def rrduet_callback(cls, url_path, url_label):
        dbconn = dbhandler()
        try:
            if cls.kwds is None:
                cls.kwds = {}
            try:
                r = dbconn.query(Urlmap).filter(sqlalchemy.and_(
                    Urlmap.url_label == url_label,
                    Urlmap.url_path == url_path
                )).one()
                setkw = set(dbconn.query(Urlmapkw.url_kw).filter(sqlalchemy.and_(
                    Urlmapkw.url_label == url_label,
                    Urlmapkw.url_path == url_path
                )))
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                setkw = set()
            if cls.cls__kwds is not None:
                setkw.update(cls.cls__kwds)
            global keywords
            keywords.update(setkw)
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
            self.dbconn_cache = dbhandler()
        return self.dbconn_cache
    def xmlresult(self):
        self.list_exc = []
        if hasattr(self, 'logic'):
            return self.logic()
    def rr_cleanup(self, exc_info=None):
        if self.admin_actions:
            self.err.dump_info('admin', self.admin_actions)
        self.dump(exc_info)
        if self.dbconn_cache is not None:
            self.dbconn_cache.close()
            del self.dbconn_cache
    def E_user(self):
        sess = self.req.environ['rrduet.sess']
        if not sess:
            # Нельзя заполнять E.user иначе воспринимается как
            # зарегестрированный пользователь.
            return E.anonymous()
        return E.user(*[ getattr(E, k)(v) for k, v in sess['sign'] ])
    def changes_commit(self, row):
        try:
            self.dbconn.commit()
        except sqlalchemy.exc.IntegrityError:
            self.dbconn.rollback()
            sys.exc_clear()
            self.errors.append(u"Запись конфликтует с уже имеющейся")
        else:
            if not self.ormloaded:
                self.results.append(u"Запись была успешно добавлена")
                self.form.load_from_orm(row)
                if 'action' in self.form:
                    self.form['action'] = 'edit'
                self.ormloaded = True
            else:
                self.results.append(u"Запись была успешно изменена")
            self.changes_saved()
    def changes_saved(self):
        pass
    def access_denied(self):
        self.resp.status_int = 500 # FIXME
        self.cls__xsllist = [
            ('', '__root__.xsl'),
        ]
        self.application()

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
                oper = dbconn.query(Distrib_oper).filter(Distrib_oper.auth_name == auth_name).one()
                if oper.auth_key == auth_key:
                    d['login'] = oper.auth_name
                    d['oper_id'] = oper.oper_id
                    d['group_id'] = oper.group_id
                    d['distrib_id'] = oper.distrib_id
                    d_sign.append(('login', oper.auth_name))
                    d_sign.append(('viewoper', '?'.join(('/private/user/manage', self.urlencode((('oper_id', str(oper.oper_id)),))))))
                    try:
                        group = dbconn.query(Admin_group).filter(Admin_group.group_id == oper.group_id).one()
                        d['group'] = group.group_info
                        d_sign.append(('group', group.group_info))
                        d_sign.append(('viewgroup', '?'.join(('/private/user/viewgroup', self.urlencode((('group_id', str(group.group_id)),))))))
                    except sqlalchemy.orm.exc.NoResultFound:
                        sys.exc_clear()

                    kwds = set(( kw.group_kw for kw in dbconn.query(Admin_groupkw).filter(
                        Admin_groupkw.group_id == oper.group_id
                    ) ))
                    for kw in dbconn.query(Admin_operkw).filter(Admin_operkw.oper_id == oper.oper_id):
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

class private_cookie_auth(cookie_auth):
    sidname = 'sid_private'
    autharea = '/private'
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
