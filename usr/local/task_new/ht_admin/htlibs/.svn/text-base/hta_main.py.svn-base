#
# -*- coding: utf-8 -*-

from hta_config import sessions_dir, dbi_info
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy
def initialize_hub(dbhandler):
    from rrduet.rr_router import router
    from hta_base import private_cookie_auth
    from fullshopapi import Urlmap

    dbconn = dbhandler()

    hub = router()

    sidname = private_cookie_auth(hub).sidname

    hub.add_route('/private/develop/urlmap', resporator='hta_sys_develop:develop_urlmap', exact=sidname)
    hub.add_route('/private/develop/urlmap_edit', resporator='hta_sys_develop:develop_urlmap_edit', exact=sidname)

    for url_path, resporator in dbconn.query(
            Urlmap.url_path, Urlmap.resporator
    ).filter(Urlmap.url_label == sidname).order_by(Urlmap.url_path.desc()):
        hub.add_exact(url_path, resporator=resporator, exact=sidname)
    hub.add_route(None, exact=sidname)
    hub.add_route('^/private/(?P<register_uri>.*)$', resporator='hta_page:notfound_page')

    if 0:
        private_cookie_auth(sidname=mark2, autharea='/xxx', authpath='/', cookie_dir=sessions_dir).register_in_router(hub)
        for url_path, resporator in dbconn.query(Urlmap.url_path, Urlmap.resporator).filter(Urlmap.url_label == mark2).order_by(Urlmap.url_path.desc()):
            hub.add_exact(url_path, resporator=resporator)
        hub.add_route(None, exact=mark2)
        hub.add_route('^(?P<register_uri>.*)$', resporator='hta_page:notfound_page')

    dbconn.close()

    return hub

class photoid2path(object):
    symbs = "0123456789abcdefghijklmnopqrstuvwxyz"
    def __init__(self, base, level=3, symbs=None):
        if symbs is None:
            symbs = self.__class__.symbs
        self.base = base
        self.level = level
        self.symbs = symbs
        self.symbs_len = len(symbs)
    def get(self, n, ext='.gif'):
        level = self.level + 1
        p = []
        h = n
        while level:
            h, l = divmod(h, self.symbs_len)
            p.append(self.symbs[l])
            level -= 1
        p[0] = str(n) + ext
        p.append(self.base)
        p.reverse()
        return os.path.join(*p)
serve = [ True ]
keywords = set()
#dbengine = create_engine(dbi_info)
#dbengine = create_engine(dbi_info, pool_size=2)
dbengine = create_engine(dbi_info, poolclass=sqlalchemy.pool.NullPool)
dbhandler = sessionmaker(bind=dbengine)
hub = initialize_hub(dbhandler)
