#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import time
import stat
import os
import urllib
import errno
import uuid
from webob import Request, Response
from webob import exc

class resporator(object):
    __slots__ = [ 'application' ]
    def __init__(self, application):
        object.__init__(self)
        self.application = application
    def __call__(self, resp, start_response):
        answer = None
        try:
            answer = self.application(resp)
            if answer is None:
                return None
        except exc.HTTPException:
            answer = sys.exc_info()[1]
            sys.exc_clear()
            return answer(resp.environ, start_response)
        if isinstance(answer, basestring):
            resp.body = answer
            return resp(resp.environ, start_response)
        return answer(resp.environ, start_response)

class router(object):
    def __init__(self):
        self._routes = []
        self._exactmap = {}
    def _load_controller(self, string):
        module_name, func_name = string.split(':', 1)
        __import__(module_name)
        module = sys.modules[module_name]
        func = getattr(module, func_name)
        return func
    def add_exact(self, template, **kw):
        self.add_route(template, **kw)
        if template is not None and template.endswith('/') and template != '/':
            kw.pop('controller', None)
            kw.pop('resporator', None)
            kw['redirect'] = template
            self.add_route(template[:-1], **kw)
    def add_route(self, *args, **kw):
        cls = self.__class__
        if len(args) != 1:
            raise TypeError("in firstly define template and only template (class=%s, args=%s, kw=%s)" % (cls.__name__, str(args), str(kw)))
        # Темплейт не может быть задан в виде ключевого слова.
        template = args[0]

        if 'controller' in kw and 'resporator' in kw:
            raise TypeError("only 'controller' or 'resporator' argument may be given in the same time (class %s)" % (cls.__name__,))

        decorator = False
        controller = None

        if 'controller' in kw:
            decorator = False
            controller = kw.pop('controller')
        elif 'resporator' in kw:
            decorator = True
            controller = kw.pop('resporator')
        elif 'redirect' in kw:
            decorator = True
            def controller(resp, location=kw.pop('redirect')):
                resp.location = location
                resp.status_int = 302
                return resp
        if isinstance(controller, basestring):
            controller = self._load_controller(controller)

        exact = kw.pop('exact', None)
        assert exact is None or type(exact) is str, exact

        if controller is not None and decorator:
            if exact is not None:
                callback = getattr(controller, 'rrduet_callback', None)
                if callback is not None:
                    assert hasattr(controller, '__call__')
                    callback(template, exact)
            controller = resporator(controller)

        assert not kw, kw

        if exact is not None:
            if template is not None:
                self._exactmap.setdefault(exact, {})[template] = controller
            else:
                self._routes.append((None, exact))
        else:
            self._routes.append((re.compile(template, re.DOTALL), controller))
    def __call__(self, environ, start_response):
        environ['rrduet.done'] = False
        req = Request(environ, unicode_errors='ignore')
        resp = Response(request=req)
        def guard_start(status, headers, excinfo=None, environ=environ, start_response=start_response):
            if environ['rrduet.done']:
                return
            environ['rrduet.done'] = True
            if excinfo is not None:
                return start_response(status, headers, excinfo)
            else:
                return start_response(status, headers)
        path_info = req.path_info
        for template, controller in self._routes:
            exact = None
            if template is None:
                exact = controller
                controller = self._exactmap.get(exact, {}).get(path_info)
                if controller is None:
                    continue
            else:
                match = template.match(path_info)
                if match is None:
                    continue
                req.urlvars = match.groupdict()
            environ['rrduet.exact'] = exact
            if issubclass(controller.__class__, resporator):
                ret = controller(resp, guard_start)
            else:
                ret = controller(environ, guard_start)
            if ret is not None and environ['rrduet.done']:
                return ret
        return exc.HTTPNotFound()(environ, guard_start)
    def load(self, other):
        self._routes = other._routes
        self._exactmap = other._exactmap
