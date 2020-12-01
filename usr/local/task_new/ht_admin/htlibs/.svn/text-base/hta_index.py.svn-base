#
# -*- coding: utf-8 -*-

from rrduet.rr_template import E
from hta_page import menu_base

class private_index__page(menu_base):
    cls__title = u"Меню: ОСНОВНОЕ"
    def E_menus(self):
        return E.menus(
            E.menu(E.url('/private/develop/'), E.text(u"Интерфейс разработчика")),
            E.menu(E.url('/private/user/'), E.text(u"Пользователи")),
            E.menu(E.url('/private/custom/'), E.text(u"Покупатели")),
            E.menu(E.url('/private/product/'), E.text(u"Управление продуктами")),
            E.menu(E.url('/private/order'), E.text(u"Управление заказами")),
            E.menu(E.url('/private/other/'), E.text(u"Прочиe установки")),
            E.menu(E.url('/private/pages/'), E.text(u"Дополнительные страницы, новости, акции")),
            E.menu(E.url('/private/reports/'), E.text(u"Отчеты")),
            E.menu(E.url('/private/supplier'), E.text(u"Управление поставщиками")),
        )
class private__report__page(menu_base):
    cls__kwds = set([ 'report' ])
    cls__title = u"Меню: Отчеты"
    def E_menus(self):
        return E.menus(
            E.menu(E.url('/private/report/order'), E.text(u"Отчет по заказам")),
            E.menu(E.url('/private/report/management'), E.text(u"Управленческий учет")),
        )
class private_user_index__page(menu_base):
    cls__kwds = set([ 'user' ])
    cls__title = u"Меню: ПОЛЬЗОВАТЕЛИ"
    def E_menus(self):
        return E.menus(
            E.menu(E.url('/private/user/manage'), E.text(u"Управление учетными записями пользователей")),
            E.menu(E.url('/private/user/groups'), E.text(u"Группы пользователей")),
            E.menu(E.url('/private/user/access'), E.text(u"Права и привилегии")),
            E.menu(E.url('/private/user/distrib'), E.text(u"Дистрибьюция")),
        )

class private_other__page(menu_base):
    cls__kwds = set([ 'other' ])
    cls__title = u"Меню: ПРОЧИЕ УСТАНОВКИ"
    def E_menus(self):
        return E.menus(
            E.menu(E.url('/private/other/delivery'), E.text(u"Типы доставок")),
            E.menu(E.url('/private/other/price_delivery'), E.text(u"Стоимость доставок")),
            E.menu(E.url('/private/other/payment'), E.text(u"Типы оплаты")),
            E.menu(E.url('/private/other/status'), E.text(u"Статусы заказов")),
            E.menu(E.url('/private/other/banners'), E.text(u"Баннеры")),
        )
class private_pages(menu_base):
    cls__kwds = set([ 'pages' ])
    cls__title = u"Меню: ПРОЧИЕ УСТАНОВКИ"
    def E_menus(self):
        return E.menus(
            E.menu(E.url('/private/pages/info'), E.text(u"Информационные страницы")),
            E.menu(E.url('/private/pages/sale'), E.text(u"Акции")),
            E.menu(E.url('/private/pages/new'), E.text(u"Новости")),
            E.menu(E.url('/private/pages/spec'), E.text(u"Спецпредложения")),
            E.menu(E.url('/private/pages/line'), E.text(u"Бегущая строка")),
        )
class index__page(menu_base):
    cls__title = u"Меню: XXX"
    def E_menus(self):
        return E.menus(
            E.menu(E.url('/haha'), E.text(u"Хо-Хо")),
        )
