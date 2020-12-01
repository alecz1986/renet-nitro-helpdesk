#
# -*- coding: utf-8 -*-

import sys
import os
import time
import cPickle

class sessdict(object):
    __slots__ = [ '_d', '_filename', '_expire', ]
    def __init__(self, filename=None, maxage=None):
        object.__init__(self)
        self._d = {}
        self.bind_filename(filename)
        self.bind_maxage(maxage)
    def __nonzero__(self):
        return bool(self._d)
    def isbind(self):
        return self._filename is not None
    def bind_filename(self, filename=None):
        self._filename = filename
    def bind_maxage(self, maxage):
        if maxage is None:
            self._expire = 0x7fffffff
        else:
            self._expire = time.time() + maxage
    def save(self, filename=None):
        if filename is not None:
            self._filename = filename
        if self._filename is None:
            return False
        mode = os.O_RDWR|os.O_EXLOCK|os.O_CREAT|os.O_EXCL
        rnd = "%s.%8.8x" % (self._filename, abs(id(self)))
        fd = os.open(rnd, mode, 0600)
        fh = os.fdopen(fd, "wb", 4096)
        cPickle.dump((self._d, self._expire), fh, 2)
        fh.close()
        os.rename(rnd, self._filename)
        return True
    def load(self, filename=None):
        if filename is not None:
            self._filename = filename
        if self._filename is None:
            return False
        try:
            data, expire = cPickle.load(open(self._filename, "rb"))
        except IOError, exc:
            sys.exc_clear()
            return False
        except cPickle.PickleError:
            sys.exc_clear()
            self.remove()
            return False
        if time.time() > expire:
            self.remove()
            return False
        else:
            self._expire = expire
            self._d.clear()
            self._d.update(data)
            return True
    def remove(self):
        status = True
        if self._filename is None:
            return status
        try:
            os.unlink(self._filename)
        except OSError:
            sys.exc_clear()
            status = False
        self._d.clear()
        self._filename = None
        return status
    def clear(self):
        self._d.clear()
        self.save()
    def update(self, *args, **kw):
        self._d.update(*args, **kw)
    def __iter__(self):
        return iter(self._d)
    def __getitem__(self, item):
        return self._d.__getitem__(item)
    def __setitem__(self, item, val):
        return self._d.__setitem__(item, val)
    def __delitem__(self, item):
        return self._d.__delitem__(item)
    def __contains__(self, item):
        return item in self._d
    def get(self, item, default=None):
        return self._d.get(item, default)
    def setdefault(self, item, default=None):
        return self._d.setdefault(item, default)
    def keys(self):
        return self._d.keys()
    def values(self):
        return self._d.values()
    def items(self):
        return self._d.items()
    def iterkeys(self):
        return self._d.iterkeys()
    def itervalues(self):
        return self._d.itervalues()
    def pop(self, item, default=None):
        return self._d.pop(item, default)
    def popitem(self):
        return self._d.popitem()
    def __str__(self):
        return self._d.__str__()
    def __repr__(self):
        return self._d.__repr__()
