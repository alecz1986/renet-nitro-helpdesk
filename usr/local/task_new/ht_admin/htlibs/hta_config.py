#
# -*- coding: utf-8 -*-

import os
import sys
import datetime
from rrduet.rr_template import E, et

base_dir = '/usr/local/fshop'
htroot_dir = os.path.join(base_dir, 'ht_admin')
templates_dir = os.path.join(htroot_dir, 'templates')
sessions_dir = os.path.join(htroot_dir, 'sessions')
htdocs_dir = os.path.join(htroot_dir, 'htdocs')
prod_dir = os.path.join(htdocs_dir, 'product')
secret_minlength = 7
dbi_info = 'mysql://fullshopa:test@localhost/shopa?charset=utf8&use_unicode=1'
product = E.product(
        E.fullname(u"Интернет-магазин Пешка"),
#        E.license(u"Версия: пре-альфа [ недо-релиз ]"),
        E.license(u"Для внутреннего использования"),
        E.url_chgsecret("/private/user/change-a-secret"),
        E.url_logout("/private/auth"),
)
