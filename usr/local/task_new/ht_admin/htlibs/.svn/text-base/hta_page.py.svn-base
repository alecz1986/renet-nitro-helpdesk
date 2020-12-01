#
# -*- coding: utf-8 -*-

import sys
import sqlalchemy
from fullshopapi import Urllabel, Urlmap
from rrduet.rr_template import E, field
from hta_base import template_base, form_base

class menu_base(template_base):
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('menu', '__menu__.xsl'),
    ]

class notfound_page(menu_base):
    cls__title = "404: Page Not Found"
    def E_menus(self):
        return E.menus(
            E.menu(E.url(self.path_up), E.text(u"Перейти к меню")),
            E.menu(
                E.url("?".join(("/private/develop/urlmap_edit", self.urlencode((('url_path', self.path_info),))))),
                E.text(u"Привязать к данной пути выполнение кода страницы")
            ),
        )
    def application(self):
        self.resp.status_int = 404
        self.errors.append(u"Страница %s не найдена" % (self.path_info,))
        template_base.application(self)
