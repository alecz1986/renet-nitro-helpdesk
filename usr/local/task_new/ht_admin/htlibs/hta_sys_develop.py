#
# -*- coding: utf-8 -*-

import sys
import sqlalchemy
from fullshopapi import Urllabel, Urlmap, Urlmapkw, Urlmapkw_info, Distrib_oper
from rrduet.rr_template import E, field
from hta_base import template_base, form_base, check_action
from hta_page import menu_base
from hta_main import keywords

class develop_index(menu_base):
    cls__kwds = set([ 'develop' ])
    cls__title = u"Интерфейс разработчика"
    def E_menus(self):
        return E.menus(
            E.menu(E.url("/private/develop/keywords"), E.text(u"Ключевые слова")),
            E.menu(E.url("/private/develop/urlmap"), E.text(u"Список страниц URL MAPPING")),
            E.menu(E.url("/private/develop/urlmap_edit"), E.text(u"Редактирование URL MAPPING")),
        )

class develop_keywords(template_base):
    cls__title = u"Ключевые слова"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', '__simpleedit__.xsl'),
        ('menu', '__menu__.xsl'),
    ]
    cls__kwds = set([ 'develop' ])
    class callback_form(form_base):
        fields = [
            field('url_kw', ''),
            field('kw_info', ''),
            field('kw_help', ''),
            field('action', '', check_action),
        ]
        labels = {
            'url_kw': u"Токен",
            'kw_info': u"Описание",
            'kw_help': u"Детальное описание",
        }
        ftypes = {
            'kw_help': 'textarea',
        }
    def logic(self):
        form = self.form
        action = form['action']
        form['action'] = 'new'

        url_kw = form['url_kw']
        kw_info = form['kw_info']
        kw_help = form['kw_help']

        dbconn = self.dbconn

        if url_kw:
            # Зачитаем данные по идентификатору.
            try:
                kwi = dbconn.query(Urlmapkw_info).filter(Urlmapkw_info.url_kw == url_kw).one()
                form['action'] = 'edit'
                self.ormloaded = True
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()

        if action == '':
            return None

        if not url_kw:
            self.errors.append(u"Должно быть задано ключевое слово")
        if not kw_info:
            self.errors.append(u"Должно быть задано описание")

        if self.errors:
            form.rollback()
            return None

        if not self.ormloaded:
            row = Urlmapkw_info()
            dbconn.add(row)
        form.store_to_orm(row)
        self.changes_commit(row)


class develop_urlmap(template_base):
    cls__title = u"Список страниц URL MAPPING"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'develop_urlmap.xsl'),
        ('menu', '__menu__.xsl'),
    ]
    cls__kwds = set([ 'develop' ])
    def E_tables(self):
        dbconn = self.dbconn
        labels = []
        for url_label, url_prefix in list(dbconn.query(Urllabel.url_label, Urllabel.url_prefix).order_by(Urllabel.url_label)):
            labels.append(E.labels(E.label(url_label), E.urlmap(*[ E.url(
                E.path(r.url_path),
                E.resporator(r.resporator)
            ) for r in dbconn.query(Urlmap).filter(Urlmap.url_label == url_label) ])))
        return E.tables(*labels)

class develop_urlmap_edit(template_base):
    cls__title = u"Редактирование URL MAPPING"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', '__simpleedit__.xsl'),
        ('menu', '__menu__.xsl'),
    ]
    cls__kwds = set([ 'develop' ])
    class callback_form(form_base):
        fields = [
            field('url_path', ''),
            field('url_label', ''),
            field('module', ''),
            field('callable', ''),
            field('action', '', check_action),
        ]
        labels = {
            'url_path': u"Путь",
            'url_label': u"Метка",
            'module': u"Модуль",
            'callable': u"Объект",
        }
        ftypes = {
            'url_label': 'select',
        }
        def select_url_label(self, field):
            return E.options(*[ E.option(E.value(r.url_label), u"%s [ %s ]" % (r.url_label, r.url_prefix)) for r in self.template_ref().dbconn.query(Urllabel).order_by(Urllabel.url_label) ])
    def E_menus(self):
        menus = [ E.menu(E.url('/private/develop/urlmap'), E.text(u"Просмотреть другие объекты")) ]
        if self.ormloaded is not None and not self.errors:
            menus.append(E.menu(E.url(self.form['url_path']), E.text(u"Перейти к редактируемому объекту")))
        return E.menus(*menus)
    def logic(self):
        form = self.form
        action = form['action']
        form['action'] = 'new'

        # FIXME: Сделать проверку доступа по ключевым словам.
        url_label = form['url_label']
        url_path = form['url_path']
        resp_module = form['module']
        resp_callable = form['callable']

        dbconn = self.dbconn

        if url_label and url_path:
            # Зачитаем данные по идентификатору.
            try:
                row = dbconn.query(Urlmap).filter(sqlalchemy.and_(
                    Urlmap.url_label == url_label,
                    Urlmap.url_path == url_path
                )).one()
                self.ormloaded = True
                form['module'], form['callable'] = row.resporator.split(':')
                form['action'] = 'edit'
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()

        # Если данные пришли со стороны то не выполнять проверку и не пытаться
        # изменить данные в базе данных (здравый смысл).
        if action == '':
            return None

        url_prefix = ''
        if not url_label:
            self.errors.append(u"Наименование метки должно быть определено")
        else:
            try:
                urllabel = dbconn.query(Urllabel).filter(Urllabel.url_label == url_label).one()
                url_prefix = urllabel.url_prefix
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                self.errors.append(u"Метка с именем '%s' не найдена"  % (url_label,))

        if not url_path.startswith(url_prefix):
            self.errors.append(u"Не совпадает префикс заданого '%s' для данной метки '%s' (должен начинаться на '%s')" % (
                url_path,
                url_label,
                url_prefix,
            ))

        if not resp_module:
            self.errors.append(u"Наименование модуля должно быть определено")
        else:
            try:
                m = __import__(resp_module)
            except ImportError:
                sys.exc_clear()
                self.errors.append(u"Имя модуля '%s' не найдено!" % (resp_module,))
            else:
                if not hasattr(m, resp_callable):
                    self.errors.append(u"Атрибут модуля '%s' - '%s' не определен" % (resp_module, resp_callable))
                else:
                    c = getattr(m, resp_callable)
                    if not hasattr(c, '__call__'):
                        self.errors.append(u"Объект модуля '%s' - '%s' должен быть исполняемым" % (resp_module, resp_callable))

        if self.errors or not urllabel:
            form.rollback()
            return None

        if not self.ormloaded:
            row = Urlmap()
            dbconn.add(row)
        form.store_to_orm(row)
        row.resporator = ':'.join((resp_module, resp_callable))
        self.changes_commit(row)
    def changes_saved(self):
        import hta_main
        try:
            hta_main.serve.pop()
        except IndexError:
            sys.exc_clear()
