#
# -*- coding: utf-8 -*-
import sys
import os

from htu_config import sessions_dir, dbi_info
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.pool

def initialize_hub(dbhandler):
    from rrduet.rr_router import router
    from htu_base import public_cookie_auth
    from task import Urlmap

    dbconnect = dbhandler()

    hub = router()

    sidname1 = public_cookie_auth(hub).sidname

    for url_path, resporator in dbconnect.query(Urlmap.url_path, Urlmap.resporator).filter(Urlmap.url_label == sidname1).order_by(Urlmap.url_path.desc()):
        hub.add_exact(url_path, resporator=resporator, exact=sidname1)
    hub.add_route(None, exact=sidname1)
    hub.add_route('^/public/(?P<register_uri>.*)$', resporator='htu_page:main_page')

    dbconnect.close()

    return hub


dbengine = create_engine(dbi_info, poolclass=sqlalchemy.pool.NullPool)
#dbengine = create_engine(dbi_info, pool_size=2)
#dbengine = create_engine(dbi_info,  max_overflow=100, pool_size=100)
dbhandler = sessionmaker(bind=dbengine)
hub = initialize_hub(dbhandler)
serve = [ True ]
