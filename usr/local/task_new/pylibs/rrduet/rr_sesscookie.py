#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import os
import urllib
import errno
import uuid
from rr_sessdict import sessdict

class cookie_auth(object):
    class __metaclass__(type):
        def __new__(cls, name, bases, d):
            ret = type.__new__(cls, name, bases, d)
            if ret.sidname is None:
                # Базовый класс
                return ret
            assert type(ret.sidname) is str and ret.sidname, ret.sidname
            assert ret.autharea.startswith('/'), ret.autharea
            assert ret.autharea == '/' or not ret.autharea.endswith('/'), ret.autharea
            assert ret.authpath is None or ret.authpath == '/' or not ret.authpath.endswith('/'), ret.authpath

            ret.autharea_long = ret.autharea
            if not ret.autharea_long.endswith('/'):
                ret.autharea_long += '/'
            if ret.authpath is None:
                ret.authpath = ret.autharea
            if not ret.authpath.endswith('/'):
                ret.authpath += '/'
            ret.authpage = ret.autharea_long + ret.authprefix
            ret.authpage_long = ret.authpage + '/'
            try:
                os.makedirs(ret.cookie_dir, 0700)
            except OSError:
                exc_info = sys.exc_info()
                if exc_info[1].errno != errno.EEXIST:
                    raise
                sys.exc_clear()
            return ret
    sidname = None
    authpath = None
    authprefix = 'auth'
    cookie_dir = '.'
    cookie_maxage = 86400*365
    env_sid = 'rrduet.sid'
    env_sess = 'rrduet.sess'
    rx_sid = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    def resp_redirect(self, resp, xfrom, xto):
        req = resp.request
        if req.method != 'POST':
            vals = req.GET.items()
        else:
            vals = req.POST.items()
        # FIXME: Поставить перекодировку.
        vals = [ (k, v) for k, v in vals if not k.startswith('auth_') ]
        urls = [ req.host_url, xto, req.path_info[len(xfrom):] ]
        if vals:
            urls.extend(( '?', urllib.urlencode(vals) ))
        location = ''.join(urls)
        resp.location = location
        resp.status_int = 302
        resp.body = ''
        return resp
    def resp_logout(self, resp):
        path_info = resp.request.path_info
        if not path_info.endswith('/'):
            path_info += '/'
        resp.location = path_info
        resp.status_int = 302
        return resp
    def sid_remove(self, resp):
        req = resp.request
        env = resp.environ

        sess = env[self.env_sess]

        sid = req.cookies.get(self.sidname)
        if sid is not None:
            req.cookies.pop(self.sidname)

            env[self.env_sid] = None

            resp.delete_cookie(self.sidname, path=self.authpath)
            if self.autharea_long != self.authpath:
                resp.delete_cookie(self.sidname, path=self.autharea)
                resp.delete_cookie(self.sidname, path=self.autharea_long)
            if self.authpath.endswith('/') and self.authpath != '/':
                resp.delete_cookie(self.sidname, path=self.authpath[:-1])
        if sess:
            sess.remove()

        env[self.env_sid] = None
    def sid_filename(self, sid):
        # Возвращаем имя файла для серилизации данных словаря.
        return os.path.join(self.cookie_dir, str(sid) + '.sid')
    def sid_generate_and_save(self, resp):
        # Авторизация прошла успешно.
        sid = self.generate(resp)
        env = resp.environ
        env[self.env_sid] = sid
        sess = env[self.env_sess]
        sess.bind_maxage(self.cookie_maxage + 5)
        sess.save(self.sid_filename(sid))
        resp.set_cookie(self.sidname, sid, max_age=self.cookie_maxage, path=self.authpath)
    def generate(self, resp):
        # Если есть другой алгоритм по генерации идентификатора сессии,
        # то нужно переопределить этот метод.
        return str(uuid.uuid1())
    def anonymoused(self, resp):
        # Переписываем URL - добавляем "auth" в пути.
        return self.resp_redirect(resp, self.autharea_long, self.authpage_long)
    def registrated(self, resp):
        # Авторизация пройдена, перенаправляем на исходную страницу.
        return self.resp_redirect(resp, self.authpage_long, self.autharea_long)
    def authorize(self, resp):
        return None
    def validate(self, resp):
        # Получаем ответ, достаточно ли данных в сессии?
        return bool(resp.environ[self.env_sess])
    def sesshandler(self, resp):
        req = resp.request
        env = resp.environ
        env[self.env_sess] = sess = sessdict()
        env[self.env_sid] = None
        path_info = req.path_info
        if not path_info.startswith(self.autharea_long):
            # Находимся вне области авторизации. Поэтому ничего не делаем.
            return None
        sid = req.cookies.get(self.sidname)
        if sid is not None:
            if self.__class__.rx_sid.match(sid) is None:
                sid = None
            else:
                if sess.load(self.sid_filename(sid)) and self.validate(resp):
                    env[self.env_sid] = sid
                    #return None
                else:
                    self.sid_remove(resp)
                    env[self.env_sid] = sid = None
        if path_info == self.authpage:
            # Удаление сессии.
            self.sid_remove(resp)
            # По умолчанию перенаправляется на страницу авторизации.
            return self.resp_logout(resp)
        if not path_info.startswith(self.authpage_long):
            if sid is not None:
                # УСПЕШНО ЗАЧИТАНО СОСТОЯНИЕ СЕССИИ.
                # ПЕРЕХОД В ФОНОВЫЙ РЕЖИМ.
                return None
            # Пользователь определен как анонимный. Метод по умолчанию
            # перенаправляет на область авторизации.
            return self.anonymoused(resp)
        if sid is not None:
            # Авторизация была пройдена ранее.
            return self.registrated(resp)
        # Сессия не была получена ранее.
        ret = self.authorize(resp)
        if self.validate(resp):
            # Генерация новой сессии. Любое наполнение сессии возложено на
            # метод authorize.
            self.sid_generate_and_save(resp)
            return self.registrated(resp)
        return ret
    def __init__(self, route=None):
        if route is not None:
            self.register_to_router(route)
    def register_to_router(self, route):
        if self.autharea != self.autharea_long:
            route.add_route('^' + re.escape(self.autharea) + '$', redirect=self.autharea_long)
        route.add_route('^' + re.escape(self.authpath) + '(?P<other>.*)$', resporator=self.sesshandler)
