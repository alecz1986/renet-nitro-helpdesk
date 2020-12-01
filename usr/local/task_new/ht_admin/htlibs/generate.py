#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sqlalchemy
import sys
import pprint

sys.path.append("/usr/local/task_new/pylibs")

from task import *

task_fields = set([ r.name for r in dbconn.query(Taskfield).order_by(Taskfield.weight) ])

for r in dbconn.query(Threads).filter(Threads.id_local == 1):
    message = r.message.replace('*$', '\n$')
    toks = message.split('$')
    tokit = iter(toks)
    d = {}
    for tok in tokit:
        if tok.endswith(":"):
            name = tok[:-1]
            if name not in task_fields:
                continue
            d[name] = tokit.next().strip()
        pprint.pprint(d)
