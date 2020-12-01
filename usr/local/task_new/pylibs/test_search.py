#
# -*- coding: utf-8 -*-

import sys
from sphinxapi import *
mode = SPH_MATCH_EXTENDED2
cl = SphinxClient()
cl._limit = 100000
cl.SetLimits ( 0, 100000, max(100000,1000) )
host = '127.0.0.1'
port = 9312
cl.SetServer ( host, port )
cl.SetWeights ( [1000, 1] )
cl.SetMatchMode ( mode )
rs = []
fulltext = '@* *226963*'
res = cl.Query('@sys ^1$ ' + fulltext)
#print fulltext
if res is not None and res.has_key('matches'):
    for match in res['matches']:
        rs.append(match['id'])
rs.sort()
rs = [ r for r in rs ]
print rs
