#
# -*- coding: utf8 -*-

#
# В данном модуле содержится класс для обработки исключения и вывода
# сопутствующей информации в лог файл. Интерфейс специально ориентирован на
# многосторочный вывод информации об исключении и связанных с ним данных.
#
# Основной метод класса dump_errors. Желательно указать первым аргументом
# логическую метку, если в данном методе возможны несколько исключений данного
# рода.
#
# Класс может быть указан в виде базового для другого. В этом случае второй
# аргумент __init__ метода может быть упущен. Но инициализация все же
# требуется:
#
# class depend_on_regerror(regerror):
#     def __init__(self, *args, **kw):
#         regerror.__init__(self)
#         ...
#
# Для поощерения использования в виде базового класса используется
# дополнительный отладочный метод, который возвращает отладочную информацию,
# важную в данном случае: get_errdebug(self). Отключить вывод отладочной
# информации можно за счет аттрибута debug. По умолчанию отладка выключена.
#
# Вывод происходит даже в случае отсутствия исключения. После выполнения метода
# dump_errors информация о текущем исключении затирается.
#

__all__ = [ 'regerror' ]

import sys
import traceback
import datetime
import fcntl

class regerror:
    def __init__(self, errfn, errclass=None):
        self.errfn = errfn
        if errclass is None:
            self.errclass = self.__class__.__name__
        else:
            self.errclass = errclass
    def dump_errors(self, method=None, errinfo=None, exc_info=None):
        if exc_info is None:
            exc_info = sys.exc_info()
        sys.exc_clear()
        if exc_info[0] is None:
            return
        return self.dump_info(method, errinfo, exc_info)
    def dump_info(self, method=None, errinfo=None, exc_info=None):
        if exc_info is None:
            exc_info = (None, None, None)
        lt = []
        if getattr(self, 'debug', False):
            errdebug = getattr(self, 'get_errdebug', None)
            if errdebug is not None and callable(errdebug):
                it = errdebug()
                lt = []
                for i, p in enumerate(it):
                    if type(p) is not tuple:
                        raise TypeError("value pair required an tuple in pos #%d" % (i,))
                    if len(p) != 2:
                        raise TypeError("required tuple with length 2 (%d is given)" % (len(p),))
                    k, v = p
                    if type(k) is unicode:
                        k = k.encode('utf8', 'ignore')
                    if type(v) is unicode:
                        v = v.encode('utf8', 'ignore')
                    lt.append((k, v))
                del it, p
        if self.errfn is None:
            exc = sys.stdout
        else:
            exc = file(self.errfn, "a")
            fcntl.flock(exc.fileno(), fcntl.LOCK_EX)
        if method is None:
            method = '[internal]'
        print >>exc, """[ %s ]: class \"%s\" in \"%s\"""" % (
            datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            self.errclass,
            method
        )
        if exc_info[0] is not None:
            for tback in ('\n'.join(traceback.format_exception(*exc_info))).split('\n'):
                if not tback:
                    continue
                print >>exc, "E:", tback
            del tback
        if errinfo:
            try:
                it = iter(errinfo)
            except:
                sys.exc_clear()
            else:
                for i, p in enumerate(it):
                    if type(p) is not tuple:
                        raise TypeError("value pair required an tuple in pos #%d" % (i,))
                    if len(p) != 2:
                        raise TypeError("required tuple with length 2 (%d is given)" % (len(p),))
                    k, v = p
                    if type(k) is unicode:
                        k = k.encode('utf8', 'ignore')
                    if type(v) is unicode:
                        v = v.encode('utf8', 'ignore')
                    print >>exc, "INFO: %s => %s" % (k, v)
                del it, p
        for k, v in lt:
            print >>exc, "DEBUG: %s => %s" % (k, v)
        print >>exc
        exc.close()
        del exc


class errtemplate(regerror):
    @staticmethod
    def uni(s):
        tp = type(s)
        if tp is unicode:
            return s
        elif tp in (int, long, float):
            return unicode(s)
        elif tp is str:
            return s.decode('utf8', 'ignore')
        elif isinstance(s, object):
            return repr(s)
        raise ValueError("incompatible type '%s'" % (tp.__name__,))
    def dump(self, exc_info=None):
        if exc_info is None:
            exc_info = sys.exc_info()
        if exc_info[0] is None:
            return
        req = self.req
        errinfo = [
                ('req.path_info', req.path_info),
        ]
        for k in self.req.GET:
            errinfo.append(("GET.%s" % k, self.uni(req.GET.get(k, u'')).encode('utf8', 'ignore')))
        for k in self.req.POST:
            errinfo.append(("POST.%s" % k, self.uni(req.POST.get(k, u'')).encode('utf8', 'ignore')))
        return self.dump_errors("dump", errinfo=errinfo, exc_info=exc_info)
