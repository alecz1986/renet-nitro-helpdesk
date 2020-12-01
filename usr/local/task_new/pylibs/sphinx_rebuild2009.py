#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from lxml.builder import E, ElementMaker
import lxml.etree as et
from lxml.builder import E
from task import *


S = ElementMaker(namespace="urn:sphinx", nsmap={'sphinx': "urn:sphinx"})
fields = []
docs = []
attrs = []


Session = sessionmaker(bind=engine)
dbconn = Session()



fields = dbconn.query(Taskfield).filter(~ Taskfield.id.in_(fs))
d = {}
for f in fields:
    d[f.name] = f.id
schema = S.schema()
for field in d:
    schema.append(S.field(name='tag'+str(d[field])))
schema.append(S.field(name='tagother'))
schema.append(S.field(name='task'))
schema.append(S.field(name='glob'))
schema.append(S.field(name='dt'))
schema.append(S.field(name='sys'))
root = S.docset(schema)
ths = dbconn.query(Threads, Tasktype).filter(Threads.title_id == Tasktype.id).filter(Threads.creation_date.like('2009%'))#.limit(20).offset(1000)



dbconn.close()
for t, p in ths:
    document = S.document(id=str(t.id))
    root.append(document)
    res = t.message.replace(u"ё", u"е").replace(u"Ё", u"е").split('$')
    #assert type(t.message) is unicode, t.message
    val_other = ''
    for i in range(1, len(res)/2+1):
        try:
            val = res[i*2].replace('/', '_')
        except:
            val = ''
        val = val.strip().replace('*', '').replace(',', ' ,')
        try:
            field = d[res[i*2-1].replace(':','')]
        except:
            field = 'other'
        if field != 'other':
            field = 'tag'+str(field)
            el = et.Element(field)
            el.text = val
            document.append(el)
        else:
            val_other += ' '+ val
    if val_other:
        el = et.Element('tagother')
        el.text = val_other
        document.append(el)
    document.append(E.task(str(t.title_id)))
    document.append(E.glob(str(t.id_global)))
    document.append(E.sys(str(p.system_id)))
    document.append(E.dt(str(t.creation_date).replace('-', '_')))
f = open('/usr/local/task_new/pylibs/last_id_sphinx2009.txt', 'w')
f.write(str(t.id))
f.close()
print et.tostring(root, encoding='UTF-8', pretty_print=1,xml_declaration=1)
