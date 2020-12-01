#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import sys
import gc; gc.enable()

sys.path.append('/usr/local/task_new/pylibs')
sys.path.append('/usr/local/task_new/ht_admin/htlibs')
sys.path.append('/usr/local/task_new/ht_users/htlibs')


if 0:
    import logging

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.DEBUG)

def startServer(pidpath, sockpath, logpath, processes=10, uid=80, umask=0):
    import threading; 
    #threading.stack_size(131072)
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
        'maxRequests': 100,
        'multiplexed': False,
        'bindAddress': sockpath,
    }
    from flup.server.fcgi_fork import WSGIServer
    class WSGIErrHandle(WSGIServer, regerror.regerror):
        def __init__(self, *args, **kw):
            WSGIServer.__init__(self, *args, **kw)
            regerror.regerror.__init__(self, logpath, 'users')
        def error(self, req):
            self.dump_errors()
    os.setuid(uid)
    import htu_main
    bind = WSGIErrHandle(htu_main.hub, **siteconf)
    bind.run()

startServer(
        pidpath="/usr/local/task_new/var/run/fcgi_user.pid",
        sockpath="/usr/local/task_new/var/run/fcgi_user.sock",
        logpath="/usr/local/task_new/var/log/error.log", processes=25)
