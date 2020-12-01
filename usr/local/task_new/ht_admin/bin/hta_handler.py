#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import gc; gc.enable()
import sys

sys.path.append('/usr/local/fshop/pylibs')
sys.path.append('/usr/local/fshop/ht_admin/htlibs')
sys.path.append('/usr/local/fshop/ht_users/htlibs')

import sys
def debug_enable():
    def excepthook(exc_type, exc_ob, exc_tb):
        print "TEST"
        if issubclass(exc_type, Warning):
            sys.exc_clear()
            return
        sys.__excepthook__(exc_type, exc_ob, exc_tb)
        sys.exc_clear()
        print "TEST_OK"
    sys.excepthook = excepthook

debug_enable()



if 0:
    import logging

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.DEBUG)

def startServer(pidpath, sockpath, logpath, processes, uid=80, umask=0):
    import threading; threading.stack_size(131072)
    import regerror
    import sys
    import time
    import signal
    import os
    import pidfile
    import getopt
    optlist, args = getopt.getopt(sys.argv[1:], "sx")
    optdict = dict(optlist)
    stop = optdict.get('-s', False)
    debug = optdict.get('-x') is not None

    assert os.getuid() == 0, uid

    pid = pidfile.pidfile(pidpath)
    if '-s' in optdict:
        exited = pid.pidfile_kill(signal.SIGTERM)
        if exited is True:
            print "Exit: server stopped"
        sys.exit(not exited)
    if not pid.pidfile_start():
        print "Exit: already running"
        sys.exit(1)
    if not debug:
        if os.fork() > 0:
            pid.pidfile_forget()
            sys.exit()
        pid.pidfile_start()
        os.setsid()
    try:
        if os.ttyname(0) == '/dev/console':
            time.sleep(10)
    except OSError:
        sys.exc_clear()

    siteconf = {
        'umask': umask,
        'minSpare': processes,
        'maxSpare': processes,
        'maxChildren': processes,
        'maxRequests': 1000,
        'multiplexed': False,
        'bindAddress': sockpath,
    }
    from flup.server.fcgi_fork import WSGIServer
    class WSGIErrHandle(WSGIServer, regerror.regerror):
        def __init__(self, *args, **kw):
            WSGIServer.__init__(self, *args, **kw)
            regerror.regerror.__init__(self, logpath, 'admin')
        def error(self, req):
            self.dump_errors(req.requestId, [
                ('params', req.params),
            ])
    os.setuid(uid)
    import hta_main
    bind = WSGIErrHandle(hta_main.hub, **siteconf)
    bind.run()

startServer(
        pidpath="/usr/local/fshop/var/run/fcgi_admin.pid",
        sockpath="/usr/local/fshop/var/run/fcgi_admin.sock",
        logpath="/usr/local/fshop/var/log/error.log",
        processes=5)
